import flet as ft
from typing import Callable
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from utils.services.indicadores.indicadores_repository import adicionar_indicador

def criar_modal_novo(page: ft.Page, estado: EstadoIndicadores, abrir_pasta: Callable[[str], None]) -> tuple[ft.AlertDialog, ft.TextField, ft.TextField, Callable]:
    """Cria o modal de cadastro de um novo indicador vazio."""
    
    # Inicia os campos zerados
    campo_titulo = ft.TextField(label="Título do Indicador", border_color=ft.Colors.BLUE_200)
    campo_desc = ft.TextField(label="Descrição", multiline=True, border_color=ft.Colors.BLUE_200)
    
    # Adiciona o indicador no banco atrelado à categoria selecionada.
    def salvar_novo(e: ft.ControlEvent) -> None:
    
        # Acesso seguro à variável de estado 'pasta_eixo' garante a localização correta do dado no banco.
        adicionar_indicador(campo_titulo.value or "", estado.pasta_eixo, campo_desc.value or "")

        # Limpeza essencial para evitar que dados antigos reapareçam caso o usuário abra o form de novo.
        campo_titulo.value = ""
        campo_desc.value = ""

        page.snack_bar = ft.SnackBar(ft.Text("Novo indicador criado!", color=ft.Colors.GREEN))
        page.snack_bar.open = True
        modal.open = False
        
        abrir_pasta(estado.pasta_titulo) # O callback 'abrir_pasta' força o Flet a redesenhar a lista interna imediatamente.
        page.update()  

    modal = ft.AlertDialog(
        title=ft.Text(
            "Novo Indicador", 
            size=18, 
            weight="bold"
        ),
        content=ft.Column(width=400, height=200, spacing=15, controls=[campo_titulo, campo_desc]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Salvar", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=salvar_novo),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Exibe o modal injetando-o diretamente na camada Overlay do Flet.
    def abrir_modal_novo() -> None:
        if modal not in page.overlay:
            page.overlay.append(modal)
            
        modal.open = True
        page.update()

    return modal, campo_titulo, campo_desc, abrir_modal_novo