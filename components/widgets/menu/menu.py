from typing import Final

import flet as ft

# Formato de cada item de menu: (ícone, texto exibido, rota de navegação)
MenuItem = tuple[str, str, str]

# Itens do menu principal (expandido)
MENU_ITEMS: Final[list[MenuItem]] = [
    (ft.Icons.HOME, "Início", "/inicio"),
    (ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/formulario"),
    (ft.Icons.GRID_VIEW_OUTLINED, "Dashboard", "/dashboard"),
    (ft.Icons.MENU_BOOK_OUTLINED, "Cursos", "/cursos"),
    (ft.Icons.PIE_CHART_OUTLINE, "Relatórios", "/relatorios"),
    (ft.Icons.SETTINGS_OUTLINED, "Configurações", "/configuracoes"),
]

# Itens do menu colapsado (versão compacta).
# Alguns ícones diferem propositalmente dos da lista acima (ex: variantes
# mais "sólidas"), pois ajudam na leitura rápida quando o menu está encolhido.
MENU_ITEMS_COLLAPSED: Final[list[MenuItem]] = [
    (ft.Icons.HOME, "Início", "/inicio"),
    (ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/formulario"),
    (ft.Icons.DASHBOARD, "Dashboard", "/dashboard"),
    (ft.Icons.BOOK, "Cursos", "/cursos"),
    (ft.Icons.PIE_CHART, "Relatórios", "/relatorios"),
    (ft.Icons.SETTINGS, "Configurações", "/configuracoes"),
]