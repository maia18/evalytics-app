from nicegui import ui


def grafico_barras(titulo, categorias, valores):

    ui.echart({

        'title': {
            'text': titulo
        },

        'tooltip': {},

        'xAxis': {
            'type': 'category',
            'data': categorias
        },

        'yAxis': {
            'type': 'value'
        },

        'series': [
            {
                'type': 'bar',
                'data': valores
            }
        ]

    }).classes('w-full h-96')