import json
import os
from typing import Optional, Dict, List
from pathlib import Path


class RAGService:
    """
    Serviço RAG (Retrieval-Augmented Generation) melhorado
    Busca contexto na base de conhecimento antes de consultar a IA
    
    Sistema de 3 camadas:
    1. Cartas Meta (exceções - jogadores específicos)
    2. Regras por Posição (padrões gerais)
    3. Problemas de Gameplay (sintoma → solução)
    """
    
    def __init__(self):
        self.knowledge_base_path = Path(__file__).parent.parent.parent / "knowledge_base"
        
        # Carrega arquivos da nova estrutura
        self.regras_posicoes = self._load_json("builds/regras_posicoes.json")
        self.cartas_meta = self._load_json("builds/cartas_meta.json")
        self.problemas_gameplay = self._load_json("gameplay/problemas_gameplay.json")
        
        # Mantém compatibilidade com arquivos antigos
        self.builds_data = self._load_json("builds/builds_guide.json")
        self.gameplay_data = self._load_json("gameplay/tactics_faq.json")
    
    def _load_json(self, relative_path: str) -> Dict:
        """Carrega arquivo JSON genérico"""
        file_path = self.knowledge_base_path / relative_path
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def find_build_context(self, player_name: str, position: str) -> Optional[str]:
        """
        Busca contexto de build na base de conhecimento
        
        Sistema de 3 camadas (ordem de prioridade):
        1. Carta Meta específica (ex: Neymar Big Time 2015)
        2. Regra geral da posição (ex: LWF Prolific Winger)
        3. Fallback para arquivo antigo (compatibilidade)
        """
        player_name_lower = player_name.lower().strip()
        position_upper = position.upper()
        
        # CAMADA 1: Buscar em Cartas Meta (exceções)
        for carta in self.cartas_meta.get("cartas_meta", []):
            if player_name_lower in carta["jogador"].lower():
                # Encontrou o jogador! Verificar se tem build para essa posição
                build_especifica = carta.get("build_especifica", {})
                
                if position_upper in build_especifica:
                    build = build_especifica[position_upper]
                    
                    # Formatar contexto RICO
                    context = f"### 🔥 CARTA META: {carta['jogador']} ({carta['versao']}) - {position_upper}\n\n"
                    context += f"**Por que é Meta?** {carta['por_que_e_meta']}\n\n"
                    context += f"**Playstyle Recomendado**: {build['playstyle_recomendado']}\n\n"
                    context += "**Distribuição de Pontos**:\n"
                    
                    for item in build["distribuicao"]:
                        context += f"- {item['atributo']}: {item['pontos']} pontos"
                        context += f" (💡 {item['justificativa']})\n"
                    
                    context += f"\n**Dicas Táticas do Pro Player**:\n"
                    for dica in build.get("dicas_taticas", []):
                        context += f"• {dica}\n"
                    
                    context += f"\n**Quando Usar**: {carta['quando_usar']}\n"
                    context += f"\n**Comentário do Pro**: \"{carta['comentario_pro']}\"\n"
                    
                    return context
        
        # CAMADA 2: Buscar em Regras por Posição (padrão geral)
        for regra in self.regras_posicoes.get("regras_por_posicao", []):
            if position_upper in regra["posicao"]:
                # Encontrou regra para essa posição
                # Por enquanto, usa o primeiro estilo disponível
                # TODO: Detectar estilo baseado em atributos do jogador
                
                estilos = regra.get("estilos", {})
                if estilos:
                    # Pega primeiro estilo (ou você pode implementar lógica para escolher)
                    primeiro_estilo = list(estilos.keys())[0]
                    estilo_data = estilos[primeiro_estilo]
                    
                    context = f"### Build Padrão para {regra['nome_posicao']} ({primeiro_estilo})\n\n"
                    context += f"**Descrição**: {estilo_data['descricao']}\n\n"
                    context += "**Prioridades de Build**:\n"
                    
                    for i in range(1, 4):
                        prio_key = f"prioridade_{i}"
                        if prio_key in estilo_data:
                            prio = estilo_data[prio_key]
                            context += f"{i}. {prio['atributo']}: {prio['pontos_sugeridos']} pontos "
                            context += f"(mínimo {prio['minimo']})\n"
                    
                    context += f"\n**Atributos a Ignorar**: {', '.join(estilo_data.get('ignorar', []))}\n"
                    context += f"\n**Dica Tática**: {estilo_data.get('dica_tatica', 'N/A')}\n"
                    
                    return context
        
        # CAMADA 3: Fallback para arquivo antigo (compatibilidade)
        for player in self.builds_data.get("players", []):
            if player_name_lower in player["name"].lower():
                positions = player.get("positions", {})
                
                if position_upper in positions:
                    build_data = positions[position_upper]
                    
                    context = f"### Build Oficial do Pro Player para {player['name']} - {position_upper}\n\n"
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
        
        Sistema de 2 camadas:
        1. Problemas de Gameplay (novo - sintoma → solução)
        2. FAQs antigas (compatibilidade)
        """
        question_lower = question.lower()
        
        # CAMADA 1: Buscar em Problemas de Gameplay (mais detalhado)
        best_match = None
        best_score = 0
        
        for problema in self.problemas_gameplay.get("problemas_gameplay", []):
            sintoma_lower = problema["sintoma"].lower()
            
            # Score de similaridade com sintoma
            common_words = set(question_lower.split()) & set(sintoma_lower.split())
            score = len(common_words)
            
            # Boost se categorias comuns aparecem
            categorias_keywords = {
                "defesa": ["defender", "defesa", "tomo gol", "levar gol"],
                "ataque": ["atacar", "ataque", "fazer gol", "finalizar"],
                "passe": ["passe", "passar", "assistencia"],
                "drible": ["drible", "driblar"]
            }
            
            for keywords in categorias_keywords.values():
                if any(kw in question_lower for kw in keywords):
                    if any(kw in sintoma_lower for kw in keywords):
                        score += 2  # Boost por contexto semântico
            
            if score > best_score:
                best_score = score
                best_match = problema
        
        if best_match and best_score >= 2:
            # Formatar contexto DETALHADO
            context = f"### 🎯 Problema Identificado: {best_match['sintoma']}\n\n"
            context += f"**Categoria**: {best_match['categoria']}\n"
            context += f"**Gravidade**: {best_match['gravidade']}\n\n"
            context += f"**Causa Raiz**: {best_match['causa_raiz']}\n\n"
            
            solucao = best_match.get("solucao", {})
            context += "**Solução Passo a Passo**:\n"
            for passo in solucao.get("passos", []):
                context += f"{passo}\n"
            
            context += f"\n**Comandos Específicos**: {solucao.get('comandos_especificos', 'N/A')}\n"
            context += f"\n**Erro Comum**: {solucao.get('erro_comum', 'N/A')}\n"
            context += f"\n**Dica Extra**: {solucao.get('dica_extra', 'N/A')}\n"
            context += f"\n**Efetividade**: {best_match.get('efetividade', 'N/A')}\n"
            
            return context
        
        # CAMADA 2: Fallback para FAQs antigas
        best_match_old = None
        best_score_old = 0
        
        for faq in self.gameplay_data.get("faqs", []):
            faq_question = faq["question"].lower()
            
            common_words = set(question_lower.split()) & set(faq_question.split())
            score = len(common_words)
            
            if score > best_score_old:
                best_score_old = score
                best_match_old = faq
        
        if best_match_old and best_score_old >= 2:
            context = f"### Dica do Pro Player\n\n"
            context += f"**Categoria**: {best_match_old.get('category', 'Geral')}\n\n"
            context += f"**Resposta**: {best_match_old['answer']}\n\n"
            
            if best_match_old.get("video_url"):
                context += f"**Tutorial em Vídeo**: {best_match_old['video_url']}\n"
            
            return context
        
        return None
    
    def get_all_meta_cards(self) -> List[Dict]:
        """Retorna lista de todas as cartas meta"""
        return self.cartas_meta.get("cartas_meta", [])
    
    def get_categories_stats(self) -> Dict:
        """Retorna estatísticas das categorias de gameplay"""
        return {
            "total_problemas": len(self.problemas_gameplay.get("problemas_gameplay", [])),
            "categorias": self.problemas_gameplay.get("categorias", [])
        }
    
    def reload_knowledge_base(self):
        """Recarrega a base de conhecimento (útil após scraping ou atualização)"""
        self.regras_posicoes = self._load_json("builds/regras_posicoes.json")
        self.cartas_meta = self._load_json("builds/cartas_meta.json")
        self.problemas_gameplay = self._load_json("gameplay/problemas_gameplay.json")
        
        # Mantém compatibilidade
        self.builds_data = self._load_json("builds/builds_guide.json")
        self.gameplay_data = self._load_json("gameplay/tactics_faq.json")


rag_service = RAGService()
