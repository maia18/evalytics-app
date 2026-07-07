from nicegui import ui
import plotly.graph_objects as go # Importação do Plotly
import csv # Importação necessária para gerar o arquivo do Excel
import io

from components.layout import layout
from components.header import titulo_pagina
from database.supabase_client import supabase
from services.relatorio_service import gerar_relatorio_avaliacao
from components.auth import require_login # Importando a trava

@ui.page('/relatorios')
def relatorios():
    # 1. Trava de Segurança
    if not require_login(): 
        return

    layout()
    titulo_pagina("📊 Relatórios", "Análise de desempenho por avaliação")

    try:
        res = supabase.table('avaliacoes').select('id, professores(nome), disciplinas(nome)').eq('status', 'concluida').execute()
        opcoes = {
            a['id']: f"Prof. {a['professores']['nome']} - {a['disciplinas']['nome']} ({a['id'][:8]})"
            for a in res.data
        } if res.data else {}
    except Exception as e:
        ui.notify(f"Erro ao buscar avaliações: {e}", type="negative")
        opcoes = {}

    with ui.row().classes('w-full items-end gap-4 mt-4'):
        select_aval = ui.select(opcoes, label="Selecione uma Avaliação", with_input=True).classes("w-full max-w-md")
        btn_gerar = ui.button("Gerar relatório", on_click=lambda: gerar()).props('color=primary')

    ui.separator().classes('my-6')
    output = ui.column().classes('w-full items-center') # Centralizado

    def gerar():
        output.clear()
        
        if not select_aval.value:
            ui.notify("Selecione uma avaliação primeiro.", type="warning")
            return

        relatorio = gerar_relatorio_avaliacao(select_aval.value)

        with output:
            if not relatorio:
                ui.label("Erro ao gerar relatório.").classes('text-red-500 font-bold')
                return
            
            with ui.card().classes('w-full max-w-4xl p-6 shadow-md rounded-lg'):
                
                # ==========================
                # CABEÇALHO E BOTÃO DE EXPORTAR
                # ==========================
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label("Resultados da Avaliação").classes('text-xl font-bold text-gray-800')
                    
                    def exportar_csv():
                        
                        nome_arquivo = f"relatorio_avaliacao_{select_aval.value[:8]}.csv"
                        
                        # Cria um arquivo "virtual" na memória
                        arquivo_memoria = io.StringIO()
                        writer = csv.writer(arquivo_memoria, delimiter=';')
                        writer.writerow(['Eixo', 'Media'])
                        
                        for eixo, media in relatorio["medias_por_eixo"].items():
                            writer.writerow([f'Eixo {eixo}', str(media).replace('.', ',')])
                        
                        # Converte o texto gerado para bytes
                        csv_bytes = arquivo_memoria.getvalue().encode('utf-8')
                        
                        # Manda o download diretamente da memória
                        ui.download(csv_bytes, filename=nome_arquivo)
                        ui.notify("Download do arquivo CSV concluído!", type='positive')

                    ui.button("Exportar CSV", on_click=exportar_csv, icon='download').props('outline size=sm')
                
                # Indicadores numéricos
                with ui.row().classes('w-full gap-8 justify-center mb-8'):
                    with ui.column().classes('items-center'):
                        ui.label("Média Geral").classes('text-sm text-gray-500 font-semibold')
                        ui.label(str(relatorio['media_geral'])).classes('text-4xl font-bold text-primary')
                    
                    with ui.column().classes('items-center'):
                        ui.label("Respostas").classes('text-sm text-gray-500 font-semibold')
                        ui.label(str(relatorio['total_respostas'])).classes('text-4xl font-bold text-primary')

                ui.separator().classes('mb-8')
                
                # ==========================
                # GRÁFICO PLOTLY (RADAR)
                # ==========================
                eixos = [f"Eixo {e}" for e in relatorio["medias_por_eixo"].keys()]
                medias = list(relatorio["medias_por_eixo"].values())
                
                # O Plotly exige que o último ponto seja igual ao primeiro para "fechar" a linha do radar
                if eixos:
                    eixos_fechado = eixos + [eixos[0]]
                    medias_fechado = medias + [medias[0]]
                else:
                    eixos_fechado, medias_fechado = [], []

                fig = go.Figure(data=go.Scatterpolar(
                    r=medias_fechado,
                    theta=eixos_fechado,
                    fill='toself',
                    name='Média',
                    line_color='#3b82f6' # Azul
                ))

                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 5]) # Notas de 0 a 5
                    ),
                    showlegend=False,
                    margin=dict(l=40, r=40, t=20, b=20)
                )

                # Renderiza o gráfico do plotly nativamente no NiceGUI
                ui.plotly(fig).classes('w-full max-w-2xl mx-auto h-[400px]')

    with output:
        ui.label("Selecione uma avaliação acima para visualizar o relatório.").classes('text-gray-500 italic mt-4')