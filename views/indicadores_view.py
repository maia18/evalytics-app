import flet as ft
from utils.services.indicadores_service import listar_indicadores, atualizar_indicador

def TelaIndicadores(page: ft.Page):
    # Container mestre para trocar o conteúdo
    container_mestre = ft.Container(expand=True)

    # --- NÍVEL 1: Dashboard de Eixos (Layout da sua imagem) ---
    def TelaListaEixos():
        dados = listar_indicadores()
        eixos_agrupados = {}
        for ind in dados:
            cat = ind.get("categoria", "Outros")
            if cat not in eixos_agrupados: eixos_agrupados[cat] = []
            eixos_agrupados[cat].append(ind)

        lista_cards = [ft.Text("Gerenciar Indicadores", size=24, weight="bold")]
        
        for nome, lista in eixos_agrupados.items():
            lista_cards.append(ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.FOLDER, color="blue700"),
                            title=ft.Text(nome, weight="bold"),
                            subtitle=ft.Text(f"{len(lista)} indicadores"),
                            on_click=lambda e, n=nome, l=lista: carregar_indicadores_do_eixo(n, l)
                        )
                    )
                ),
                width=800 # Mantém o layout alinhado e controlado
            ))
        return ft.Container(padding=20, content=ft.Column(lista_cards))

    # --- NÍVEL 2: Títulos dos Indicadores ---
    def carregar_indicadores_do_eixo(eixo_nome, indicadores):
        lista = ft.Column([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: voltar_lista()),
            ft.Text(eixo_nome, size=24, weight="bold"),
            *[ft.Card(content=ft.ListTile(
                title=ft.Text(ind.get("nome", "Sem título")),
                trailing=ft.Icon(ft.Icons.EDIT),
                on_click=lambda e, i=ind: carregar_editor(i, eixo_nome, indicadores)
            )) for ind in indicadores]
        ], scroll=ft.ScrollMode.AUTO)
        container_mestre.content = ft.Container(padding=20, content=lista)
        container_mestre.update()

    # --- NÍVEL 3: Editor de Descrição e Critérios ---
    def carregar_editor(ind, eixo_nome, indicadores_originais):
        nome_f = ft.TextField(value=ind.get("nome", ""), label="Título do Indicador")
        desc_f = ft.TextField(value=ind.get("descricao", ""), label="Descrição", multiline=True)
        
        # Cria campos para os 5 critérios
        crit_inputs = []
        criterios = ind.get("criterios", {})
        for i in range(1, 6):
            crit_inputs.append(ft.TextField(
                value=criterios.get(str(i), ""), 
                label=f"Critério {i}", multiline=True
            ))

        def salvar(e):
            # Lógica de atualização (exige a função atualizar_indicador no seu service)
            # atualizar_indicador(ind['id'], nome_f.value, ...) 
            page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas!"))
            page.snack_bar.open = True
            page.update()

        container_mestre.content = ft.Container(padding=20, content=ft.Column([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: carregar_indicadores_do_eixo(eixo_nome, indicadores_originais)),
            ft.Text("Editando Indicador", size=20, weight="bold"),
            nome_f, desc_f, *crit_inputs,
            ft.ElevatedButton("Salvar Alterações", icon=ft.Icons.SAVE, on_click=salvar)
        ], scroll=ft.ScrollMode.AUTO))
        container_mestre.update()

    def voltar_lista():
        container_mestre.content = TelaListaEixos()
        container_mestre.update()

    container_mestre.content = TelaListaEixos()
    return container_mestre