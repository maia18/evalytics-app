import flet as ft
import json
from database.indicadores import INDICADORES # Importando a lista real

def ViewConfiguracoes(page: ft.Page, mudar_tela):
    
    # === 1. VARIÁVEIS DE ESTADO E MODAIS ===
    pasta_aberta_atualmente = {"titulo": "", "eixo": 0}
    item_alvo_acao = {}

    # (Modais reaproveitados da lógica do seu avaliacoes.py)
    campo_add_titulo = ft.TextField(label="Título do Indicador", border_color="blue200")
    campo_add_desc = ft.TextField(label="Descrição (Opcional)", multiline=True, min_lines=2, border_color="blue200")
    
    def fechar_modais(e=None):
        modal_novo.open = False
        page.update()

    modal_novo = ft.AlertDialog(
        title=ft.Text("Adicionar Indicador", size=18, weight="bold"),
        content=ft.Column([campo_add_titulo, campo_add_desc], height=150),
        actions=[ft.ElevatedButton("Salvar", bgcolor="blue700", color="white", on_click=lambda e: fechar_modais())]
    )

    # === 2. LÓGICA DE NAVEGAÇÃO EXPANSÍVEL (A MÁGICA) ===
    
    def criar_linha_indicador(item):
        return ft.Container(
            padding=15, bgcolor="white", border_radius=8,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
            content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Text(item["titulo"], weight="w500", color="blue700"),
                ft.Row([
                    ft.Container(content=ft.Text("ATIVO", color="white", size=10, weight="bold"), bgcolor="green600", padding=5, border_radius=4),
                    ft.IconButton(ft.Icons.EDIT, icon_color="blue700"),
                    ft.IconButton(ft.Icons.DELETE, icon_color="red700")
                ])
            ])
        )

    def entrar_na_pasta(titulo_pasta, eixo_id):
        pasta_aberta_atualmente.update({"titulo": titulo_pasta, "eixo": eixo_id})
        
        lista_itens = [criar_linha_indicador(item) for item in INDICADORES if item.get("eixo") == eixo_id]
        
        # O layout expandido que substitui a tela toda
        area_conteudo.content = ft.Container(
            expand=True, bgcolor="white", padding=40,
            content=ft.Column([
                ft.Row([
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas()),
                    ft.Text(titulo_pasta, size=22, weight="bold")
                ]),
                ft.Divider(height=20, color="transparent"),
                *lista_itens
            ])
        )
        area_conteudo.padding = 0
        page.update()

    def voltar_para_pastas(e=None):
        area_conteudo.content = layout_configuracoes_gerais
        area_conteudo.padding = 40
        page.update()

    # === 3. VISUAL: ABA INDICADORES (Pastas) ===
    def criar_pasta_indicador(titulo, qtd):
        return ft.Container(
            bgcolor="#F4F6F9", border_radius=8, padding=20, ink=True,
            on_click=lambda e: entrar_na_pasta(titulo, {"Organização Didático-Pedagógica": 1, "Corpo Docente e Tutorial": 2, "Infraestrutura": 3}[titulo]),
            content=ft.Row([
                ft.Icon(ft.Icons.FOLDER, color="blue700", size=28),
                ft.Column([
                    ft.Text(titulo, size=16, weight="bold"),
                    ft.Text(f"{qtd} indicadores", size=13, color="black54")
                ])
            ])
        )

    aba_indicadores = ft.Column([
        ft.Text("Gerenciar Indicadores", size=20, weight="bold"),
        criar_pasta_indicador("Organização Didático-Pedagógica", sum(1 for i in INDICADORES if i["eixo"]==1)),
        criar_pasta_indicador("Corpo Docente e Tutorial", sum(1 for i in INDICADORES if i["eixo"]==2)),
        criar_pasta_indicador("Infraestrutura", sum(1 for i in INDICADORES if i["eixo"]==3)),
    ])

    # === 4. ABAS DE SEGURANÇA E BANCO (Mantidas) ===
    aba_seguranca = ft.Container(padding=20, content=ft.Column([
        ft.Text("Políticas de Segurança", size=18, weight="bold"),
        ft.Switch(label="Exigir autenticação em duas etapas (2FA)", value=True)
    ]))

    aba_banco = ft.Container(padding=20, content=ft.Column([
        ft.Text("Gerenciamento de Dados", size=18, weight="bold"),
        ft.ElevatedButton("Realizar Backup", icon=ft.Icons.DOWNLOAD, bgcolor="green700", color="white")
    ]))

    # === 5. SISTEMA DE ABAS ===
    area_conteudo_aba = ft.Container(content=aba_indicadores, expand=True, padding=20)

    def mudar_aba(e, painel):
        area_conteudo_aba.content = painel
        page.update()

    menu_abas = ft.Row([
        ft.TextButton("Indicadores", icon=ft.Icons.RULE, on_click=lambda e: mudar_aba(e, aba_indicadores)),
        ft.TextButton("Segurança", icon=ft.Icons.SECURITY, on_click=lambda e: mudar_aba(e, aba_seguranca)),
        ft.TextButton("Banco de Dados", icon=ft.Icons.STORAGE, on_click=lambda e: mudar_aba(e, aba_banco))
    ])

    layout_configuracoes_gerais = ft.Column(expand=True, controls=[
        ft.Text("Configurações do Sistema", size=28, weight="bold"),
        ft.Container(bgcolor="white", border_radius=10, padding=20, shadow=ft.BoxShadow(blur_radius=5, color="black12"),
            content=ft.Column([menu_abas, ft.Divider(), area_conteudo_aba])
        )
    ])

    # === 6. MONTAGEM FINAL ===
    sidebar = ft.Container(width=260, bgcolor="blue900", padding=20, content=ft.Column([
        ft.Text("Evalytics", size=24, weight="bold", color="white"),
        ft.Divider(),
        ft.TextButton("Dashboard", icon=ft.Icons.DASHBOARD, on_click=lambda _: mudar_tela("/dashboard")),
        ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, on_click=lambda _: mudar_tela("/configuracoes"))
    ]))

    area_conteudo = ft.Container(expand=True, padding=40, bgcolor="#F4F6F9", content=layout_configuracoes_gerais)

    return ft.View(route="/configuracoes", padding=0, controls=[ft.Row(expand=True, spacing=0, controls=[sidebar, area_conteudo])])