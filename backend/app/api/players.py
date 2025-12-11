from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from app.schemas import PlayerCreate, PlayerResponse, PlayerUpdate, MessageResponse
from app.services.supabase_service import supabase_service
from app.core.security import get_current_user
from app.models import UserRole

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_data: PlayerCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Cria um novo jogador
    
    **Apenas administradores podem criar jogadores**
    
    - **name**: Nome do jogador (ex: "Lionel Messi")
    - **nationality**: Nacionalidade (ex: "Argentina")
    """
    user_role = current_user.get("role", "free")
    
    if user_role != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar jogadores"
        )
    
    try:
        # Verificar se jogador já existe
        existing = supabase_service.client.table("players")\
            .select("id, name")\
            .ilike("name", player_data.name)\
            .execute()
        
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Jogador '{player_data.name}' já existe"
            )
        
        # Inserir jogador
        response = supabase_service.client.table("players")\
            .insert(player_data.dict())\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar jogador no banco de dados"
            )
        
        return PlayerResponse(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar jogador: {str(e)}"
        )


@router.get("/", response_model=List[PlayerResponse])
async def list_players(
    search: Optional[str] = None,
    nationality: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """
    Lista jogadores com filtros opcionais
    
    **Acessível para todos os usuários autenticados**
    
    - **search**: Busca por nome do jogador
    - **nationality**: Filtrar por nacionalidade
    - **limit**: Quantidade de resultados (padrão: 50)
    - **offset**: Paginação (padrão: 0)
    """
    try:
        query = supabase_service.client.table("players").select("*")
        
        if search:
            query = query.ilike("name", f"%{search}%")
        
        if nationality:
            query = query.eq("nationality", nationality)
        
        response = query.order("name", desc=False)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        return [PlayerResponse(**player) for player in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar jogadores: {str(e)}"
        )


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna dados de um jogador específico
    
    **Acessível para todos os usuários autenticados**
    """
    try:
        response = supabase_service.client.table("players")\
            .select("*")\
            .eq("id", player_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jogador com ID {player_id} não encontrado"
            )
        
        return PlayerResponse(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar jogador: {str(e)}"
        )


@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(
    player_id: int,
    player_data: PlayerUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza dados de um jogador
    
    **Apenas administradores podem atualizar jogadores**
    """
    user_role = current_user.get("role", "free")
    
    if user_role != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem editar jogadores"
        )
    
    try:
        # Verificar se jogador existe
        existing = supabase_service.client.table("players")\
            .select("id")\
            .eq("id", player_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jogador com ID {player_id} não encontrado"
            )
        
        # Atualizar apenas campos não nulos
        update_dict = {k: v for k, v in player_data.dict().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum campo para atualizar"
            )
        
        response = supabase_service.client.table("players")\
            .update(update_dict)\
            .eq("id", player_id)\
            .execute()
        
        return PlayerResponse(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar jogador: {str(e)}"
        )


@router.delete("/{player_id}", response_model=MessageResponse)
async def delete_player(
    player_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Deleta um jogador
    
    **Apenas administradores podem deletar jogadores**
    """
    user_role = current_user.get("role", "free")
    
    if user_role != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem deletar jogadores"
        )
    
    try:
        # Verificar se jogador existe
        existing = supabase_service.client.table("players")\
            .select("id")\
            .eq("id", player_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jogador com ID {player_id} não encontrado"
            )
        
        # Verificar se há cartas associadas
        cards = supabase_service.client.table("cards")\
            .select("id")\
            .eq("player_id", player_id)\
            .execute()
        
        if cards.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não é possível deletar jogador com {len(cards.data)} carta(s) associada(s)"
            )
        
        supabase_service.client.table("players")\
            .delete()\
            .eq("id", player_id)\
            .execute()
        
        return MessageResponse(
            message="Jogador deletado com sucesso",
            detail=f"Jogador ID {player_id} foi removido"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar jogador: {str(e)}"
        )
