import flet as ft 

# Cria um botão apenas com ícone
def criar_botao_icon(icone: str, tooltip_text: str, rota: str, dark_mode: bool, cor_texto: str, mudar_tela) -> ft.Container: 
    """
    Cria um botão compacto que exibe apenas um ícone. 
    Ideal para a sidebar quando o menu está recolhido.
    """
    return ft.Container( 
        height=45, # Define uma altura fixa para garantir que todos os botões tenham a mesma proporção
        alignment=ft.Alignment(0, 0), # Centraliza o botão perfeitamente dentro do container
        content=ft.TextButton( 
            expand=True, # Força o botão a ocupar todo o espaço disponível no container de 45px
            content=ft.Icon( 
                icone, 
                color=cor_texto, 
                size=24, 
                tooltip=tooltip_text, # Exibe um pequeno balão de texto (dica) quando o mouse passa por cima, já que não há texto escrito no botão
            ), 
            style=ft.ButtonStyle( 
                padding=10, 
                shape=ft.RoundedRectangleBorder(radius=8), # Bordas levemente arredondadas no padrão do design
                overlay_color="#3C3C3C" if dark_mode else "#CCCCCC", # Cor de destaque quando o botão é clicado ou recebe "hover" do mouse, baseada no tema
            ), 
            # Associa o clique à mudança de tela. O 'lambda _:' ignora o evento de clique e chama a função de rotas
            on_click=lambda _: mudar_tela(rota) if mudar_tela else None, 
        ), 
    ) 