import flet as ft
from utils.services.indicadores_service import listar_indicadores
from utils.services.avaliacoes_service import salvar_avaliacao
from database.indicadores import INDICADORES 

def TelaAvaliacao(page: ft.Page, curso, on_voltar):
    
    """
    Tela de Avaliação Institucional.
    
    Fluxo:
    1. Carrega indicadores do banco e organiza por eixo.
    2. Exibe perguntas com critérios de resposta (radio buttons).
    3. Permite navegação entre indicadores e eixos.
    4. Salva respostas no banco ao finalizar.
    
    Parâmetros:
    - page: objeto da página Flet.
    - curso: dicionário com dados do curso avaliado.
    - on_voltar: função callback para retornar à tela anterior.
    """

    # Carrega indicadores do banco
    indicadores_banco = listar_indicadores()
    
    # Estado da tela (controle de navegação e respostas)
    estado = {
        "eixo_atual": 1,
        "indice_atual": 0, 
        "respostas": {}
    }

    # Estrutura dos eixos
    eixos_agrupados = {
        1: {"nome": "Organização Didático-Pedagógica", "indicadores": []},
        2: {"nome": "Corpo Docente e Tutorial", "indicadores": []},
        3: {"nome": "Infraestrutura", "indicadores": []}
    }

    # Mantém ordem original dos indicadores
    ordem_original = [ind["titulo"] for ind in INDICADORES]
    
    def pegar_posicao_original(ind_banco):
        try: return ordem_original.index(ind_banco["nome"])
        except ValueError: return 999 

    # Ordena indicadores conforme ordem original
    indicadores_banco.sort(key=pegar_posicao_original)

    # Distribui indicadores nos eixos
    for ind in indicadores_banco:
        eixo_num = ind.get("eixo", 1)
        if eixo_num in eixos_agrupados:
            eixos_agrupados[eixo_num]["indicadores"].append(ind)

    # Adiciona numeração exibida (ex: 1.1, 2.3 etc.)
    for eixo_num, dados in eixos_agrupados.items():
        for i, ind in enumerate(dados["indicadores"]):
            ind["numero_exibicao"] = f"{eixo_num}.{i + 1}"

    # --- CONTROLES DE NAVEGAÇÃO ---
    botoes_abas = ft.Row(alignment=ft.MainAxisAlignment.END, spacing=5)
    
    slider_progresso = ft.Slider(
        min=1, max=10, value=1, divisions=9, 
        active_color="blue700", inactive_color="grey300",
        label="Indicador {value}", expand=True 
    )
    texto_progresso = ft.Text(size=12, color="grey700", weight="bold")
    
    def pular_pelo_slider(e):
        novo_indice = int(e.control.value) - 1 
        if estado["indice_atual"] != novo_indice:
            estado["indice_atual"] = novo_indice
            atualizar_tela()

    slider_progresso.on_change = pular_pelo_slider

    container_progresso = ft.Row([
        slider_progresso,
        texto_progresso
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    area_pergunta = ft.Container(expand=True)
    
    # Botões de navegação
    btn_voltar = ft.ElevatedButton("Anterior", icon=ft.Icons.ARROW_BACK, height=35)
    btn_avancar = ft.ElevatedButton("Avançar", icon=ft.Icons.ARROW_FORWARD, height=35, style=ft.ButtonStyle(bgcolor="blue700", color="white"))
    btn_finalizar = ft.ElevatedButton("Finalizar", icon=ft.Icons.CHECK, height=35, style=ft.ButtonStyle(bgcolor="green700", color="white"), visible=False)

    # --- FUNÇÃO PRINCIPAL DE ATUALIZAÇÃO ---
    def atualizar_tela():
        eixo_id = estado["eixo_atual"]
        idx = estado["indice_atual"]
        
        lista_atual = eixos_agrupados[eixo_id]["indicadores"]
        if not lista_atual: return

        ind_atual = lista_atual[idx]
        total_eixo = len(lista_atual)

        # Atualiza abas de eixos
        botoes_abas.controls.clear()
        for e_id in [1, 2, 3]:
            is_ativo = (e_id == eixo_id)
            botoes_abas.controls.append(
                ft.ElevatedButton(
                    f"Eixo {e_id}",
                    height=28,
                    style=ft.ButtonStyle(
                        bgcolor="blue700" if is_ativo else "grey200", 
                        color="white" if is_ativo else "black"
                    ),
                    on_click=lambda e, id_eixo=e_id: mudar_eixo(id_eixo)
                )
            )

        # Atualiza slider de progresso
        if total_eixo > 1:
            slider_progresso.max = total_eixo
            slider_progresso.divisions = total_eixo - 1
            slider_progresso.value = idx + 1
            slider_progresso.disabled = False
        else:
            slider_progresso.max = 1
            slider_progresso.divisions = 1
            slider_progresso.value = 1
            slider_progresso.disabled = True

        texto_progresso.value = f"{idx + 1} / {total_eixo}"

        # Opções de resposta (radio buttons)
        coluna_opcoes = ft.Column(spacing=4)
        
        def salvar_resposta(valor):
            estado["respostas"][ind_atual["id"]] = valor
            atualizar_tela()

        grupo_radios = ft.RadioGroup(
            content=coluna_opcoes,
            value=estado["respostas"].get(ind_atual["id"]),
            on_change=lambda e: salvar_resposta(e.control.value)
        )

        criterios = ind_atual.get("criterios", {})
        criterios_ordenados = sorted(criterios.items(), key=lambda item: int(item[0]))

        for nota, texto in criterios_ordenados:
            def click_caixa(e, n=str(nota)):
                grupo_radios.value = n
                salvar_resposta(n)

            coluna_opcoes.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Radio(value=str(nota)),
                        ft.Text(texto, expand=True, size=13)
                    ], vertical_alignment=ft.CrossAxisAlignment.START),
                    padding=8,
                    bgcolor="grey50",
                    border_radius=8,
                    on_click=click_caixa
                )
            )

        # Descrição do indicador
        desc_texto = ind_atual.get("descricao", "")
        descricao_ui = ft.Text(desc_texto, size=12, color="grey600", italic=True) if desc_texto else ft.Container()

        # Monta área da pergunta
        area_pergunta.content = ft.Container(
            padding=0, 
            content=ft.Column([
                ft.Text(eixos_agrupados[eixo_id]["nome"], size=12, color="blue700", weight="bold"),
                ft.Text(f"{ind_atual['numero_exibicao']}. {ind_atual.get('nome', '')}", size=16, weight="bold"),
                descricao_ui,
                grupo_radios
            ], spacing=2)
        )

        # Controle de botões
        btn_voltar.disabled = (eixo_id == 1 and idx == 0)
        is_ultimo_indicador = (eixo_id == 3 and idx == len(eixos_agrupados[3]["indicadores"]) - 1)
        btn_avancar.visible = not is_ultimo_indicador
        btn_finalizar.visible = is_ultimo_indicador

        page.update()

    # --- FUNÇÕES DE NAVEGAÇÃO ---
    def mudar_eixo(novo_eixo):
        estado["eixo_atual"] = novo_eixo
        estado["indice_atual"] = 0
        atualizar_tela()

    def avancar_click(e):
        eixo_id = estado["eixo_atual"]
        idx = estado["indice_atual"]
        total_eixo = len(eixos_agrupados[eixo_id]["indicadores"])
        
        # Caso final -> salvar avaliação
        if eixo_id == 3 and idx == total_eixo - 1:
            btn_finalizar.disabled = True
            page.update()
            
            sucesso = salvar_avaliacao(curso["id"], curso["nome"], estado["respostas"])
            if sucesso:
                page.snack_bar = ft.SnackBar(ft.Text("Avaliação registrada com sucesso!"), bgcolor="green700")
                page.snack_bar.open = True
                on_voltar()
            else:
                btn_finalizar.disabled = False
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar avaliação."), bgcolor="red700")
                page.snack_bar.open = True
                page.update()
            return

        # Avança dentro do eixo ou para o próximo eixo
        if idx < total_eixo - 1:
            estado["indice_atual"] += 1
        else:
            estado["eixo_atual"] += 1
            # Define o índice inicial como 0 e atualiza a tela
            estado["indice_atual"] = 0
            atualizar_tela()

            # Função chamada ao clicar no botão "Voltar"
            def voltar_click(e):
                idx = estado["indice_atual"]
                if idx > 0:
                    # Se ainda há perguntas anteriores no mesmo eixo, apenas decrementa o índice
                    estado["indice_atual"] -= 1
                else:
                    # Caso contrário, volta para o eixo anterior e posiciona no último indicador dele
                    estado["eixo_atual"] -= 1
                    estado["indice_atual"] = len(eixos_agrupados[estado["eixo_atual"]]["indicadores"]) - 1
                atualizar_tela()

            # Ambos os botões "Avançar" e "Finalizar" disparam a mesma função
            # O código interno decide se deve salvar ou avançar
            btn_avancar.on_click = avancar_click
            btn_finalizar.on_click = avancar_click
            btn_voltar.on_click = voltar_click

            # Atualiza a tela inicial
            atualizar_tela()

            # Estrutura principal da tela
            return ft.Column([
                # Cabeçalho com nome do curso e abas de navegação
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"Avaliando: {curso.get('nome')}", size=16, weight="bold"),
                            botoes_abas
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        container_progresso  # Barra de progresso
                    ], spacing=0),
                    padding=10
                ),

                # Linha divisória
                ft.Divider(height=1, color="grey300"),
                
                # Área da pergunta com scroll automático
                ft.Container(
                    content=ft.Column([
                        area_pergunta
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=10,
                    expand=True 
                ),
                
                # Linha divisória
                ft.Divider(height=1, color="grey300"),
                
                # Rodapé com botões de ação
                ft.Container(
                    padding=10,
                    bgcolor="white",
                    content=ft.Row(
                        controls=[
                            # Botão cancelar volta para a tela anterior
                            ft.TextButton("Cancelar", icon=ft.Icons.CANCEL, icon_color="red", height=35, on_click=lambda _: on_voltar()),
                            
                            # Botões de navegação (Voltar, Avançar e Finalizar)
                            ft.Row([btn_voltar, btn_avancar, btn_finalizar]) 
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
            ], expand=True, spacing=0)
