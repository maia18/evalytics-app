import flet as ft

from components.landing.palette import (
    BORDA,
    CARD,
    FUNDO,
    ROXO,
    ROSA,
    VERDE,
    TEXTO,
    TEXTO_SECUNDARIO,
)


def criar_painel_hero() -> ft.Container:
    """Demonstração interativa de uma avaliação e de seus resultados."""
    nota_selecionada = 4
    opcoes_nota: list[ft.Container] = []
    texto_retorno = ft.Text(
        "Boa! Sua resposta ajuda a enxergar o que funciona.",
        size=11,
        color=ROXO,
        weight=ft.FontWeight.BOLD,
    )

    def selecionar_nota(nota: int):
        nonlocal nota_selecionada
        nota_selecionada = nota
        for valor, opcao in enumerate(opcoes_nota, start=1):
            selecionada = valor == nota
            opcao.bgcolor = ROXO if selecionada else "#F3F0F8"
            opcao.content.color = ft.Colors.WHITE if selecionada else TEXTO
            opcao.scale = 1.06 if selecionada else 1.0
            opcao.update()
        texto_retorno.value = {
            1: "Obrigado por responder. Vamos melhorar juntos.",
            2: "Sua opinião é importante para a instituição.",
            3: "Resposta registrada na prévia interativa.",
            4: "Boa! Sua resposta ajuda a enxergar o que funciona.",
            5: "Que ótimo! Sua percepção também gera melhorias.",
        }[nota]
        texto_retorno.update()

    for nota in range(1, 6):
        selecionada = nota == nota_selecionada
        opcao = ft.Container(
            width=42,
            height=42,
            border_radius=14,
            alignment=ft.Alignment.CENTER,
            bgcolor=ROXO if selecionada else "#F3F0F8",
            scale=1.06 if selecionada else 1.0,
            animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
            ink=True,
            on_click=lambda _, valor=nota: selecionar_nota(valor),
            content=ft.Text(
                str(nota),
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE if selecionada else TEXTO,
            ),
        )
        opcoes_nota.append(opcao)

    question_card = ft.Container(
        padding=22,
        border_radius=22,
        bgcolor=CARD,
        border=ft.Border.all(1, BORDA),
        shadow=ft.BoxShadow(
            blur_radius=22,
            color="#160E2830",
            offset=ft.Offset(0, 9),
        ),
        offset=ft.Offset(0, 0),
        animate_offset=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Container(
                                    width=28,
                                    height=28,
                                    border_radius=9,
                                    bgcolor="#EEE8FF",
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(ft.Icons.SCHOOL_OUTLINED, size=16, color=ROXO),
                                ),
                                ft.Text("Avaliação semestral", size=11, weight=ft.FontWeight.BOLD, color=TEXTO),
                            ],
                        ),
                        ft.Text("1 de 8", size=10, color=TEXTO_SECUNDARIO),
                    ],
                ),
                ft.Text(
                    "Como você avalia a experiência no seu curso?",
                    size=19,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO,
                ),
                ft.Text(
                    "Escolha uma nota para ver a interação.",
                    size=11,
                    color=TEXTO_SECUNDARIO,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=opcoes_nota,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Precisa melhorar", size=9, color=TEXTO_SECUNDARIO),
                        ft.Text("Excelente", size=9, color=TEXTO_SECUNDARIO),
                    ],
                ),
                ft.Container(
                    padding=ft.Padding.only(top=7),
                    border=ft.Border(top=ft.BorderSide(1, BORDA)),
                    content=texto_retorno,
                ),
            ],
        ),
    )

    def animar_hover(e):
        question_card.offset = ft.Offset(0, -0.018) if e.data == "true" else ft.Offset(0, 0)
        question_card.update()

    question_card.on_hover = animar_hover

    return ft.Container(
        padding=20,
        border_radius=30,
        bgcolor="#F0E9FF",
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=7,
                            controls=[
                                ft.Container(width=8, height=8, border_radius=8, bgcolor=VERDE),
                                ft.Text("PRÉVIA · DADOS DE EXEMPLO", size=10, weight=ft.FontWeight.BOLD, color=TEXTO),
                            ],
                        ),
                        ft.Icon(ft.Icons.AUTO_AWESOME, color=ROXO, size=18),
                    ],
                ),
                question_card,
                ft.Row(
                    spacing=10,
                    controls=[
                        _mini_indicador("82", "respostas", ROXO),
                        _mini_indicador("3,8 / 5", "média do eixo", ROSA),
                    ],
                ),
                ft.Row(
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.LOCK_OUTLINE, size=12, color=TEXTO_SECUNDARIO),
                        ft.Text("Respostas protegidas e apresentadas de forma consolidada", size=9, color=TEXTO_SECUNDARIO),
                    ],
                ),
            ],
        ),
    )


def _mini_indicador(valor: str, legenda: str, cor: str) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=12,
        border_radius=15,
        bgcolor=CARD,
        border=ft.Border.all(1, BORDA),
        animate=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Container(width=5, height=31, border_radius=5, bgcolor=cor),
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text(valor, size=15, weight=ft.FontWeight.BOLD, color=TEXTO),
                        ft.Text(legenda, size=9, color=TEXTO_SECUNDARIO),
                    ],
                ),
            ],
        ),
    )
