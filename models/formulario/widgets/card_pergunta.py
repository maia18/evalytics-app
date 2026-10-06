import flet as ft
from components.core.constants.constants import (
    COR_PRIMARIA,
    TEXTO_PRINCIPAL,
    BORDA,
    CARD,
)

def criar_card_pergunta(
    page: ft.Page,
    indicador: dict,
    estado: dict,
    rodape: ft.Container,
    cores: dict[str, str],
) -> ft.Container:
    """Constrói o cartão central com opções, rolagem e campo de justificativa."""

    # ==========================================================
    # DADOS DO INDICADOR
    # ==========================================================

    indicador_id = indicador.get("id")
    titulo_ind = indicador["titulo"]
    criterios = indicador.get("criterios", {})

    valor_inicial = str(
        estado["respostas"].get(
            indicador_id,
            ""
        )
    )

    # ==========================================================
    # RESPOSTA
    # ==========================================================

    def ao_mudar_opcao(e: ft.ControlEvent) -> None:
        if indicador_id:
            estado["respostas"][indicador_id] = int(
                e.control.value
            )

    # ==========================================================
    # OPÇÕES DE RESPOSTA
    # ==========================================================

    opcoes_radio = []

    for chave, texto_criterio in sorted(
        criterios.items(),
        key=lambda x: str(x[0]),
    ):
        linha_opcao = ft.Container(
            padding=ft.Padding.symmetric(vertical=4),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Radio(
                        value=str(chave),
                        active_color=cores[COR_PRIMARIA],
                    ),
                    ft.Container(
                        expand=True,
                        padding=ft.Padding.only(top=12),
                        content=ft.Text(
                            f"Nível {chave}: {texto_criterio}",
                            color=cores[TEXTO_PRINCIPAL],
                            size=14,
                        ),
                    ),
                ],
            ),
        )

        opcoes_radio.append(linha_opcao)

    grupo_radio = ft.RadioGroup(
        content=ft.Column(
            spacing=0,
            controls=opcoes_radio,
        ),
        value=valor_inicial,
        on_change=ao_mudar_opcao,
    )

    # ==========================================================
    # JUSTIFICATIVA
    # ==========================================================

    campo_justificativa = ft.TextField(
        label="Justificativa (Opcional)",
        multiline=True,
        min_lines=1,
        max_lines=3,
        border_color=cores[BORDA],
        text_size=14,
        content_padding=15,
    )

    # ==========================================================
    # DESCRIÇÃO
    # ==========================================================

    descricao_texto = indicador.get("descricao", "")

    # ==========================================================
    # CABEÇALHO FIXO
    # ==========================================================

    cabecalho_card = [
        ft.Text(
            titulo_ind,
            size=20,
            weight="bold",
            color=cores[TEXTO_PRINCIPAL],
        ),
    ]

    if descricao_texto:
        cabecalho_card.append(
            ft.Text(
                descricao_texto,
                size=14,
                color="onSurfaceVariant",
                italic=True,
            )
        )

    cabecalho_card.append(
        ft.Divider(
            height=1,
            color=cores[BORDA],
        )
    )

    # ==========================================================
    # ÁREA CENTRAL ROLÁVEL
    # ==========================================================

    area_rolavel = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        controls=[
            grupo_radio,
            ft.Container(height=10),
            campo_justificativa,
        ],
    )

    # ==========================================================
    # CARD
    # ==========================================================

    return ft.Container(
        bgcolor=cores[CARD],
        padding=30,
        border_radius=12,
        border=ft.Border.all(
            1,
            cores[BORDA],
        ),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 4),
        ),
        expand=True,
        content=ft.Column(
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                *cabecalho_card,
                area_rolavel,
                ft.Divider(
                    height=1,
                    color=cores[BORDA],
                ),
                rodape,
            ],
        ),
    )