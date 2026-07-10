import flet as ft

def ViewAvaliacoes(page: ft.Page, mudar_tela):
    
    # =====================================================================
    # 1. MENU LATERAL (COLE AQUI A SUA SIDEBAR DO DASHBOARD)
    # =====================================================================
    # Vá no seu arquivo dashboard.py, copie toda a variável "sidebar" 
    # (e o estilo_botao_menu se precisar) e cole aqui por cima deste placeholder:
    
    sidebar = ft.Container(
        width=250,
        bgcolor="blue900",
        content=ft.Column([
            ft.Text("Menu Temporário", color="white"),
            ft.TextButton("Voltar pro Dashboard", on_click=lambda _: mudar_tela("/dashboard"))
            # Substitua isso pela sua sidebar real!
        ])
    )
    # =====================================================================

    # === LÓGICA DO MODAL DE EDIÇÃO ===
    def fechar_modal(e):
        modal_edicao.open = False
        page.update()

    def salvar_edicao(e):
        # Aqui no futuro enviaremos os dados para o Firebase
        fechar_modal(e)
        page.snack_bar = ft.SnackBar(ft.Text("Melhoria registrada com sucesso!", color="green"))
        page.snack_bar.open = True
        page.update()

    modal_edicao = ft.AlertDialog(
        title=ft.Text("Corrigir ou Melhorar Indicador", size=18, weight="bold"),
        content=ft.Column(
            width=500,
            height=250,
            controls=[
                ft.Text("Descreva a falha encontrada ou a nova melhoria:", size=14),
                ft.TextField(multiline=True, min_lines=2, max_lines=2, border_color="blue200"),
                ft.Container(height=10),
                ft.Text("Justificativa da alteração:", size=14),
                ft.TextField(multiline=True, min_lines=3, max_lines=3, border_color="blue200", hint_text="Explique o motivo desta ação..."),
            ]
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal, col={"color": "red"}),
            ft.ElevatedButton("Salvar Alterações", bgcolor="blue700", color="white", on_click=salvar_edicao)
        ]
    )

    def abrir_modal(e):
        page.dialog = modal_edicao
        modal_edicao.open = True
        page.update()

    # === TELA 2: LISTA DE INDICADORES ===
    def criar_linha_indicador(titulo, status, cor_status):
        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=8,
            content=ft.Row(
                alignment="spaceBetween",
                controls=[
                    ft.Text(titulo, size=14, weight="bold", color="black87", expand=True),
                    ft.Container(
                        bgcolor=cor_status, padding=5, border_radius=4,
                        content=ft.Text(status, size=12, color="white", weight="bold")
                    ),
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Editar / Justificar", on_click=abrir_modal)
                ]
            )
        )

    def abrir_pasta(titulo_pasta):
        # Limpa o conteúdo principal e carrega a lista
        area_conteudo.content = ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas()),
                    ft.Text(titulo_pasta, size=22, weight="bold", color="black87")
                ]),
                # Simulando alguns indicadores dentro da pasta
                criar_linha_indicador("1.1 - Clareza do Plano de Ensino", "ATIVO", "green600"),
                criar_linha_indicador("1.2 - Cumprimento da Ementa", "REVISÃO", "amber600"),
                criar_linha_indicador("1.3 - Metodologia de Avaliação", "ATIVO", "green600"),
            ]
        )
        page.update()

    def voltar_para_pastas():
        area_conteudo.content = layout_pastas
        page.update()

    # === TELA 1: PASTAS (VISÃO INICIAL) ===
    def criar_pasta_indicador(titulo_pasta, qtd_indicadores):
        return ft.Container(
            bgcolor="#F4F6F9",
            border_radius=8,
            padding=20,
            ink=True,
            on_click=lambda e: abrir_pasta(titulo_pasta), # O clique agora abre a lista!
            content=ft.Row(
                spacing=15,
                controls=[
                    ft.Icon(ft.Icons.FOLDER, color="blue700", size=28),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(titulo_pasta, size=16, weight="bold", color="black87"),
                            ft.Text(f"{qtd_indicadores} indicadores", size=13, color="black54"),
                        ]
                    )
                ]
            )
        )

    layout_pastas = ft.Column(
        expand=True,
        spacing=25,
        controls=[
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color="black87"),
            ft.Column(
                spacing=15,
                controls=[
                    criar_pasta_indicador("Organização Didático-Pedagógica", 24),
                    criar_pasta_indicador("Infraestrutura", 18),
                    criar_pasta_indicador("Corpo Docente e Tutorial", 16),
                ]
            )
        ]
    )

    # === ESTRUTURA BASE DA TELA ===
    # O area_conteudo é um espaço dinâmico que começa com as pastas, mas pode mudar para a lista
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="white",
        content=layout_pastas 
    )

    # === RETORNO DA VIEW (AQUI DIVIDIMOS A TELA EM SIDEBAR + CONTEÚDO) ===
    return ft.View(
        route="/avaliacoes",
        padding=0, # Tiramos o padding global para a sidebar grudar no canto
        bgcolor="white",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    sidebar,       # Coluna Esquerda: Menu sempre visível
                    area_conteudo  # Coluna Direita: O conteúdo dinâmico
                ]
            )
        ]
    )