import flet as ft
from components.core.theme.theme import AppColors, get_app_theme

# Configura o tema visual da aplicação (cores, modo) na página do Flet
def configurar_tema(page: ft.Page, dark_mode: bool) -> dict[str, str]:
    """
    Retorna a paleta de cores correspondente ao tema aplicado, para uso manual em componentes que precisem de cores específicas.
    """
    page.theme = get_app_theme(dark_mode) # Aplica o tema configurado com a semente primária na página.
    page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT # Alterna o motor de renderização da página inteira entre o padrão Dark ou Light do Material Design.

    return AppColors.get(dark_mode) # Ao retornar as cores aqui, permite-se que o chamador guarde essa paleta para repassar aos componentes de tela.