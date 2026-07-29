import flet as ft
from pathlib import Path # PathLib é a forma mais moderna e segura de manipular caminhos de arquivos no Python, evitando problemas com as barras de diretório entre Windows (\) e Linux/Mac (/).
import logging as lg # módulo nativo de logs para registrar eventos do sistema (neste caso, se o ícone não for encontrado).
'''
Importa as constantes do projeto. 
Centralizar esses valores em um arquivo de constantes é uma excelente prática, pois facilita a manutenção (se quiser mudar o tamanho da tela, muda num lugar só).
'''
from components.core.constants.constants import (
    APP_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)

logger = lg.getLogger(__name__) # Cria um logger específico para este módulo.

'''
Descobre o caminho absoluto do diretório raiz do projeto:
    1. __file__ pega o caminho do arquivo atual (globals.py).
    2. .resolve() converte para um caminho absoluto garantido.
    3. Cada .parent sobe um nível de pasta: 
        globals.py -> (1) core -> (2) components -> (3) raiz do projeto.
'''
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ICON_PATH = BASE_DIR / "assets" / "imgs" / "logo.ico" # Monta o caminho exato para o ícone do aplicativo juntando as pastas com a sintaxe de barra (/).

# função chamada uma única vez pelo arquivo main.py no momento em que o app inicia
def configurar_aplicacao(page: ft.Page) -> None:
    """
    Aplica as configurações globais da aplicação na página.
    Define título, dimensões da janela, tema, cor de fundo e ícone.
    """
    page.title = APP_TITLE # Define o título da janela (que aparece na barra superior do sistema operacional).
    
    # Trava/Define as dimensões iniciais da janela do aplicativo baseadas nas suas constantes.
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.padding = 0 # Remove as margens internas padrão do Flet (que costumam ser de 10px).

    page.theme_mode = ft.ThemeMode.LIGHT # Força o aplicativo a usar o modo Claro (LIGHT), ignorando a preferência do sistema operacional do usuário.
    page.bgcolor = ft.Colors.BLUE_GREY_50 # Define a cor de fundo padrão de todas as telas.

    # Programação defensiva: verifica se o arquivo do ícone realmente existe no disco antes de tentar aplicá-lo.
    if ICON_PATH.exists():
        page.window.icon = str(ICON_PATH) # O Flet espera que o caminho do ícone seja uma string, então precisamos converter o objeto Path usando str().
    else:
        """
        Se alguém apagar ou renomear o arquivo, o app não "quebra" (crash).
        Ele apenas avisa no terminal/log que o ícone não foi encontrado.
        """
        logger.warning("Ícone da janela não encontrado em: %s", ICON_PATH)