from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import QuotaResponse, UserResponse, MessageResponse
from app.services.supabase_service import supabase_service
from app.core.security import get_current_user

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


@router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """
    Retorna estatísticas de uso do usuário
    """
    # TODO: Implementar tracking de estatísticas
    return {
        "total_questions": 45,
        "builds_consulted": 23,
        "gameplay_questions": 22,
        "favorite_position": "CF",
        "most_searched_player": "Messi"
    }
