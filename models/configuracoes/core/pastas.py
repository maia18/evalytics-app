import flet as ft
from database.indicadores import INDICADORES
from models.configuracoes.core.indicadores_ui import criar_linha_indicador, criar_pasta_indicador

def abrir_pasta(page, titulo_pasta, pasta_aberta_atualmente, area_conteudo_aba, abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao):
    mapa_eixos = {
        "Organização Didático-Pedagógica": 1,
        "Corpo Docente e Tutorial": 2,
        "Infraestrutura": 3
    }
    eixo_id = mapa_eixos.get(titulo_pasta)
    pasta_aberta_atualmente["titulo"] = titulo_pasta
    pasta_aberta_atualmente["eixo"] = eixo_id

    lista_da_pasta = [item for item in INDICADORES if item.get("eixo") == eixo_id]

    controles_lista = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas(page, area_conteudo_aba)),
                    ft.Text(titulo_pasta, size=22, weight="bold", color="black87")
                ]),
                ft.ElevatedButton("Novo Indicador", icon=ft.Icons.ADD, bgcolor="blue700", color="white", on_click=lambda e: abrir_modal_novo())
            ]
        ),
        ft.Divider(height=20, color="transparent")
    ]

    for item in lista_da_pasta:
        controles_lista.append(
            criar_linha_indicador(
                item,
                lambda e, i=item: abrir_modal_criterios(e, i),
                lambda e, i=item: abrir_modal_edicao(e, i),
                lambda i=item: preparar_exclusao(i)
            )
        )

    area_conteudo_aba.content = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15, controls=controles_lista)
    page.update()


def voltar_para_pastas(page, area_conteudo_aba):
    qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
    qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
    qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)

    layout_pastas = ft.Column(
        expand=True,
        spacing=25,
        controls=[
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color="black87"),
            ft.Column(
                spacing=15,
                controls=[
                    criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1, lambda t: abrir_pasta(page, t, {"titulo": "", "eixo": 0}, area_conteudo_aba, None, None, None, None)),
                    criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2, lambda t: abrir_pasta(page, t, {"titulo": "", "eixo": 0}, area_conteudo_aba, None, None, None, None)),
                    criar_pasta_indicador("Infraestrutura", qtd_eixo_3, lambda t: abrir_pasta(page, t, {"titulo": "", "eixo": 0}, area_conteudo_aba, None, None, None, None)),
                ]
            )
        ]
    )

    area_conteudo_aba.content = layout_pastas
    page.update()
