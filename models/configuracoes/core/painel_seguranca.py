import flet as ft

from components.core.constants.constants import (
    CARD,
    BORDA,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)


def criar_painel_seguranca(
    cores: dict[str, str],
) -> ft.Container:
    """
    Constrói o painel de políticas de segurança do sistema.

    O painel utiliza o sistema centralizado de cores do Evalytics
    para permanecer compatível com os temas claro e escuro.
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
                    "Políticas de Segurança",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=cores[TEXTO_PRINCIPAL],
                ),

                ft.Divider(
                    color=cores[BORDA],
                ),

                ft.Text(
                    "Configure políticas de segurança e controle de acesso "
                    "do sistema.",
                    size=14,
                    color=cores[TEXTO_SECUNDARIO],
                ),

                # =========================================================
                # Políticas de segurança
                # =========================================================
                ft.Switch(
                    label="Exigir autenticação em duas etapas (2FA)",
                    value=True,
                    active_color=cores[COR_PRIMARIA],
                    label_text_style=ft.TextStyle(
                        color=cores[TEXTO_PRINCIPAL],
                    ),
                ),

                ft.Switch(
                    label="Bloquear acesso após 5 tentativas falhas",
                    value=True,
                    active_color=cores[COR_PRIMARIA],
                    label_text_style=ft.TextStyle(
                        color=cores[TEXTO_PRINCIPAL],
                    ),
                ),

                ft.Switch(
                    label="Registrar logs de auditoria",
                    value=True,
                    active_color=cores[COR_PRIMARIA],
                    label_text_style=ft.TextStyle(
                        color=cores[TEXTO_PRINCIPAL],
                    ),
                ),

                ft.Divider(
                    color=cores[BORDA],
                ),

                # =========================================================
                # Exportação
                # =========================================================
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Exportar Relatório de Acessos",
                            icon=ft.Icons.SECURITY_UPDATE_WARNING,
                            color=ft.Colors.WHITE,
                            bgcolor=cores[COR_PRIMARIA],
                        ),
                    ],
                ),
            ],
        ),
    )