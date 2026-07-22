import flet as ft 
from components.core.constants.constants import * 

def criar_card_controle_ciclo(layout, mudar_tela, page): 
    """
    Gera o cartão responsável por exibir o status do ciclo de avaliação e abrigar botões de ação principais.
    """
    
    # Cria a "tag" (badge) visual para indicar que o ciclo está rodando
    status_ciclo = ft.Container( 
        content=ft.Text("EM ANDAMENTO", color="white", size=12, weight="bold"), 
        bgcolor="green600", # Fundo verde para indicar atividade/sucesso
        padding=8, 
        border_radius=15 # Bordas bem arredondadas, estilo pílula
    ) 

    # Retorna o container principal que atua como o fundo do cartão
    return ft.Container( 
        bgcolor=layout.cores[CARD], # Usa a cor dinâmica do tema para cartões
        padding=25, # Margem interna espaçosa
        border_radius=10, # Bordas levemente arredondadas
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"), # Adiciona sombra para profundidade
        content=ft.Column( 
            spacing=20, 
            controls=[ 
                # Linha superior contendo as informações e os botões de ação
                ft.Row( 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Separa título e botões nos extremos
                    controls=[ 
                        # Título e tag de status
                        ft.Column( 
                            spacing=2, 
                            controls=[ 
                                ft.Text("Ciclo de Avaliação Ativo", size=14, color="grey600"), 
                                ft.Row([ft.Text("Semestre 2026.1", size=22, weight="bold", color=COR_PRIMARIA), status_ciclo]) 
                            ] 
                        ), 
                        # Grupo de botões à direita
                        ft.Row( 
                            spacing=10, 
                            controls=[ 
                                ft.ElevatedButton( # Botão para navegar para a criação de form
                                    "Nova Avaliação", 
                                    icon=ft.Icons.OPEN_IN_NEW, 
                                    bgcolor="blue700", 
                                    color="white", 
                                    on_click=lambda _: mudar_tela("/formulario") 
                                ), 
                                ft.ElevatedButton( # Botão para gerar link rápido
                                    "Copiar Link", 
                                    icon=ft.Icons.CONTENT_COPY, 
                                    bgcolor="blue50", 
                                    color="blue700", 
                                    # Usa funções encadeadas no lambda para abrir uma barra de notificação (SnackBar) confirmando a cópia
                                    on_click=lambda _: setattr(page.snack_bar, 'open', True) or setattr(page.snack_bar, 'content', ft.Text("Link copiado para a área de transferência!")) or page.update() 
                                ) 
                            ] 
                        ) 
                    ] 
                ), 
                ft.Divider(color="grey200"), # Linha divisória horizontal
                # Rodapé do cartão mostrando totalizadores e opção de encerrar
                ft.Row( 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    controls=[ 
                        ft.Text("342 respostas coletadas até o momento.", size=14, color="black87"), 
                        ft.TextButton("Encerrar Ciclo", icon=ft.Icons.STOP_CIRCLE, style=ft.ButtonStyle(color="red700")) # Ação destrutiva destacada em vermelho
                    ] 
                ) 
            ] 
        ) 
    ) 