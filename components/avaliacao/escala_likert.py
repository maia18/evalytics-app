from nicegui import ui

def escala_likert(criterios: dict, valor_inicial=None, on_change=None):
    # Armazena qual nota está selecionada no momento
    estado = {"selecionado": str(valor_inicial) if valor_inicial else None}
    
    # Dicionários para guardar os elementos de UI para alterarmos a cor depois do clique
    cards = {}
    icones = {}

    def selecionar(nota_str):
        estado["selecionado"] = nota_str
        
        # Atualiza o visual de todos os cards
        for n, card in cards.items():
            if n == nota_str:
                # Destaca o card selecionado
                card.classes(remove="border-transparent bg-white hover:bg-gray-50", add="border-blue-500 bg-blue-50")
                icones[n].name = 'radio_button_checked'
                icones[n].classes(remove="text-gray-400", add="text-blue-500")
            else:
                # Volta os outros cards ao normal
                card.classes(remove="border-blue-500 bg-blue-50", add="border-transparent bg-white hover:bg-gray-50")
                icones[n].name = 'radio_button_unchecked'
                icones[n].classes(remove="text-blue-500", add="text-gray-400")
        
        # Dispara o callback mandando a nota (em inteiro) para o card_indicador
        if on_change:
            on_change(int(nota_str))

    with ui.column().classes("w-full gap-3"):
        ui.label("Selecione o critério que melhor representa sua avaliação:").classes("text-sm text-gray-600 mb-2")

        for nota, texto in criterios.items():
            nota_str = str(nota)
            
            # Card principal interativo
            card = ui.card().classes(
                "w-full cursor-pointer transition-all p-0 shadow-sm border"
            )
            
            # Aplica o estilo inicial (útil para quando o usuário clicar no botão "Voltar")
            if nota_str == estado["selecionado"]:
                card.classes(add="border-blue-500 bg-blue-50")
            else:
                card.classes(add="border-transparent bg-white hover:bg-gray-50")
                
            cards[nota_str] = card

            with card:
                # Linha inteira clicável
                with ui.row().classes("w-full items-start no-wrap p-4").on('click', lambda e, n=nota_str: selecionar(n)):
                    
                    # Ícone simulando rádio
                    icone_nome = 'radio_button_checked' if nota_str == estado["selecionado"] else 'radio_button_unchecked'
                    icone_cor = 'text-blue-500' if nota_str == estado["selecionado"] else 'text-gray-400'
                    
                    icone = ui.icon(icone_nome, size='sm').classes(f'{icone_cor} mt-1')
                    icones[nota_str] = icone
                    
                    # Textos
                    with ui.column().classes("gap-1 flex-1"):
                        ui.label(f"Nota {nota}").classes("font-bold text-gray-800")
                        ui.label(texto).classes("whitespace-normal text-gray-700")