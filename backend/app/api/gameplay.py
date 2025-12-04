from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import GameplayQuery, GameplayResponse, MessageResponse
from app.services.gemini_service import gemini_service
from app.services.rag_service import rag_service
from app.services.cache_service import cache_service
from app.services.supabase_service import supabase_service
from app.core.security import get_current_user

router = APIRouter(prefix="/gameplay", tags=["Gameplay"])


@router.post("/ask", response_model=GameplayResponse)
async def ask_gameplay_question(
    query: GameplayQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Faz uma pergunta sobre gameplay e recebe dicas do Pro Player via IA
    
    - **question**: Sua dúvida sobre gameplay (ex: "Como fazer finesse shot?")
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
    cache_key = cache_service.generate_gameplay_key(query.question)
    cached_response = cache_service.get(cache_key)
    
    if cached_response:
        cached_response["from_cache"] = True
        return GameplayResponse(**cached_response)
    
    # 3. Buscar contexto no RAG (FAQs do Pro Player)
    context = rag_service.find_gameplay_context(query.question)
    
    # 4. Gerar resposta com Gemini
    try:
        ai_response = await gemini_service.generate_gameplay_response(
            question=query.question,
            context=context
        )
        
        response_data = {
            "question": query.question,
            "answer": ai_response,
            "category": "Geral",
            "video_url": None,
            "from_cache": False
        }
        
        # 5. Salvar no cache (24 horas)
        cache_service.set(cache_key, response_data, expire=86400)
        
        return GameplayResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar pergunta: {str(e)}"
        )


@router.get("/categories")
async def get_categories():
    """
    Retorna categorias de dúvidas disponíveis
    """
    return {
        "categories": [
            {"name": "Ataque", "icon": "⚽", "questions_count": 15},
            {"name": "Defesa", "icon": "🛡️", "questions_count": 12},
            {"name": "Passes", "icon": "🎯", "questions_count": 8},
            {"name": "Finalizações", "icon": "🥅", "questions_count": 10},
            {"name": "Táticas", "icon": "📋", "questions_count": 7},
        ]
    }


@router.get("/faq")
async def get_faq():
    """
    Retorna FAQs mais comuns
    """
    faqs = rag_service.gameplay_data.get("faqs", [])[:10]
    return {"faqs": faqs}
