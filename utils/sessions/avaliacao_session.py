class AvaliacaoSession:
    
    """
    Gerencia o estado temporário de uma avaliação em andamento.
    No Flet, você pode instanciar essa classe e guardá-bar no page.session.
    """
    
    def __init__(self):
        self.professor_id = None
        self.disciplina_id = None
        self.respostas = {}  # Formato: {"id_do_indicador": nota}

    def iniciar_avaliacao(self, professor_id: str, disciplina_id: str):
        self.professor_id = professor_id
        self.disciplina_id = disciplina_id
        self.respostas = {}

    def registrar_resposta(self, indicador_id: str, nota: int):
        """Salva ou atualiza a nota de um indicador específico."""
        self.respostas[indicador_id] = nota

    def obter_progresso(self, total_indicadores: int) -> float:
        """Retorna o percentual de conclusão (0.0 a 1.0)."""
        if total_indicadores == 0:
            return 0.0
        return len(self.respostas) / total_indicadores

    def formatar_para_envio(self) -> list:
        """Converte o dicionário interno para a lista que o Firebase espera."""
        return [{"indicador_id": ind, "nota": nota} for ind, nota in self.respostas.items()]
    
    def limpar(self):
        """Limpa a sessão após o envio bem-sucedido."""
        self.professor_id = None
        self.disciplina_id = None
        self.respostas = {}