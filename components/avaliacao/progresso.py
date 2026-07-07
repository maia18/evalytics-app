from nicegui import ui


def progresso(atual: int, total: int):

    percentual = int((atual / total) * 100)

    ui.label(
        f'Indicador {atual} de {total}'
    ).classes('font-bold')

    ui.linear_progress(
        percentual / 100
    ).classes('w-full')