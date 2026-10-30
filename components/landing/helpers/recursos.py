import flet as ft
from components.landing.palette import TEXTO, TEXTO_SECUNDARIO, ROXO, CARD, CARD_HOVER, BORDA

def criar_card_recurso(icone, titulo: str, descricao: str, cor_acento: str = ROXO) -> ft.Container:
    """Cria um card horizontal com ícone à esquerda e texto à direita."""

    card = ft.Container(
        padding=20,
        bgcolor=CARD,
        border_radius=16,
        border=ft.Border.all(1, BORDA),
        offset=ft.Offset(0, 0),
        animate_offset=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
        animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
        content=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[

                # =================================================
                # ÍCONE
                # =================================================

                ft.Container(
                    width=44,
                    height=44,
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(
                        0.12,
                        cor_acento,
                    ),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        icone,
                        size=22,
                        color=cor_acento,
                    ),
                ),

                # =================================================
                # TEXTO
                # =================================================

                ft.Column(
                    spacing=4,
                    expand=True,
                    controls=[
                        ft.Text(
                            titulo,
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=TEXTO,
                        ),
                        ft.Text(
                            descricao,
                            size=13,
                            color=TEXTO_SECUNDARIO,
                        ),
                    ],
                ),
            ],
        ),
    )

    def animar_hover(e):
        if e.data == "true":
            card.offset = ft.Offset(0, -0.025)
            card.bgcolor = CARD_HOVER
            card.border = ft.Border.all(1, cor_acento)
        else:
            card.offset = ft.Offset(0, 0)
            card.bgcolor = CARD
            card.border = ft.Border.all(1, BORDA)
        card.update()

    card.on_hover = animar_hover
    return card
