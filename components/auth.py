from nicegui import app, ui

def require_login():
    """
    Verifica se o usuário está autenticado. 
    Se não estiver, redireciona para a tela de login.
    """
    if not app.storage.user.get('autenticado', False):
        ui.navigate.to('/login')
        return False
    return True

def logout():
    """Encerra a sessão e volta para o login."""
    app.storage.user['autenticado'] = False
    ui.navigate.to('/login')