import flet as ft

from components.core.constants.constants import (
    COR_PRIMARIA,
    SUCESSO,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
)
from components.core.constants.texts import NOMES_EIXOS
from models.formulario.widgets.card_pergunta import criar_card_pergunta
from models.formulario.widgets.stepper_eixos import criar_stepper_eixos


class FormularioRenderMixin:
    """
    Mixin responsável por ler o estado atual do Controller
    e refleti-lo graficamente na tela.
    """

    # Reconstrói cabeçalho, pergunta atual e rodapé
    # com base no índice atual do formulário.
    def atualizar_renderizacao(self) -> None:

        # ==========================================================
        # FALLBACK — NENHUM INDICADOR
        # ==========================================================

        if not self.indicadores_ativos:
            self.area_dinamica.controls = [
                ft.Text(
                    "Nenhum indicador ativo.",
                    color="onSurfaceVariant",
                )
            ]

            self.page.update()
            return

        # ==========================================================
        # INDICADOR ATUAL
        # ==========================================================

        ind_atual = self.indicadores_ativos[
            self.estado["indice_atual"]
        ]

        eixo_atual = ind_atual.get("eixo")

        # ==========================================================
        # CONTADOR DE PERGUNTAS DO EIXO
        # ==========================================================

        inds_neste_eixo = [
            indicador
            for indicador in self.indicadores_ativos
            if indicador.get("eixo") == eixo_atual
        ]

        posicao_neste_eixo = (
            inds_neste_eixo.index(ind_atual) + 1
        )

        total_neste_eixo = len(inds_neste_eixo)

        # ==========================================================
        # STEPPER DOS EIXOS
        # ==========================================================

        linha_stepper = criar_stepper_eixos(
            eixo_atual,
            self.pular_para_eixo,
            self.cores,
            getattr(
                self.page,
                "is_dark_mode",
                False,
            ),
        )

        # ==========================================================
        # PROGRESSO GERAL
        # ==========================================================

        progresso_geral = (
            (self.estado["indice_atual"] + 1)
            / len(self.indicadores_ativos)
        )

        # ==========================================================
        # CABEÇALHO
        # ==========================================================

        cabecalho = ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Progresso da Avaliação",
                            size=18,
                            weight="bold",
                            color=self.cores[TEXTO_PRINCIPAL],
                        ),
                        linha_stepper,
                    ],
                ),

                ft.ProgressBar(
                    value=progresso_geral,
                    color=self.cores[COR_PRIMARIA],
                    bgcolor=self.cores[TEXTO_SECUNDARIO],
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            NOMES_EIXOS.get(
                                eixo_atual,
                                f"Eixo {eixo_atual}",
                            ),
                            size=16,
                            weight="bold",
                            color=self.cores[COR_PRIMARIA],
                        ),

                        ft.Text(
                            (
                                f"Pergunta "
                                f"{posicao_neste_eixo} "
                                f"de {total_neste_eixo}"
                            ),
                            size=14,
                            color=self.cores[TEXTO_SECUNDARIO],
                        ),
                    ],
                ),

                ft.Divider(
                    height=5,
                    color=self.cores[TEXTO_SECUNDARIO],
                ),
            ],
        )

        # ==========================================================
        # BOTÃO CANCELAR
        # ==========================================================

        btn_cancelar = ft.TextButton(
            "Cancelar",
            icon=ft.Icons.CANCEL,
            icon_color="error",
            style=ft.ButtonStyle(
                color="error",
            ),
            on_click=self.cancelar_avaliacao,
        )

        # ==========================================================
        # BOTÃO ANTERIOR
        # ==========================================================

        btn_anterior = ft.OutlinedButton(
            "Anterior",
            icon=ft.Icons.ARROW_BACK,
            disabled=(
                self.estado["indice_atual"] == 0
            ),
            on_click=self.anterior,
        )

        # ==========================================================
        # VERIFICA SE É A ÚLTIMA PERGUNTA
        # ==========================================================

        eh_ultima_pergunta = (
            self.estado["indice_atual"]
            == len(self.indicadores_ativos) - 1
        )

        # ==========================================================
        # BOTÃO AVANÇAR / FINALIZAR
        # ==========================================================

        btn_avancar = ft.ElevatedButton(
            "Finalizar"
            if eh_ultima_pergunta
            else "Avançar",

            icon=(
                ft.Icons.CHECK
                if eh_ultima_pergunta
                else ft.Icons.ARROW_FORWARD
            ),

            bgcolor=(
                self.cores[SUCESSO]
                if eh_ultima_pergunta
                else self.cores[COR_PRIMARIA]
            ),

            color=self.cores[TEXTO_PRINCIPAL],

            on_click=self.avancar,
        )

        # ==========================================================
        # RODAPÉ
        # ==========================================================

        rodape_integrado = ft.Container(
            padding=ft.Padding.only(
                top=10,
            ),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    btn_cancelar,

                    ft.Row(
                        controls=[
                            btn_anterior,
                            btn_avancar,
                        ],
                        spacing=10,
                    ),
                ],
            ),
        )

        # ==========================================================
        # CARD PRINCIPAL
        # ==========================================================

        card_unificado = criar_card_pergunta(
            self.page,
            ind_atual,
            self.estado,
            rodape_integrado,
            self.cores,
        )

        # ==========================================================
        # ATUALIZA A ÁREA DINÂMICA
        # ==========================================================

        self.area_dinamica.controls = [
            cabecalho,
            card_unificado,
        ]

        self.page.update()