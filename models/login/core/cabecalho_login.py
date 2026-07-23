import flet as ft

def criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO):
    """
    Cria o componente de cabeçalho da tela de login, contendo o logotipo da aplicação 
    e as mensagens de boas-vindas.
    
    Args:
        COR_TEXTO_TITULO (str): Cor principal usada para o título de destaque.
        COR_TEXTO_SECUNDARIO (str): Cor mais suave (geralmente cinza) usada para o subtítulo explicativo.
    """
    
    # Retorna uma Coluna para empilhar o logo e os textos verticalmente
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza perfeitamente todos os itens no eixo horizontal
        spacing=10, # Define um respiro padrão de 10 pixels entre a imagem, o título e o subtítulo
        controls=[
            # Container que abriga a imagem do logotipo
            ft.Container(
                # Carrega o logo da pasta local 'imgs'. 
                # O fit="CONTAIN" garante que a imagem não seja esticada ou cortada, mantendo sua proporção original dentro do espaço de 60x60.
                content=ft.Image(src="imgs/logo.png", width=60, height=60, fit="CONTAIN")
            ),
            
            # Texto principal de boas-vindas (Título) em destaque com fonte maior e negrito
            ft.Text("Bem-vindo ao Evalytics", size=28, weight="bold", color=COR_TEXTO_TITULO),
            
            # Texto de apoio (Subtítulo) descrevendo o propósito da tela atual
            ft.Text(
                "Faça login para gerenciar as avaliações institucionais.",
                size=16,
                color=COR_TEXTO_SECUNDARIO,
                text_align=ft.TextAlign.CENTER # Garante que o texto fique bem alinhado caso a tela seja muito estreita e ele quebre para uma segunda linha
            )
        ]
    )
