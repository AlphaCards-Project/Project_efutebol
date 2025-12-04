import json
import os
from typing import Optional, Dict, List
from pathlib import Path


class RAGService:
    """
    Serviço RAG (Retrieval-Augmented Generation) simples
    Busca contexto na base de conhecimento antes de consultar a IA
    """
    
    def __init__(self):
        self.knowledge_base_path = Path(__file__).parent.parent.parent / "knowledge_base"
        self.builds_data = self._load_builds()
        self.gameplay_data = self._load_gameplay()
    
    def _load_builds(self) -> Dict:
        """Carrega dados de builds"""
        builds_file = self.knowledge_base_path / "builds" / "builds_guide.json"
        if builds_file.exists():
            with open(builds_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"players": []}
    
    def _load_gameplay(self) -> Dict:
        """Carrega FAQs de gameplay"""
        gameplay_file = self.knowledge_base_path / "gameplay" / "tactics_faq.json"
        if gameplay_file.exists():
            with open(gameplay_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"faqs": []}
    
    def find_build_context(self, player_name: str, position: str) -> Optional[str]:
        """
        Busca contexto de build na base de conhecimento
        """
        player_name_lower = player_name.lower().strip()
        
        for player in self.builds_data.get("players", []):
            if player_name_lower in player["name"].lower():
                positions = player.get("positions", {})
                
                if position in positions:
                    build_data = positions[position]
                    
                    # Formatar contexto
                    context = f"### Build Oficial do Pro Player para {player['name']} - {position}\n\n"
                    context += f"**Playstyle**: {build_data.get('playstyle', 'N/A')}\n\n"
                    context += "**Distribuição de Pontos Prioritários**:\n"
                    
                    for skill in build_data.get("priority_points", []):
                        context += f"- {skill['skill']}: {skill['points']} pontos\n"
                    
                    context += f"\n**Dicas Táticas**: {build_data.get('tips', 'N/A')}\n"
                    
                    return context
        
        return None
    
    def find_gameplay_context(self, question: str) -> Optional[str]:
        """
        Busca contexto de gameplay na base de conhecimento
        """
        question_lower = question.lower()
        
        # Busca por palavras-chave
        best_match = None
        best_score = 0
        
        for faq in self.gameplay_data.get("faqs", []):
            faq_question = faq["question"].lower()
            
            # Score simples de similaridade
            common_words = set(question_lower.split()) & set(faq_question.split())
            score = len(common_words)
            
            if score > best_score:
                best_score = score
                best_match = faq
        
        if best_match and best_score >= 2:  # Pelo menos 2 palavras em comum
            context = f"### Dica do Pro Player\n\n"
            context += f"**Categoria**: {best_match.get('category', 'Geral')}\n\n"
            context += f"**Resposta**: {best_match['answer']}\n\n"
            
            if best_match.get("video_url"):
                context += f"**Tutorial em Vídeo**: {best_match['video_url']}\n"
            
            return context
        
        return None
    
    def reload_knowledge_base(self):
        """Recarrega a base de conhecimento (útil após scraping)"""
        self.builds_data = self._load_builds()
        self.gameplay_data = self._load_gameplay()


rag_service = RAGService()
