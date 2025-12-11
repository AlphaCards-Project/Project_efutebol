"""
Rotas Administrativas
Apenas usuários com role 'admin' podem acessar estas rotas
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict
from app.core.deps import get_current_admin, require_roles
from app.core.security import get_current_user
from app.services.supabase_service import supabase_service
from app.models import UserRole
from app.schemas import MessageResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=Dict)
async def admin_dashboard(
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Dashboard administrativo com estatísticas do sistema
    
    **Apenas administradores têm acesso**
    
    Retorna:
    - Total de usuários
    - Total de cartas
    - Total de jogadores
    - Total de builds
    """
    try:
        # Buscar estatísticas
        users_count = len(supabase_service.client.table("users").select("id").execute().data)
        cards_count = len(supabase_service.client.table("cards").select("id").execute().data)
        players_count = len(supabase_service.client.table("players").select("id").execute().data)
        builds_count = len(supabase_service.client.table("builds").select("id").execute().data)
        
        return {
            "admin_email": current_admin.get("email"),
            "statistics": {
                "total_users": users_count,
                "total_cards": cards_count,
                "total_players": players_count,
                "total_builds": builds_count
            },
            "message": "Dashboard carregado com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar dashboard: {str(e)}"
        )


@router.get("/users", response_model=List[Dict])
async def list_all_users(
    limit: int = 50,
    offset: int = 0,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Lista todos os usuários do sistema
    
    **Apenas administradores têm acesso**
    
    Args:
        limit: Quantidade máxima de usuários (padrão: 50)
        offset: Paginação (padrão: 0)
    """
    try:
        response = supabase_service.client.table("users")\
            .select("id, email, name, role, created_at")\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar usuários: {str(e)}"
        )


@router.patch("/users/{user_id}/promote", response_model=MessageResponse)
async def promote_user_to_admin(
    user_id: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Promove um usuário para administrador
    
    **Apenas administradores podem promover outros usuários**
    
    Args:
        user_id: UUID do usuário a ser promovido
    """
    try:
        # Verificar se usuário existe
        user = supabase_service.client.table("users")\
            .select("id, email, role")\
            .eq("id", user_id)\
            .execute()
        
        if not user.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        
        # Promover para admin
        supabase_service.client.table("users")\
            .update({"role": UserRole.admin.value})\
            .eq("id", user_id)\
            .execute()
        
        return MessageResponse(
            message="Usuário promovido com sucesso",
            detail=f"Usuário {user.data[0]['email']} agora é administrador. Ele deve fazer login novamente."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao promover usuário: {str(e)}"
        )


@router.patch("/users/{user_id}/demote", response_model=MessageResponse)
async def demote_user(
    user_id: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Remove privilégios de administrador de um usuário
    
    **Apenas administradores podem fazer isso**
    
    Args:
        user_id: UUID do usuário
    """
    try:
        # Não permitir que admin remova seus próprios privilégios
        if user_id == current_admin.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você não pode remover seus próprios privilégios de admin"
            )
        
        # Verificar se usuário existe
        user = supabase_service.client.table("users")\
            .select("id, email, role")\
            .eq("id", user_id)\
            .execute()
        
        if not user.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        
        # Rebaixar para free
        supabase_service.client.table("users")\
            .update({"role": UserRole.free.value})\
            .eq("id", user_id)\
            .execute()
        
        return MessageResponse(
            message="Privilégios removidos com sucesso",
            detail=f"Usuário {user.data[0]['email']} agora é free"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao rebaixar usuário: {str(e)}"
        )


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Deleta um usuário do sistema (use com cuidado!)
    
    **Apenas administradores podem deletar usuários**
    
    Args:
        user_id: UUID do usuário a ser deletado
    """
    try:
        # Não permitir que admin delete a si mesmo
        if user_id == current_admin.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você não pode deletar sua própria conta de admin"
            )
        
        # Verificar se usuário existe
        user = supabase_service.client.table("users")\
            .select("id, email")\
            .eq("id", user_id)\
            .execute()
        
        if not user.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        
        # Deletar usuário
        supabase_service.client.table("users")\
            .delete()\
            .eq("id", user_id)\
            .execute()
        
        return MessageResponse(
            message="Usuário deletado com sucesso",
            detail=f"Usuário {user.data[0]['email']} foi removido do sistema"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )


@router.get("/logs/recent")
async def get_recent_logs(
    limit: int = 100,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Retorna logs recentes do sistema
    
    **Apenas administradores têm acesso**
    """
    # TODO: Implementar sistema de logs
    return {
        "message": "Sistema de logs não implementado ainda",
        "admin": current_admin.get("email")
    }


# Exemplo usando require_roles para permitir admin E premium
@router.get("/premium-content")
async def premium_content(
    current_user: Dict = Depends(require_roles(UserRole.admin, UserRole.premium))
):
    """
    Exemplo de rota acessível por admins E usuários premium
    
    Demonstra o uso da factory function require_roles
    """
    return {
        "message": "Conteúdo premium",
        "user_role": current_user.get("role"),
        "access_level": "premium" if current_user.get("role") == "premium" else "admin"
    }
