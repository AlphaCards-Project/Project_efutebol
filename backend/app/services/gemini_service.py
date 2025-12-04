import google.generativeai as genai
from app.core.config import settings
from typing import Dict, Optional


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_build_response(
        self, 
        player_name: str, 
        position: str,
        context: Optional[str] = None
    ) -> str:
        """
        Gera resposta sobre build de carta usando Gemini
        """
        prompt = f"""Você é um especialista em eFootball que ajuda jogadores a montar builds de cartas.

Jogador: {player_name}
Posição: {position}

{f"Contexto adicional do Pro Player:\n{context}\n" if context else ""}

Forneça uma build detalhada com:
1. Distribuição de pontos prioritários (habilidades principais)
2. Playstyle recomendado
3. Dicas táticas de como usar esse jogador

Responda em português do Brasil, de forma clara e objetiva."""

        response = self.model.generate_content(prompt)
        return response.text
    
    async def generate_gameplay_response(
        self, 
        question: str,
        context: Optional[str] = None
    ) -> str:
        """
        Gera resposta sobre gameplay usando Gemini
        """
        prompt = f"""Você é um coach profissional de eFootball que ajuda jogadores a melhorarem seu gameplay.

Pergunta do jogador: {question}

{f"Dicas do Pro Player:\n{context}\n" if context else ""}

Forneça uma resposta:
1. Clara e objetiva
2. Com passos práticos
3. Incluindo comandos específicos (botões do controle)
4. Dicas extras se aplicável

Responda em português do Brasil."""

        response = self.model.generate_content(prompt)
        return response.text
    
    async def simple_query(self, prompt: str) -> str:
        """Query genérica ao Gemini"""
        response = self.model.generate_content(prompt)
        return response.text


gemini_service = GeminiService()
