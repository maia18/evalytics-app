import flet as ft
from components.core.constants.constants import (
    CARD_SECUNDARIO,
    BORDA,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_painel_banco(
    cores: dict[str, str],
) -> ft.Container:
    """
    Constrói o painel de gerenciamento e manutenção dos dados.
        O painel utiliza o sistema centralizado de cores do Evalytics, mantendo compatibilidade com os temas claro e escuro.
    """

    return ft.Container(
        padding=20,
        content=ft.Column(
            spacing=20,
            controls=[
                # =========================================================
                # Cabeçalho
                # =========================================================
                ft.Text(
                    "Gerenciamento de Dados",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=cores[TEXTO_PRINCIPAL],
                ),

                ft.Divider(
                    color=cores[BORDA],
                ),

                ft.Text(
                    "Ferramentas para manutenção periódica do sistema.",
                    size=14,
                    color=cores[TEXTO_SECUNDARIO],
                ),

                # =========================================================
                # Ações de manutenção
                # =========================================================
                ft.Row(
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    controls=[
                        ft.ElevatedButton(
                            "Backup Completo",
                            icon=ft.Icons.DOWNLOAD,
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                        ),

                        ft.ElevatedButton(
                            "Otimizar Índices",
                            icon=ft.Icons.SPEED,
                            bgcolor=cores[COR_PRIMARIA],
                            color=ft.Colors.WHITE,
                        ),
                    ],
                ),

                # =========================================================
                # Zona de risco
                # =========================================================
                ft.Text(
                    "Zona de Risco",
                    size=16,
                    color=ft.Colors.RED_700,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(
                    padding=15,
                    bgcolor=cores[CARD_SECUNDARIO],
                    border=ft.Border(
                        top=ft.BorderSide(1, cores[BORDA]),
                        bottom=ft.BorderSide(1, cores[BORDA]),
                        left=ft.BorderSide(1, cores[BORDA]),
                        right=ft.BorderSide(1, cores[BORDA]),
                    ),
                    border_radius=8,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        wrap=True,
                        spacing=15,
                        run_spacing=10,
                        controls=[
                            ft.Text(
                                "Excluir avaliações com mais de 5 anos.",
                                color=cores[TEXTO_PRINCIPAL],
                            ),
                            ft.ElevatedButton(
                                "Limpar Dados Antigos",
                                icon=ft.Icons.DELETE_FOREVER,
                                bgcolor=ft.Colors.RED_700,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )