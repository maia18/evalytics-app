from nicegui import ui


def criar_grid(colunas, dados, on_select=None):

    grid = ui.aggrid({
        'columnDefs': colunas,
        'rowData': dados,
        'rowSelection': 'single',
    }).classes('w-full')

    if on_select:
        grid.on('rowSelected', lambda e: on_select())

    return grid