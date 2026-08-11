import flet as ft
from typing import Callable, Optional
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from utils.services.indicadores.indicadores_repository import atualizar_criterios_indicador

NUM_CRITERIOS = 5

def criar_modal_criterios(page: ft.Page, estado: EstadoIndicadores) -> tuple[ft.AlertDialog, list[ft.TextField], Callable]:
    """Gera um popup para gerenciar os critérios de avaliação de um indicador."""

    # Cria a lista de 5 campos de texto dinamicamente usando List Comprehension.
    campos_criterios = [ft.TextField(label=f"Critério {i + 1}", multiline=True, width=600, border_color=ft.Colors.BLUE_200) for i in range(NUM_CRITERIOS)]
    
    # Coleta os dados dos campos e persiste os novos critérios do indicador.
    def salvar_criterios(e: ft.ControlEvent) -> None:
        novos_criterios = {str(i + 1): (campos_criterios[i].value or "") for i in range(NUM_CRITERIOS)} # Constrói o dicionário de respostas utilizando Dictionary Comprehension.
        
        atualizar_criterios_indicador(estado.item_alvo.get("titulo"), estado.item_alvo.get("eixo"), novos_criterios)

        # Feedback visual de sucesso.
        page.snack_bar = ft.SnackBar(ft.Text("Critérios atualizados com sucesso!", color=ft.Colors.GREEN))
        page.snack_bar.open = True
        modal.open = False
        
        page.update()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Critérios", size=20, weight="bold"),
        content=ft.Column(width=600, height=450, scroll=ft.ScrollMode.AUTO, spacing=15, controls=campos_criterios),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Salvar", on_click=salvar_criterios, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        ],
    )

    # Prepara o modal preenchendo os campos com os critérios existentes do item clicado.
    def abrir_modal_criterios(e: Optional[ft.ControlEvent], indicador_selecionado: dict) -> None:
        estado.definir_item_alvo(indicador_selecionado)

        criterios_atuais = indicador_selecionado.get("criterios", {})
        for i in range(NUM_CRITERIOS):
            valor_salvo = criterios_atuais.get(str(i + 1), criterios_atuais.get(i + 1, "")) # Extrai o valor salvo aceitando chaves em formato string ou inteiro (compatibilidade retroativa).
            campos_criterios[i].value = valor_salvo

        if modal not in page.overlay:
            page.overlay.append(modal)

        modal.open = True
        page.update()

    return modal, campos_criterios, abrir_modal_criterios