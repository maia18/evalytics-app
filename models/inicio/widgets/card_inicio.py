import flet as ft
from components.core.constants.constants import *

def criar_card(layout, titulo, descricao, icone, rota, mudar_tela):
    """
    Gera um cartão interativo (Card) padronizado para ser usado como atalho de navegação.
    
    Args:
        layout: A instância do layout atual (usada para extrair as cores ativas do tema).
        titulo (str): O nome em destaque do atalho (ex: "Dashboard").
        descricao (str): Um texto explicativo menor logo abaixo do título.
        icone (str): A constante do ícone representativo (do Flet/Material Design).
        rota (str): O caminho interno para onde o clique deve levar (ex: "/dashboard").
        mudar_tela (callable): Função callback responsável por executar a troca de rota.
    """
    return ft.Container(
        width=300, # Largura fixa para manter todos os cartões padronizados e alinhados na grade (Row)
        bgcolor=layout.cores[CARD], # Cor de fundo que se adapta ao modo Claro/Escuro automaticamente
        padding=20, # Espaçamento interno para que o conteúdo não fique "grudado" nas bordas
        border_radius=12, # Cantos arredondados suaves para um visual mais moderno
        # Aplica uma borda fina (1px) em todas as direções do container usando as cores dinâmicas
        border=ft.Border(
            left=ft.BorderSide(width=1, color=layout.cores[BORDA]),
            top=ft.BorderSide(width=1, color=layout.cores[BORDA]),
            right=ft.BorderSide(width=1, color=layout.cores[BORDA]),
            bottom=ft.BorderSide(width=1, color=layout.cores[BORDA]),
        ),
        ink=True, # Habilita o efeito visual de onda ('ripple effect') do Material Design ao clicar
        # Função lambda (anônima) para ignorar o parâmetro nativo de evento 'e' e apenas disparar a mudança de rota
        on_click=lambda e: mudar_tela(rota),
        # O conteúdo interno do cartão é empilhado verticalmente
        content=ft.Column([
            ft.Icon(icone, color=COR_PRIMARIA, size=30), # Ícone em destaque usando a cor de marca do sistema
            ft.Text(titulo, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]), # Título com destaque (negrito)
            ft.Text(descricao, size=12, color="grey") # Texto de apoio menor e em tom neutro
        ])
    )
