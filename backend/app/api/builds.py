from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import BuildQuery, BuildResponse, MessageResponse
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
