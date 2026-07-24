import flet as ft
# Simulação das importações baseadas na arquitetura do seu projeto
from utils.services.relatorio_service import calcular_medias_eixos
# Integrando com a função unificada e poderosa que criamos no passo anterior!
from models.relatorios.core.export_pdf import gerar_pdf_completo 

def TelaResultados(page: ft.Page):
    """
    Dashboard Executivo de Resultados.
    Atua como a View principal de análise, onde os gestores podem visualizar 
    o desempenho da instituição através de indicadores semafóricos (cores) 
    e exportar os dados consolidados.
    """
    
    # 1. Busca os dados matemáticos já calculados pela regra de negócio
    medias = calcular_medias_eixos()
    
    # 2. Dicionário (De/Para) para traduzir os IDs do banco para textos amigáveis na interface
    nomes_eixos = {
        1: "Organização Didático-Pedagógica",
        2: "Corpo Docente e Tutorial",
        3: "Infraestrutura"
    }

    # === AÇÕES ===
    def exportar_pdf(e):
        """
        Callback acionado pelo botão de exportação. 
        Conecta a interface visual ao motor de geração de PDF + Plotly.
        """
        # Altera visualmente o botão para indicar carregamento
        e.control.text = "Gerando Relatório..."
        e.control.disabled = True
        page.update()
        
        # Chama a nossa função unificada! 
        # Como ela já possui o mostrar_feedback(page) internamente, não precisamos 
        # criar Snackbars manuais aqui, mantendo a View extremamente limpa.
        gerar_pdf_completo(page, medias, nomes_eixos, semestre="2026.1")
        
        # Restaura o estado original do botão
        e.control.text = "Exportar Relatório PDF"
        e.control.disabled = False
        page.update()

    # === CONSTRUÇÃO DA INTERFACE ===
    cards_resultados = []
    
    # Itera sobre os dados para gerar os cartões dinamicamente.
    # Se no futuro você adicionar 10 eixos, a tela se adapta automaticamente sem precisar alterar o front-end!
    for eixo_id, nota in medias.items():
        
        # Lógica de "Semáforo" (Thresholding) para feedback visual rápido:
        # Acima de 3.5 = Verde (Bom) | Acima de 2.5 = Laranja (Alerta) | Abaixo = Vermelho (Crítico)
        cor_barra = "green" if nota >= 3.5 else "orange" if nota >= 2.5 else "red"
        
        # Adiciona o cartão à lista de componentes
        cards_resultados.append(
            ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            # Título do Eixo
                            ft.Text(nomes_eixos.get(eixo_id, f"Eixo {eixo_id}"), weight="bold", size=16),
                            
                            # Linha com o label e a nota formatada (ex: 4.5 / 5.0)
                            ft.Row([
                                ft.Text("Desempenho", size=12, color="grey"),
                                ft.Text(f"{nota:.1f} / 5.0", weight="bold", size=14, color=cor_barra),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            
                            # Barra de progresso preenchida proporcionalmente (nota dividida pelo máximo que é 5)
                            ft.ProgressBar(value=nota/5, color=cor_barra, height=10, border_radius=5),
                        ]
                    )
                )
            )
        )

    # NOVO: Cabeçalho com o título à esquerda e botão à direita (Opção 1)
    cabecalho = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            # Textos de título agrupados em uma coluna
            ft.Column(
                spacing=5,
                controls=[
                    ft.Text("Dashboard de Resultados", size=28, weight="bold"),
                    ft.Text("Acompanhe o desempenho institucional através dos eixos avaliados.", size=14, color="grey"),
                ]
            ),
            # O botão que antes estava no final, agora vem pro topo!
            ft.ElevatedButton(
                "Exportar Relatório PDF", 
                icon=ft.Icons.PICTURE_AS_PDF,
                bgcolor="red700",
                color="white",
                height=45,
                on_click=exportar_pdf
            )
        ]
    )

    # Retorna o contêiner principal que envelopa toda a tela
    return ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                # O cabeçalho agora já inclui o título e o botão lado a lado
                cabecalho,
                ft.Divider(height=20, color="transparent"),
                
                ft.Column(
                    expand=True, # Preenche o resto da tela abaixo do cabeçalho
                    controls=cards_resultados 
                ),
            ], 
        )
    )