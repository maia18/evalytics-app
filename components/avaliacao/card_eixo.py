from nicegui import ui

EIXOS = [
    ("1", "📘 Organização Didático-Pedagógica"),
    ("2", "👨‍🏫 Corpo Docente"),
    ("3", "🏢 Infraestrutura"),
    ("4", "📈 Planejamento e Avaliação"),
    ("5", "🎯 Desenvolvimento Institucional"),
]

def cards_eixos():

    with ui.grid(columns=2).classes('w-full gap-4'):

        for codigo, nome in EIXOS:

            with ui.card().classes('w-full'):

                ui.label(nome).classes('text-lg font-bold')

                ui.label(f'Eixo {codigo}')

                ui.button(
                    'Abrir',
                    on_click=lambda e=codigo:
                        ui.navigate.to(f'/eixo/{e}')
                ).classes('w-full')