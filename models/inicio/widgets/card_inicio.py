import flet as ft
from components.core.constants.constants import *

def criar_card(layout, titulo, descricao, icone, rota, mudar_tela):
    """
    Gera um cartão interativo (Card) padronizado para ser usado como atalho de navegação.

    Aprimoramentos em relação à versão anterior:
        - Ícone dentro de um badge circular com fundo translúcido (mais destaque visual).
        - Seta indicativa que aparece suavemente ao passar o mouse (affordance de clique).
        - Sombra e borda que reagem ao hover, dando sensação de profundidade/elevação.
        - Transições animadas em vez de troca abrupta de estilo.

    Args:
        layout: A instância do layout atual (usada para extrair as cores ativas do tema).
        titulo (str): O nome em destaque do atalho (ex: "Dashboard").
        descricao (str): Um texto explicativo menor logo abaixo do título.
        icone (str): A constante do ícone representativo (do Flet/Material Design).
        rota (str): O caminho interno para onde o clique deve levar (ex: "/dashboard").
        mudar_tela (callable): Função callback responsável por executar a troca de rota.
    """

    # Ícone de seta que fica invisível por padrão e some/aparece no hover,
    # reforçando visualmente que o cartão é clicável.
    seta_indicadora = ft.Icon(
        ft.Icons.ARROW_FORWARD_ROUNDED,
        color=ft.Colors.TRANSPARENT,
        size=18,
        animate_opacity=200,
    )

    # Badge circular que envolve o ícone principal do card, com fundo translúcido
    # na cor primária -- dá mais destaque do que um ícone "solto".
    badge_icone = ft.Container(
        width=44,
        height=44,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.12, COR_PRIMARIA),
        alignment=ft.alignment.Alignment.CENTER,
        content=ft.Icon(icone, color=COR_PRIMARIA, size=22),
    )

    card = ft.Container(
        width=300,  # Largura fixa para manter todos os cartões padronizados e alinhados na grade (Row)
        bgcolor=layout.cores[CARD],  # Cor de fundo que se adapta ao modo Claro/Escuro automaticamente
        padding=20,  # Espaçamento interno para que o conteúdo não fique "grudado" nas bordas
        border_radius=14,  # Cantos levemente mais arredondados para um visual mais moderno
        # Borda fina em todas as direções, usando a cor dinâmica do tema (estado padrão/sem hover)
        border=ft.Border(
            left=ft.BorderSide(width=1, color=layout.cores[BORDA]),
            top=ft.BorderSide(width=1, color=layout.cores[BORDA]),
            right=ft.BorderSide(width=1, color=layout.cores[BORDA]),
            bottom=ft.BorderSide(width=1, color=layout.cores[BORDA]),
        ),
        # Sombra sutil, que se intensifica no hover para dar sensação de "elevação" do card
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=0,
            color=ft.Colors.with_opacity(0.18, COR_PRIMARIA),
            offset=ft.Offset(0, 6),
        ),
        # Transição suave para border, shadow e bgcolor quando o estado do hover muda
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        ink=True,  # Mantém o efeito de onda ('ripple effect') do Material Design ao clicar
        on_click=lambda e: mudar_tela(rota),
        content=ft.Column(
            spacing=12,
            controls=[
                # Cabeçalho do card: badge do ícone à esquerda, seta indicadora à direita
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[badge_icone, seta_indicadora],
                ),
                ft.Text(titulo, weight="bold", size=16, color=layout.cores[TEXTO_PRINCIPAL]),
                ft.Text(descricao, size=12, color=COR_TEXTO_SECUNDARIO),
            ],
        ),
    )

    def ao_passar_mouse(e):
        """Aplica (ou remove) o estado visual de destaque quando o mouse entra/sai do card."""
        em_hover = e.data == "true"

        cor_borda = COR_PRIMARIA if em_hover else layout.cores[BORDA]
        card.border = ft.Border(
            left=ft.BorderSide(width=1, color=cor_borda),
            top=ft.BorderSide(width=1, color=cor_borda),
            right=ft.BorderSide(width=1, color=cor_borda),
            bottom=ft.BorderSide(width=1, color=cor_borda),
        )
        card.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=18 if em_hover else 0,
            color=ft.Colors.with_opacity(0.18, COR_PRIMARIA),
            offset=ft.Offset(0, 6),
        )
        seta_indicadora.color = COR_PRIMARIA if em_hover else ft.Colors.TRANSPARENT

        card.update()

    card.on_hover = ao_passar_mouse

    return card