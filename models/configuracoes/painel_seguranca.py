import flet as ft

def criar_painel_seguranca():
    return ft.Container(
        padding=20,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Políticas de Segurança", size=18, weight="bold"),
                ft.Divider(color="grey300"),
                ft.Switch(label="Exigir autenticação em duas etapas (2FA)", value=True, active_color="blue700"),
                ft.Switch(label="Bloquear acesso após 5 tentativas falhas", value=True, active_color="blue700"),
                ft.Switch(label="Registrar logs de auditoria", value=True, active_color="blue700"),
                ft.ElevatedButton("Exportar Relatório de Acessos", icon=ft.Icons.SECURITY_UPDATE_WARNING, color="blue700")
            ]
        )
    )
