from nicegui import app, ui

@ui.page('/login')
def login():
    # Se já estiver logado, manda direto para o dashboard
    if app.storage.user.get('autenticado', False):
        ui.navigate.to('/dashboard')
        return

    # Interface centralizada
    with ui.column().classes('w-full max-w-md mx-auto items-center mt-24 p-8 shadow-xl rounded-xl border border-gray-200 bg-white'):
        ui.label('🔐 Acesso Restrito').classes('text-2xl font-bold mb-6 text-gray-800')
        
        usuario = ui.input('Usuário').classes('w-full text-lg')
        senha = ui.input('Senha', password=True, password_toggle_button=True).classes('w-full text-lg mt-2')
        
        def tentar_login():
            # Credenciais fixas para esta etapa do projeto
            if usuario.value == 'admin' and senha.value == 'admin123':
                app.storage.user['autenticado'] = True
                ui.navigate.to('/dashboard')
                ui.notify('Bem-vindo ao Evalytics!', type='positive')
            else:
                ui.notify('Usuário ou senha incorretos.', type='negative')

        ui.button('Entrar', on_click=tentar_login, icon='login').classes('w-full h-12 mt-6 text-lg').props('color=primary')