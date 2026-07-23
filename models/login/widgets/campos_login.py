import flet as ft

def criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA):
    """
    Cria o campo de entrada para o 'Nome' do usuário.
    Este campo é exclusivo para a etapa de cadastro (Sign Up).
    """
    return ft.Column(
        spacing=5, # Espaçamento curto entre o rótulo (label) e o campo de texto
        visible=False, # Inicia oculto, pois a tela abre por padrão no modo "Sign In" (Login)
        controls=[
            # Rótulo do campo
            ft.Text("Nome", size=14, weight="w500", color=COR_TEXTO_TITULO),
            
            # Campo de entrada de texto
            ft.TextField(
                hint_text="John Doe", # Texto de dica (placeholder) indicando o formato esperado
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO), # Estilo da dica (geralmente uma cor mais clara/cinza)
                border_color=COR_BORDA, # Cor da linha delimitadora do campo
                border_radius=8, # Arredondamento das bordas para um visual moderno
                content_padding=15, # Espaço interno (respiro) entre o texto digitado e a borda do campo
                cursor_color=COR_TEXTO_TITULO, # Cor do cursor piscante (caret)
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO) # Cor do texto efetivamente digitado pelo usuário
            )
        ]
    )

def criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA):
    """
    Cria o campo de entrada para o 'Email' do usuário.
    Utilizado tanto no Login quanto no Cadastro.
    """
    return ft.Column(
        spacing=5,
        controls=[
            ft.Text("Email", size=14, weight="w500", color=COR_TEXTO_TITULO),
            ft.TextField(
                hint_text="voce@instituicao.com", # Exemplo de email voltado para o ambiente institucional
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO),
                border_color=COR_BORDA,
                border_radius=8,
                content_padding=15,
                cursor_color=COR_TEXTO_TITULO,
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO)
            )
        ]
    )

def criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA):
    """
    Cria o campo de entrada para a 'Senha' do usuário.
    Possui recursos nativos de segurança e visibilidade.
    """
    return ft.Column(
        spacing=5,
        controls=[
            ft.Text("Senha", size=14, weight="w500", color=COR_TEXTO_TITULO),
            ft.TextField(
                hint_text="Digite sua senha",
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO),
                
                # Propriedades específicas para campos de senha:
                password=True, # Mascara o texto digitado substituindo os caracteres por bolinhas/asteriscos
                can_reveal_password=True, # Adiciona automaticamente o ícone de "olho" clicável no canto direito para mostrar/ocultar a senha
                
                border_color=COR_BORDA,
                border_radius=8,
                content_padding=15,
                cursor_color=COR_TEXTO_TITULO,
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO)
            )
        ]
    )