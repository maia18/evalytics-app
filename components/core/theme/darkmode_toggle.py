import flet as ft
from typing import Callable, Optional
from components.core.theme.theme_config import configurar_tema

# Alterna entre os temas claro e escuro (Dark Mode/Light Mode) da aplicação
def toggle_dark_mode(
    page: ft.Page,
    dark_mode: bool,
    mudar_tela: Optional[Callable[[str], None]],
    rota_atual: Optional[str],
) -> bool:
    """
    Inverte o estado atual, aplica o novo tema na página e, se uma função
    de navegação e a rota atual forem fornecidas, recarrega a tela para
    que os componentes sejam recriados com o novo tema.

    Retorna o novo estado de dark_mode, para ser armazenado externamente.
    """
    
    # Inverte o estado booleano do tema
    dark_mode = not dark_mode

    page.is_dark_mode = dark_mode  # Fonte de verdade pública do tema atual na página
    configurar_tema(page, dark_mode) # Chama a função responsável por aplicar as configurações visuais na página.
    page.update() # Avisa ao Flet para atualizar a interface gráfica.

    if mudar_tela and rota_atual:
        mudar_tela(rota_atual) # Recarrega a tela atual para que os componentes sejam recriados/atualizados com o novo tema

    return dark_mode # Retorna o novo estado para quem chamou a função (ex: para atualizar a variável do botão de toggle).