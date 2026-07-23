import flet as ft

def criar_stepper_eixos(eixo_atual, pular_para_eixo):
    """
    Cria uma barra de navegação visual (Stepper) composta por botões em formato de "pílula".
    Permite visualizar o eixo atual e clicar nos demais para saltar diretamente para eles.
    
    Args:
        eixo_atual (int): O número do eixo onde o usuário se encontra no momento.
        pular_para_eixo (callable): Função callback disparada ao clicar em um dos botões.
    """
    controles = []
    
    # Laço de repetição que cria os 3 botões (Eixos de 1 a 3 da avaliação)
    for i in range(1, 4):
        # Verifica se o botão sendo desenhado agora corresponde à etapa atual
        ativo = (i == eixo_atual) 
        
        controles.append(
            ft.Container(
                # O texto muda de cor dependendo se a pílula está ativa (contraste alto) ou inativa
                content=ft.Text(f"Eixo {i}", color="onPrimary" if ativo else "onSurface", weight="bold"),
                # O fundo ganha a cor primária se estiver ativo, ou um tom de cinza se inativo
                bgcolor="primary" if ativo else "surfaceVariant",
                padding=10,
                border_radius=20, # Bordas bem arredondadas, criando o efeito visual de pílula
                ink=True, # Habilita a animação nativa de clique (Ripple effect) do Material Design
                # O parâmetro 'e_alvo=i' "congela" o valor da variável 'i' neste momento específico do loop,
                # garantindo que o clique direcione para o eixo correto.
                on_click=lambda e, e_alvo=i: pular_para_eixo(e_alvo)
            )
        )
        
    # Retorna todos os botões empacotados em uma linha horizontal, alinhados à direita
    return ft.Row(controles, alignment=ft.MainAxisAlignment.END, spacing=10)