import flet as ft
import logging as lg # módulo nativo do Python usado para registrar mensagens, avisos e erros no console ou em arquivos.
from components.core.globals import configurar_aplicacao # configurações visuais da página (título, tema, tamanho da janela, etc).
from components.core.navigator import Navigator # classe customizada criada para gerenciar o roteamento/troca de telas no app.

logger = lg.getLogger(__name__) # Cria uma instância de logger específica para este arquivo. Usar __name__ ajuda a identificar nos logs exatamente de qual módulo (arquivo) a mensagem veio.
ROTA_INICIAL = "/" # Define uma constante para a rota inicial. O padrão "/" geralmente aponta para a Home ou tela de Login.

def main(page: ft.Page) -> None:
    """
    Ponto de entrada (entry point) da aplicação Flet.
        O Flet chama esta função automaticamente, passando o objeto 'page' (que representa a janela do app ou a aba do navegador)
    """
    try:
        configurar_aplicacao(page) # Configura os aspectos globais da interface da página (cores, fontes, alinhamentos, etc).
        Navigator(page).go(ROTA_INICIAL) # Instancia a classe de navegação passando a página atual, e envia o usuário para a primeira tela.
        
    except Exception:
        logger.exception("Falha ao inicializar a aplicação.") # Se qualquer erro crítico acontecer na montagem da tela inicial, o logger registra o erro completo (com o traceback).
        
        raise # Propaga o erro para frente, forçando o programa a parar. Isso evita que o app abra quebrado e oculte o problema (fail-fast).

if __name__ == "__main__":
    lg.basicConfig(level=lg.INFO) # Configura o sistema de logs para exibir mensagens a partir do nível INFO (ignora mensagens de DEBUG, mas mostra avisos e erros).
    
    ft.run(
        main, 
        assets_dir="assets", # Pasta onde ficam os arquivos estáticos (imagens, ícones, etc.)
    )