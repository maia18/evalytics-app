import logging
import flet as ft
from components.core.navigator import Navigator
from components.core.auth.auth_state import auth_state
from database.services.firebase_keys import FIREBASE_API_KEY
from components.core.theme.theme_config import configurar_tema
from components.core.globals import configurar_aplicacao

'''
Cria uma instância de logger específica para este arquivo.
'''
logger = logging.getLogger(__name__)
ROTA_INICIAL = "/" # Define uma constante para a rota inicial.

async def main(page: ft.Page) -> None:
    try:
        configurar_aplicacao(page)
        
        # Tema escuro como padrão.
        page.is_dark_mode = True
        configurar_tema(page, page.is_dark_mode)

        await auth_state.inicializar_storage(page)

        sessao_restaurada = await auth_state.restaurar_sessao(
            page=page,
            api_key=FIREBASE_API_KEY,
        )

        if sessao_restaurada:
            logger.info(
                "Sessão persistida restaurada com sucesso."
            )
        
            Navigator(page).go("/inicio")

        else:
            logger.info(
                "Nenhuma sessão persistida encontrada."
            )
            
            Navigator(page).go(ROTA_INICIAL)

    except Exception:
        logger.exception(
            "Falha ao inicializar a aplicação."
        )
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) # Configura o sistema de logs para exibir mensagens a partir do nível INFO (ignora mensagens de DEBUG, mas mostra avisos e erros).
    ft.run(
        main, 
        assets_dir="assets", # Pasta onde ficam os arquivos estáticos (imagens, ícones, etc.)
    )