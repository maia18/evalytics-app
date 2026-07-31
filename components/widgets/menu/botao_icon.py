import flet as ft
from typing import Callable, Optional
from components.widgets.menu.menu_button_base import criar_botao_menu_base

def criar_botao_icon(
    icone: str,
    tooltip_text: str,
    rota: str,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela: Optional[Callable[[str], None]],
) -> ft.Container:
    """Cria um botão compacto que exibe apenas um ícone.

    Ideal para a sidebar quando o menu está recolhido.
    """
    
    # Prepara o controle visual central isoladamente
    icone_control = ft.Icon(
        icone,
        color=cor_texto,
        size=24,
        tooltip=tooltip_text,  # A tooltip é crucial para acessibilidade aqui: como o menu não tem texto, o balão indica para onde a rota vai quando o usuário repousa o mouse sobre o botão
    )
    
    # Chama o componente "casca" e injeta o ícone dentro dele
    return criar_botao_menu_base(
        content=icone_control,
        rota=rota,
        dark_mode=dark_mode,
        mudar_tela=mudar_tela,
        alignment=ft.Alignment(0, 0),  # Alignment(0, 0) força o ícone a ficar perfeitamente no centro matemático do container
        expand=True,  # Ocupa todo o espaço disponível no container de 45px (conforme configurado na casca)
    )