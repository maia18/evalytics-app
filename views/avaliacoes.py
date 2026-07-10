import flet as ft
import json
from database.indicadores import INDICADORES

def ViewAvaliacoes(page: ft.Page, mudar_tela):
    
    # === 1. SIDEBAR (MENU LATERAL) ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        alignment=ft.alignment.Alignment(-1, 0) 
    )

    sidebar = ft.Container(
        width=260,
        bgcolor="blue900",
        padding=20,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ANALYTICS, color="white", size=32),
                        ft.Text("Evalytics", size=24, weight="bold", color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(color="white24", height=30),
                ft.TextButton("Dashboard", on_click=lambda _: mudar_tela("/dashboard"), style=estilo_botao_menu),
            ]
        )
    )
    
    # === 2. ESTADO AUXILIAR DA TELA ===
    pasta_aberta_atualmente = {"titulo": "", "eixo": 0}
    item_alvo_acao = {} # Guarda qual item clicamos para editar ou excluir

    # === 3. LÓGICA DO MODAL: EDIÇÃO (LÁPIS) ===
    def fechar_modal_edicao(e):
        modal_edicao.open = False
        page.update()

    def salvar_edicao(e):
        fechar_modal_edicao(e)
        page.snack_bar = ft.SnackBar(ft.Text("Melhoria registrada com sucesso!", color="green"))
        page.snack_bar.open = True
        page.update()

    modal_edicao = ft.AlertDialog(
        title=ft.Text("Corrigir / Melhorar Indicador", size=18, weight="bold"),
        content=ft.Column(
            width=500,
            height=280,
            spacing=15,
            controls=[
                ft.Text("Descreva a falha encontrada ou nova melhoria:", size=14, weight="bold"),
                ft.TextField(multiline=True, min_lines=2, max_lines=2, border_color="blue200"),
                ft.Text("Justificativa / Plano de Ação:", size=14, weight="bold"),
                ft.TextField(multiline=True, min_lines=3, max_lines=3, border_color="blue200"),
            ]
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal_edicao, style=ft.ButtonStyle(color="red")),
            ft.ElevatedButton("Salvar Alterações", bgcolor="blue700", color="white", on_click=salvar_edicao)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal_edicao(e):
        if modal_edicao not in page.overlay:
            page.overlay.append(modal_edicao)
        modal_edicao.open = True
        page.update()


    # === 4. LÓGICA DO MODAL: EXCLUSÃO (LIXEIRA) ===
    def fechar_modal_exclusao(e):
        modal_exclusao.open = False
        page.update()

    def confirmar_exclusao(e):
        # 1. Remove da memória procurando pelo título exato
        for idx, item in enumerate(INDICADORES):
            if item["titulo"] == item_alvo_acao["titulo"] and item["eixo"] == item_alvo_acao["eixo"]:
                INDICADORES.pop(idx)
                break
        
        # 2. Atualiza o arquivo físico indicadores.py
        try:
            with open("database/indicadores.py", "w", encoding="utf-8") as f:
                lista_em_texto = json.dumps(INDICADORES, indent=4, ensure_ascii=False)
                f.write(f"INDICADORES = {lista_em_texto}\n")
        except Exception as erro:
            print(f"Erro ao apagar no arquivo: {erro}")
            
        fechar_modal_exclusao(e)
        page.snack_bar = ft.SnackBar(ft.Text("Indicador removido permanentemente!", color="red700"))
        page.snack_bar.open = True
        
        # 3. Atualiza a tela
        abrir_pasta(pasta_aberta_atualmente["titulo"])

    modal_exclusao = ft.AlertDialog(
        title=ft.Text("Confirmar Exclusão", size=18, weight="bold", color="red700"),
        content=ft.Text("Tem certeza que deseja apagar este indicador? Esta ação será salva no arquivo físico e não pode ser desfeita."),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal_exclusao, style=ft.ButtonStyle(color="black54")),
            ft.ElevatedButton("Sim, Excluir", bgcolor="red700", color="white", on_click=confirmar_exclusao)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def preparar_exclusao(item):
        item_alvo_acao.clear()
        item_alvo_acao.update(item)
        if modal_exclusao not in page.overlay:
            page.overlay.append(modal_exclusao)
        modal_exclusao.open = True
        page.update()


    # === 5. LÓGICA DO MODAL: NOVO INDICADOR (BOTÃO AZUL) ===
    campo_titulo = ft.TextField(label="Título do Indicador", border_color="blue200")
    campo_descricao = ft.TextField(label="Descrição / Observação (Opcional)", multiline=True, min_lines=2, border_color="blue200")
    
    def fechar_modal_novo(e):
        modal_novo.open = False
        page.update()

    def salvar_novo(e):
        novo_item = {
            "titulo": campo_titulo.value,
            "eixo": pasta_aberta_atualmente["eixo"],
            "descricao": campo_descricao.value,
            "status": "ATIVO", 
            "criterios": {1: "", 2: "", 3: "", 4: "", 5: ""}
        }
        
        # LÓGICA DE ORGANIZAÇÃO: Encontra o último item do eixo atual
        eixo_atual = pasta_aberta_atualmente["eixo"]
        indice_insercao = len(INDICADORES) # Padrão: joga pro final se não achar nada
        
        # Percorre a lista de trás para frente (reverse) para achar o último do mesmo eixo
        for i in range(len(INDICADORES) - 1, -1, -1):
            if INDICADORES[i].get("eixo") == eixo_atual:
                indice_insercao = i + 1 # A posição exata para inserir é logo após ele
                break
                
        # Insere na posição calculada em vez de jogar no final
        INDICADORES.insert(indice_insercao, novo_item)
        
        # Atualiza o arquivo físico
        try:
            with open("database/indicadores.py", "w", encoding="utf-8") as f:
                lista_em_texto = json.dumps(INDICADORES, indent=4, ensure_ascii=False)
                f.write(f"INDICADORES = {lista_em_texto}\n")
        except Exception as erro:
            print(f"Erro ao salvar no arquivo: {erro}")
        
        # Limpa os campos
        campo_titulo.value = ""
        campo_descricao.value = ""
        
        # Fecha e notifica
        fechar_modal_novo(e)
        page.snack_bar = ft.SnackBar(ft.Text("Novo indicador salvo e organizado no arquivo!", color="green"))
        page.snack_bar.open = True
        
        # Atualiza a tela
        abrir_pasta(pasta_aberta_atualmente["titulo"])
        
    modal_novo = ft.AlertDialog(
        title=ft.Text("Adicionar Novo Indicador", size=18, weight="bold"),
        content=ft.Column(
            width=500,
            height=200,
            spacing=15,
            controls=[campo_titulo, campo_descricao]
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal_novo, style=ft.ButtonStyle(color="red")),
            ft.ElevatedButton("Salvar Indicador", bgcolor="blue700", color="white", on_click=salvar_novo)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal_novo(e):
        if modal_novo not in page.overlay:
            page.overlay.append(modal_novo)
        modal_novo.open = True
        page.update()


    # === 6. TELA SECUNDÁRIA: LISTA DE INDICADORES ===
    def criar_linha_indicador(item, status):
        cor_fundo_status = "green600" if status == "ATIVO" else ("red600" if status == "FALHA" else "amber600")
        
        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=8,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(item["titulo"], size=15, weight="w500", color="black87", expand=True),
                    ft.Container(
                        bgcolor=cor_fundo_status, padding=5, border_radius=4,
                        content=ft.Text(status, size=12, color="white", weight="bold")
                    ),
                    # Agrupamos os botões de Editar e Excluir
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Adicionar Correção", on_click=abrir_modal_edicao),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color="red700", tooltip="Excluir", on_click=lambda e: preparar_exclusao(item))
                    ])
                ]
            )
        )

    def abrir_pasta(titulo_pasta):
        mapa_eixos = {
            "Organização Didático-Pedagógica": 1,
            "Corpo Docente e Tutorial": 2,
            "Infraestrutura": 3
        }
        eixo_id = mapa_eixos.get(titulo_pasta)
        
        pasta_aberta_atualmente["titulo"] = titulo_pasta
        pasta_aberta_atualmente["eixo"] = eixo_id
        
        lista_da_pasta = [item for item in INDICADORES if item.get("eixo") == eixo_id]
        
        controles_lista = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas()),
                        ft.Text(titulo_pasta, size=22, weight="bold", color="black87")
                    ]),
                    ft.ElevatedButton(
                        "Novo Indicador",
                        icon=ft.Icons.ADD,
                        bgcolor="blue700",
                        color="white",
                        height=40,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                        on_click=abrir_modal_novo 
                    )
                ]
            ),
            ft.Divider(height=20, color="transparent")
        ]
        
        for item in lista_da_pasta:
            status_visual = item.get("status", "ATIVO")
            controles_lista.append(criar_linha_indicador(item, status_visual))
            
        area_conteudo.content = ft.Column(
            expand=True, 
            spacing=15, 
            controls=controles_lista,
            scroll=ft.ScrollMode.AUTO
        )
        page.update()

    def voltar_para_pastas():
        qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
        qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
        qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)
        
        layout_pastas.controls[1].controls[0] = criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1)
        layout_pastas.controls[1].controls[1] = criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2)
        layout_pastas.controls[1].controls[2] = criar_pasta_indicador("Infraestrutura", qtd_eixo_3)

        area_conteudo.content = layout_pastas
        page.update()

    # === 7. TELA INICIAL: PASTAS (EIXOS) ===
    def criar_pasta_indicador(titulo_pasta, qtd_indicadores):
        return ft.Container(
            bgcolor="#F4F6F9",
            border_radius=8,
            padding=20,
            ink=True,
            on_click=lambda e: abrir_pasta(titulo_pasta),
            content=ft.Row(
                spacing=15,
                controls=[
                    ft.Icon(ft.Icons.FOLDER, color="blue700", size=28),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(titulo_pasta, size=16, weight="bold", color="black87"),
                            ft.Text(f"{qtd_indicadores} indicadores", size=13, color="black54"),
                        ]
                    )
                ]
            )
        )

    qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
    qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
    qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)

    layout_pastas = ft.Column(
        expand=True,
        spacing=25,
        controls=[
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color="black87"),
            ft.Column(
                spacing=15,
                controls=[
                    criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1),
                    criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2),
                    criar_pasta_indicador("Infraestrutura", qtd_eixo_3),
                ]
            )
        ]
    )

    # === 8. MONTAGEM DA ESTRUTURA FINAL ===
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="white",
        content=layout_pastas 
    )

    return ft.View(
        route="/avaliacoes",
        padding=0,
        bgcolor="white",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    sidebar,
                    area_conteudo
                ]
            )
        ]
    )
