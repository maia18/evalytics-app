import flet as ft

# Exibe um SnackBar com mensagem de sucesso (verde) ou erro (vermelho)
def mostrar_feedback(page: ft.Page, mensagem: str, sucesso: bool = True) -> None:
    cor = ft.Colors.GREEN if sucesso else ft.Colors.RED # Operador ternário para definir dinamicamente a cor baseada na flag de sucesso
    
    '''Substitui a barra de notificação atual da página pela nova e avisa o Flet para renderizá-la'''
    page.snack_bar = ft.SnackBar(ft.Text(mensagem, color=cor))
    page.snack_bar.open = True
    page.update()