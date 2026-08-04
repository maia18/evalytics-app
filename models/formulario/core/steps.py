from typing import Optional
import flet as ft
from models.formulario.widgets.tela_sucesso import criar_tela_sucesso

class FormularioStepsMixin:
    """Mixin que concentra a lógica matemática de transição entre as etapas do formulário.

    NOTA: as chamadas de page.update() com opacidade ocorrem de forma síncrona. 
    O efeito de fade pode não ser percebido perfeitamente devido à rapidez de execução. 
    Isso é um sinalizador arquitetural que pode ser evoluído com métodos assíncronos (asyncio) posteriormente.
    """

    def pular_para_eixo(self, eixo_alvo: int) -> None:
        """Altera o índice atual para a primeira pergunta correspondente ao eixo clicado no Stepper superior."""
        self.area_dinamica.opacity = 0
        self.page.update()

        # Busca pelo primeiro indicador que bata com o eixo alvo e registra o índice
        for i, ind in enumerate(self.indicadores_ativos):
            if ind.get("eixo") == eixo_alvo:
                self.estado["indice_atual"] = i
                break

        self.atualizar_renderizacao()
        self.area_dinamica.opacity = 1
        self.page.update()

    def avancar(self, e: Optional[ft.ControlEvent] = None) -> None:
        """Soma +1 ao índice e avança. Caso seja a última pergunta, encerra o fluxo e carrega a tela de sucesso."""
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
        """Retorna para a pergunta anterior, prevenindo acesso a índices negativos."""
        if self.estado["indice_atual"] > 0:
            self.area_dinamica.opacity = 0
            self.page.update()

            self.estado["indice_atual"] -= 1
            self.atualizar_renderizacao()

            self.area_dinamica.opacity = 1
            self.page.update()