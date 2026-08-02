import flet as ft

# Estilo global compartilhado do botão "Cancelar" em todos os modais de curso para manter consistência de UI
ESTILO_BOTAO_CANCELAR = ft.ButtonStyle(color=ft.Colors.RED_700)

def abrir_modal(page: ft.Page, modal: ft.AlertDialog) -> None:
    """Adiciona o modal ao overlay da página (se ainda não estiver lá) e o exibe."""
    if modal not in page.overlay:
        page.overlay.append(modal)
    modal.open = True
    page.update()


def fechar_modal(page: ft.Page, modal: ft.AlertDialog) -> None:
    """Oculta o modal e atualiza a página de forma fluida."""
    modal.open = False
    page.update()