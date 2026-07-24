import flet as ft 

# Lista de itens do menu principal (expandido)
# A estrutura de dados é uma lista de tuplas: (Constante de Ícone, Nome Exibido, Rota de Navegação)
MENU_ITEMS = [ 
    (ft.Icons.HOME, "Início", "/inicio"), 
    (ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/formulario"), 
    (ft.Icons.GRID_VIEW_OUTLINED, "Dashboard", "/dashboard"), 
    (ft.Icons.MENU_BOOK_OUTLINED, "Cursos", "/cursos"), 
    (ft.Icons.PIE_CHART_OUTLINE, "Relatórios", "/relatorios"), 
    (ft.Icons.SETTINGS_OUTLINED, "Configurações", "/configuracoes"), 
] 

# Lista de itens do menu colapsado (versão compacta)
# Alguns ícones aqui diferem propositalmente da lista acima (ex: ADD_BOX_OUTLINED virou ADD_CIRCLE). 
# Ícones mais "sólidos" ajudam na visualização rápida quando o menu está encolhido.
MENU_ITEMS_COLLAPSED = [ 
    (ft.Icons.HOME, "Início", "/inicio"), 
    (ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/formulario"), 
    (ft.Icons.DASHBOARD, "Dashboard", "/dashboard"), 
    (ft.Icons.BOOK, "Cursos", "/cursos"), 
    (ft.Icons.PIE_CHART, "Relatórios", "/relatorios"), 
    (ft.Icons.SETTINGS, "Configurações", "/configuracoes"), 
] 