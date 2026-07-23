class AvaliacaoSession:
    """
    Gerencia o estado temporário (State Management) de uma avaliação em andamento.
    Projetada para atuar em conjunto com o Flet, onde uma instância desta classe 
    pode ser armazenada com segurança em `page.session.set()` para manter os dados 
    vivos enquanto o usuário navega entre as etapas do formulário.
    """
    
    def __init__(self):
        """
        Inicializa a sessão com valores nulos e um dicionário vazio.
        Garante que a classe já nasça com a estrutura de dados correta,
        evitando erros de 'AttributeError' ao tentar acessar as variáveis.
        """
        self.professor_id = None
        self.disciplina_id = None
        
        # O dicionário é perfeito aqui, pois garante que o usuário pode mudar 
        # a nota de um mesmo indicador várias vezes sem duplicar o registro.
        # Formato esperado: {"id_do_indicador_X": 4, "id_do_indicador_Y": 5}
        self.respostas = {} 

    def iniciar_avaliacao(self, professor_id: str, disciplina_id: str):
        """
        Prepara a sessão para uma nova avaliação.
        Útil para reaproveitar a mesma instância da classe sem precisar destruí-la
        e recriá-la na memória.
        
        Args:
            professor_id (str): O ID único do professor sendo avaliado.
            disciplina_id (str): O ID único da disciplina em questão.
        """
        self.professor_id = professor_id
        self.disciplina_id = disciplina_id
        
        # Zera as respostas anteriores, garantindo que o novo formulário comece limpo
        self.respostas = {}

    def registrar_resposta(self, indicador_id: str, nota: int):
        """
        Salva uma nova nota ou atualiza uma nota existente para um indicador específico.
        
        Args:
            indicador_id (str): A chave do critério sendo avaliado (ex: "didatica_01").
            nota (int): O valor numérico atribuído pelo usuário (ex: 1 a 5).
        """
        # Se a chave 'indicador_id' já existir, o dicionário apenas sobrescreve o valor.
        # Isso é ideal para componentes como Sliders ou RadioButtons, onde o usuário
        # pode mudar de ideia antes de enviar o formulário.
        self.respostas[indicador_id] = nota

    def obter_progresso(self, total_indicadores: int) -> float:
        """
        Calcula a porcentagem de conclusão do formulário.
        Excelente para alimentar barras de progresso (ProgressBar) na interface de usuário.
        
        Args:
            total_indicadores (int): O número total de perguntas que o formulário possui.
            
        Returns:
            float: Um valor decimal entre 0.0 e 1.0 representando o progresso.
        """
        # Prevenção contra divisão por zero, caso o formulário não tenha perguntas cadastradas
        if total_indicadores == 0:
            return 0.0
            
        # O tamanho (len) do dicionário indica quantas perguntas únicas já foram respondidas
        return len(self.respostas) / total_indicadores

    def formatar_para_envio(self) -> list:
        """
        Converte o dicionário interno para o formato de lista de objetos (dicts).
        Muitos bancos de dados NoSQL (como o Firebase) lidam melhor com listas de objetos
        do que com dicionários de chaves dinâmicas ao realizar consultas (queries) posteriormente.
        
        Returns:
            list: Exemplo: [{"indicador_id": "ind_01", "nota": 5}, {"indicador_id": "ind_02", "nota": 4}]
        """
        # Utiliza List Comprehension para iterar pelas chaves e valores simultaneamente (.items())
        return [{"indicador_id": ind, "nota": nota} for ind, nota in self.respostas.items()]
    
    def limpar(self):
        """
        Reseta completamente a sessão.
        Deve ser chamada estritamente após o envio bem-sucedido dos dados ao banco de dados,
        garantindo que não fiquem dados sensíveis na memória ("vazamento de estado").
        """
        self.professor_id = None
        self.disciplina_id = None
        self.respostas = {}