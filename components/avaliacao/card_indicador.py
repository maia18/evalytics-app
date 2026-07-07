from nicegui import ui
from components.avaliacao.escala_likert import escala_likert

def card_indicador(indicador: dict, resposta_salva: dict, on_change):
    """
    Renderiza o card de um indicador, exibindo o título, descrição, 
    a escala likert interativa e o campo de comentário.
    """
    with ui.card().classes('w-full p-6 shadow-md rounded-lg'):
        
        ui.label(indicador["titulo"]).classes('text-xl font-bold text-gray-800')
        
        if indicador.get("descricao"):
            ui.label(indicador["descricao"]).classes('text-md text-gray-600 mb-4')
            
        ui.separator().classes('my-4')
        
        criterios = indicador.get("criterios", {})
        
        # Cria um estado local para isolar a resposta deste indicador
        estado_local = {
            "nota": resposta_salva.get("nota"),
            "comentario": resposta_salva.get("comentario", "")
        }
        
        def disparar_alteracao():
            # Apenas envia os dados para a sessão se a nota já foi selecionada
            if estado_local["nota"]: 
                on_change(estado_local["nota"], estado_local["comentario"])

        def ao_mudar_nota(nova_nota: int):
            estado_local["nota"] = nova_nota
            disparar_alteracao()

        # Renderiza a nossa nova Escala Likert clicável
        escala_likert(
            criterios=criterios, 
            valor_inicial=estado_local["nota"], 
            on_change=ao_mudar_nota
        )
        
        ui.separator().classes('my-4')
        
        comentario = ui.textarea("Comentário (opcional)").classes('w-full')
        
        if estado_local["comentario"]:
            comentario.value = estado_local["comentario"]
            
        def ao_mudar_comentario(e):
            estado_local["comentario"] = comentario.value
            disparar_alteracao()

        comentario.on('blur', ao_mudar_comentario)