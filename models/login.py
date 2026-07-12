""" Importações """  
import flet as ft

def ViewLogin(page: ft.Page, mudar_tela):
    """
    Tela de login do sistema Evalytics.
    Possui campos de e-mail e senha, validação simples e design com efeito de vidro sobre fundo animado.
    """

    # === 1. CAMPOS DE ENTRADA ===
    email_input = ft.TextField(
        label="E-mail",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        border_radius=12, 
        width=350,
        bgcolor="transparent",
        border_color="blue800",          
        focused_border_color="blue900",  
        color="black87"
    )
    
    senha_input = ft.TextField(
        label="Senha",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border_radius=12,
        width=350,
        bgcolor="transparent",  
        border_color="blue800",
        focused_border_color="blue900",
        color="black87"
    )
    
    # === 2. LÓGICA DE LOGIN ===
    def fazer_login(e):
        if email_input.value == "admin" and senha_input.value == "admin123":
            page.snack_bar = ft.SnackBar(ft.Text("Login realizado com sucesso!", color="green"))
            page.snack_bar.open = True
            page.update()
            mudar_tela("/inicio")  # redireciona para a página principal
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Credenciais inválidas.", color="red"))
            page.snack_bar.open = True
            page.update()
            
    # Permite login ao pressionar Enter
    email_input.on_submit = fazer_login
    senha_input.on_submit = fazer_login

    # Botão de entrar
    btn_entrar = ft.ElevatedButton(
        "Entrar",
        width=350,
        height=50,
        on_click=fazer_login,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor={"":"blue700", "hovered":"blue800"}, 
            color="white",
            elevation={"":"2", "hovered":"6"}, 
            animation_duration=250
        )
    )

    # === 3. PAINEL DE LOGIN COM EFEITO VIDRO ===
    painel_vidro = ft.Container(
        expand=1,
        bgcolor="#D9FFFFFF",  # efeito translúcido
        blur=15,
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color="blue700"),
                ft.Text("Acesso ao Sistema", size=28, weight="bold", color="black87"),
                ft.Container(height=30),
                email_input,
                ft.Container(height=5),
                senha_input,
                ft.Container(height=25),
                btn_entrar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # === 4. CAMADAS VISUAIS (FUNDO + CONTEÚDO) ===
    return ft.View(
        route="/",
        padding=0,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    # CAMADA 1: Fundo animado
                    ft.Image(
                        src="fundo.gif", 
                        fit="cover",
                        width=3000,  
                        height=3000, 
                    ),
                    
                    # CAMADA 2: Conteúdo principal
                    ft.Row(
                        expand=True,
                        controls=[
                            # Lado esquerdo: título e slogan
                            ft.Container(
                                expand=1,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Evalytics", size=70, weight="w900", color="white"),
                                        ft.Text("Gestão de Avaliação Institucional", size=18, color="white")
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            ),
                            # Lado direito: painel de login
                            painel_vidro
                        ],
                        spacing=0
                    )
                ]
            )
        ]
    )
