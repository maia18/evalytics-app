import flet as ft

# Exibe SnackBar com mensagem de sucesso ou erro
def mostrar_feedback(page, mensagem, sucesso=True):
    cor = "green" if sucesso else "red"
    page.snack_bar = ft.SnackBar(ft.Text(mensagem, color=cor))
    page.snack_bar.open = True
    page.update()