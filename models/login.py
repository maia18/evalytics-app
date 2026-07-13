import flet as ft

def ViewLogin(page: ft.Page, mudar_tela):
    
    # === ESTILOS E PALETA ===
    COR_PRIMARIA = "#F59E0B" # Laranja do template
    COR_FUNDO = "#F9FAFB"    # Fundo cinza super claro
    COR_CARD = "#FFFFFF"     # Cartão branco
    COR_BORDA = "#E5E7EB"    # Borda sutil
    COR_TEXTO_TITULO = "#111827"
    COR_TEXTO_SECUNDARIO = "#6B7280"

    # === LÓGICA DE LOGIN ===
    def fazer_login(e):
        # Aqui no futuro você conectará com o firebase_config.py
        mudar_tela("/inicio")

    # === 1. CABEÇALHO (LOGO E BOAS-VINDAS) ===
    cabecalho = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            # Logo no lugar do ícone
            ft.Container(
                # padding=5,
                content=ft.Image(
                    src="logo.png",
                    width=60,
                    height=60,
                    fit="CONTAIN",
                )
            ),
            # Textos
            ft.Text("Bem-vindo ao Evalytics", size=28, weight="bold", color=COR_TEXTO_TITULO),
            ft.Text(
                "Faça login para gerenciar as avaliações institucionais.", 
                size=16, 
                color=COR_TEXTO_SECUNDARIO,
                text_align=ft.TextAlign.CENTER
            )
        ]
    )

    # === 2. CAMPOS DE ENTRADA (ESTILO CLEAN) ===
    campo_email = ft.Column(
        spacing=5,
        controls=[
            ft.Text("Email", size=14, weight="w500", color=COR_TEXTO_TITULO),
            ft.TextField(
                hint_text="voce@instituicao.com",
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO),
                border_color=COR_BORDA,
                border_radius=8,
                content_padding=15,
                cursor_color=COR_TEXTO_TITULO,
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO)
            )
        ]
    )

    campo_senha = ft.Column(
        spacing=5,
        controls=[
            ft.Text("Senha", size=14, weight="w500", color=COR_TEXTO_TITULO),
            ft.TextField(
                hint_text="Digite sua senha",
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO),
                password=True,
                can_reveal_password=True,
                border_color=COR_BORDA,
                border_radius=8,
                content_padding=15,
                cursor_color=COR_TEXTO_TITULO,
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO)
            )
        ]
    )

    # === 3. AÇÕES EXTRAS ===
    opcoes_extras = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Checkbox(
                label="Lembrar-me", 
                label_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO, size=14), 
                fill_color=COR_PRIMARIA
            ),
            ft.TextButton(
                "Esqueceu a senha?", 
                style=ft.ButtonStyle(color=COR_PRIMARIA)
            )
        ]
    )

    # === 4. BOTÃO PRINCIPAL ===
    btn_login = ft.ElevatedButton(
        "Entrar",
        bgcolor=COR_PRIMARIA,
        color="white",
        width=float("inf"),
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login
    )

    # === 5. CARTÃO DO FORMULÁRIO ===
    card_login = ft.Container(
        width=420,
        bgcolor=COR_CARD,
        padding=40,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"), 
        content=ft.Column(
            spacing=20,
            controls=[
                campo_email,
                campo_senha,
                opcoes_extras,
                btn_login
            ]
        )
    )

    # === VIEW FINAL ===
    return ft.View(
        route="/",
        bgcolor=COR_FUNDO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        padding=20,
        controls=[
            ft.Container(
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[cabecalho, card_login]
                )
            )
        ]
    )