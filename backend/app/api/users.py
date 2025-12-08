from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas import QuotaResponse, UserResponse, MessageResponse, UserUpdate, UserStatsResponse
from app.services.supabase_service import supabase_service
from app.core.security import get_current_user
from app.database import get_db
from app.models import User, UserStats

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/quota", response_model=QuotaResponse)
async def get_user_quota(current_user: dict = Depends(get_current_user)):
    """
    Retorna informações de quota do usuário
    (quantas perguntas restam hoje)
    """
    try:
        quota_info = await supabase_service.get_quota_info(current_user["user_id"])
        return QuotaResponse(**quota_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar quota: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Retorna perfil completo do usuário autenticado
    """
    user = await supabase_service.get_user(current_user["user_id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return UserResponse(**user)


@router.post("/upgrade-premium", response_model=MessageResponse)
async def upgrade_to_premium(current_user: dict = Depends(get_current_user)):
    """
    Upgrade para conta Premium
    TODO: Integrar com Stripe/Mercado Pago
    """
    # Por enquanto, apenas mockado
    return MessageResponse(
        message="Upgrade para Premium em desenvolvimento",
        detail="Integração com pagamento será adicionada em breve"
    )


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza perfil do usuário autenticado
    """
    try:
        # Buscar usuário no Supabase
        response = supabase_service.client.table("users").select("*").eq("id", current_user["user_id"]).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        user = response.data[0]
        update_data = {}
        
        if user_update.full_name is not None:
            update_data["name"] = user_update.full_name
        
        if user_update.nickname is not None:
            # Verificar se nickname já existe
            existing = supabase_service.client.table("users").select("id").eq("nickname", user_update.nickname).neq("id", current_user["user_id"]).execute()
            if existing.data and len(existing.data) > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nickname já está em uso"
                )
            update_data["nickname"] = user_update.nickname
        
        if user_update.platform is not None:
            update_data["platform"] = user_update.platform
        
        # Atualizar no Supabase
        if update_data:
            updated = supabase_service.client.table("users").update(update_data).eq("id", current_user["user_id"]).execute()
            if updated.data and len(updated.data) > 0:
                user = updated.data[0]
        
        return UserResponse(
            id=str(user["id"]),
            email=user["email"],
            name=user.get("name"),
            nickname=user.get("nickname"),
            platform=user.get("platform"),
            role=user.get("role", "user"),
            is_premium=user.get("is_premium", False),
            daily_questions_used=user.get("daily_questions_used", 0),
            created_at=user.get("created_at")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar perfil: {str(e)}"
        )


@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """
    Retorna estatísticas de uso do usuário
    """
    from datetime import datetime
    
    try:
        # Buscar stats do Supabase
        response = supabase_service.client.table("user_stats").select("*").eq("user_id", current_user["user_id"]).execute()
        
        if response.data and len(response.data) > 0:
            stats = response.data[0]
            return UserStatsResponse(
                total_questions=stats.get("total_questions", 0),
                builds_consulted=stats.get("builds_consulted", 0),
                gameplay_questions=stats.get("gameplay_questions", 0),
                favorite_position=stats.get("favorite_position"),
                most_searched_player=stats.get("most_searched_player"),
                last_active=stats.get("last_active", stats.get("created_at"))
            )
        else:
            # Retornar stats vazias se não existir (não tentar criar)
            return UserStatsResponse(
                total_questions=0,
                builds_consulted=0,
                gameplay_questions=0,
                favorite_position=None,
                most_searched_player=None,
                last_active=datetime.utcnow().isoformat()
            )
    except Exception as e:
        # Log do erro e retorna stats vazias
        print(f"Erro ao buscar estatísticas: {str(e)}")
        from datetime import datetime
        return UserStatsResponse(
            total_questions=0,
            builds_consulted=0,
            gameplay_questions=0,
            favorite_position=None,
            most_searched_player=None,
            last_active=datetime.utcnow().isoformat()
        )
