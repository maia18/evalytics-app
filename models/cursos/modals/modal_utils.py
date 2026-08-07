import flet as ft

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