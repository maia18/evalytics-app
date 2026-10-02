import flet as ft
from components.core.constants.constants import (
    COR_PRIMARIA,
    CARD_SECUNDARIO,
    TEXTO_PRINCIPAL,
)

def criar_abas(
    page: ft.Page,
    area_dinamica_indicadores: ft.Container,
    painel_seguranca: ft.Container,
    painel_banco: ft.Container,
    cores: dict[str, str],
) -> tuple[ft.Row, ft.Container]:
    """Cria a barra de navegação superior (tabs) e o container que exibirá os painéis correspondentes"""
    
    # Injeta a tela de indicadores como aba inicial ativa
    area_conteudo_aba = ft.Container(content=area_dinamica_indicadores, expand=True, padding=20)

    def mudar_aba(
        e: ft.ControlEvent,
        painel_selecionado: ft.Control,
        btn_indicadores: ft.TextButton,
        btn_seguranca: ft.TextButton,
        btn_banco: ft.TextButton,
    ) -> None:

        area_conteudo_aba.content = painel_selecionado

        botoes = {
            btn_indicadores: area_dinamica_indicadores,
            btn_seguranca: painel_seguranca,
            btn_banco: painel_banco,
        }

        for botao, painel in botoes.items():
            ativo = painel_selecionado == painel

            botao.style = ft.ButtonStyle(
                color=(
                    cores[COR_PRIMARIA]
                    if ativo
                    else cores[TEXTO_PRINCIPAL]
                ),
                bgcolor=(
                    cores[CARD_SECUNDARIO]
                    if ativo
                    else ft.Colors.TRANSPARENT
                ),
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=15,
            )

        page.update()

    estilo_btn_aba = ft.ButtonStyle(
        color=cores[TEXTO_PRINCIPAL],
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
    )
    
    # Monta os botões injetando os painéis respectivos em seus callbacks on_click
    btn_indicadores = ft.TextButton(
        "Indicadores", 
        icon=ft.Icons.RULE, 
        style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, area_dinamica_indicadores, btn_indicadores, btn_seguranca, btn_banco),
    )
    btn_seguranca = ft.TextButton(
        "Segurança", 
        icon=ft.Icons.SECURITY, 
        style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, painel_seguranca, btn_indicadores, btn_seguranca, btn_banco),
    )
    btn_banco = ft.TextButton(
        "Banco de Dados", 
        icon=ft.Icons.STORAGE, 
        style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, painel_banco, btn_indicadores, btn_seguranca, btn_banco),
    )

    menu_abas = ft.Row([btn_indicadores, btn_seguranca, btn_banco], spacing=10)
    return menu_abas, area_conteudo_aba