from components.core.theme.theme import AppColors, get_app_theme
import flet as ft

def configurar_tema(page: ft.Page, dark_mode: bool):
    page.theme = get_app_theme(dark_mode)
    page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT
    return AppColors.get(dark_mode)