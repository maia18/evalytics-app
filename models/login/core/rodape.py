import flet as ft

def criar_rodape_termos(cor_texto_secundario, cor_primaria):
    """
    Cria o rodapé da tela de login/cadastro contendo o aviso de concordância 
    com os Termos de Serviço e a Política de Privacidade.
    
    Args:
        cor_texto_secundario (str): Cor usada para o texto base da frase.
        cor_primaria (str): Cor de destaque (brand color) usada para simular os links clicáveis.
    """
    
    return ft.Container(
        # Aplica uma margem superior para desgrudar o rodapé do cartão principal de login
        margin=ft.Margin.only(top=10),
        
        # O controle principal de texto
        content=ft.Text(
            text_align=ft.TextAlign.CENTER, # Centraliza todo o parágrafo
            size=12, # Tamanho de fonte pequeno, típico de rodapés (fine print)
            
            # A propriedade 'spans' permite formatar pedaços específicos (substrings) 
            # de um mesmo bloco de texto de maneiras diferentes, ideal para criar "falsos links"
            spans=[
                # Primeiro trecho: Texto normal
                ft.TextSpan(
                    "By signing up, you agree to our ", 
                    ft.TextStyle(color=cor_texto_secundario)
                ),
                
                # Segundo trecho: Destaque para "Termos de Serviço"
                ft.TextSpan(
                    "Terms of Service", 
                    # Usa a cor primária e um peso de fonte médio (W_500) para destacar a palavra
                    ft.TextStyle(color=cor_primaria, weight=ft.FontWeight.W_500)
                ),
                
                # Terceiro trecho: Conectivo "and" em texto normal
                ft.TextSpan(
                    " and ", 
                    ft.TextStyle(color=cor_texto_secundario)
                ),
                
                # Quarto trecho: Destaque para "Política de Privacidade"
                ft.TextSpan(
                    "Privacy Policy", 
                    ft.TextStyle(color=cor_primaria, weight=ft.FontWeight.W_500)
                ),
            ],
        )
    )