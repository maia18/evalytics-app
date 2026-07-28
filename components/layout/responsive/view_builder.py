import flet as ft 
from components.core.constants.constants import * 

# Estrutura fisicamente a página final, definindo as camadas (z-index) e eixos
def criar_view(route, cores, sidebar_desktop, topbar, conteudo_principal, overlay, sidebar_mobile, ajustar_responsividade, page): 
    
    page.on_resize = ajustar_responsividade # Vincula o evento nativo de redimensionamento de janela à nossa função de ajuste
    ajustar_responsividade() # Chama logo de início para aplicar formatação inicial

    return ft.View( 
        route=route, # Rota da tela atual
        padding=0, # Remove espaçamento padrão ao redor da janela
        bgcolor=cores[FUNDO], # Define o fundo global de acordo com a constante e tema
        controls=[ 
            ft.Stack( # Usa Stack para permitir que a sidebar_mobile e o overlay fiquem "voando" por cima do conteúdo principal
                expand=True, # Ocupa todo o espaço
                controls=[ 
                    ft.Row( # Distribuição horizontal principal
                        expand=True, 
                        spacing=0, # Elimina o espaço nativo entre as colunas
                        controls=[ 
                            sidebar_desktop, # Lado Esquerdo: Navegação
                            ft.Column( # Lado Direito: Topbar e Área de trabalho do usuário
                                expand=True, 
                                spacing=0, 
                                controls=[ 
                                    topbar, # Fica no topo da área direita (fixa, não rola)
                                    ft.Container( 
                                        expand=True, 
                                        padding=16, # Reduzido de 20 para 16: mais espaço útil vertical
                                        content=conteudo_principal # Injeta dinamicamente a tela em questão
                                    ) 
                                ], 
                                # NOTA: scroll=AUTO foi removido daqui de propósito.
                                # Combinar expand=True + scroll na MESMA Column é um bug conhecido do Flet
                                # (github.com/flet-dev/flet/issues/6087): o Flutter reserva uma área de
                                # scroll muito maior que o necessário, criando espaço em branco e uma
                                # barra de rolagem falsa. O scroll agora é responsabilidade de cada tela
                                # individualmente (ex: conteudo_dashboard_executivo), de forma isolada.
                            ) 
                        ] 
                    ), 
                    overlay, # Camada oculta que será chamada por cima da tela ao abrir menu mobile
                    sidebar_mobile # Menu fora de tela inicialmente, pronto para deslizar pra dentro
                ] 
            ) 
        ] 
    )