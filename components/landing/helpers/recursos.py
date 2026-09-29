import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_FUNDO,
)

def criar_card_recurso(icone, titulo: str, descricao: str) -> ft.Container:
    """Cria e retorna um componente visual (Card) para exibir um recurso ou funcionalidade."""
    
    # O Container principal atua como o "fundo" do card.
    return ft.Container(
        width=235,                  # Largura fixa do card para manter o padrão na grade
        height=190,                 # Altura fixa do card
        padding=24,                 # Espaçamento interno (respiro) entre a borda e o conteúdo
        bgcolor=COR_FUNDO,          # Cor de fundo padrão puxada das constantes
        border_radius=14,           # Arredondamento dos cantos do card
        border=ft.Border.all(
            1,                      # Espessura da borda
            ft.Colors.BLACK12,      # Cor da borda (preto com 12% de opacidade)
        ),
        
        # O conteúdo do card é organizado verticalmente usando uma Coluna
        content=ft.Column(
            spacing=14,             # Espaço vertical de 14px entre o ícone, título e descrição
            controls=[
                
                # 1. Bloco do Ícone: Envolvido em um Container menor para dar o efeito de "caixa" colorida
                ft.Container(
                    width=42,
                    height=42,
                    border_radius=9,
                    # Aplica a cor primária com 10% de opacidade para criar um fundo suave atrás do ícone
                    bgcolor=ft.Colors.with_opacity(
                        0.10,
                        COR_PRIMARIA,
                    ),
                    alignment=ft.Alignment.CENTER,  # Centraliza o ícone perfeitamente dentro do quadrado
                    content=ft.Icon(
                        icone,
                        size=21,                    # Tamanho proporcional ao container de 42px
                        color=COR_PRIMARIA,         # Ícone sólido usando a cor primária da marca
                    ),
                ),

                # 2. Bloco do Título
                ft.Text(
                    titulo,
                    size=16,                        # Fonte ligeiramente maior para hierarquia visual
                    weight=ft.FontWeight.BOLD,      # Negrito para dar destaque
                    color=COR_TEXTO_TITULO,
                ),

                # 3. Bloco da Descrição
                ft.Text(
                    descricao,
                    size=13,                        # Fonte menor para leitura secundária
                    color=COR_TEXTO_SECUNDARIO,
                ),
            ],
        ),
    )