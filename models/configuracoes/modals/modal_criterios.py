import flet as ft
import json
from database.indicadores import INDICADORES

def criar_modal_criterios(page, item_alvo_acao):
    campos_criterios = [
        ft.TextField(
            label=f"Critério {i+1}", 
            multiline=True, 
            width=600,
            border_color="blue200",
        ) for i in range(5)
    ]

    def salvar_criterios(e):
        novos_criterios = {str(i+1): campos_criterios[i].value for i in range(5)}
        
        for item in INDICADORES:
            if item.get("titulo") == item_alvo_acao.get("titulo") and item.get("eixo") == item_alvo_acao.get("eixo"):
                item["criterios"] = novos_criterios
                break
                
        with open("database/indicadores.py", "w", encoding="utf-8") as f:
            f.write(f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n")
        
        page.snack_bar = ft.SnackBar(ft.Text("Critérios atualizados com sucesso!", color="green"))
        page.snack_bar.open = True
        modal.open = False
        page.update()

    # 2. Estrutura visual do Modal
    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Critérios", size=20, weight="bold"),
        content=ft.Column(
            width=600, 
            height=450, 
            scroll=ft.ScrollMode.AUTO, 
            spacing=15, 
            controls=campos_criterios
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Salvar", on_click=salvar_criterios, bgcolor="blue700", color="white"),
        ],
    )

    # 3. Lógica para carregar os dados
    def abrir_modal_criterios(e, indicador_selecionado):
        item_alvo_acao.clear()
        item_alvo_acao.update(indicador_selecionado)
        
        criterios_atuais = indicador_selecionado.get("criterios", {})
        
        for i in range(5):
            # Tenta pegar as chaves tanto como string quanto inteiro para evitar bugs com o JSON
            valor_salvo = criterios_atuais.get(str(i+1), criterios_atuais.get(i+1, ""))
            campos_criterios[i].value = valor_salvo
            
        if modal not in page.overlay:
            page.overlay.append(modal)
        
        modal.open = True
        page.update() 

    return modal, campos_criterios, abrir_modal_criterios