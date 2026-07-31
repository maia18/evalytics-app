import flet as ft
from typing import Callable, Iterable

'''
Define um formato padrão esperado para os itens (Ícone, Texto, Rota)[cite: 18].
    Ex: (ft.Icons.HOME, "Início", "/inicio").
'''
MenuItem = tuple[str, str, str]

MenuItemBuilder = Callable[[str, str, str, bool, str, Callable[[str], None]], ft.Control] # Type Alias definindo exatamente quais argumentos a função que constrói o botão precisa receber

def montar_botoes_menu(
    items: Iterable[MenuItem],
    builder: MenuItemBuilder,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela: Callable[[str], None],
) -> list[ft.Control]:
    """Constrói a lista de controles de menu aplicando `builder` a cada item.

    Compartilhado entre a sidebar completa e a sidebar colapsada, que diferem
    apenas na função construtora (`criar_item_menu` vs `criar_botao_icon`) e
    na lista de itens percorrida.
    """
    
    # Utiliza List Comprehension nativa do Python para gerar a lista de botões finais de forma otimizada
    return [
        builder(icone, texto, rota, dark_mode, cor_texto, mudar_tela)
        for icone, texto, rota in items
    ]