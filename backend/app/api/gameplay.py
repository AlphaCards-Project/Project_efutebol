from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import Optional
from app.schemas import GameplayQuery, GameplayResponse, MessageResponse
from app.services.gemini_service import gemini_service
from app.services.rag_service import rag_service
from app.services.cache_service import cache_service
from app.services.supabase_service import supabase_service
from app.core.security import get_current_user_optional

router = APIRouter(prefix="/gameplay", tags=["Gameplay"])


@router.post("/ask", response_model=GameplayResponse)
async def ask_gameplay_question(
    query: GameplayQuery,
    request: Request,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Faz uma pergunta sobre gameplay e recebe dicas do Pro Player via IA
    
    - **question**: Sua dúvida sobre gameplay (ex: "Como fazer finesse shot?")
    
    **Modo sem login:** Usa apenas cache (respostas comuns)
    **Modo logado:** Usa IA + cache + quota de perguntas diárias
    """
    
    # 1. Verificar cache primeiro (para todos)
    cache_key = cache_service.generate_gameplay_key(query.question)
    cached_response = cache_service.get(cache_key)
    
    if cached_response:
        cached_response["from_cache"] = True
        return GameplayResponse(**cached_response)
    
    # 2. Se não logado, apenas retorna resposta genérica do cache/FAQ
    if not current_user:
        # Busca contexto no RAG (base de conhecimento local)
        context = rag_service.find_gameplay_context(query.question)
        
        if context:
            # context é uma string formatada com a resposta
            response_data = {
                "question": query.question,
                "answer": context,
                "category": "FAQ",
                "video_url": None,
                "from_cache": True
            }
            return GameplayResponse(**response_data)
        
        # Se não tem no FAQ, informa que precisa login
        response_data = {
            "question": query.question,
            "answer": "🔒 Pergunta não encontrada no FAQ gratuito.\n\nFaça login para acessar a IA completa e fazer qualquer pergunta sobre eFootball!",
            "category": "Sistema",
            "video_url": None,
            "from_cache": False
        }
        return GameplayResponse(**response_data)
    
    # 3. Usuário logado - verificar quota
    user_id = current_user["user_id"]
    has_quota = await supabase_service.check_and_increment_quota(user_id)
    if not has_quota:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite diário de perguntas atingido. Faça upgrade para Premium!"
        )
    
    # 4. Buscar contexto no RAG (FAQs do Pro Player)
    context = rag_service.find_gameplay_context(query.question)
    
    # 5. Gerar resposta com IA
    try:
        ai_response = await gemini_service.generate_gameplay_response(
            question=query.question,
            context=context
        )
        
        response_data = {
            "question": query.question,
            "answer": ai_response,
            "category": "Davi",
            "video_url": None,
            "from_cache": False
        }
        
        # 6. Salvar no cache (24 horas)
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
