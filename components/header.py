from nicegui import ui


def titulo_pagina(titulo: str, subtitulo: str = ''):

    ui.label(titulo).classes(
        'text-3xl font-bold'
    )

    if subtitulo:

        ui.label(subtitulo).classes(
            'text-gray-500 mb-4'
        )