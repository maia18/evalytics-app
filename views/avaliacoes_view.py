import flet as ft
from services.indicadores_service import listar_indicadores
from services.avaliacoes_service import salvar_avaliacao

def TelaAvaliacao(page: ft.Page, curso, on_voltar):
    
    indicadores = listar_indicadores()
    total_indicadores = len(indicadores)
    
    estado = {
        "indice": 0,
        "respostas": {}
    }
    
    # --- CABEÇALHO E BARRA DE NAVEGAÇÃO ---
    texto_eixo = ft.Text(size=20, weight="bold", color="blue700")
    
    # A nova barra de rolagem horizontal com os números
    linha_navegacao = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=10)
    
    # --- CORPO DA PERGUNTA ---
    titulo_indicador = ft.Text(size=18, weight="bold")
    desc_indicador = ft.Text(size=14, color="grey600", italic=True)
    
    coluna_opcoes = ft.Column(spacing=15)
    
    # Salva a resposta automaticamente ao clicar (não depende mais do "Avançar")
    def salvar_resposta(e):
        ind_id = indicadores[estado["indice"]]["id"]
        estado["respostas"][ind_id] = grupo_radios.value
        atualizar_interface() # Atualiza a tela para pintar a "pílula" de verde

    grupo_radios = ft.RadioGroup(content=coluna_opcoes, on_change=salvar_resposta)
    
    # --- BOTÕES DE AÇÃO ---
    btn_cancelar = ft.TextButton("Cancelar Avaliação", icon=ft.Icons.CANCEL, icon_color="red", on_click=lambda _: on_voltar())
    btn_voltar = ft.ElevatedButton("Anterior", icon=ft.Icons.ARROW_BACK)
    btn_avancar = ft.ElevatedButton("Avançar", icon=ft.Icons.ARROW_FORWARD, style=ft.ButtonStyle(bgcolor="blue700", color="white"))

    # Pula direto para a pergunta clicada na barra superior
    def pular_para_indicador(novo_indice):
        estado["indice"] = novo_indice
        atualizar_interface()

    # Truque de UX: Seleciona o rádio clicando na caixa inteira
    def selecionar_caixa(nota_str):
        grupo_radios.value = nota_str
        salvar_resposta(None)

    # --- DESENHA A TELA ATUAL ---
    def atualizar_interface():
        ind = indicadores[estado["indice"]]
        
        # 1. Textos
        texto_eixo.value = f"Eixo {ind.get('eixo', '')}: {ind.get('categoria', '')}"
        titulo_indicador.value = f"{estado['indice'] + 1}. {ind.get('nome', '')}"
        desc_indicador.value = ind.get("descricao", "")
        desc_indicador.visible = bool(ind.get("descricao"))
        
        # 2. Constrói a Barra de Navegação Horizontal Superior
        linha_navegacao.controls.clear()
        for i in range(total_indicadores):
            id_ind_i = indicadores[i]["id"]
            respondido = id_ind_i in estado["respostas"]
            
            # Lógica de cores: Azul (Atual), Verde (Respondido), Cinza (Pendente)
            cor_fundo = "blue700" if i == estado["indice"] else ("green100" if respondido else "grey200")
            cor_texto = "white" if i == estado["indice"] else ("green900" if respondido else "black")
            
            linha_navegacao.controls.append(
                ft.Container(
                    content=ft.Text(str(i + 1), color=cor_texto, weight="bold"),
                    bgcolor=cor_fundo,
                    padding=10, # <-- CORREÇÃO APLICADA AQUI
                    border_radius=20,
                    on_click=lambda e, idx=i: pular_para_indicador(idx) 
                )
            )

        # 3. Constrói as Opções de Resposta
        coluna_opcoes.controls.clear()
        criterios = ind.get("criterios", {})
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
                    # O clique no container seleciona o radio
                    on_click=lambda e, n=str(nota): selecionar_caixa(n) 
                )
            )
            
        # 4. Restaura a resposta marcada ao voltar na página
        grupo_radios.value = estado["respostas"].get(ind["id"], None)
        
        # 5. Atualiza botões
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

    # --- CONTROLES DOS BOTÕES INFERIORES ---
    def avancar_click(e):
        if estado["indice"] == total_indicadores - 1:
            # Botão de Finalizar clicado
            btn_avancar.disabled = True
            page.update()
            
            sucesso = salvar_avaliacao(curso["id"], curso["nome"], estado["respostas"])
            
            if sucesso:
                # Mostra quantas foram respondidas do total
                qtd = len(estado["respostas"])
                page.snack_bar = ft.SnackBar(ft.Text(f"Avaliação salva! ({qtd}/{total_indicadores} respondidas)"), bgcolor="green700")
                page.snack_bar.open = True
                on_voltar()
            else:
                btn_avancar.disabled = False
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar. Verifique o terminal."), bgcolor="red700")
                page.snack_bar.open = True
                page.update()
        else:
            estado["indice"] += 1
            atualizar_interface()

    def voltar_click(e):
        if estado["indice"] > 0:
            estado["indice"] -= 1
            atualizar_interface()

    btn_avancar.on_click = avancar_click
    btn_voltar.on_click = voltar_click

    # --- MONTAGEM DO LAYOUT PRINCIPAL ---
    cartao_principal = ft.Card(
        elevation=2,
        content=ft.Container(
            padding=40,
            content=ft.Column([
                texto_eixo,
                
                # Barra de navegação livre no lugar da barra de progresso rígida
                linha_navegacao,
                ft.Divider(height=20, color="transparent"),
                
                titulo_indicador,
                desc_indicador,
                ft.Divider(height=10, color="transparent"),
                
                grupo_radios,
                
                ft.Divider(height=20, color="transparent"),
                
                ft.Row([
                    btn_cancelar,
                    ft.Row([btn_voltar, btn_avancar])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )
    )

    if total_indicadores > 0:
        atualizar_interface()
    else:
        cartao_principal.content = ft.Text("Nenhum indicador cadastrado.", color="red")

    return ft.Container(
        content=ft.Column([
            ft.Text(f"Avaliando: {curso.get('nome')}", size=24, weight="bold"),
            cartao_principal
        ], expand=True, scroll=ft.ScrollMode.AUTO),
        expand=True
    )