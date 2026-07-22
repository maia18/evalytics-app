import flet as ft 

def criar_painel_banco(): 
    """Constrói a interface para manutenção e gestão de backups do banco."""
    return ft.Container( 
        padding=20, 
        content=ft.Column( 
            spacing=20, 
            controls=[ 
                ft.Text("Gerenciamento de Dados", size=18, weight="bold"), 
                ft.Divider(color="grey300"), 
                ft.Text("Ferramentas para manutenção periódica do sistema.", color="grey700"), 
                
                # Ações de manutenção de rotina
                ft.Row( 
                    controls=[ 
                        ft.ElevatedButton("Backup Completo", icon=ft.Icons.DOWNLOAD, bgcolor="green700", color="white"), 
                        ft.ElevatedButton("Otimizar Índices", icon=ft.Icons.SPEED, bgcolor="blue700", color="white"), 
                    ] 
                ), 
                
                # Zona de Risco (Danger Zone) - Área para exclusões severas
                ft.Text("Zona de Risco", size=16, color="red700", weight="bold"), 
                ft.Container( 
                    padding=15, 
                    bgcolor="red50", # Fundo vermelho claro para chamar atenção
                    border_radius=8, 
                    content=ft.Row( 
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                        controls=[ 
                            ft.Text("Excluir avaliações com mais de 5 anos.", color="red900"), 
                            ft.ElevatedButton("Limpar Dados Antigos", icon=ft.Icons.DELETE_FOREVER, bgcolor="red700", color="white") 
                        ] 
                    ) 
                ) 
            ] 
        ) 
    ) 