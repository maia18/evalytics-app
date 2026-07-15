import flet as ft

# Lista de itens do menu principal (expandido)
MENU_ITEMS = [
    (ft.Icons.HOME, "Início", "/inicio"),
    (ft.Icons.ADD_BOX_OUTLINED, "Avaliação", "/avaliacoes"),
    (ft.Icons.GRID_VIEW_OUTLINED, "Dashboard", "/dashboard"),
    (ft.Icons.MENU_BOOK_OUTLINED, "Cursos", "/cursos"),
    (ft.Icons.PIE_CHART_OUTLINE, "Relatórios", "/relatorios"),
    (ft.Icons.SETTINGS_OUTLINED, "Configurações", "/configuracoes"),
]

# Lista de itens do menu colapsado (versão compacta)
MENU_ITEMS_COLLAPSED = [
    (ft.Icons.HOME, "Início", "/inicio"),
    (ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/avaliacoes"),
    (ft.Icons.DASHBOARD, "Dashboard", "/dashboard"),
    (ft.Icons.BOOK, "Cursos", "/cursos"),
    (ft.Icons.PIE_CHART, "Relatórios", "/relatorios"),
    (ft.Icons.SETTINGS, "Configurações", "/configuracoes"),
]