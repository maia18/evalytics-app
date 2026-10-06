import flet as ft
from typing import Optional

from models.formulario.widgets.tela_sucesso import criar_tela_sucesso
from utils.services.avaliacoes.avaliacoes_service import salvar_avaliacao


class FormularioStepsMixin:
    """
    Mixin que concentra a lógica de transição entre
    as etapas do formulário.

    Durante a fase de desenvolvimento/testes, as perguntas podem ser
    puladas sem resposta.
    """

    # ==========================================================
    # NAVEGAÇÃO ENTRE EIXOS
    # ==========================================================

    def pular_para_eixo(
        self,
        eixo_alvo: int,
    ) -> None:
        """
        Vai para a primeira pergunta pertencente ao eixo selecionado.
        """

        for i, indicador in enumerate(
            self.indicadores_ativos
        ):
            if indicador.get("eixo") == eixo_alvo:
                self.estado["indice_atual"] = i
                break

        self.atualizar_renderizacao()

    # ==========================================================
    # AVANÇAR / FINALIZAR
    # ==========================================================

    def avancar(
        self,
        e: Optional[ft.ControlEvent] = None,
    ) -> None:
        """
        Avança para a próxima pergunta.

        Durante os testes:

        - permite avançar sem responder;
        - permite pular perguntas;
        - permite finalizar mesmo com respostas incompletas.

        Ao finalizar:

        - valida apenas o curso selecionado;
        - salva as respostas existentes no Firestore;
        - exibe a tela de sucesso após o salvamento.
        """

        # ======================================================
        # NÃO HÁ INDICADORES
        # ======================================================

        if not self.indicadores_ativos:
            self.page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        "Não existem indicadores ativos "
                        "para esta avaliação."
                    ),
                    bgcolor=ft.Colors.RED_700,
                )
            )
            return

        # ======================================================
        # AINDA EXISTEM PERGUNTAS
        # ======================================================

        if (
            self.estado["indice_atual"]
            < len(self.indicadores_ativos) - 1
        ):
            self.estado["indice_atual"] += 1
            self.atualizar_renderizacao()
            return

        # ======================================================
        # ÚLTIMA PERGUNTA → FINALIZAR
        # ======================================================

        if not self.curso_id or not self.curso_nome:
            self.page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        "Selecione um curso antes de "
                        "finalizar a avaliação."
                    ),
                    bgcolor=ft.Colors.RED_700,
                )
            )
            return

        # ======================================================
        # SALVA A AVALIAÇÃO
        # ======================================================

        sucesso = salvar_avaliacao(
            curso_id=self.curso_id,
            curso_nome=self.curso_nome,
            respostas=self.estado["respostas"],
        )

        # ======================================================
        # FALHA NO SALVAMENTO
        # ======================================================

        if not sucesso:
            self.page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        "Não foi possível salvar a avaliação. "
                        "Tente novamente."
                    ),
                    bgcolor=ft.Colors.RED_700,
                )
            )
            return

        # ======================================================
        # SUCESSO
        # ======================================================

        # A avaliação terminou.
        # Remove o controller para que uma nova avaliação
        # comece com estado limpo.
        self.page._formulario_controller = None

        self.area_central.content = criar_tela_sucesso(
            self.mudar_tela
        )

        self.page.update()

    # ==========================================================
    # VOLTAR
    # ==========================================================

    def anterior(
        self,
        e: Optional[ft.ControlEvent] = None,
    ) -> None:
        """
        Retorna para a pergunta anterior.
        """

        if self.estado["indice_atual"] > 0:
            self.estado["indice_atual"] -= 1
            self.atualizar_renderizacao()

    # ==========================================================
    # CANCELAR AVALIAÇÃO
    # ==========================================================

    def cancelar_avaliacao(
        self,
        e: Optional[ft.ControlEvent] = None,
    ) -> None:
        """
        Cancela a avaliação atual e retorna para a tela inicial.

        O controller é removido para que, ao iniciar uma nova
        avaliação posteriormente, o formulário seja criado
        novamente com estado limpo.
        """

        self.page._formulario_controller = None

        self.mudar_tela("/inicio")