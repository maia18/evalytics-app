import flet as ft
from database.indicadores import INDICADORES

def ViewAvaliacoes(page: ft.Page, mudar_tela):
    
    # === ESTILOS BASE ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        alignment=ft.alignment.Alignment(-1, 0) 
    )

    sidebar = ft.Container(
        width=260,
        bgcolor="blue900",
        padding=20,
        content=ft.Column(
            expand=True,
            controls=[
                # Logo e Título
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ANALYTICS, color="white", size=32),
                        ft.Text("Evalytics", size=24, weight="bold", color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(color="white24", height=30),
                
                # Link de Navegação
                ft.TextButton("Dashboard", on_click=lambda _: mudar_tela("/dashboard"), style=estilo_botao_menu),
                
            ]
        )
    )
    
    # === 2. LÓGICA DO MODAL (CAIXA DE JUSTIFICATIVA) ===
    def fechar_modal(e):
        modal_edicao.open = False
        page.update()

    def salvar_edicao(e):
        fechar_modal(e)
        page.snack_bar = ft.SnackBar(ft.Text("Melhoria registrada com sucesso!", color="green"))
        page.snack_bar.open = True
        page.update()

    modal_edicao = ft.AlertDialog(
        title=ft.Text("Corrigir / Melhorar Indicador", size=18, weight="bold"),
        content=ft.Column(
            width=500,
            height=280,
            spacing=15,
            controls=[
                ft.Text("Descreva a falha encontrada ou nova melhoria:", size=14, weight="bold"),
                ft.TextField(multiline=True, min_lines=2, max_lines=2, border_color="blue200", hint_text="Ex: Roteador do bloco B apresenta instabilidade..."),
                
                ft.Text("Justificativa / Plano de Ação:", size=14, weight="bold"),
                ft.TextField(multiline=True, min_lines=3, max_lines=3, border_color="blue200", hint_text="Ex: Acionado a equipe de TI para substituição do equipamento..."),
            ]
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal, style=ft.ButtonStyle(color="red")),
            ft.ElevatedButton("Salvar Alterações", bgcolor="blue700", color="white", on_click=salvar_edicao)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal(e):
        page.dialog = modal_edicao
        modal_edicao.open = True
        page.update()

    # === 3. TELA SECUNDÁRIA: LISTA DE INDICADORES ===
    def criar_linha_indicador(titulo, status):
        # Muda a cor da tag dependendo do status do indicador
        cor_fundo_status = "green600" if status == "ATIVO" else ("red600" if status == "FALHA" else "amber600")
        
        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=8,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"), # Sombra leve para destacar a linha
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(titulo, size=15, weight="w500", color="black87", expand=True),
                    ft.Container(
                        bgcolor=cor_fundo_status, padding=5, border_radius=4,
                        content=ft.Text(status, size=12, color="white", weight="bold")
                    ),
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Adicionar Correção", on_click=abrir_modal)
                ]
            )
        )

    def abrir_pasta(titulo_pasta):
        
        # 1. Mapear o título da pasta para o número do Eixo correspondente no banco
        mapa_eixos = {
            "Organização Didático-Pedagógica": 1,
            "Corpo Docente e Tutorial": 2,
            "Infraestrutura": 3
        }
        eixo_id = mapa_eixos.get(titulo_pasta)
        
        # 2. Filtrar a lista INDICADORES para pegar apenas os que pertencem a este eixo
        lista_da_pasta = [item for item in INDICADORES if item.get("eixo") == eixo_id]
        
        # Função temporária para o botão Novo
        def acao_novo_indicador(e):
            page.snack_bar = ft.SnackBar(ft.Text("Aqui abriremos o formulário de um Novo Indicador!", color="white"))
            page.snack_bar.open = True
            page.update()

        # Cria o cabeçalho com o botão de voltar à esquerda e o "Novo" à direita
        controles_lista = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas()),
                        ft.Text(titulo_pasta, size=22, weight="bold", color="black87")
                    ]),
                    ft.ElevatedButton(
                        "Novo Indicador",
                        icon=ft.Icons.ADD,
                        bgcolor="blue700",
                        color="white",
                        height=40,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                        on_click=acao_novo_indicador
                    )
                ]
            ),
            ft.Divider(height=20, color="transparent")
        ]
        
        # Adiciona cada indicador filtrado na tela
        for item in lista_da_pasta:
            # Como o banco de dados oficial não tem "status" cadastrado, definimos "ATIVO" visualmente
            status_visual = item.get("status", "ATIVO")
            controles_lista.append(criar_linha_indicador(item["titulo"], status_visual))
            
        # Troca o conteúdo da tela principal
        area_conteudo.content = ft.Column(
            expand=True, 
            spacing=15, 
            controls=controles_lista,
            scroll=ft.ScrollMode.AUTO # <-- ADICIONADO: Essencial para conseguir rolar a página para baixo!
        )
        page.update()

    def voltar_para_pastas():
        area_conteudo.content = layout_pastas
        page.update()

    # === 4. TELA INICIAL: PASTAS (EIXOS) ===
    def criar_pasta_indicador(titulo_pasta, qtd_indicadores):
        return ft.Container(
            bgcolor="#F4F6F9",
            border_radius=8,
            padding=20,
            ink=True,
            on_click=lambda e: abrir_pasta(titulo_pasta), # Ao clicar, chama a lista
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

    # Lógica para contar os indicadores reais da sua base de dados
    qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
    qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
    qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)

    layout_pastas = ft.Column(
        expand=True,
        spacing=25,
        controls=[
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color="black87"),
            ft.Column(
                spacing=15,
                controls=[
                    criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1),
                    criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2),
                    criar_pasta_indicador("Infraestrutura", qtd_eixo_3),
                ]
            )
        ]
    )
    
    # === 5. MONTAGEM DA ESTRUTURA FINAL ===
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="white",
        content=layout_pastas
    )

    return ft.View(
        route="/avaliacoes",
        padding=0,
        bgcolor="white",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    sidebar,
                    area_conteudo
                ]
            )
        ]
    )