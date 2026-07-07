from nicegui import ui
from database.supabase_client import supabase
from services.avaliacao_session import session

@ui.page('/nova_avaliacao')
def nova_avaliacao():
    with ui.column().classes('w-full max-w-2xl mx-auto p-4 gap-6 items-center'):
        ui.label('Iniciar Nova Avaliação').classes('text-3xl font-bold text-primary mt-8 mb-4')

        # ======================
        # BUSCA DE DADOS (SUPABASE)
        # ======================
        try:
            prof_res = supabase.table('professores').select('id, nome').eq('ativo', True).execute()
            disc_res = supabase.table('disciplinas').select('id, nome, codigo').execute()
            
            # Formata os dados para o formato esperado pelo ui.select {id: "Label Visível"}
            opcoes_professores = {p['id']: p['nome'] for p in prof_res.data} if prof_res.data else {}
            opcoes_disciplinas = {d['id']: f"{d['codigo']} - {d['nome']}" for d in disc_res.data} if disc_res.data else {}
            
        except Exception as e:
            ui.notify(f"Erro ao carregar dados: {e}", type='negative')
            opcoes_professores, opcoes_disciplinas = {}, {}

        # ======================
        # FORMULÁRIO DE SELEÇÃO
        # ======================
        with ui.card().classes('w-full p-8 shadow-lg rounded-xl gap-4'):
            
            ui.label('Selecione os parâmetros da avaliação:').classes('text-lg text-gray-700 mb-2')
            
            select_prof = ui.select(
                opcoes_professores, 
                label='Selecione o Professor', 
                with_input=True # Permite digitar para buscar
            ).classes('w-full text-lg')
            
            select_disc = ui.select(
                opcoes_disciplinas, 
                label='Selecione a Disciplina', 
                with_input=True
            ).classes('w-full text-lg')

            ui.separator().classes('my-4')

            # ======================
            # AÇÃO DE INÍCIO
            # ======================
            def iniciar_fluxo():
                if not select_prof.value or not select_disc.value:
                    ui.notify('Por favor, selecione o professor e a disciplina.', type='warning')
                    return
                
                # Injeta os IDs na sessão global e zera o estado de respostas
                session.iniciar_avaliacao(
                    professor_id=select_prof.value,
                    disciplina_id=select_disc.value
                )
                
                # Navega para a página do primeiro eixo (que configuramos anteriormente)
                ui.navigate.to('/avaliacao')

            ui.button(
                'Começar Avaliação', 
                on_click=iniciar_fluxo, 
                icon='play_arrow'
            ).classes('w-full h-14 text-lg font-bold').props('color=primary')
            
            ui.button(
                'Voltar ao Início', 
                on_click=lambda: ui.navigate.to('/dashboard')
            ).classes('w-full mt-2').props('flat color=gray')