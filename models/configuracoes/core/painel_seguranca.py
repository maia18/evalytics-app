import flet as ft 

def criar_painel_seguranca(): 
    """Constrói a interface contendo chaves de ativação (Switches) para políticas de segurança."""
    return ft.Container( 
        padding=20, 
        content=ft.Column( 
            spacing=20, 
            controls=[ 
                ft.Text("Políticas de Segurança", size=18, weight="bold"), 
                ft.Divider(color="grey300"), 
                
                # Chaves ativadoras para políticas rígidas
                ft.Switch(label="Exigir autenticação em duas etapas (2FA)", value=True, active_color="blue700"), 
                ft.Switch(label="Bloquear acesso após 5 tentativas falhas", value=True, active_color="blue700"), 
                ft.Switch(label="Registrar logs de auditoria", value=True, active_color="blue700"), 
                
                # Ação de exportação
                ft.ElevatedButton("Exportar Relatório de Acessos", icon=ft.Icons.SECURITY_UPDATE_WARNING, color="blue700") 
            ] 
        ) 
    ) 