import flet as ft

def criar_card_pergunta(page: ft.Page, indicador: dict, estado: dict) -> ft.Container:
    """Constrói o cartão central de uma pergunta da avaliação, com título, descrição e slider interativo.

    NOTA ARQUITETURAL: este módulo usa os tokens semânticos nativos do Material 3 do Flutter 
    (ex.: "primary", "onSurface", "surface") em vez do seu dicionário `layout.cores` padrão. 
    Isso mostra as duas abordagens funcionais, onde os tokens semânticos já se resolvem no modo claro/escuro de forma automática.
    """
    titulo_ind = indicador["titulo"]
    criterios = indicador.get("criterios", {})

    # Resgata a resposta anterior do usuário ou usa 3 como nota inicial padrão
    valor_inicial = estado["respostas"].get(titulo_ind, 3)
    
    # Previne quebra de leitura caso a chave dos critérios esteja salva como int ou str no banco
    texto_inicial = criterios.get(str(valor_inicial), criterios.get(valor_inicial, "Critério não definido."))

    lbl_nota_destaque = ft.Text(str(valor_inicial), size=28, weight="bold", color="primary")
    txt_criterio_dinamico = ft.Text(texto_inicial, size=14, color="onSurfaceVariant", italic=True, text_align=ft.TextAlign.CENTER)

    def ao_deslizar(e: ft.ControlEvent) -> None:
        """Atualiza a nota no dicionário do estado e altera os textos explicativos em tempo real ao mexer na barra."""
        nota_atual = int(e.control.value)
        estado["respostas"][titulo_ind] = nota_atual

        lbl_nota_destaque.value = str(nota_atual)
        txt_criterio_dinamico.value = criterios.get(str(nota_atual), criterios.get(nota_atual, "Sem descrição."))

        page.update()

    # Slider que trava os valores nas divisões corretas (1 a 5)
    slider_nota = ft.Slider(
        min=1, max=5, divisions=4,  # Força valores estritamente inteiros (escala Likert de 1 a 5)
        value=valor_inicial, active_color="primary", inactive_color="outlineVariant",
        on_change=ao_deslizar, expand=True,
    )

    return ft.Container(
        bgcolor="surface", padding=30, border_radius=12, shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="shadow"),
        content=ft.Column(
            spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(titulo_ind, size=18, weight="bold", color="onSurface", text_align=ft.TextAlign.CENTER),
                ft.Text(indicador.get("descricao", ""), size=14, color="onSurfaceVariant", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=10, color="transparent"),
                ft.Row([ft.Text("1", color="onSurfaceVariant", weight="bold"), slider_nota, ft.Text("5", color="onSurfaceVariant", weight="bold")]),
                ft.Container(
                    bgcolor="surfaceVariant", padding=15, border_radius=8,
                    content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5, controls=[lbl_nota_destaque, txt_criterio_dinamico])
                ),
            ],
        ),
    )