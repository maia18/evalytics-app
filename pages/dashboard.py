from nicegui import ui
from components.layout import layout
from components.header import titulo_pagina
from services.relatorio_service import obter_resumo_dashboard, gerar_relatorio_ultima_avaliacao
from components.auth import require_login

@ui.page('/dashboard')
@ui.page('/')
def dashboard():
    # Trava de segurança: se retornar False, o código abaixo não executa
    if not require_login(): 
        return

    layout()
    titulo_pagina('📊 Dashboard', 'Visão geral do sistema')

    # ==========================
    # CARDS DE RESUMO
    # ==========================
    resumo = obter_resumo_dashboard()

    with ui.row().classes('w-full gap-4 mb-8'):
        with ui.card().classes('flex-1 p-4 bg-blue-50 items-center justify-center shadow-sm'):
            ui.label('Avaliações').classes('text-gray-500 font-semibold uppercase text-xs')
            ui.label(str(resumo['avaliacoes'])).classes('text-4xl font-bold text-blue-700')
            
        with ui.card().classes('flex-1 p-4 bg-green-50 items-center justify-center shadow-sm'):
            ui.label('Professores').classes('text-gray-500 font-semibold uppercase text-xs')
            ui.label(str(resumo['professores'])).classes('text-4xl font-bold text-green-700')
            
        with ui.card().classes('flex-1 p-4 bg-orange-50 items-center justify-center shadow-sm'):
            ui.label('Disciplinas').classes('text-gray-500 font-semibold uppercase text-xs')
            ui.label(str(resumo['disciplinas'])).classes('text-4xl font-bold text-orange-700')

    ui.separator().classes('mb-8')

    # ==========================
    # ÚLTIMA AVALIAÇÃO
    # ==========================
    ui.label('📌 Última Avaliação Concluída').classes('text-xl font-bold mb-4 text-gray-800')

    relatorio = gerar_relatorio_ultima_avaliacao()

    if not relatorio:
        ui.label("Nenhuma avaliação concluída registrada ainda.").classes('text-gray-500 italic')
        return

    # Extrai os dados populados pelo Supabase
    aval = relatorio['avaliacao']
    prof_nome = aval.get('professores', {}).get('nome', 'Desconhecido')
    disc_nome = aval.get('disciplinas', {}).get('nome', 'Desconhecida')

    with ui.card().classes('w-full p-6 shadow-md rounded-lg'):
        ui.label(f"Professor: {prof_nome}").classes('text-lg font-bold text-gray-800')
        ui.label(f"Disciplina: {disc_nome}").classes('text-md text-gray-600 mb-4')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column():
                ui.label("Média Geral").classes('text-sm text-gray-500 font-semibold')
                ui.label(str(relatorio['media_geral'])).classes('text-3xl font-bold text-primary')
            
            with ui.column():
                ui.label("Total de Respostas").classes('text-sm text-gray-500 font-semibold')
                ui.label(str(relatorio['total_respostas'])).classes('text-3xl font-bold text-primary')
                
        ui.separator().classes('my-4')
        
        ui.label("Médias por Eixo:").classes('font-bold text-gray-700 mb-2')
        with ui.row().classes('gap-4 w-full'):
            for eixo, media in relatorio["medias_por_eixo"].items():
                with ui.card().classes('p-3 bg-gray-50 flex-1 items-center border border-gray-100 shadow-none'):
                    ui.label(f"Eixo {eixo}").classes('text-xs text-gray-500 uppercase font-bold')
                    ui.label(str(media)).classes('text-xl font-bold text-gray-800')