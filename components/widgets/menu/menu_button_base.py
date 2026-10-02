import flet as ft
from typing import Callable, Optional

from components.core.constants.constants import (
    HOVER,
    ALTURA_BOTAO_MENU,
    RAIO_BOTAO_MENU,
    PADDING_BOTAO_MENU,
    HOVER_CLARO_BOTAO_MENU,
)

def criar_botao_menu_base(
    content: ft.Control,
    rota: str,
    dark_mode: bool,
    mudar_tela: Optional[Callable[[str], None]],
    alignment: Optional[ft.Alignment] = None,
    expand: bool = False,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
) -> ft.Container:
    """Casca compartilhada de um botão de navegação do menu (sidebar).

    Usada tanto pelo botão só-com-ícone (versão colapsada) quanto pelo
    botão ícone+texto (versão completa) — a diferença entre eles fica
    inteiramente no `content` recebido.
    """
    
    def executar_click(e: ft.ControlEvent) -> None:
        if on_click:
            on_click(e)
        elif mudar_tela:
            mudar_tela(rota)

    return ft.Container(
        height=ALTURA_BOTAO_MENU, # Trava a altura do botão com base na sua constante global
        alignment=alignment, # Útil para centralizar o botão de ícone ou alinhar o de texto
        
        # O elemento interativo real é um TextButton nativo do Flet
        content=ft.TextButton(
            expand=expand,
            content=content, # Aqui é injetado o conteúdo visual (Row com texto ou só o Icon)
            style=ft.ButtonStyle(
                padding=PADDING_BOTAO_MENU,
                shape=ft.RoundedRectangleBorder(
                    radius=RAIO_BOTAO_MENU
                ),
                
                # Define a cor de fundo dinamicamente quando o mouse passa por cima, com base no tema claro/escuro
                overlay_color=(
                    HOVER
                    if dark_mode
                    else HOVER_CLARO_BOTAO_MENU
                ),
            ),
            
            # Executa a função de mudança de rota se houver uma função injetada (evita erro caso mudar_tela seja None)
            on_click=executar_click,
        ),
    )