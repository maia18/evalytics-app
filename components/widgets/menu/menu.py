import flet as ft
from typing import Final

'''
Define formalmente a assinatura de um item de menu para o tipo (Type Hinting).      
    Formato de cada item de menu: (ícone, texto exibido, rota de navegação)
'''
MenuItem = tuple[str, str, str]

# =======================================================
# ITENS DO MENU EXPANDIDO (TEXTO + ÍCONE DE CONTORNO)
# =======================================================

'''
    A tipagem "Final" avisa outros desenvolvedores (e o linter) de que esta lista atua como uma constante e não deve ser mutada.
'''
MENU_ITEMS: Final[list[MenuItem]] = [
    (ft.Icons.HOME, "Início", "/inicio"),
    (ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/formulario"),
    
    # Repare no sufixo "_OUTLINED" - Ícones mais finos e elegantes combinam bem quando há texto acompanhando.
    (ft.Icons.GRID_VIEW_OUTLINED, "Dashboard", "/dashboard"),
    (ft.Icons.MENU_BOOK_OUTLINED, "Cursos", "/cursos"),
    (ft.Icons.PIE_CHART_OUTLINE, "Relatórios", "/relatorios"),
    (ft.Icons.SETTINGS_OUTLINED, "Configurações", "/configuracoes"),
]

# =======================================================
# ITENS DO MENU COLAPSADO (SÓ ÍCONE SÓLIDO)
# =======================================================

'''
Itens do menu colapsado (versão compacta).
    Alguns ícones diferem propositalmente dos da lista acima (ex: variantes mais "sólidas"), pois ajudam na leitura rápida quando o menu está encolhido.
'''
MENU_ITEMS_COLLAPSED: Final[list[MenuItem]] = [
    (ft.Icons.HOME, "Início", "/inicio"),
    (ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/formulario"),
    
    # Aqui os sufixos _OUTLINED sumiram. Como não há texto de apoio, usar variantes com mais massa preenchida ajuda na legibilidade rápida (Scanability) da interface.
    (ft.Icons.DASHBOARD, "Dashboard", "/dashboard"),
    (ft.Icons.BOOK, "Cursos", "/cursos"),
    (ft.Icons.PIE_CHART, "Relatórios", "/relatorios"),
    (ft.Icons.SETTINGS, "Configurações", "/configuracoes"),
]