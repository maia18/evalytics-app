import flet as ft
import json
from database.indicadores import INDICADORES

def criar_modal_criterios(page, item_alvo_acao):
    campos = [ft.TextField(label=f"Critério {i}", multiline=True, border_color="blue200") for i in range(1,6)]

    def salvar_criterios(e):
        for item in INDICADORES:
            if item["titulo"] == item_alvo_acao["titulo"] and item["eixo"] == item_alvo_acao["eixo"]:
                item["criterios"] = {i+1: campos[i].value for i in range(5)}
                break
        with open("database/indicadores.py", "w", encoding="utf-8") as f:
            f.write(f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n")
        page.snack_bar = ft.SnackBar(ft.Text("Critérios atualizados!", color="green"))
        page.snack_bar.open = True
        page.update()

    modal = ft.AlertDialog(
        title=ft.Text("Editar Critérios", size=20, weight="bold"),
        content=ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15, controls=campos),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Salvar", bgcolor="blue700", color="white", on_click=salvar_criterios)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal_criterios(e, item):
        item_alvo_acao.clear()
        item_alvo_acao.update(item)
        if modal not in page.overlay:
            page.overlay.append(modal)
        modal.open = True
        page.update()

    return modal, campos, abrir_modal_criterios
