from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from app.schemas import CardCreate, CardResponse, CardUpdate, MessageResponse
from app.services.supabase_service import supabase_service
from app.core.security import get_current_user

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def create_card(
    card_data: CardCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Cria uma nova carta de jogador
    
    **Apenas administradores podem criar cartas**
    
    - **player_id**: ID do jogador associado
    - **name**: Nome da carta (ex: "Messi TOTY 2024")
    - **version**: Versão da carta (ex: "TOTY", "Base", "Icon")
    - **card_type**: Tipo (ex: "Legend", "Featured", "Standard")
    - **position**: Posição (ex: "RWF", "CF", "AMF")
    - **overall_rating**: Overall da carta (ex: 98)
    - **image_url**: URL da imagem da carta (opcional)
    """
    user_role = current_user.get("role", "free")
    
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar cartas"
        )
    
    try:
        # Verificar se o jogador existe
        player = supabase_service.client.table("players")\
            .select("id, name")\
            .eq("id", card_data.player_id)\
            .execute()
        
        if not player.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jogador com ID {card_data.player_id} não encontrado. Crie o jogador primeiro."
            )
        
        # Inserir carta
        response = supabase_service.client.table("cards")\
            .insert(card_data.dict())\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar carta no banco de dados"
            )
        
        return CardResponse(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar carta: {str(e)}"
        )


@router.get("/", response_model=List[CardResponse])
async def list_cards(
    player_id: Optional[int] = None,
    position: Optional[str] = None,
    card_type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """
    Lista cartas com filtros opcionais
    
    **Acessível para todos os usuários autenticados**
    
    - **player_id**: Filtrar por jogador
    - **position**: Filtrar por posição
    - **card_type**: Filtrar por tipo de carta
    - **search**: Busca por nome da carta
    - **limit**: Quantidade de resultados (padrão: 50)
    - **offset**: Paginação (padrão: 0)
    """
    try:
        query = supabase_service.client.table("cards").select("*")
        
        if player_id:
            query = query.eq("player_id", player_id)
        
        if position:
            query = query.eq("position", position)
        
        if card_type:
            query = query.eq("card_type", card_type)
        
        if search:
            query = query.ilike("name", f"%{search}%")
        
        response = query.order("overall_rating", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        return [CardResponse(**card) for card in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar cartas: {str(e)}"
        )


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna dados de uma carta específica
    
    **Acessível para todos os usuários autenticados**
    """
    try:
        response = supabase_service.client.table("cards")\
            .select("*")\
            .eq("id", card_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carta com ID {card_id} não encontrada"
            )
        
        return CardResponse(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar carta: {str(e)}"
        )


@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: int,
    card_data: CardUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza dados de uma carta
    
    **Apenas administradores podem atualizar cartas**
    """
    user_role = current_user.get("role", "free")
    
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem editar cartas"
        )
    
    try:
        # Verificar se carta existe
        existing = supabase_service.client.table("cards")\
            .select("id")\
            .eq("id", card_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carta com ID {card_id} não encontrada"
            )
        
        # Atualizar apenas campos não nulos
        update_dict = {k: v for k, v in card_data.dict().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum campo para atualizar"
            )
        
        response = supabase_service.client.table("cards")\
            .update(update_dict)\
            .eq("id", card_id)\
            .execute()
        
        return CardResponse(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar carta: {str(e)}"
        )


@router.delete("/{card_id}", response_model=MessageResponse)
async def delete_card(
    card_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Deleta uma carta
    
    **Apenas administradores podem deletar cartas**
    """
    user_role = current_user.get("role", "free")
    
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem deletar cartas"
        )
    
    try:
        # Verificar se carta existe
        existing = supabase_service.client.table("cards")\
            .select("id")\
            .eq("id", card_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carta com ID {card_id} não encontrada"
            )
        
        # Verificar se há builds associadas
        builds = supabase_service.client.table("builds")\
            .select("id")\
            .eq("card_id", card_id)\
            .execute()
        
        if builds.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não é possível deletar carta com {len(builds.data)} build(s) associada(s)"
            )
        
        supabase_service.client.table("cards")\
            .delete()\
            .eq("id", card_id)\
            .execute()
        
        return MessageResponse(
            message="Carta deletada com sucesso",
            detail=f"Carta ID {card_id} foi removida"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar carta: {str(e)}"
        )
