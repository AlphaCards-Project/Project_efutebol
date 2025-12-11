"""
Dependências de Autenticação e Autorização (RBAC)
"""
from fastapi import Depends, HTTPException, status
from typing import Dict
from app.core.security import get_current_user
from app.models import UserRole


async def get_current_admin(
    current_user: Dict = Depends(get_current_user)
) -> Dict:
    """
    Dependency Injection para verificar se o usuário é administrador.
    
    Esta função atua como um "porteiro" que bloqueia acesso a rotas sensíveis.
    Só permite passar usuários com role 'admin'.
    
    Args:
        current_user: Dados do usuário autenticado (injetado por get_current_user)
    
    Returns:
        Dict: Dados do usuário admin
    
    Raises:
        HTTPException: 403 FORBIDDEN se o usuário não for admin
    
    Exemplo de uso:
        @router.post("/admin/cards")
        async def create_card(user: Dict = Depends(get_current_admin)):
            # Apenas admins chegam aqui
            pass
    """
    user_role = current_user.get("role", "free")
    
    # Verificação crítica: bloqueia não-admins
    if user_role != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Privilégios de administrador são necessários para esta operação."
        )
    
    return current_user


async def get_current_premium_user(
    current_user: Dict = Depends(get_current_user)
) -> Dict:
    """
    Dependency para verificar se o usuário é premium ou admin.
    
    Permite acesso a funcionalidades premium.
    
    Args:
        current_user: Dados do usuário autenticado
    
    Returns:
        Dict: Dados do usuário premium/admin
    
    Raises:
        HTTPException: 403 FORBIDDEN se o usuário for free
    """
    user_role = current_user.get("role", "free")
    is_premium = current_user.get("is_premium", False)
    
    # Admin sempre tem acesso
    if user_role == UserRole.admin.value:
        return current_user
    
    # Verifica se é premium
    if not is_premium and user_role != UserRole.premium.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta funcionalidade requer assinatura premium."
        )
    
    return current_user


def require_roles(*allowed_roles: UserRole):
    """
    Factory function para criar dependências que verificam múltiplas roles.
    
    Uso avançado para verificar se usuário tem uma das roles permitidas.
    
    Args:
        *allowed_roles: Roles permitidas (UserRole.admin, UserRole.premium, etc)
    
    Returns:
        Função de dependência que valida as roles
    
    Exemplo:
        @router.get("/special-feature")
        async def special_feature(
            user: Dict = Depends(require_roles(UserRole.admin, UserRole.premium))
        ):
            pass
    """
    async def check_role(current_user: Dict = Depends(get_current_user)) -> Dict:
        user_role = current_user.get("role", "free")
        
        # Converte roles permitidas para valores string
        allowed_values = [role.value for role in allowed_roles]
        
        if user_role not in allowed_values:
            roles_str = ", ".join(allowed_values)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Roles permitidas: {roles_str}"
            )
        
        return current_user
    
    return check_role
