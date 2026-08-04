import flet as ft

def criar_estilo_aba(ativo: bool, cor_primaria: str, cor_texto_inativo: str) -> ft.ButtonStyle:
    """Estilo compartilhado das abas Sign In / Sign Up."""
    return ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        color=cor_primaria if ativo else cor_texto_inativo,
        bgcolor=ft.Colors.with_opacity(0.1, cor_primaria) if ativo else ft.Colors.TRANSPARENT,
        side=ft.BorderSide(0, ft.Colors.TRANSPARENT),  # Remove o contorno padrão de foco/hover.
        overlay_color=ft.Colors.TRANSPARENT,  # Remove o overlay que o Flet desenha ao focar/pressionar garantindo visual limpo.
    )