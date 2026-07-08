import flet as ft

from views.cursos_view import TelaCursos
from views.indicadores_view import TelaIndicadores
from views.avaliacoes_view import TelaAvaliacao
from views.resultados_view import TelaResultados

# Removemos a importação da TelaProfessores, pois ela não faz mais parte da regra de negócio.

def ViewDashboard(page: ft.Page, mudar_tela):
    
    area_conteudo = ft.Container(padding=40, expand=True)

    # --- NOVAS FUNÇÕES DE NAVEGAÇÃO INTERNA ---
    def abrir_tela_avaliacao(curso):
        # Troca o conteúdo do painel pela tela de formulário
        area_conteudo.content = TelaAvaliacao(page, curso, on_voltar=voltar_para_cursos)
        page.update()

    def voltar_para_cursos():
        # Retorna para a tabela de cursos
        area_conteudo.content = TelaCursos(page, on_avaliar=abrir_tela_avaliacao)
        page.update()
        
    # ------------------------------------------

    # 1. Tela de Início (Visão Geral)
    tela_inicio = ft.Column(
        controls=[
            ft.Text("Visão Geral Institucional", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Selecione um módulo no menu lateral para gerenciar as avaliações dos cursos.", size=16),
            ft.Divider(height=40, color="transparent"),
            ft.Text(
                "Dica: Comece cadastrando os cursos, como Engenharia de Telecomunicações, na aba 'Cursos'.", 
                color="grey700", 
                italic=True
            ),
            ft.Divider(height=20, color="transparent"),
            ft.ElevatedButton("Sair do Sistema", on_click=lambda _: mudar_tela("/"), color="red")
        ]
    )

    # Define o conteúdo inicial
    area_conteudo.content = tela_inicio

    # 2. Gerenciador de Abas do Menu
    def alterar_aba(e):
        index = e.control.selected_index
        
        if index == 0:
            area_conteudo.content = tela_inicio
        elif index == 1:
            area_conteudo.content = TelaCursos(page, on_avaliar=abrir_tela_avaliacao)
        elif index == 2:
            area_conteudo.content = TelaIndicadores(page)
        elif index == 3:
            area_conteudo.content = TelaResultados(page)
            
        page.update()

    # 3. O Novo Menu Lateral (Focado na Coordenação)
    menu_lateral = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Início"),
            ft.NavigationRailDestination(icon=ft.Icons.SCHOOL, label="Cursos"), # Substitui Professores/Disciplinas
            ft.NavigationRailDestination(icon=ft.Icons.FACT_CHECK, label="Indicadores"),
            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART, label="Resultados"),
        ],
        on_change=alterar_aba
    )

    # 4. Layout Final
    layout_dashboard = ft.Row(
        controls=[
            menu_lateral,
            ft.VerticalDivider(width=1),
            area_conteudo
        ],
        expand=True
    )

    return ft.View(
        route="/dashboard",
        # Atualizamos o título da barra superior para refletir o usuário final
        appbar=ft.AppBar(title=ft.Text("Evalytics - Coordenação", color="white"), bgcolor="blue700"),
        controls=[layout_dashboard]
    )