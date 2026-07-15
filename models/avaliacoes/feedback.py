import flet as ft

def mostrar_feedback(page, mensagem, sucesso=True):
    
    """Exibe SnackBar com mensagem de sucesso ou erro"""
    
    cor = "green" if sucesso else "red"
    page.snack_bar = ft.SnackBar(ft.Text(mensagem, color=cor))
    page.snack_bar.open = True
    page.update()
