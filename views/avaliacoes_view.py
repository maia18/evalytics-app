import flet as ft
from services.indicadores_service import listar_indicadores
from services.avaliacoes_service import salvar_avaliacao

def TelaAvaliacao(page: ft.Page, curso, on_voltar):
    
    indicadores = listar_indicadores()
    total_indicadores = len(indicadores)
    
    # Variáveis de Estado para controlar em qual passo estamos e as respostas
    estado = {
        "indice": 0,
        "respostas": {}
    }
    
    # --- COMPONENTES DO CABEÇALHO ---
    texto_eixo = ft.Text(size=20, weight="bold", color="blue700")
    texto_progresso = ft.Text(size=12, color="grey700")
    barra_progresso = ft.ProgressBar(value=0, color="blue700", bgcolor="grey200", height=8)
    
    # --- COMPONENTES DO CORPO DA PERGUNTA ---
    titulo_indicador = ft.Text(size=18, weight="bold")
    desc_indicador = ft.Text(size=14, color="grey600", italic=True)
    
    # O container onde vamos injetar as opções de 1 a 5 com os textos completos
    coluna_opcoes = ft.Column(spacing=15)
    grupo_radios = ft.RadioGroup(content=coluna_opcoes)
    
    # --- BOTÕES DE AÇÃO ---
    btn_cancelar = ft.TextButton("Cancelar Avaliação", icon=ft.Icons.CANCEL, icon_color="red", on_click=lambda _: on_voltar())
    btn_voltar = ft.ElevatedButton("Anterior", icon=ft.Icons.ARROW_BACK, disabled=True)
    btn_avancar = ft.ElevatedButton("Avançar", icon=ft.Icons.ARROW_FORWARD, style=ft.ButtonStyle(bgcolor="blue700", color="white"))

    # --- FUNÇÃO CENTRAL QUE DESENHA A TELA ATUAL ---
    def atualizar_interface():
        ind = indicadores[estado["indice"]]
        
        # 1. Atualiza Textos e Progresso
        texto_eixo.value = f"Eixo {ind.get('eixo', '')}: {ind.get('categoria', '')}"
        texto_progresso.value = f"Indicador {estado['indice'] + 1} de {total_indicadores}"
        barra_progresso.value = (estado["indice"] + 1) / total_indicadores
        
        titulo_indicador.value = ind.get("nome", "")
        desc_indicador.value = ind.get("descricao", "")
        desc_indicador.visible = bool(ind.get("descricao")) # Oculta se não tiver descrição
        
        # 2. Constrói os "Cards" das opções de resposta
        coluna_opcoes.controls.clear()
        criterios = ind.get("criterios", {})
        
        # A MÁGICA DA ORDENAÇÃO: Forçamos o Python a ordenar as chaves como números (1, 2, 3, 4, 5)
        criterios_ordenados = sorted(criterios.items(), key=lambda item: int(item[0]))
        
        for nota, texto in criterios_ordenados:
            coluna_opcoes.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Radio(value=str(nota)),
                        ft.Text(f"Nota {nota}:\n{texto}", expand=True, size=14)
                    ], vertical_alignment=ft.CrossAxisAlignment.START),
                    padding=15,
                    bgcolor="grey50",
                    border_radius=8,
                    on_hover=lambda e: e.control.update()
                )
            )
            
        # # Opção Não Se Aplica (NSA)
        # coluna_opcoes.controls.append(
        #     ft.Container(
        #         content=ft.Row([
        #             ft.Radio(value="NSA"),
        #             ft.Text("Não se aplica (NSA)", expand=True, size=14, weight="bold")
        #         ]),
        #         padding=15, 
                
        #         # A CORREÇÃO ESTÁ AQUI TAMBÉM
        #         bgcolor="grey50", 
        #         border_radius=8
        #     )
        # )
        
        # 3. Restaura a resposta se o usuário já tiver respondido e voltado a página
        grupo_radios.value = estado["respostas"].get(ind["id"], None)
        
        # 4. Atualiza os botões do rodapé
        btn_voltar.disabled = estado["indice"] == 0
        if estado["indice"] == total_indicadores - 1:
            btn_avancar.text = "Finalizar Avaliação"
            btn_avancar.icon = ft.Icons.CHECK
            btn_avancar.style = ft.ButtonStyle(bgcolor="green700", color="white")
        else:
            btn_avancar.text = "Avançar"
            btn_avancar.icon = ft.Icons.ARROW_FORWARD
            btn_avancar.style = ft.ButtonStyle(bgcolor="blue700", color="white")
            
        page.update()

    # --- FUNÇÕES DE NAVEGAÇÃO ---
    def avancar_click(e):
        ind_id = indicadores[estado["indice"]]["id"]
        
        # Validação: Obriga a responder antes de avançar
        if not grupo_radios.value:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione uma opção antes de avançar!"), bgcolor="red700")
            page.snack_bar.open = True
            page.update()
            return
            
        # Salva a resposta na memória
        estado["respostas"][ind_id] = grupo_radios.value
        
        # Se for o último, finaliza e salva no Firebase
        if estado["indice"] == total_indicadores - 1:
            btn_avancar.disabled = True
            page.update()
            
            sucesso = salvar_avaliacao(curso["id"], curso["nome"], estado["respostas"])
            
            if sucesso:
                page.snack_bar = ft.SnackBar(ft.Text("Avaliação salva com sucesso!"), bgcolor="green700")
                page.snack_bar.open = True
                on_voltar()
            else:
                btn_avancar.disabled = False
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar. Verifique o terminal."), bgcolor="red700")
                page.snack_bar.open = True
                page.update()
        else:
            # Apenas avança para a próxima pergunta
            estado["indice"] += 1
            atualizar_interface()

    def voltar_click(e):
        if estado["indice"] > 0:
            estado["indice"] -= 1
            atualizar_interface()

    # Conecta as funções aos botões
    btn_avancar.on_click = avancar_click
    btn_voltar.on_click = voltar_click

    # --- MONTAGEM DO LAYOUT PRINCIPAL (Semelhante ao Mockup) ---
    cartao_principal = ft.Card(
        elevation=2,
        content=ft.Container(
            padding=40,
            content=ft.Column([
                # Cabeçalho
                texto_eixo,
                ft.Row([barra_progresso], expand=True), # Força a barra a ocupar a largura toda
                ft.Row([texto_progresso], alignment=ft.MainAxisAlignment.END),
                ft.Divider(height=20, color="transparent"),
                
                # Pergunta
                titulo_indicador,
                desc_indicador,
                ft.Divider(height=10, color="transparent"),
                
                # Opções de Resposta
                grupo_radios,
                
                ft.Divider(height=20, color="transparent"),
                
                # Rodapé de Navegação
                ft.Row([
                    btn_cancelar,
                    ft.Row([btn_voltar, btn_avancar])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                
            ])
        )
    )

    # Inicia a tela desenhando a primeira pergunta
    if total_indicadores > 0:
        atualizar_interface()
    else:
        cartao_principal.content = ft.Text("Nenhum indicador cadastrado no sistema.", color="red")

    # Retorna o container centralizado
    return ft.Container(
        content=ft.Column([
            ft.Text(f"Avaliando: {curso.get('nome')}", size=24, weight="bold"),
            cartao_principal
        ], expand=True, scroll=ft.ScrollMode.AUTO),
        expand=True
    )