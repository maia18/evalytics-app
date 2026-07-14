""" Importações """  
import flet as ft
from components.responsive_layout import ResponsiveLayout
from database.conexao import adicionar_curso_db, obter_cursos_db, atualizar_curso_db, excluir_curso_db 

def ViewCursos(page: ft.Page, mudar_tela):
    
    """
    Tela de gerenciamento de cursos.
    Permite cadastrar, editar e excluir cursos integrados ao banco Firebase.
    """
    
    # Criar o layout responsivo
    
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Gestão de Cursos", 
        subtitulo="Adicione, edite ou remova os cursos da instituição.", 
        mudar_tela=mudar_tela
    )
    
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
                atualizar_interface()
                
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
        heading_row_color="#3C3C3C",
        columns=[
            ft.DataColumn(ft.Text("Código", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Nome do Curso", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Departamento", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Coordenador", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Ações", color="white", weight="bold")),
        ],
        rows=[],
    )
    
    area_tabela = ft.Container(
        alignment=ft.Alignment.CENTER,
        content=tabela_cursos
    )
    
    # Borda do card
    borda_container = ft.Border(
    top=ft.BorderSide(1, layout.COR_BORDA),
    bottom=ft.BorderSide(1, layout.COR_BORDA),
    left=ft.BorderSide(1, layout.COR_BORDA),
    right=ft.BorderSide(1, layout.COR_BORDA),
    )
    
    def criar_stats_card(titulo, controle_valor):
        return ft.Container(
            expand=1,
            padding=15,
            border_radius=8,
            bgcolor=layout.COR_CARD,
            border=borda_container,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Text(titulo, size=12, color="grey"),
                    controle_valor,
                ]
            )
        )
        
    # Adicione isto aqui:
    txt_total = ft.Text(str(len(tabela_cursos.rows)), size=20, weight="bold", color=layout.COR_TEXTO_PRINCIPAL)
    
    # Defina esta variável antes de criar a linha_stats
    txt_depto_card = ft.Text("0", size=20, weight="bold", color=layout.COR_TEXTO_PRINCIPAL)
    
    linha_stats = ft.Row(
        spacing=20,
        controls=[
            criar_stats_card("Total de Cursos", txt_total),
            criar_stats_card(
                "Cursos Ativos", 
                ft.Text(
                    "0", 
                    size=20, 
                    weight="bold", 
                    color=layout.COR_TEXTO_PRINCIPAL
                    )
                ),
            criar_stats_card("Departamentos", txt_depto_card),
        ]
    )
    
    def atualizar_interface():
        txt_total.value = str(len(tabela_cursos.rows)) # Atualiza o total de cursos
        departamentos_unicos = {
            linha.cells[2].content.value.strip()
            for linha in tabela_cursos.rows
            if linha.cells[2].content.value.strip()
        }

        txt_depto_card.value = str(len(departamentos_unicos)) # Atualiza o total de departamentos
    
        area_tabela.content = tabela_cursos if len(tabela_cursos.rows) > 0 else ft.Text("Nenhum curso cadastrado ainda.", color="grey", size=14)
        
        page.update()

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
            
        atualizar_interface()
    
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

        if nome:
            novo_id = adicionar_curso_db(codigo_novo, nome, depto, coord)

            if novo_id:
                nova_linha = criar_linha_curso(
                    novo_id,
                    codigo_novo,
                    nome,
                    depto,
                    coord,
                )
                tabela_cursos.rows.append(nova_linha)

                campo_nome.value = ""
                campo_departamento.value = ""
                campo_coordenador.value = ""

                fechar_modal_add(e)
                atualizar_interface()

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
        
    area_tabela = ft.Container(
        alignment=ft.Alignment.CENTER,
        content=tabela_cursos if len(tabela_cursos.rows) > 0 else ft.Text("Nenhum curso cadastrado ainda.", color="grey", size=14)
    )
    
    # === 2. CONTEÚDO PRINCIPAL (Atualizado) ===
    conteudo = ft.Column(
        expand=True,
        spacing=25,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.ElevatedButton(
                        "Novo curso", 
                        icon=ft.Icons.ADD, 
                        bgcolor=layout.COR_PRIMARIA, 
                        color="white",
                        on_click=abrir_modal_add
                    )
                ]
            ),
            linha_stats, 
            ft.Container(
                bgcolor=layout.COR_CARD,
                padding=30,
                border_radius=8,
                border=borda_container,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Text("Lista de Cursos", size=16, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                        area_tabela
                    ]
                )
            )
        ]
    )
      
    
    # Adicionar conteúdo ao layout
    layout.add_content(conteudo)
    
    # === RETORNO FINAL DA VIEW ===
    return layout.criar_view("/cursos")