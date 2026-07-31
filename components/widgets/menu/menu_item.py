import flet as ft
from typing import Callable, Optional
from components.widgets.menu.menu_button_base import criar_botao_menu_base

def criar_item_menu(
    icone: str,
    texto: str,
    rota: str,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela: Optional[Callable[[str], None]],
) -> ft.Container:
    """Cria o botão de navegação tradicional: ícone à esquerda alinhado a um texto."""
    
    # Prepara o bloco visual: organiza ícone e texto lado a lado (Row)
    conteudo = ft.Row(
        spacing=12,
        controls=[
            ft.Icon(
                icone,
                size=20, # Sutilmente menor que a versão colapsada (24) para balancear o design com o texto)
                color=ft.Colors.GREY_700 if not dark_mode else ft.Colors.GREY_300, # Regra de design: O ícone recebe um tom levemente acinzentado (variando conforme o tema) para servir como apoio visual e não roubar o peso de leitura do texto principal
            ),
            ft.Text(texto, size=14, weight="w500", color=cor_texto), # O texto da rota com peso médio (w500) para facilitar a leitura.
        ], 
    )
    
    # Retorna o componente base injetando a linha (Row) recém-criada
    return criar_botao_menu_base(
        content=conteudo,
        rota=rota,
        dark_mode=dark_mode,
        mudar_tela=mudar_tela,
    )