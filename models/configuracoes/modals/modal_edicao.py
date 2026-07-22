import flet as ft 
import json 
from database.indicadores import INDICADORES 

def criar_modal_edicao(page, item_alvo_acao, abrir_pasta, pasta_aberta_atualmente): 
    """Permite reescrever os metadados textuais básicos de um indicador."""
    # Define campos de formulário para título e texto descritivo
    campo_titulo = ft.TextField(label="Título", border_color="blue200") 
    campo_descricao = ft.TextField(label="Descrição", multiline=True, border_color="blue200") 

    def salvar_edicao(e): 
        """Busca o elemento no banco e atualiza suas strings."""
        for item in INDICADORES: 
            if item["titulo"] == item_alvo_acao["titulo"] and item["eixo"] == item_alvo_acao["eixo"]: 
                item["titulo"] = campo_titulo.value 
                item["descricao"] = campo_descricao.value 
                break 
                
        # Grava o dump das alterações no disco rígido
        with open("database/indicadores.py", "w", encoding="utf-8") as f: 
            f.write(f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n") 
            
        # Feedback visual
        page.snack_bar = ft.SnackBar(ft.Text("Indicador atualizado!", color="green")) 
        page.snack_bar.open = True 
        
        # Chama callback para renderizar a visão de pastas novamente, já com os novos dados
        abrir_pasta(pasta_aberta_atualmente["titulo"]) 
        page.update() 

    # Compõe o pop-up na interface
    modal = ft.AlertDialog( 
        title=ft.Text("Editar Indicador", size=20, weight="bold"), 
        content=ft.Column(width=400, height=200, spacing=15, controls=[campo_titulo, campo_descricao]), 
        actions=[ 
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)), 
            ft.ElevatedButton("Salvar", bgcolor="blue700", color="white", on_click=salvar_edicao) 
        ], 
        actions_alignment=ft.MainAxisAlignment.END 
    ) 

    def abrir_modal_edicao(e, item): 
        """Seta o objeto alvo e mostra o modal."""
        item_alvo_acao.clear() 
        item_alvo_acao.update(item) 
        if modal not in page.overlay: 
            page.overlay.append(modal) 
        modal.open = True 
        page.update() 

    return modal, campo_titulo, campo_descricao, abrir_modal_edicao 