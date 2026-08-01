from typing import Callable

import flet as ft


def criar_abas(
    page: ft.Page,
    area_dinamica_indicadores: ft.Container,
    painel_seguranca: ft.Container,
    painel_banco: ft.Container,
) -> tuple[ft.Row, ft.Container]:
    """Cria a barra de navegação superior (tabs) e o container que exibirá os painéis correspondentes."""
    area_conteudo_aba = ft.Container(content=area_dinamica_indicadores, expand=True, padding=20)

    def mudar_aba(
        e: ft.ControlEvent,
        painel_selecionado: ft.Control,
        btn_indicadores: ft.TextButton,
        btn_seguranca: ft.TextButton,
        btn_banco: ft.TextButton,
    ) -> None:
        """Injeta o novo painel no container e atualiza a cor dos botões para indicar a aba ativa."""
        area_conteudo_aba.content = painel_selecionado

        btn_indicadores.bgcolor = ft.Colors.BLUE_50 if painel_selecionado == area_dinamica_indicadores else ft.Colors.TRANSPARENT
        btn_seguranca.bgcolor = ft.Colors.BLUE_50 if painel_selecionado == painel_seguranca else ft.Colors.TRANSPARENT
        btn_banco.bgcolor = ft.Colors.BLUE_50 if painel_selecionado == painel_banco else ft.Colors.TRANSPARENT
        page.update()

    estilo_btn_aba = ft.ButtonStyle(
        color={"": ft.Colors.BLUE_900},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
    )

    btn_indicadores = ft.TextButton(
        "Indicadores", icon=ft.Icons.RULE, style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, area_dinamica_indicadores, btn_indicadores, btn_seguranca, btn_banco),
    )
    btn_seguranca = ft.TextButton(
        "Segurança", icon=ft.Icons.SECURITY, style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, painel_seguranca, btn_indicadores, btn_seguranca, btn_banco),
    )
    btn_banco = ft.TextButton(
        "Banco de Dados", icon=ft.Icons.STORAGE, style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, painel_banco, btn_indicadores, btn_seguranca, btn_banco),
    )

    menu_abas = ft.Row([btn_indicadores, btn_seguranca, btn_banco], spacing=10)

    return menu_abas, area_conteudo_aba