import flet as ft

def criar_card_pergunta(page, indicador, estado):
    """
    Constrói o cartão visual (Card) para uma pergunta específica da avaliação.
    Inclui o título, descrição, e um slider interativo que exibe o critério em tempo real.
    """
    
    # Extrai as informações base do indicador atual
    titulo_ind = indicador["titulo"]
    criterios = indicador.get("criterios", {})

    # Resgata o valor anterior salvo no estado caso o usuário tenha clicado em "Anterior" e retornado para esta pergunta.
    # Se for a primeira vez acessando a pergunta, define o valor intermediário (3) como padrão.
    valor_inicial = estado["respostas"].get(titulo_ind, 3)
    
    # Busca a descrição de texto que corresponde à nota inicial (ex: o que significa dar nota 3?).
    # Usa duplo .get() para prevenir erros caso a chave no JSON tenha sido salva como string ou inteiro.
    texto_inicial = criterios.get(str(valor_inicial), criterios.get(valor_inicial, "Critério não definido."))

    # Textos que serão alterados dinamicamente na tela.
    # Precisam ser criados fora da estrutura final para podermos modificar a propriedade '.value' deles depois.
    lbl_nota_destaque = ft.Text(str(valor_inicial), size=28, weight="bold", color="primary")
    txt_criterio_dinamico = ft.Text(texto_inicial, size=14, color="onSurfaceVariant", italic=True, text_align=ft.TextAlign.CENTER)

    def ao_deslizar(e):
        """
        Callback disparado sempre que o usuário move o controle deslizante (Slider).
        Atualiza o estado central e modifica os textos na tela instantaneamente.
        """
        # Captura o novo valor do Slider e converte para inteiro
        nota_atual = int(e.control.value)
        
        # Salva a resposta no dicionário global de estado na memória
        estado["respostas"][titulo_ind] = nota_atual
        
        # Atualiza a interface gráfica com o número em destaque e o texto descritivo
        lbl_nota_destaque.value = str(nota_atual)
        txt_criterio_dinamico.value = criterios.get(str(nota_atual), criterios.get(nota_atual, "Sem descrição."))
        
        # Comunica o Flet que essas pequenas partes da interface mudaram e precisam ser redesenhadas
        page.update()

    # Cria o controle deslizante com 5 etapas (escala Likert de 1 a 5)
    slider_nota = ft.Slider(
        min=1, 
        max=5, 
        divisions=4, # Cria os "degraus" para que o valor não seja quebrado (como 3.4), forçando números inteiros.
        value=valor_inicial, # Define onde a bolinha inicia
        active_color="primary",
        inactive_color="outlineVariant",
        on_change=ao_deslizar, # Vincula a função criada acima
        expand=True # Ocupa toda a largura horizontal disponível na Row
    )

    # Retorna a estrutura final empacotada em um Card elegante com sombras
    return ft.Container(
        bgcolor="surface", # Fundo adaptativo
        padding=30, # Espaço interno generoso
        border_radius=12,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="shadow"), # Efeito de elevação
        content=ft.Column(
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza todos os componentes internos verticalmente
            controls=[
                # Título e Descrição da pergunta
                ft.Text(titulo_ind, size=18, weight="bold", color="onSurface", text_align=ft.TextAlign.CENTER),
                ft.Text(indicador.get("descricao", ""), size=14, color="onSurfaceVariant", text_align=ft.TextAlign.CENTER),
                
                ft.Divider(height=10, color="transparent"), # Espaçador invisível
                
                # Linha com o controle deslizante e os números 1 e 5 nas pontas
                ft.Row([
                    ft.Text("1", color="onSurfaceVariant", weight="bold"), 
                    slider_nota, 
                    ft.Text("5", color="onSurfaceVariant", weight="bold")
                ]),
                
                # Bloco de destaque que exibe a nota atual e o texto descritivo correspondente
                ft.Container(
                    bgcolor="surfaceVariant", # Tom levemente diferente do fundo principal para destacar
                    padding=15,
                    border_radius=8,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[lbl_nota_destaque, txt_criterio_dinamico]
                    )
                )
            ]
        )
    )