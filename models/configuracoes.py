""" Importações """  
import json
import flet as ft
from components.responsive_layout import ResponsiveLayout
from database.indicadores import INDICADORES

def ViewConfiguracoes(page: ft.Page, mudar_tela):
    
    """
    Tela de Configurações do sistema Evalytics.
    Contém a sidebar de navegação e modais para edição, exclusão e critérios dos indicadores.
    """
    
    # Criar o layout responsivo
    
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Configurações", 
        subtitulo="Gerencie indicadores e critérios de avaliação.", 
        mudar_tela=mudar_tela
    )

    # === 2. ESTADO AUXILIAR DA TELA ===
    # Variáveis auxiliares para controlar qual pasta está aberta e qual item está sendo editado/excluído
    pasta_aberta_atualmente = {"titulo": "", "eixo": 0}    
    # Preparar conteúdo principal para ser adicionado ao layout responsivo    
    item_alvo_acao = {}

    # =====================================================================
    # === 3. LÓGICA DO MODAL: EDIÇÃO DE TÍTULO E DESCRIÇÃO ========
    # =====================================================================
    
    campo_edicao_titulo = ft.TextField(label="Título", min_lines=1, max_lines=2, border_color="blue200")
    campo_edicao_descricao = ft.TextField(label="Descrição / Observação", min_lines=2, max_lines=4, border_color="blue200")

    def fechar_modal_edicao(e):
        modal_edicao.open = False
        page.update()

    def salvar_edicao(e):
        # Atualiza título e descrição do indicador selecionado
        for item in INDICADORES:
            if item["titulo"] == item_alvo_acao["titulo"] and item["eixo"] == item_alvo_acao["eixo"]:
                item["titulo"] = campo_edicao_titulo.value
                item["descricao"] = campo_edicao_descricao.value
                break
            
        # Persiste alterações no arquivo físico
        try:
            with open("database/indicadores.py", "w", encoding="utf-8") as f:
                lista_em_texto = json.dumps(INDICADORES, indent=4, ensure_ascii=False)
                f.write(f"INDICADORES = {lista_em_texto}\n")
        except Exception as erro:
            print(f"Erro ao atualizar o arquivo: {erro}")

        fechar_modal_edicao(e)
        page.snack_bar = ft.SnackBar(ft.Text("Indicador atualizado com sucesso!", color="green"))
        page.snack_bar.open = True
        abrir_pasta(pasta_aberta_atualmente["titulo"])
        
    # Modal de edição
    modal_edicao = ft.AlertDialog(
        title=ft.Text("Editar Título e/ou Descrição", size=20, weight="bold"),
        content=ft.Column(
            width=400,
            height=200,
            spacing=15,
            controls=[campo_edicao_titulo, campo_edicao_descricao]
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal_edicao, style=ft.ButtonStyle(color="red")),
            ft.ElevatedButton("Salvar Alterações", bgcolor="blue700", color="white", on_click=salvar_edicao)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal_edicao(e, item):
        # Preenche campos com dados do item selecionado
        item_alvo_acao.clear()
        item_alvo_acao.update(item)
        campo_edicao_titulo.value = item.get("titulo", "")
        campo_edicao_descricao.value = item.get("descricao", "")
        
        if modal_edicao not in page.overlay:
            page.overlay.append(modal_edicao)
        modal_edicao.open = True
        page.update()

    # =====================================================================
    # === 4. LÓGICA DO MODAL: CRITÉRIOS DE AVALIAÇÃO ===
    # =====================================================================
    
    # Campos para até 5 critérios
    c1 = ft.TextField(label="Critério 1", multiline=True, expand=True, border_color="blue200")
    c2 = ft.TextField(label="Critério 2", multiline=True, expand=True, border_color="blue200")
    c3 = ft.TextField(label="Critério 3", multiline=True, expand=True, border_color="blue200")
    c4 = ft.TextField(label="Critério 4", multiline=True, expand=True, border_color="blue200")
    c5 = ft.TextField(label="Critério 5", multiline=True, expand=True, border_color="blue200")

    def fechar_modal_criterios(e):
        modal_criterios.open = False
        page.update()

    def salvar_criterios(e):
        # Atualiza critérios do indicador selecionado
        for item in INDICADORES:
            if item["titulo"] == item_alvo_acao["titulo"] and item["eixo"] == item_alvo_acao["eixo"]:
                item["criterios"] = {
                    1: c1.value,
                    2: c2.value,
                    3: c3.value,
                    4: c4.value,
                    5: c5.value
                }
                break
            
        # Persiste alterações no arquivo físico
        try:
            with open("database/indicadores.py", "w", encoding="utf-8") as f:
                lista_em_texto = json.dumps(INDICADORES, indent=4, ensure_ascii=False)
                f.write(f"INDICADORES = {lista_em_texto}\n")
        except Exception as erro:
            print(f"Erro ao atualizar critérios no arquivo: {erro}")

        fechar_modal_criterios(e)
        page.snack_bar = ft.SnackBar(ft.Text("Critério(s) atualizado(s) com sucesso!", color="green"))
        page.snack_bar.open = True
        
    # Modal de critérios
    modal_criterios = ft.AlertDialog(
        title=ft.Text("Editar Critérios de Avaliação", size=20, weight="bold"),
        content=ft.Container(
            width=800,
            height=600,
            padding=10, 
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=20,
                controls=[
                    ft.Container(height=5),
                    c1, c2, c3, c4, c5,
                    ft.Container(height=5)
                ]
            )
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal_criterios, style=ft.ButtonStyle(color="red")),
            ft.ElevatedButton("Salvar", bgcolor="blue700", color="white", on_click=salvar_criterios)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal_criterios(e, item):
        # Preenche campos com critérios existentes
        item_alvo_acao.clear()
        item_alvo_acao.update(item)
        
        crit = item.get("criterios", {})
        c1.value = crit.get(1, crit.get("1", ""))
        c2.value = crit.get(2, crit.get("2", ""))
        c3.value = crit.get(3, crit.get("3", ""))
        c4.value = crit.get(4, crit.get("4", ""))
        c5.value = crit.get(5, crit.get("5", ""))
        
        if modal_criterios not in page.overlay:
            page.overlay.append(modal_criterios)
        modal_criterios.open = True
        page.update()


    # =====================================================================
    # === 5. MODAL DE EXCLUSÃO DE INDICADOR ==========================
    # =====================================================================
    
    def fechar_modal_exclusao(e):
        """Fecha o modal de exclusão sem realizar nenhuma ação."""
        modal_exclusao.open = False
        page.update()

    def confirmar_exclusao(e):
        """Remove o indicador selecionado da lista e atualiza o arquivo físico."""
        for idx, item in enumerate(INDICADORES):
            if item["titulo"] == item_alvo_acao["titulo"] and item["eixo"] == item_alvo_acao["eixo"]:
                INDICADORES.pop(idx)
                break
        
        # Persiste a exclusão no arquivo
        try:
            with open("database/indicadores.py", "w", encoding="utf-8") as f:
                lista_em_texto = json.dumps(INDICADORES, indent=4, ensure_ascii=False)
                f.write(f"INDICADORES = {lista_em_texto}\n")
        except Exception as erro:
            print(f"Erro ao apagar no arquivo: {erro}")
            
        fechar_modal_exclusao(e)
        page.snack_bar = ft.SnackBar(ft.Text("Indicador removido permanentemente!", color="red700"))
        page.snack_bar.open = True
        abrir_pasta(pasta_aberta_atualmente["titulo"])

    # Modal de confirmação de exclusão
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
        """Prepara o modal de exclusão com o item selecionado."""
        item_alvo_acao.clear()
        item_alvo_acao.update(item)
        if modal_exclusao not in page.overlay:
            page.overlay.append(modal_exclusao)
        modal_exclusao.open = True
        page.update()


    # =====================================================================
    # === 6. MODAL DE NOVO INDICADOR =================
    # =====================================================================
    
    # Campos de entrada para novo indicador
    campo_titulo = ft.TextField(label="Título do Indicador", border_color="blue200")
    campo_descricao = ft.TextField(label="Descrição / Observação (Opcional)", multiline=True, min_lines=2, border_color="blue200")
    
    def fechar_modal_novo(e):
        # Campos de entrada para novo indicador
        modal_novo.open = False
        page.update()

    def salvar_novo(e):
        """Cria um novo indicador e insere na lista, respeitando o eixo atual."""
        novo_item = {
            "titulo": campo_titulo.value,
            "eixo": pasta_aberta_atualmente["eixo"],
            "descricao": campo_descricao.value,
            "status": "ATIVO", 
            "criterios": {1: "", 2: "", 3: "", 4: "", 5: ""}
        }
        
        # Insere o novo item logo após o último indicador do mesmo eixo
        eixo_atual = pasta_aberta_atualmente["eixo"]
        indice_insercao = len(INDICADORES)
        for i in range(len(INDICADORES) - 1, -1, -1):
            if INDICADORES[i].get("eixo") == eixo_atual:
                indice_insercao = i + 1
                break
                
        INDICADORES.insert(indice_insercao, novo_item)
        
        # Persiste no arquivo físico
        try:
            with open("database/indicadores.py", "w", encoding="utf-8") as f:
                lista_em_texto = json.dumps(INDICADORES, indent=4, ensure_ascii=False)
                f.write(f"INDICADORES = {lista_em_texto}\n")
        except Exception as erro:
            print(f"Erro ao salvar no arquivo: {erro}")
        
        # Limpa campos e fecha modal
        campo_titulo.value = ""
        campo_descricao.value = ""
        
        fechar_modal_novo(e)
        page.snack_bar = ft.SnackBar(ft.Text("Novo indicador salvo e organizado no arquivo!", color="green"))
        page.snack_bar.open = True
        abrir_pasta(pasta_aberta_atualmente["titulo"])

    # Modal de criação de novo indicador
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
        """Abre o modal para adicionar novo indicador."""
        if modal_novo not in page.overlay:
            page.overlay.append(modal_novo)
        modal_novo.open = True
        page.update()
        
    # Área dinâmica onde os indicadores serão renderizados
    area_dinamica_indicadores = ft.Container(expand=True)
    
    # =====================================================================
    # === 7. TELA SECUNDÁRIA: LISTA DE INDICADORES ========================
    # =====================================================================
    
    def criar_linha_indicador(item, status):
        
        """
        Cria uma linha visual para cada indicador da lista.
        Inclui título interativo (abre critérios), status colorido e botões de ação.
        """
        # Define cor de fundo do status conforme valor
        cor_fundo_status = "green600" if status == "ATIVO" else ("red600" if status == "FALHA" else "amber600")
        
        # O título é clicável e abre o modal de critérios
        titulo_interativo = ft.Container(
            content=ft.Text(item["titulo"], size=15, weight="w500", color="blue700"),
            expand=True,
            tooltip="Editar critérios",
            on_click=lambda e, i=item: abrir_modal_criterios(e, i)
        )
        
        # Linha completa com título, status e botões de editar/excluir
        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=8,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    titulo_interativo,
                    ft.Container(
                        bgcolor=cor_fundo_status, padding=5, border_radius=4,
                        content=ft.Text(status, size=12, color="white", weight="bold")
                    ),
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Editar Título", on_click=lambda e, i=item: abrir_modal_edicao(e, i)),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color="red700", tooltip="Excluir", on_click=lambda e: preparar_exclusao(item))
                    ])
                ]
            )
        )

    def abrir_pasta(titulo_pasta):
        
        """
        Abre uma pasta (eixo) e lista todos os indicadores relacionados.
        Também adiciona botão para criar novo indicador.
        """
        
        # Mapeamento dos títulos para IDs de eixo
        mapa_eixos = {
            "Organização Didático-Pedagógica": 1,
            "Corpo Docente e Tutorial": 2,
            "Infraestrutura": 3
        }
        eixo_id = mapa_eixos.get(titulo_pasta)
        
        # Atualiza estado da pasta aberta
        pasta_aberta_atualmente["titulo"] = titulo_pasta
        pasta_aberta_atualmente["eixo"] = eixo_id
        
        # Filtra indicadores do eixo selecionado
        lista_da_pasta = [item for item in INDICADORES if item.get("eixo") == eixo_id]
        
        # Cabeçalho da pasta com botão de voltar e botão de novo indicador
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
        
        # Adiciona cada indicador da pasta à lista
        for item in lista_da_pasta:
            status_visual = item.get("status", "ATIVO")
            controles_lista.append(criar_linha_indicador(item, status_visual))
        
        # Renderiza lista na área de conteúdo
        area_conteudo_aba.content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
            controls=controles_lista
        )
        page.update()

    def voltar_para_pastas():
        
        """
        Volta para a visão geral das pastas (eixos).
        Atualiza a contagem de indicadores em cada pasta.
        """
        
        # Conta indicadores por eixo
        qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
        qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
        qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)
        
        # Atualiza visual das pastas com contagem
        layout_pastas.controls[1].controls[0] = criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1)
        layout_pastas.controls[1].controls[1] = criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2)
        layout_pastas.controls[1].controls[2] = criar_pasta_indicador("Infraestrutura", qtd_eixo_3)

        # Renderiza novamente a visão de pastas
        area_conteudo_aba.content = layout_pastas
        page.update()

    # =====================================================================
    # === 8. TELA INICIAL: PASTAS (EIXOS) =================================
    # =====================================================================
    
    def criar_pasta_indicador(titulo_pasta, qtd_indicadores):
        
        """
        Cria um card visual representando uma pasta (eixo).
        Mostra ícone de pasta, título e quantidade de indicadores.
        Ao clicar, abre a lista de indicadores do eixo.
        """
        
        return ft.Container(
            bgcolor="#F4F6F9",
            border_radius=8,
            padding=20,
            ink=True, # Permite efeito visual de clique
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
        
    # Conta indicadores por eixo para exibir na tela inicial
    qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
    qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
    qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)
    
    # Layout inicial com as pastas (eixos)
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

    # Estado inicial da aba: mostra as pastas
    area_dinamica_indicadores.content = layout_pastas    
    
    # =====================================================================
    # === 9. OUTRAS ABAS: SEGURANÇA E BANCO DE DADOS ======================
    # =====================================================================
    
    # Aba de Segurança
    painel_seguranca = ft.Container(
        padding=20,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Políticas de Segurança", size=18, weight="bold"),
                ft.Divider(color="grey300"),
                ft.Switch(label="Exigir autenticação em duas etapas (2FA) para Administradores", value=True, active_color="blue700"),
                ft.Switch(label="Bloquear acesso após 5 tentativas de login falhas", value=True, active_color="blue700"),
                ft.Switch(label="Registrar logs de auditoria para exclusão de dados", value=True, active_color="blue700"),
                ft.Container(height=10),
                ft.ElevatedButton("Exportar Relatório de Acessos", icon=ft.Icons.SECURITY_UPDATE_WARNING, color="blue700")
            ]
        )
    )
    
    # Aba de Banco de Dados
    painel_banco = ft.Container(
        padding=20,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Gerenciamento de Dados", size=18, weight="bold"),
                ft.Divider(color="grey300"),
                ft.Text("Utilize estas ferramentas para manutenção periódica do sistema.", color="grey700"),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Realizar Backup Completo", icon=ft.Icons.DOWNLOAD, bgcolor="green700", color="white"),
                        ft.ElevatedButton("Otimizar Índices do Firestore", icon=ft.Icons.SPEED, bgcolor="blue700", color="white"),
                    ]
                ),
                ft.Container(height=20),
                ft.Text("Zona de Risco", size=16, color="red700", weight="bold"),
                ft.Container(
                    padding=15,
                    bgcolor="red50",
                    border_radius=8,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Excluir todas as avaliações com mais de 5 anos.", color="red900"),
                            ft.ElevatedButton("Limpar Dados Antigos", icon=ft.Icons.DELETE_FOREVER, bgcolor="red700", color="white")
                        ]
                    )
                )
            ]
        )
    )

    # =====================================================================
    # === 10. SISTEMA DE ABAS CUSTOMIZADO =================================
    # =====================================================================
    
    # Container que troca o conteúdo conforme aba selecionada
    area_conteudo_aba = ft.Container(content=area_dinamica_indicadores, expand=True, padding=20)

    def mudar_aba(e, painel_selecionado):
        
        """
        Alterna entre as abas (Indicadores, Segurança, Banco).
        Atualiza cor de fundo do botão ativo.
        """
        
        area_conteudo_aba.content = painel_selecionado
        btn_indicadores.bgcolor = "blue50" if painel_selecionado == area_dinamica_indicadores else "transparent"
        btn_seguranca.bgcolor = "blue50" if painel_selecionado == painel_seguranca else "transparent"
        btn_banco.bgcolor = "blue50" if painel_selecionado == painel_banco else "transparent"
        page.update()

    # Estilo dos botões de aba
    estilo_btn_aba = ft.ButtonStyle(color={"":"blue900"}, shape=ft.RoundedRectangleBorder(radius=8), padding=15)
    
    # Botões de navegação entre abas
    btn_indicadores = ft.TextButton("Indicadores", icon=ft.Icons.RULE, style=estilo_btn_aba, on_click=lambda e: mudar_aba(e, area_dinamica_indicadores))
    btn_seguranca = ft.TextButton("Segurança", icon=ft.Icons.SECURITY, style=estilo_btn_aba, on_click=lambda e: mudar_aba(e, painel_seguranca))
    btn_banco = ft.TextButton("Banco de Dados", icon=ft.Icons.STORAGE, style=estilo_btn_aba, on_click=lambda e: mudar_aba(e, painel_banco))
    
    # Linha com os botões de abas
    menu_abas = ft.Row([btn_indicadores, btn_seguranca, btn_banco], spacing=10)

    # === CONTEÚDO PARA LAYOUT RESPONSIVO ===
    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Column(
                spacing=5,
                controls=[
                    ft.Text("Configurações do Sistema", size=28, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                    ft.Text("Gerencie indicadores, acessos e manutenção de dados.", size=16, color="grey"),
                ]
            ),
            ft.Divider(height=20, color="transparent"),
            
            ft.Container(
                expand=True,
                bgcolor=layout.COR_CARD,
                border_radius=10,
                padding=20,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
                content=ft.Column(
                    expand=True,
                    controls=[
                        menu_abas,
                        ft.Divider(height=20, color="grey200"),
                        ft.Container(
                            expand=True,
                            padding=10,
                            content=area_conteudo_aba
                        )
                    ]
                )
            )
        ]
    )
    
    # Adicionar conteúdo ao layout
    layout.add_content(conteudo)
    
    # Retorno final da View
    return layout.criar_view("/configuracoes")