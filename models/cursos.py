""" Importações """  
import flet as ft
from database.conexao import adicionar_curso_db, obter_cursos_db, atualizar_curso_db, excluir_curso_db 

def ViewCursos(page: ft.Page, mudar_tela):
    
    """
    Tela de gerenciamento de cursos.
    Permite cadastrar, editar e excluir cursos integrados ao banco Firebase.
    """
    
    # === 1. CAMPOS DE FORMULÁRIO (Adicionar e Editar) ===
    
    # Campos para adicionar novo curso
    campo_nome = ft.TextField(label="Nome do Curso", border_color="blue200", dense=True)
    campo_departamento = ft.TextField(label="Departamento", border_color="blue200", dense=True)
    campo_coordenador = ft.TextField(label="Coordenador Responsável", border_color="blue200", dense=True)

    # Campos para edição de curso existente
    campo_edit_nome = ft.TextField(label="Nome do Curso", border_color="blue200", dense=True)
    campo_edit_departamento = ft.TextField(label="Departamento", border_color="blue200", dense=True)
    campo_edit_coordenador = ft.TextField(label="Coordenador Responsável", border_color="blue200", dense=True)

    # Estado auxiliar para guardar linha em edição e ID do documento no Firebase
    estado = {"linha_atual": None, "id_firebase": None}

    # === 2. FUNÇÕES DE CRIAÇÃO DE LINHAS E AÇÕES ===
    def criar_linha_curso(doc_id, codigo, nome_val, depto_val, coord_val):
        
        """
        Cria uma linha da tabela com dados do curso.
        Inclui botões de editar e excluir que interagem com o banco.
        """
        
        txt_codigo = ft.Text(codigo, color="green" if codigo == "NOVO" else "black", weight="bold")
        txt_nome = ft.Text(nome_val, weight="bold")
        txt_depto = ft.Text(depto_val)
        txt_coord = ft.Text(coord_val)

        linha = ft.DataRow(
            cells=[
                ft.DataCell(txt_codigo),
                ft.DataCell(txt_nome),
                ft.DataCell(txt_depto),
                ft.DataCell(txt_coord),
                ft.DataCell(ft.Row()) # célula reservada para ações
            ]
        )
        
        # Ação de excluir curso
        def acao_deletar(e):
            sucesso = excluir_curso_db(doc_id)  # remove do banco
            if sucesso:
                tabela_cursos.rows.remove(linha) # remove da tabela
                page.update()
                
        # Ação de editar curso
        def acao_editar(e):
            # Preenche campos de edição com valores atuais
            campo_edit_nome.value = txt_nome.value
            campo_edit_departamento.value = txt_depto.value
            campo_edit_coordenador.value = txt_coord.value
            
            # Guarda referência da linha e ID do documento
            estado["linha_atual"] = linha
            estado["id_firebase"] = doc_id
            
            if modal_editar not in page.overlay:
                page.overlay.append(modal_editar)
            modal_editar.open = True
            page.update()
        
        # Botões de ação na última célula
        linha.cells[4].content = ft.Row([
            ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Editar", on_click=acao_editar),
            ft.IconButton(icon=ft.Icons.DELETE, icon_color="red700", tooltip="Excluir", on_click=acao_deletar)
        ])
        
        return linha

    # === 3. TABELA DE CURSOS (Inicialmente vazia) ===
    
    tabela_cursos = ft.DataTable(
        heading_row_color="blue50",
        columns=[
            ft.DataColumn(ft.Text("Código", weight="bold")),
            ft.DataColumn(ft.Text("Nome do Curso", weight="bold")),
            ft.DataColumn(ft.Text("Departamento", weight="bold")),
            ft.DataColumn(ft.Text("Coordenador", weight="bold")),
            ft.DataColumn(ft.Text("Ações", weight="bold")),
        ],
        rows=[],
    )

    # === 4. CARREGAR CURSOS DO BANCO ===
    def carregar_cursos_iniciais():
        """
        Busca cursos no Firebase e popula a tabela.
        """
        cursos_do_banco = obter_cursos_db()
        tabela_cursos.rows.clear() # limpa linhas antigas
        for c in cursos_do_banco:
            codigo = c.get("codigo", "S/C")
            nome = c.get("nome", "")
            depto = c.get("departamento", "")
            coord = c.get("coordenador", "")
            doc_id = c.get("id")
            nova_linha = criar_linha_curso(doc_id, codigo, nome, depto, coord)
            tabela_cursos.rows.append(nova_linha)
    
    carregar_cursos_iniciais()

    # === 5. FUNÇÕES DE MODAIS ===
    def fechar_modal_add(e):
        modal_adicionar.open = False
        page.update()

    def fechar_modal_edit(e):
        modal_editar.open = False
        page.update()

    def salvar_curso(e):
        """
        Adiciona novo curso ao banco e à tabela.
        """
        nome = campo_nome.value
        depto = campo_departamento.value
        coord = campo_coordenador.value
        codigo_novo = "NOVO"  # placeholder para código

        if nome and depto:
            novo_id = adicionar_curso_db(codigo_novo, nome, depto, coord)
            
            if novo_id:
                nova_linha = criar_linha_curso(novo_id, codigo_novo, nome, depto, coord)
                tabela_cursos.rows.append(nova_linha)
                
                # limpa campos e fecha modal
                campo_nome.value = ""
                campo_departamento.value = ""
                campo_coordenador.value = ""
                fechar_modal_add(e)

    def salvar_edicao(e):
        """
        Atualiza curso no banco e na tabela.
        """
        linha_em_edicao = estado["linha_atual"]
        id_banco = estado["id_firebase"]
        
        nome = campo_edit_nome.value
        depto = campo_edit_departamento.value
        coord = campo_edit_coordenador.value

        if linha_em_edicao and id_banco:
            sucesso = atualizar_curso_db(id_banco, nome, depto, coord)
            
            if sucesso:
                linha_em_edicao.cells[1].content.value = nome
                linha_em_edicao.cells[2].content.value = depto
                linha_em_edicao.cells[3].content.value = coord
                
        fechar_modal_edit(e)

    def abrir_modal_add(e):
        if modal_adicionar not in page.overlay:
            page.overlay.append(modal_adicionar)
        modal_adicionar.open = True
        page.update()

    # === 6. DEFINIÇÃO DOS MODAIS ===
    modal_adicionar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar Novo Curso", size=20, weight="bold"),
        content=ft.Column(width=400, height=220, spacing=15, controls=[campo_nome, campo_departamento, campo_coordenador]),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal_add, style=ft.ButtonStyle(color="red700")),
            ft.ElevatedButton("Salvar", on_click=salvar_curso, bgcolor="blue700", color="white"),
        ],
    )

    modal_editar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Curso", size=20, weight="bold"),
        content=ft.Column(width=400, height=220, spacing=15, controls=[campo_edit_nome, campo_edit_departamento, campo_edit_coordenador]),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal_edit, style=ft.ButtonStyle(color="red700")),
            ft.ElevatedButton("Atualizar", on_click=salvar_edicao, bgcolor="blue700", color="white"),
        ],
    )

    # === 7. SIDEBAR ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        alignment=ft.Alignment(-1, 0) 
    )
    
    def sair(e):
        mudar_tela("/") # Redireciona para tela inicial

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
                ft.TextButton("Visão Geral", icon=ft.Icons.HOME, on_click=lambda _: mudar_tela("/inicio"), style=estilo_botao_menu),
                ft.TextButton("Dashboard", icon=ft.Icons.DASHBOARD, on_click=lambda _: mudar_tela("/dashboard"), style=estilo_botao_menu),
                ft.TextButton("Avaliações", icon=ft.Icons.ASSIGNMENT, on_click=lambda _: mudar_tela("/avaliacoes"), style=estilo_botao_menu),
                ft.TextButton("Relatórios", icon=ft.Icons.PIE_CHART, on_click=lambda _: mudar_tela("/relatorios"), style=estilo_botao_menu),
                ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, on_click=lambda _: mudar_tela("/configuracoes"), style=estilo_botao_menu),
                
                ft.Container(expand=True), 
                
                # Botão de Logout
                ft.TextButton(
                    "Sair do Sistema", 
                    icon=ft.Icons.LOGOUT, 
                    style=estilo_botao_menu,
                    on_click=sair
                )
            ]
        )
    )

    # === 8. CONTEÚDO PRINCIPAL ===
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="#F4F6F9",
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text("Gestão de Cursos", size=28, weight="bold", color="black87"),
                                ft.Text("Adicione, edite ou remova os cursos da instituição.", size=16, color="black54"),
                            ]
                        ),
                        ft.ElevatedButton(
                            "Adicionar Curso", 
                            icon=ft.Icons.ADD, 
                            bgcolor="blue700", 
                            color="white",
                            height=45,
                            on_click=abrir_modal_add # Botão devidamente renomeado!
                        )
                    ]
                ),
                ft.Divider(height=30, color="transparent"),
                
                ft.Container(
                    expand=True,
                    bgcolor="white",
                    border_radius=10,
                    padding=25,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.TextField(
                                prefix_icon=ft.Icons.SEARCH,
                                hint_text="Buscar curso pelo nome...",
                                border_color="blue200",
                                height=45,
                                text_size=14,
                                expand=False
                            ),
                            ft.Divider(height=20, color="transparent"),
                            
                            ft.ListView(
                                expand=True,
                                controls=[
                                    tabela_cursos # Tabela dinâmica de cursos
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    )

    # === RETORNO FINAL DA VIEW ===
    return ft.View(
        route="/cursos",
        padding=0,
        bgcolor="white",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[sidebar, area_conteudo]
            )
        ]
    )