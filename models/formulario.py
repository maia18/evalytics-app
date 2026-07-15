""" Importações """  
import flet as ft
from database.indicadores import INDICADORES

def ViewFormulario(page: ft.Page, mudar_tela):
    
    """
    Tela de formulário de avaliação institucional.
    Percorre os indicadores ativos, permitindo notas de 1 a 5 com critérios explicativos.
    """

    indicadores_ativos = [ind for ind in INDICADORES if ind.get("status", "ATIVO") == "ATIVO"]
    
    estado = {
        "indice_atual": 0,
        "respostas": {} 
    }

    nomes_eixos = {
        1: "Organização Didático-Pedagógica",
        2: "Corpo Docente e Tutorial",
        3: "Infraestrutura"
    }

    # === COMPONENTE: CARD DE PERGUNTA ===
    def criar_card_pergunta(indicador):
        """
        Cria o card de uma pergunta única com slider de nota e critério dinâmico.
        """
        titulo_ind = indicador["titulo"]
        criterios = indicador.get("criterios", {})
        
        # Valor inicial da resposta (default = 3)
        valor_inicial = estado["respostas"].get(titulo_ind, 3)
        texto_inicial = criterios.get(str(valor_inicial), criterios.get(valor_inicial, "Critério não definido."))

        lbl_nota_destaque = ft.Text(str(valor_inicial), size=28, weight="bold", color="blue700")
        txt_criterio_dinamico = ft.Text(texto_inicial, size=14, color="grey700", italic=True, text_align=ft.TextAlign.CENTER)

        # Atualiza nota e critério ao deslizar
        def ao_deslizar(e):
            nota_atual = int(e.control.value)
            estado["respostas"][titulo_ind] = nota_atual
            
            lbl_nota_destaque.value = str(nota_atual)
            texto_criterio = criterios.get(str(nota_atual), criterios.get(nota_atual, "Sem descrição."))
            txt_criterio_dinamico.value = texto_criterio
            page.update()

        slider_nota = ft.Slider(
            min=1, max=5, divisions=4,
            value=valor_inicial, 
            label="Nota {value}", 
            active_color="blue700",
            inactive_color="blue100",
            on_change=ao_deslizar,
            expand=True
        )

        return ft.Container(
            bgcolor="white",
            padding=30, 
            border_radius=12,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12"),
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text(titulo_ind, size=18, weight="bold", color="black87"),
                    ft.Text(indicador.get("descricao", ""), size=14, color="grey500"),
                    ft.Divider(height=10, color="transparent"),
                    ft.Row([ft.Text("1", color="grey400", weight="bold"), slider_nota, ft.Text("5", color="grey400", weight="bold")]),
                    ft.Container(
                        bgcolor="#F8F9FA",
                        padding=15,
                        border_radius=8,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                            controls=[lbl_nota_destaque, txt_criterio_dinamico]
                        )
                    )
                ]
            )
        )

    # === 3. LÓGICA DE NAVEGAÇÃO ===
    area_dinamica_conteudo = ft.Column(spacing=25)

    def pular_para_eixo(eixo_alvo):
        """Permite pular diretamente para o primeiro indicador de um eixo."""
        for i, ind in enumerate(indicadores_ativos):
            if ind.get("eixo") == eixo_alvo:
                estado["indice_atual"] = i
                break
        atualizar_renderizacao()

    def avancar(e):
        """Avança para próxima pergunta ou finaliza se for a última."""
        if estado["indice_atual"] < len(indicadores_ativos) - 1:
            estado["indice_atual"] += 1
            atualizar_renderizacao()
        else:
            area_central.content = tela_sucesso
            page.update()

    def anterior(e):
        """Volta para pergunta anterior."""
        if estado["indice_atual"] > 0:
            estado["indice_atual"] -= 1
            atualizar_renderizacao()

    def atualizar_renderizacao():
        """Renderiza a pergunta atual com cabeçalho, card e rodapé."""
        if not indicadores_ativos:
            area_dinamica_conteudo.controls = [ft.Text("Nenhum indicador ativo.", color="grey500")]
            page.update()
            return

        ind_atual = indicadores_ativos[estado["indice_atual"]]
        eixo_atual = ind_atual.get("eixo")
        
        # Calcula posição dentro do eixo
        inds_neste_eixo = [i for i in indicadores_ativos if i.get("eixo") == eixo_atual]
        posicao_neste_eixo = inds_neste_eixo.index(ind_atual) + 1
        total_neste_eixo = len(inds_neste_eixo)

        # Stepper de eixos
        controles_stepper = []
        for i in range(1, 4):
            ativo = (i == eixo_atual)
            controles_stepper.append(
                ft.Container(
                    content=ft.Text(f"Eixo {i}", color="white" if ativo else "black87", weight="bold"),
                    bgcolor="#1976D2" if ativo else "#E0E0E0", 
                    padding=10,
                    border_radius=20,
                    ink=True,
                    on_click=lambda e, e_alvo=i: pular_para_eixo(e_alvo)
                )
            )
        linha_stepper = ft.Row(controles_stepper, alignment=ft.MainAxisAlignment.END, spacing=10)

        # Cabeçalho com progresso geral
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

        # Card da pergunta
        card = criar_card_pergunta(ind_atual)

        # Rodapé com botões
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

    # === 4. TELA DE SUCESSO ===
    tela_sucesso = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Container(height=50),
            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="green700", size=80),
            ft.Text("Avaliação Enviada!", size=28, weight="bold", color="black87"),
            ft.Text(
                "Muito obrigado pelo seu tempo e contribuição.\nSuas respostas foram registradas com sucesso.",
                text_align=ft.TextAlign.CENTER,
                color="grey600"
            ),
            ft.Container(height=20),
            ft.ElevatedButton("Voltar para o Painel", on_click=lambda _: mudar_tela("/inicio"))
        ]
    )

    # === 5. ESTRUTURA PRINCIPAL ===
    area_central = ft.Container(
        width=900,
        padding=20,
        content=area_dinamica_conteudo
    )

    # Inicializa o formulário na primeira pergunta
    atualizar_renderizacao()

    # === RETORNO FINAL DA VIEW ===
    return ft.View(
        route="/formulario",
        padding=0,
        bgcolor="#F4F6F9", 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        controls=[area_central]
    )
