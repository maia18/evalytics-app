from typing import Optional

import flet as ft

from models.formulario.widgets.tela_sucesso import criar_tela_sucesso


class FormularioStepsMixin:
    """Mixin que concentra a lógica de transição entre as etapas do formulário.

    NOTA: as chamadas de page.update() abaixo (opacidade 0 -> reconstrução ->
    opacidade 1) acontecem em sequência síncrona, sem pausa real entre elas.
    Como a transição configurada é de 300ms (animate_opacity, ver
    formulario.py), é provável que o efeito de fade não seja percebido de
    forma completa antes do conteúdo ser trocado. Sinalizado para revisão
    futura; corrigir de fato exigiria tornar estes métodos assíncronos, o que
    mudaria a assinatura usada pelos callbacks on_click.
    """

    def pular_para_eixo(self, eixo_alvo: int) -> None:
        """Navega diretamente para a primeira pergunta de um eixo específico."""
        self.area_dinamica.opacity = 0
        self.page.update()

        for i, ind in enumerate(self.indicadores_ativos):
            if ind.get("eixo") == eixo_alvo:
                self.estado["indice_atual"] = i
                break

        self.atualizar_renderizacao()

        self.area_dinamica.opacity = 1
        self.page.update()

    def avancar(self, e: Optional[ft.ControlEvent] = None) -> None:
        """Avança para a próxima pergunta ou encerra o formulário se for a última etapa."""
        if self.estado["indice_atual"] < len(self.indicadores_ativos) - 1:
            self.area_dinamica.opacity = 0
            self.page.update()

            self.estado["indice_atual"] += 1
            self.atualizar_renderizacao()

            self.area_dinamica.opacity = 1
            self.page.update()
        else:
            self.area_central.content = criar_tela_sucesso(self.mudar_tela)
            self.page.update()

    def anterior(self, e: Optional[ft.ControlEvent] = None) -> None:
        """Retorna para a pergunta anterior, sem permitir índices negativos."""
        if self.estado["indice_atual"] > 0:
            self.area_dinamica.opacity = 0
            self.page.update()

            self.estado["indice_atual"] -= 1
            self.atualizar_renderizacao()

            self.area_dinamica.opacity = 1
            self.page.update()