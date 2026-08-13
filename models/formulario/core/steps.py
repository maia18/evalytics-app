import flet as ft
from typing import Optional
from models.formulario.widgets.tela_sucesso import criar_tela_sucesso

class FormularioStepsMixin:
    """
    Mixin que concentra a lógica matemática de transição entre as etapas do formulário.

    NOTA: 
        As chamadas de page.update() com opacidade ocorrem de forma síncrona.
        Isso é um sinalizador arquitetural que pode ser evoluído com métodos assíncronos (asyncio) posteriormente.
    """

    # Altera o índice atual para a primeira pergunta correspondente ao eixo clicado no Stepper superior
    def pular_para_eixo(self, eixo_alvo: int) -> None:
        # Busca pelo primeiro indicador que bata com o eixo alvo e registra o índice
        for i, ind in enumerate(self.indicadores_ativos):
            if ind.get("eixo") == eixo_alvo:
                self.estado["indice_atual"] = i
                break

        self.atualizar_renderizacao()

    # Soma +1 ao índice e avança. Caso seja a última pergunta, encerra o fluxo e carrega a tela de sucesso
    def avancar(self, e: Optional[ft.ControlEvent] = None) -> None:
        if self.estado["indice_atual"] < len(self.indicadores_ativos) - 1:
            self.estado["indice_atual"] += 1
            self.atualizar_renderizacao()
        else:
            self.area_central.content = criar_tela_sucesso(self.mudar_tela)
            self.page.update()
            
    # Retorna para a pergunta anterior, prevenindo acesso a índices negativos
    def anterior(self, e: Optional[ft.ControlEvent] = None) -> None:
        if self.estado["indice_atual"] > 0:
            self.estado["indice_atual"] -= 1
            self.atualizar_renderizacao()