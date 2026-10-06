import flet as ft
import logging as lg # módulo nativo do Python usado para registrar mensagens, avisos e erros no console ou em arquivos.
from components.core.globals import configurar_aplicacao # configurações visuais da página (título, tema, tamanho da janela, etc).
from components.core.navigator import Navigator # classe customizada criada para gerenciar o roteamento/troca de telas no app.
from components.core.auth import auth_state

'''
Cria uma instância de logger específica para este arquivo. 
    Usar __name__ ajuda a identificar nos logs exatamente de qual módulo (arquivo) a mensagem veio.
'''
logger = lg.getLogger(__name__)

ROTA_INICIAL = "/" # Define uma constante para a rota inicial.

# FIREBASE_API_KEY = "xxxxxxxxxxxxxxxxxxxx"
FIREBASE_API_KEY = "AIzaSyAqGHhj3-BihICWHvD70smkjcbP2D8Sxnk"

async def main(page: ft.Page) -> None:
    try:
        configurar_aplicacao(page)

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
    lg.basicConfig(level=lg.INFO) # Configura o sistema de logs para exibir mensagens a partir do nível INFO (ignora mensagens de DEBUG, mas mostra avisos e erros).
    ft.run(
        main, 
        assets_dir="assets", # Pasta onde ficam os arquivos estáticos (imagens, ícones, etc.)
    )