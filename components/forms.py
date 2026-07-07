from nicegui import ui


def campo(label: str):
    return ui.input(label).classes('w-96')


def numero(label: str):
    return ui.number(label).classes('w-40')


def botao(texto, on_click, color='primary'):
    return ui.button(
        texto,
        on_click=on_click
    ).props(f'color={color}')