import flet as ft
from typing import Optional

from models.formulario.widgets.tela_sucesso import (
    criar_tela_sucesso,
)
from utils.services.avaliacoes.avaliacoes_service import (
    salvar_avaliacao,
)


class FormularioStepsMixin:
    """Mixin que concentra a navegação e finalização do formulário."""

    # ==========================================================
    # NOTIFICAÇÕES
    # ==========================================================

    def _mostrar_mensagem(
        self,
        mensagem: str,
        erro: bool = False,
    ) -> None:
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor=(
                    ft.Colors.RED_700
                    if erro
                    else ft.Colors.GREEN_700
                ),
            )
        )

    # ==========================================================
    # NAVEGAÇÃO ENTRE EIXOS
    # ==========================================================

    def pular_para_eixo(self, eixo_alvo: int) -> None:
        """Vai para a primeira pergunta do eixo selecionado."""

        for i, indicador in enumerate(self.indicadores_ativos):
            if indicador.get("eixo") == eixo_alvo:
                self.estado["indice_atual"] = i
                self.atualizar_renderizacao()
                return

    # ==========================================================
    # AVANÇAR / FINALIZAR
    # ==========================================================

    def avancar(
        self,
        e: Optional[ft.ControlEvent] = None,
    ) -> None:
        """Avança ou envia a avaliação completa ao backend."""

        if not self.indicadores_ativos:
            self._mostrar_mensagem(
                "Não existem indicadores ativos para esta avaliação.",
                erro=True,
            )
            return

        indice_atual = self.estado["indice_atual"]

        if indice_atual < len(self.indicadores_ativos) - 1:
            self.estado["indice_atual"] += 1
            self.atualizar_renderizacao()
            return

        # ------------------------------------------------------
        # VALIDAR CURSO
        # ------------------------------------------------------

        if not self.curso_id or not self.curso_nome:
            self._mostrar_mensagem(
                "Selecione um curso antes de finalizar a avaliação.",
                erro=True,
            )
            return

        # ------------------------------------------------------
        # REUNIR DADOS DO FORMULÁRIO
        # ------------------------------------------------------

        respostas = dict(self.estado.get("respostas", {}))

        justificativas = dict(
            self.estado.get("justificativas", {})
        )

        anexos_por_indicador = self.estado.get("anexos", {})

        anexos = {
            indicador_id: list(lista)
            for indicador_id, lista in anexos_por_indicador.items()
            if lista
        }

        # ------------------------------------------------------
        # ENVIAR PARA O SERVIÇO
        # ------------------------------------------------------

        try:
            sucesso = salvar_avaliacao(
                curso_id=self.curso_id,
                curso_nome=self.curso_nome,
                respostas=respostas,
                justificativas=justificativas,
                anexos=anexos,
            )
        except Exception:
            sucesso = False

        if not sucesso:
            self._mostrar_mensagem(
                "Não foi possível salvar a avaliação e suas evidências. "
                "Verifique a conexão e tente novamente.",
                erro=True,
            )
            return

        # ------------------------------------------------------
        # SUCESSO
        # ------------------------------------------------------

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
        """Retorna à pergunta anterior."""

        if self.estado["indice_atual"] > 0:
            self.estado["indice_atual"] -= 1
            self.atualizar_renderizacao()

    # ==========================================================
    # CANCELAR
    # ==========================================================

    def cancelar_avaliacao(
        self,
        e: Optional[ft.ControlEvent] = None,
    ) -> None:
        """Cancela a avaliação atual e retorna à tela inicial."""

        self.page._formulario_controller = None
        self.mudar_tela("/inicio")