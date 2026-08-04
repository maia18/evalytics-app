import flet as ft


def criar_borda_uniforme(cor: str, largura: int = 1) -> ft.Border:
    """Cria uma borda de mesma cor e espessura nos quatro lados do controle."""
    lado = ft.BorderSide(largura, cor)
    return ft.Border(top=lado, bottom=lado, left=lado, right=lado)