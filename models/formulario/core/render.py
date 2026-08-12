import flet as ft
from components.core.constants.texts import NOMES_EIXOS
from models.formulario.widgets.card_pergunta import criar_card_pergunta
from models.formulario.widgets.stepper_eixos import criar_stepper_eixos

class FormularioRenderMixin:
    """Mixin responsável por ler o estado atual do Controller e refleti-lo graficamente na tela."""

    # Reconstrói cabeçalho, pergunta atual e rodapé com base no índice atual do formulário (estado)
    def atualizar_renderizacao(self) -> None:
        
        '''Fallback de segurança se nenhum indicador foi cadastrado no banco'''
        if not self.indicadores_ativos:
            self.area_dinamica.controls = [ft.Text("Nenhum indicador ativo.", color="onSurfaceVariant")]
            self.page.update()
            return

        # Busca a pergunta pertinente ao índice atual
        ind_atual = self.indicadores_ativos[self.estado["indice_atual"]]
        eixo_atual = ind_atual.get("eixo")

        # Realiza os cálculos para exibir o contador dinâmico (ex: "Pergunta 2 de 5")
        inds_neste_eixo = [i for i in self.indicadores_ativos if i.get("eixo") == eixo_atual]
        posicao_neste_eixo = inds_neste_eixo.index(ind_atual) + 1
        total_neste_eixo = len(inds_neste_eixo)

        linha_stepper = criar_stepper_eixos(eixo_atual, self.pular_para_eixo)
        progresso_geral = (self.estado["indice_atual"] + 1) / len(self.indicadores_ativos)

        cabecalho = ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[ft.Text("Progresso da Avaliação", size=18, weight="bold", color="onSurface"), linha_stepper],
                ),
                ft.ProgressBar(value=progresso_geral, color="primary", bgcolor="surfaceVariant"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(NOMES_EIXOS.get(eixo_atual, f"Eixo {eixo_atual}"), size=16, weight="bold", color="primary"),
                        ft.Text(f"Pergunta {posicao_neste_eixo} de {total_neste_eixo}", size=14, color="onSurfaceVariant"),
                    ],
                ),
                ft.Divider(height=10, color="outlineVariant"),
            ],
        )

        card = criar_card_pergunta(self.page, ind_atual, self.estado) # Constroi o card principal de slider

        # Monta os botões de ação do rodapé
        btn_cancelar = ft.TextButton(
            "Cancelar", 
            icon=ft.Icons.CANCEL, 
            icon_color="error", 
            style=ft.ButtonStyle(color="error"), 
            on_click=lambda _: self.mudar_tela("/inicio")
        )
        
        # Desabilita o botão 'Anterior' se estivermos na primeira pergunta (índice 0)
        btn_anterior = ft.ElevatedButton(
            "Anterior", 
            icon=ft.Icons.ARROW_BACK, 
            bgcolor="surfaceVariant", 
            color="onSurface", 
            disabled=(self.estado["indice_atual"] == 0), 
            on_click=self.anterior
        )

        eh_ultima_pergunta = self.estado["indice_atual"] == len(self.indicadores_ativos) - 1
        btn_avancar = ft.ElevatedButton(
            "Finalizar" if eh_ultima_pergunta else "Avançar",
            icon=ft.Icons.CHECK if eh_ultima_pergunta else ft.Icons.ARROW_FORWARD,
            bgcolor=ft.Colors.GREEN if eh_ultima_pergunta else "primary",
            color=ft.Colors.WHITE if eh_ultima_pergunta else "onPrimary",
            on_click=self.avancar,
        )

        rodape = ft.Container(
            padding=20, bgcolor="surface", border_radius=8, shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="shadow"),
            content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[btn_cancelar, ft.Row([btn_anterior, btn_avancar], spacing=10)])
        )

        # Injeta os 3 blocos renderizados na tela ao mesmo tempo
        self.area_dinamica.controls = [cabecalho, card, rodape]
        self.page.update()