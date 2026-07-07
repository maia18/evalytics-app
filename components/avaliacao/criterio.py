from nicegui import ui


def criterio(valor: int, texto: str):

    with ui.row().classes('items-start w-full gap-3'):

        radio = ui.radio(
            options=[valor]
        ).props('keep-color')

        with ui.column().classes('gap-0'):

            ui.label(f'Nota {valor}').classes(
                'font-bold'
            )

            ui.label(texto).classes(
                'whitespace-normal text-gray-700'
            )

    return radio