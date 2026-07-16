import flet as ft

def criar_card_pergunta(page, indicador, estado):
    titulo_ind = indicador["titulo"]
    criterios = indicador.get("criterios", {})

    valor_inicial = estado["respostas"].get(titulo_ind, 3)
    texto_inicial = criterios.get(str(valor_inicial), criterios.get(valor_inicial, "Critério não definido."))

    lbl_nota_destaque = ft.Text(str(valor_inicial), size=28, weight="bold", color="blue700")
    txt_criterio_dinamico = ft.Text(texto_inicial, size=14, color="grey700", italic=True, text_align=ft.TextAlign.CENTER)

    def ao_deslizar(e):
        nota_atual = int(e.control.value)
        estado["respostas"][titulo_ind] = nota_atual
        lbl_nota_destaque.value = str(nota_atual)
        txt_criterio_dinamico.value = criterios.get(str(nota_atual), criterios.get(nota_atual, "Sem descrição."))
        page.update()

    slider_nota = ft.Slider(
        min=1, max=5, divisions=4,
        value=valor_inicial,
        label="Nota {value}",
        active_color="blue700",
        inactive_color="blue100",
        on_change=ao_deslizar,
        expand=True
    )

    return ft.Container(
        bgcolor="white",
        padding=30,
        border_radius=12,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12"),
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text(titulo_ind, size=18, weight="bold", color="black87"),
                ft.Text(indicador.get("descricao", ""), size=14, color="grey500"),
                ft.Divider(height=10, color="transparent"),
                ft.Row([ft.Text("1", color="grey400", weight="bold"), slider_nota, ft.Text("5", color="grey400", weight="bold")]),
                ft.Container(
                    bgcolor="#F8F9FA",
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
