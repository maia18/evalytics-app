import flet as ft
from components.core.constants.constants import *

def criar_kpi_card(layout, titulo, valor, icone, cor_icone):
    """
    Constrói um cartão de indicador chave de desempenho (KPI) contendo um título, valor em destaque e um ícone representativo.
    """
    
    # Configuração do contorno delimitador usando cores dinâmicas do tema 
    borda_card = ft.Border(
        top=ft.BorderSide(1, layout.cores[BORDA]),
        bottom=ft.BorderSide(1, layout.cores[BORDA]),
        left=ft.BorderSide(1, layout.cores[BORDA]),
        right=ft.BorderSide(1, layout.cores[BORDA])
    ) 
    
    return ft.Container(
        width=240, # Trava a largura para os cartões ficarem uniformes
        bgcolor=layout.cores[CARD], # Fundo reativo a dark/light mode
        padding=20,
        border_radius=8,
        border=borda_card,
        content=ft.Column(
            spacing=15,
            controls=[
                # Linha superior contendo o Título e o Ícone
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Joga o texto para a esquerda e o ícone para a direita
                    controls=[
                        ft.Text(titulo, size=14, color="grey600", weight="w500"),
                        ft.Icon(icone, color=cor_icone, size=18)
                    ]
                ),
                # Linha inferior contendo o grande número em destaque
                ft.Text(valor, size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ]
        )
    )
