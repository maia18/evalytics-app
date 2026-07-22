import flet as ft 
import json 
from database.indicadores import INDICADORES 

def criar_modal_novo(page, pasta_aberta_atualmente, abrir_pasta): 
    """Cria a estrutura base (dicionário) para injeção de uma métrica inédita."""
    campo_titulo = ft.TextField(label="Título do Indicador", border_color="blue200") 
    campo_desc = ft.TextField(label="Descrição", multiline=True, border_color="blue200") 

    def salvar_novo(e): 
        """Configura a hierarquia do objeto recém-nascido e apenda (append) no BD."""
        novo_item = { 
            "titulo": campo_titulo.value, 
            "eixo": pasta_aberta_atualmente["eixo"], # Herda automaticamente o eixo da visualização atual
            "descricao": campo_desc.value, 
            "status": "ATIVO", # Define status padrão
            "criterios": {i: "" for i in range(1,6)} # Pré-formata um dict contendo as 5 chaves de critérios vazias
        } 
        
        INDICADORES.append(novo_item) # Insere no array
        
        # Salva o arquivo local
        with open("database/indicadores.py", "w", encoding="utf-8") as f: 
            f.write(f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n") 
            
        # Esvazia os campos para evitar resíduos em um próximo uso
        campo_titulo.value = "" 
        campo_desc.value = "" 
        
        page.snack_bar = ft.SnackBar(ft.Text("Novo indicador criado!", color="green")) 
        page.snack_bar.open = True 
        abrir_pasta(pasta_aberta_atualmente["titulo"]) 
        page.update() 

    modal = ft.AlertDialog( 
        title=ft.Text("Novo Indicador", size=18, weight="bold"), 
        content=ft.Column(width=400, height=200, spacing=15, controls=[campo_titulo, campo_desc]), 
        actions=[ 
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)), 
            ft.ElevatedButton("Salvar", bgcolor="blue700", color="white", on_click=salvar_novo) 
        ], 
        actions_alignment=ft.MainAxisAlignment.END 
    ) 

    def abrir_modal_novo(): 
        if modal not in page.overlay: 
            page.overlay.append(modal) 
        modal.open = True 
        page.update() 

    return modal, campo_titulo, campo_desc, abrir_modal_novo 