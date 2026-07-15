import flet as ft
import json
from database.indicadores import INDICADORES

def criar_modal_exclusao(page, item_alvo_acao, abrir_pasta, pasta_aberta_atualmente):
    def confirmar_exclusao(e):
        for idx, item in enumerate(INDICADORES):
            if item["titulo"] == item_alvo_acao["titulo"] and item["eixo"] == item_alvo_acao["eixo"]:
                INDICADORES.pop(idx)
                break
        with open("database/indicadores.py", "w", encoding="utf-8") as f:
            f.write(f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n")
        page.snack_bar = ft.SnackBar(ft.Text("Indicador removido!", color="red"))
        page.snack_bar.open = True
        abrir_pasta(pasta_aberta_atualmente["titulo"])
        page.update()

    modal = ft.AlertDialog(
        title=ft.Text("Confirmar Exclusão", size=18, weight="bold", color="red700"),
        content=ft.Text("Tem certeza que deseja excluir este indicador?"),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Excluir", bgcolor="red700", color="white", on_click=confirmar_exclusao)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def preparar_exclusao(item):
        item_alvo_acao.clear()
        item_alvo_acao.update(item)
        if modal not in page.overlay:
            page.overlay.append(modal)
        modal.open = True
        page.update()

    return modal, preparar_exclusao
