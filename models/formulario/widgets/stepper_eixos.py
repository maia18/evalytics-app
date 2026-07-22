import flet as ft

def criar_stepper_eixos(eixo_atual, pular_para_eixo):
    controles = []
    for i in range(1, 4):
        ativo = (i == eixo_atual)
        controles.append(
            ft.Container(
                content=ft.Text(f"Eixo {i}", color="onPrimary" if ativo else "onSurface", weight="bold"),
                bgcolor="primary" if ativo else "surfaceVariant",
                padding=10,
                border_radius=20,
                ink=True,
                on_click=lambda e, e_alvo=i: pular_para_eixo(e_alvo)
            )
        )
    return ft.Row(controles, alignment=ft.MainAxisAlignment.END, spacing=10)