from nicegui import ui
from database.supabase_client import supabase
from services.avaliacao_session import session
from components.avaliacao.card_indicador import card_indicador

@ui.page('/avaliacao')
def pagina_avaliacao():
    # Proteção de rota: garante que a avaliação foi iniciada
    if not session.professor_id or not session.disciplina_id:
        ui.navigate.to('/nova_avaliacao') # Ajuste para sua rota de início
        ui.notify("Inicie uma avaliação antes de prosseguir.", type='warning')
        return

    renderizar_fluxo()

@ui.refreshable
def renderizar_fluxo():
    """
    Renderiza a interface buscando os dados diretamente do Supabase
    baseado no estado atual da sessão (session.eixo_atual e session.indice_indicador).
    """
    # 1. Busca os dados do Eixo Atual
    eixo_res = supabase.table('eixos').select('*').eq('id', session.eixo_atual).execute()
    if not eixo_res.data:
        ui.notify(f"Erro: Eixo {session.eixo_atual} não encontrado.", type='negative')
        return
    eixo_dados = eixo_res.data[0]

    # 2. Busca os Indicadores do Eixo Atual
    ind_res = supabase.table('indicadores').select('*').eq('eixo_id', session.eixo_atual).order('ordem').execute()
    indicadores = ind_res.data

    if not indicadores:
        ui.notify("Nenhum indicador cadastrado para este eixo.", type='warning')
        return

    total_indicadores = len(indicadores)
    indicador_atual = indicadores[session.indice_indicador]

    # Layout Centralizado
    with ui.column().classes('w-full max-w-4xl mx-auto p-4 gap-6'):
        
        # Cabeçalho do Eixo
        with ui.column().classes('w-full gap-1'):
            ui.label(f'Eixo {session.eixo_atual}: {eixo_dados["nome"]}').classes('text-2xl font-bold text-primary')
            if eixo_dados.get("descricao"):
                ui.label(eixo_dados["descricao"]).classes('text-gray-600')

        # Progresso
        progresso_valor = (session.indice_indicador + 1) / total_indicadores
        ui.linear_progress(progresso_valor, show_value=False).classes('w-full h-2 rounded-full')
        ui.label(f'Indicador {session.indice_indicador + 1} de {total_indicadores}').classes('text-sm text-gray-500 self-end')

        # Renderização do Card do Indicador Atual
        resposta_atual = session.get_resposta(indicador_atual['id'])
        
        # Callback para injetar a resposta na sessão em tempo real
        def atualizar_sessao(nota, comentario):
            session.salvar_resposta(indicador_atual['id'], nota, comentario)

        card_indicador(indicador_atual, resposta_atual, atualizar_sessao)

        # ======================
        # NAVEGAÇÃO E FINALIZAÇÃO
        # ======================
        with ui.row().classes('w-full justify-between mt-6'):
            
            # Botão Voltar/Cancelar
            if session.eixo_atual == 1 and session.indice_indicador == 0:
                ui.button('Cancelar Avaliação', on_click=lambda: ui.navigate.to('/dashboard'), color='red').props('outline')
            else:
                def acao_voltar():
                    # Lógica para descobrir a quantidade de indicadores do eixo anterior (necessário para o índice correto ao voltar de eixo)
                    if session.indice_indicador == 0 and session.eixo_atual > 1:
                        eixo_ant = session.eixo_atual - 1
                        ant_res = supabase.table('indicadores').select('id').eq('eixo_id', eixo_ant).execute()
                        total_ant = len(ant_res.data)
                        session.retroceder(total_ant)
                    else:
                        session.retroceder()
                    renderizar_fluxo.refresh()
                    
                ui.button('Voltar', on_click=acao_voltar, color='secondary').props('outline')

            # Botão Avançar/Finalizar
            def acao_avancar():
                resp = session.get_resposta(indicador_atual['id'])
                if not resp.get('nota'):
                    ui.notify('Selecione uma nota antes de avançar.', type='warning')
                    return

                acao = session.avancar(total_indicadores)
                
                if acao == "finalizar":
                    finalizar_avaliacao()
                else:
                    renderizar_fluxo.refresh()

            is_ultimo = (session.eixo_atual == session.TOTAL_EIXOS and session.indice_indicador == total_indicadores - 1)
            texto_btn = 'Finalizar Avaliação' if is_ultimo else 'Avançar'
            icone_btn = 'check' if is_ultimo else 'arrow_forward'
            
            ui.button(texto_btn, on_click=acao_avancar, color='primary').props(f'icon-right={icone_btn}').classes('px-6')
            
# ======================
# LÓGICA DE PERSISTÊNCIA NO BANCO
# ======================
def finalizar_avaliacao():
    """
    Cria o registro da avaliação e envia todas as respostas para o Supabase.
    """
    try:
        # 1. Cria o registro "Mãe" da avaliação
        aval_payload = {
            'professor_id': session.professor_id,
            'disciplina_id': session.disciplina_id,
            'status': 'concluida'
            # 'completed_at' será preenchido automaticamente pelo banco caso você prefira, ou podemos enviar datetime.now().isoformat()
        }
        aval_res = supabase.table('avaliacoes').insert(aval_payload).execute()
        avaliacao_id = aval_res.data[0]['id']

        # 2. Prepara o batch (lote) de respostas para inserir de uma vez
        respostas_batch = []
        for ind_id, dados in session.respostas.items():
            respostas_batch.append({
                'avaliacao_id': avaliacao_id,
                'indicador_id': ind_id,
                'nota': dados['nota'],
                'comentario': dados['comentario']
            })
        
        # 3. Insere todas as respostas
        if respostas_batch:
            supabase.table('respostas').insert(respostas_batch).execute()

        # 4. Limpa a sessão e redireciona
        ui.notify('Avaliação concluída e salva com sucesso!', type='positive', position='top')
        session.reset()
        ui.navigate.to('/dashboard')

    except Exception as e:
        ui.notify(f"Erro ao salvar avaliação: {str(e)}", type='negative', position='top')
        print(f"Erro detalhado (Supabase): {e}")