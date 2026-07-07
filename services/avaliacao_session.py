from typing import Dict, Any

class AvaliacaoSession:
    TOTAL_EIXOS = 3

    def __init__(self):
        self.reset()

    def reset(self):
        """Limpa o estado para iniciar uma nova avaliação do zero."""
        self.professor_id = None
        self.disciplina_id = None
        self.eixo_atual = 1
        self.indice_indicador = 0
        self.respostas: Dict[str, Dict[str, Any]] = {}
        self.finalizada = False

    def iniciar_avaliacao(self, professor_id: str, disciplina_id: str):
        self.reset()
        self.professor_id = professor_id
        self.disciplina_id = disciplina_id

    def salvar_resposta(self, indicador_id: str, nota: int, comentario: str = ""):
        """Salva ou atualiza a resposta do indicador atual na memória."""
        self.respostas[indicador_id] = {
            "nota": nota,
            "comentario": comentario
        }

    def get_resposta(self, indicador_id: str) -> Dict[str, Any]:
        """Recupera a resposta salva (útil caso o usuário retroceda)."""
        return self.respostas.get(indicador_id, {"nota": None, "comentario": ""})

    def avancar(self, total_indicadores_eixo_atual: int) -> str:
        """
        Calcula o próximo passo do fluxo.
        Retorna: 'proximo_indicador', 'proximo_eixo' ou 'finalizar'.
        """
        # Se ainda houver indicadores no eixo atual, apenas avança o índice
        if self.indice_indicador < total_indicadores_eixo_atual - 1:
            self.indice_indicador += 1
            return "proximo_indicador"
        
        # Se acabaram os indicadores, mas ainda há eixos, pula para o próximo eixo
        if self.eixo_atual < self.TOTAL_EIXOS:
            self.eixo_atual += 1
            self.indice_indicador = 0
            return "proximo_eixo"
        
        # Se acabaram os eixos e os indicadores, a avaliação acabou
        self.finalizada = True
        return "finalizar"

    def retroceder(self, total_indicadores_eixo_anterior: int = 0) -> str:
        """
        Calcula o passo anterior do fluxo.
        """
        if self.indice_indicador > 0:
            self.indice_indicador -= 1
            return "indicador_anterior"
        
        if self.eixo_atual > 1:
            self.eixo_atual -= 1
            # Ao voltar de eixo, o usuário deve cair no último indicador do eixo anterior
            self.indice_indicador = max(0, total_indicadores_eixo_anterior - 1)
            return "eixo_anterior"
        
        return "inicio"

# Instância global para uso no NiceGUI 
# (Se houver múltiplos usuários no futuro, migraremos isso para o app.storage.user)
session = AvaliacaoSession()