from typing import Optional

class AvaliacaoSession:
    """Gerencia o estado temporário (State Management) de uma avaliação em andamento.

    NOTA: Identificado que o Controller do formulário atual gerencia seu próprio estado local. 
    Esta classe pode atuar como um excelente componente futuro para isolar o estado no `page.session.set()` do Flet, 
    garantindo sobrevivência dos dados durante a navegação.
    """

    def __init__(self) -> None:
        """Inicializa a sessão com valores nulos e um dicionário de respostas vazio."""
        self.professor_id: Optional[str] = None
        self.disciplina_id: Optional[str] = None
        # Formato esperado: {"id_do_indicador_X": 4, "id_do_indicador_Y": 5}
        self.respostas: dict[str, int] = {}

    def iniciar_avaliacao(self, professor_id: str, disciplina_id: str) -> None:
        """Prepara a sessão para uma nova avaliação, reaproveitando a mesma instância na memória."""
        self.professor_id = professor_id
        self.disciplina_id = disciplina_id
        self.respostas = {}

    def registrar_resposta(self, indicador_id: str, nota: int) -> None:
        """Salva ou atualiza a nota atribuída pelo usuário em um dicionário interno."""
        self.respostas[indicador_id] = nota

    def obter_progresso(self, total_indicadores: int) -> float:
        """Calcula matematicamente a porcentagem de conclusão do formulário (escala 0.0 a 1.0 para ProgressBar)."""
        if total_indicadores == 0:
            return 0.0
        return len(self.respostas) / total_indicadores

    def formatar_para_envio(self) -> list[dict]:
        """Gera uma lista de objetos padronizada, sendo um formato muito mais amigável para bancos NoSQL."""
        return [{"indicador_id": ind, "nota": nota} for ind, nota in self.respostas.items()]

    def limpar(self) -> None:
        """Reseta completamente a sessão da memória após sucesso no envio."""
        self.professor_id = None
        self.disciplina_id = None
        self.respostas = {}