from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.schemas import (
    BuildQuery, BuildResponse, MessageResponse,
    BuildCreate, BuildUpdate, BuildResponseDB
)
from app.services.gemini_service import gemini_service
from app.services.rag_service import rag_service
from app.services.cache_service import cache_service
from app.services.supabase_service import supabase_service
from app.core.security import get_current_user

router = APIRouter(prefix="/builds", tags=["Builds"])


@router.post("/", response_model=BuildResponse)
async def get_build_recommendation(
    query: BuildQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna recomendação de build para um jogador específico
    
    - **player_name**: Nome do jogador (ex: "Neymar Jr")
    - **position**: Posição desejada (ex: "CF", "LWF", "AMF")
    """
    user_id = current_user["user_id"]
    
    # 1. Verificar quota
    has_quota = await supabase_service.check_and_increment_quota(user_id)
    if not has_quota:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite diário de perguntas atingido. Faça upgrade para Premium!"
        )
    
    # 2. Verificar cache
    cache_key = cache_service.generate_build_key(query.player_name, query.position)
    cached_response = cache_service.get(cache_key)
    
    if cached_response:
        cached_response["from_cache"] = True
        return BuildResponse(**cached_response)
    
    # 3. Buscar contexto no RAG (base de conhecimento)
    context = rag_service.find_build_context(query.player_name, query.position)
    
    # 4. Gerar resposta com Gemini
    try:
        ai_response = await gemini_service.generate_build_response(
            player_name=query.player_name,
            position=query.position,
            context=context
        )
        
        # Parse da resposta (simplificado - melhorar depois)
        response_data = {
            "player_name": query.player_name,
            "position": query.position,
            "priority_points": [
                {"skill": "Offensive Awareness", "points": 10},
                {"skill": "Finishing", "points": 10},
                {"skill": "Speed", "points": 8}
            ],
            "playstyle": "Goal Poacher",
            "tips": ai_response,
            "from_cache": False
        }
        
        # 5. Salvar no cache (1 semana)
        cache_service.set(cache_key, response_data, expire=604800)
        
        return BuildResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar build: {str(e)}"
        )


@router.get("/popular")
async def get_popular_builds():
    """
    Retorna lista de builds populares (top 10 jogadores)
    """
    # TODO: Implementar sistema de tracking de builds mais consultadas
    return {
        "popular_builds": [
            {"player": "Messi", "position": "RWF", "queries": 1523},
            {"player": "Ronaldo", "position": "CF", "queries": 1445},
            {"player": "Neymar", "position": "LWF", "queries": 1289},
        ]
    }


@router.post("/create", response_model=BuildResponseDB, status_code=status.HTTP_201_CREATED)
async def create_build(
    build_data: BuildCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Cria uma nova build de jogador
    
    - **card_id**: ID da carta do jogador
    - **title**: Título da build (ex: "Meta CF", "False 9")
    - **shooting, passing, dribbling, etc**: Pontos distribuídos (0-99 cada)
    - **overall_rating**: Overall final calculado (opcional)
    - **is_official_meta**: Se é uma build oficial/meta
    - **meta_content**: Conteúdo adicional em JSON (dicas, playstyle, etc)
    """
    user_id = current_user["user_id"]
    
    try:
        # Verificar se a carta existe
        card_response = supabase_service.client.table("cards")\
            .select("id, name")\
            .eq("id", build_data.card_id)\
            .execute()
        
        if not card_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carta com ID {build_data.card_id} não encontrada"
            )
        
        # Calcular total de pontos (validação básica - máximo ~100 pontos)
        total_points = (
            build_data.shooting + build_data.passing + build_data.dribbling +
            build_data.dexterity + build_data.lower_body_strength +
            build_data.aerial_strength + build_data.defending +
            build_data.gk_1 + build_data.gk_2 + build_data.gk_3
        )
        
        if total_points > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Total de pontos ({total_points}) excede o limite de 100"
            )
        
        # Inserir build no banco
        build_dict = build_data.dict()
        build_dict["user_id"] = user_id
        
        response = supabase_service.client.table("builds")\
            .insert(build_dict)\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar build no banco de dados"
            )
        
        return BuildResponseDB(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar build: {str(e)}"
        )


@router.get("/my-builds", response_model=List[BuildResponseDB])
async def get_my_builds(
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna todas as builds criadas pelo usuário atual
    """
    user_id = current_user["user_id"]
    
    try:
        response = supabase_service.client.table("builds")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()
        
        return [BuildResponseDB(**build) for build in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar builds: {str(e)}"
        )


@router.get("/card/{card_id}", response_model=List[BuildResponseDB])
async def get_builds_by_card(
    card_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna todas as builds para uma carta específica
    """
    try:
        response = supabase_service.client.table("builds")\
            .select("*")\
            .eq("card_id", card_id)\
            .order("is_official_meta", desc=True)\
            .order("created_at", desc=True)\
            .execute()
        
        return [BuildResponseDB(**build) for build in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar builds: {str(e)}"
        )


@router.get("/{build_id}", response_model=BuildResponseDB)
async def get_build_by_id(
    build_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna uma build específica por ID
    """
    try:
        response = supabase_service.client.table("builds")\
            .select("*")\
            .eq("id", build_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Build com ID {build_id} não encontrada"
            )
        
        return BuildResponseDB(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar build: {str(e)}"
        )


@router.put("/{build_id}", response_model=BuildResponseDB)
async def update_build(
    build_id: int,
    build_data: BuildUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza uma build existente (apenas o dono pode atualizar)
    """
    user_id = current_user["user_id"]
    
    try:
        # Verificar se a build existe e pertence ao usuário
        existing = supabase_service.client.table("builds")\
            .select("*")\
            .eq("id", build_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Build com ID {build_id} não encontrada"
            )
        
        if existing.data[0]["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para editar esta build"
            )
        
        # Atualizar apenas campos não nulos
        update_dict = {k: v for k, v in build_data.dict().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum campo para atualizar"
            )
        
        # Validar total de pontos se houver alteração
        if any(key in update_dict for key in ["shooting", "passing", "dribbling", "dexterity", 
                                                "lower_body_strength", "aerial_strength", 
                                                "defending", "gk_1", "gk_2", "gk_3"]):
            current_build = existing.data[0]
            total_points = sum([
                update_dict.get("shooting", current_build["shooting"]),
                update_dict.get("passing", current_build["passing"]),
                update_dict.get("dribbling", current_build["dribbling"]),
                update_dict.get("dexterity", current_build["dexterity"]),
                update_dict.get("lower_body_strength", current_build["lower_body_strength"]),
                update_dict.get("aerial_strength", current_build["aerial_strength"]),
                update_dict.get("defending", current_build["defending"]),
                update_dict.get("gk_1", current_build["gk_1"]),
                update_dict.get("gk_2", current_build["gk_2"]),
                update_dict.get("gk_3", current_build["gk_3"])
            ])
            
            if total_points > 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Total de pontos ({total_points}) excede o limite de 100"
                )
        
        response = supabase_service.client.table("builds")\
            .update(update_dict)\
            .eq("id", build_id)\
            .execute()
        
        return BuildResponseDB(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar build: {str(e)}"
        )


@router.delete("/{build_id}", response_model=MessageResponse)
async def delete_build(
    build_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Deleta uma build (apenas o dono ou admin pode deletar)
    """
    user_id = current_user["user_id"]
    user_role = current_user.get("role", "free")
    
    try:
        # Verificar se a build existe
        existing = supabase_service.client.table("builds")\
            .select("*")\
            .eq("id", build_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Build com ID {build_id} não encontrada"
            )
        
        # Apenas dono ou admin pode deletar
        if existing.data[0]["user_id"] != user_id and user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar esta build"
            )
        
        supabase_service.client.table("builds")\
            .delete()\
            .eq("id", build_id)\
            .execute()
        
        return MessageResponse(
            message="Build deletada com sucesso",
            detail=f"Build ID {build_id} foi removida"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar build: {str(e)}"
        )
