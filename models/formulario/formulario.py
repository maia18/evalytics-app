import flet as ft
from database.indicadores import INDICADORES
from models.formulario.widgets.card_pergunta import criar_card_pergunta
from models.formulario.widgets.stepper_eixos import criar_stepper_eixos
from models.formulario.widgets.tela_sucesso import criar_tela_sucesso

def ViewFormulario(page: ft.Page, mudar_tela):
    indicadores_ativos = [ind for ind in INDICADORES if ind.get("status", "ATIVO") == "ATIVO"]

    estado = {"indice_atual": 0, "respostas": {}}
    nomes_eixos = {
        1: "Organização Didático-Pedagógica",
        2: "Corpo Docente e Tutorial",
        3: "Infraestrutura"
    }

    area_dinamica_conteudo = ft.Column(spacing=25)

    def pular_para_eixo(eixo_alvo):
        for i, ind in enumerate(indicadores_ativos):
            if ind.get("eixo") == eixo_alvo:
                estado["indice_atual"] = i
                break
        atualizar_renderizacao()

    def avancar(e):
        if estado["indice_atual"] < len(indicadores_ativos) - 1:
            estado["indice_atual"] += 1
            atualizar_renderizacao()
        else:
            area_central.content = criar_tela_sucesso(mudar_tela)
            page.update()

    def anterior(e):
        if estado["indice_atual"] > 0:
            estado["indice_atual"] -= 1
            atualizar_renderizacao()

    def atualizar_renderizacao():
        if not indicadores_ativos:
            area_dinamica_conteudo.controls = [ft.Text("Nenhum indicador ativo.", color="grey500")]
            page.update()
            return

        ind_atual = indicadores_ativos[estado["indice_atual"]]
        eixo_atual = ind_atual.get("eixo")

        inds_neste_eixo = [i for i in indicadores_ativos if i.get("eixo") == eixo_atual]
        posicao_neste_eixo = inds_neste_eixo.index(ind_atual) + 1
        total_neste_eixo = len(inds_neste_eixo)

        linha_stepper = criar_stepper_eixos(eixo_atual, pular_para_eixo)
        progresso_geral = (estado["indice_atual"] + 1) / len(indicadores_ativos)

        cabecalho = ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[ft.Text("Avaliação Institucional", size=22, weight="bold", color="black87"), linha_stepper]
                ),
                ft.ProgressBar(value=progresso_geral, color="#1976D2", bgcolor="#E0E0E0"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(nomes_eixos.get(eixo_atual, f"Eixo {eixo_atual}"), size=16, weight="bold", color="#1976D2"),
                        ft.Text(f"Pergunta {posicao_neste_eixo} de {total_neste_eixo}", size=14, color="grey600")
                    ]
                ),
                ft.Divider(height=10, color="grey300")
            ]
        )

        card = criar_card_pergunta(page, ind_atual, estado)

        btn_cancelar = ft.TextButton("Cancelar", icon=ft.Icons.CANCEL, icon_color="red", style=ft.ButtonStyle(color="red"), on_click=lambda _: mudar_tela("/inicio"))
        btn_anterior = ft.ElevatedButton("Anterior", icon=ft.Icons.ARROW_BACK, bgcolor="#E0E0E0", color="black87", disabled=(estado["indice_atual"] == 0), on_click=anterior)
        eh_ultima_pergunta = (estado["indice_atual"] == len(indicadores_ativos) - 1)
        btn_avancar = ft.ElevatedButton("Finalizar" if eh_ultima_pergunta else "Avançar", icon=ft.Icons.CHECK if eh_ultima_pergunta else ft.Icons.ARROW_FORWARD, bgcolor="#388E3C" if eh_ultima_pergunta else "#1976D2", color="white", on_click=avancar)

        rodape = ft.Container(
            padding=20,
            bgcolor="white",
            border_radius=8,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
            content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[btn_cancelar, ft.Row([btn_anterior, btn_avancar], spacing=10)])
        )

        area_dinamica_conteudo.controls = [cabecalho, card, rodape]
        page.update()

    area_central = ft.Container(width=900, padding=20, content=area_dinamica_conteudo)

    atualizar_renderizacao()

    return ft.View(
        route="/formulario",
        padding=0,
        bgcolor="#F4F6F9",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        controls=[area_central]
    )