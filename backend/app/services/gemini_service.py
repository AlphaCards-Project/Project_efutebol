from groq import Groq
from app.core.config import settings
from typing import Dict, Optional


class GeminiService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
    
    async def generate_build_response(
        self,
        player_name: str,
        position: str,
        context: Optional[str] = None
    ) -> str:
        """
        Gera resposta sobre build de carta usando Groq AI
        """
        system_prompt = "Você é um especialista em eFootball que ajuda jogadores a montar builds de cartas. Responda em português do Brasil, de forma clara e objetiva."
        
        user_prompt = f"""
Jogador: {player_name}
Posição: {position}

{f"Contexto adicional do Pro Player:\n{context}\n" if context else ""}

Forneça uma build detalhada com:
1. Distribuição de pontos prioritários (habilidades principais)
2. Playstyle recomendado
3. Dicas táticas de como usar esse jogador
"""

        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=self.model,
            temperature=0.7,
        )
        return completion.choices[0].message.content
    
    async def generate_gameplay_response(
        self,
        question: str,
        context: Optional[str] = None
    ) -> str:
        """
        Gera resposta sobre gameplay usando Groq AI
        """
        system_prompt = "Você é um coach profissional de eFootball que ajuda jogadores a melhorarem seu gameplay. Responda em português do Brasil."
        
        user_prompt = f"""
Pergunta do jogador: {question}

{f"Dicas do Pro Player:\n{context}\n" if context else ""}

Forneça uma resposta:
1. Clara e objetiva
2. Com passos práticos
3. Incluindo comandos específicos (botões do controle)
4. Dicas extras se aplicável
"""

        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=self.model,
            temperature=0.7,
        )
        return completion.choices[0].message.content
    
    async def simple_query(self, prompt: str) -> str:
        """Query genérica ao Groq"""
        completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            temperature=0.7,
        )
        return completion.choices[0].message.content


# Mantendo o nome da instância para compatibilidade com o resto do código
gemini_service = GeminiService()
