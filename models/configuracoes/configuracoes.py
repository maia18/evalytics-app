import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from database.indicadores import INDICADORES

# Importa modais e painéis
from models.configuracoes.modals.modal_edicao import criar_modal_edicao
from models.configuracoes.modals.modal_criterios import criar_modal_criterios
from models.configuracoes.modals.modal_exclusao import criar_modal_exclusao
from models.configuracoes.modals.modal_novo import criar_modal_novo
from models.configuracoes.core.indicadores_ui import criar_linha_indicador, criar_pasta_indicador
from models.configuracoes.core.painel_seguranca import criar_painel_seguranca
from models.configuracoes.core.painel_banco import criar_painel_banco

def ViewConfiguracoes(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Configurações",
        subtitulo="Gerencie indicadores e critérios de avaliação.",
        mudar_tela=mudar_tela
    )

    pasta_aberta_atualmente = {"titulo": "", "eixo": 0}
    item_alvo_acao = {}

    # === Modais com funções de abertura ===
    modal_edicao, campo_titulo, campo_descricao, abrir_modal_edicao = criar_modal_edicao(page, item_alvo_acao, lambda t: abrir_pasta(t), pasta_aberta_atualmente)
    modal_criterios, _, abrir_modal_criterios = criar_modal_criterios(page, item_alvo_acao)
    modal_exclusao, preparar_exclusao = criar_modal_exclusao(page, item_alvo_acao, lambda t: abrir_pasta(t), pasta_aberta_atualmente)
    modal_novo, campo_titulo_novo, campo_desc_novo, abrir_modal_novo = criar_modal_novo(page, pasta_aberta_atualmente, lambda t: abrir_pasta(t))

    # Área dinâmica
    area_dinamica_indicadores = ft.Container(expand=True)

    def abrir_pasta(titulo_pasta):
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
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas()),
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

    def voltar_para_pastas():
        qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
        qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
        qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)

        layout_pastas.controls[1].controls[0] = criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1, abrir_pasta)
        layout_pastas.controls[1].controls[1] = criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2, abrir_pasta)
        layout_pastas.controls[1].controls[2] = criar_pasta_indicador("Infraestrutura", qtd_eixo_3, abrir_pasta)

        area_conteudo_aba.content = layout_pastas
        page.update()

    # Layout inicial
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
                    criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1, abrir_pasta),
                    criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2, abrir_pasta),
                    criar_pasta_indicador("Infraestrutura", qtd_eixo_3, abrir_pasta),
                ]
            )
        ]
    )

    area_dinamica_indicadores.content = layout_pastas

    # Abas
    painel_seguranca = criar_painel_seguranca()
    painel_banco = criar_painel_banco()
    area_conteudo_aba = ft.Container(content=area_dinamica_indicadores, expand=True, padding=20)

    def mudar_aba(e, painel_selecionado):
        area_conteudo_aba.content = painel_selecionado
        btn_indicadores.bgcolor = "blue50" if painel_selecionado == area_dinamica_indicadores else "transparent"
        btn_seguranca.bgcolor = "blue50" if painel_selecionado == painel_seguranca else "transparent"
        btn_banco.bgcolor = "blue50" if painel_selecionado == painel_banco else "transparent"
        page.update()

    estilo_btn_aba = ft.ButtonStyle(color={"":"blue900"}, shape=ft.RoundedRectangleBorder(radius=8), padding=15)
    btn_indicadores = ft.TextButton("Indicadores", icon=ft.Icons.RULE, style=estilo_btn_aba, on_click=lambda e: mudar_aba(e, area_dinamica_indicadores))
    btn_seguranca = ft.TextButton("Segurança", icon=ft.Icons.SECURITY, style=estilo_btn_aba, on_click=lambda e: mudar_aba(e, painel_seguranca))
    btn_banco = ft.TextButton("Banco de Dados", icon=ft.Icons.STORAGE, style=estilo_btn_aba, on_click=lambda e: mudar_aba(e, painel_banco))

    menu_abas = ft.Row([btn_indicadores, btn_seguranca, btn_banco], spacing=10)

    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Text("Configurações do Sistema", size=28, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
            ft.Text("Gerencie indicadores, acessos e manutenção de dados.", size=16, color="grey"),
            ft.Divider(height=20, color="transparent"),
            ft.Container(
                expand=True,
                bgcolor=layout.cores["CARD"],
                border_radius=10,
                padding=20,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
                content=ft.Column(
                    expand=True,
                    controls=[
                        menu_abas,
                        ft.Divider(height=20, color="grey200"),
                        ft.Container(expand=True, padding=10, content=area_conteudo_aba)
                    ]
                )
            )
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/configuracoes")
