from typing import Optional


class AvaliacaoSession:
    """Gerencia o estado temporário (State Management) de uma avaliação em andamento.

    Projetada para atuar em conjunto com o Flet, onde uma instância desta classe
    pode ser armazenada com segurança em `page.session.set()` para manter os dados
    vivos enquanto o usuário navega entre as etapas do formulário.

    NOTA: não identifiquei nenhum ponto do projeto (incluindo form_controller.py,
    já revisado) que instancie ou use esta classe atualmente — o formulário mantém
    seu próprio estado local em vez de usá-la. Pode ser um componente já pronto
    aguardando integração, ou código legado de uma versão anterior; vale confirmar
    antes de removê-la ou de conectá-la ao fluxo do formulário.
    """

    def __init__(self) -> None:
        """Inicializa a sessão com valores nulos e um dicionário de respostas vazio."""
        self.professor_id: Optional[str] = None
        self.disciplina_id: Optional[str] = None

        # Formato esperado: {"id_do_indicador_X": 4, "id_do_indicador_Y": 5}
        self.respostas: dict[str, int] = {}

    def iniciar_avaliacao(self, professor_id: str, disciplina_id: str) -> None:
        """Prepara a sessão para uma nova avaliação, reaproveitando a mesma instância.

        Args:
            professor_id: ID único do professor sendo avaliado.
            disciplina_id: ID único da disciplina em questão.
        """
        self.professor_id = professor_id
        self.disciplina_id = disciplina_id
        self.respostas = {}

    def registrar_resposta(self, indicador_id: str, nota: int) -> None:
        """Salva ou atualiza a nota de um indicador específico.

        Args:
            indicador_id: chave do critério sendo avaliado (ex: "didatica_01").
            nota: valor numérico atribuído pelo usuário (ex: 1 a 5).
        """
        self.respostas[indicador_id] = nota

    def obter_progresso(self, total_indicadores: int) -> float:
        """Calcula a porcentagem de conclusão do formulário (0.0 a 1.0).

        Args:
            total_indicadores: número total de perguntas do formulário.
        """
        if total_indicadores == 0:
            return 0.0
        return len(self.respostas) / total_indicadores

    def formatar_para_envio(self) -> list[dict]:
        """Converte o dicionário interno em uma lista de objetos, formato mais
        amigável para consultas em bancos NoSQL como o Firestore.

        Returns:
            Ex.: [{"indicador_id": "ind_01", "nota": 5}, {"indicador_id": "ind_02", "nota": 4}]
        """
        return [{"indicador_id": ind, "nota": nota} for ind, nota in self.respostas.items()]

    def limpar(self) -> None:
        """Reseta completamente a sessão. Chamar após o envio bem-sucedido ao banco."""
        self.professor_id = None
        self.disciplina_id = None
        self.respostas = {}