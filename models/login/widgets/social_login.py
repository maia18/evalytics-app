import flet as ft

def criar_login_social(cor_texto_secundario, cor_borda):
    """
    Cria a seção inferior do formulário de login destinada à autenticação por terceiros (Social Login).
    Inclui um divisor visual simétrico ("OU CONTINUE COM") e uma fileira de botões padronizados.
    
    Args:
        cor_texto_secundario (str): Cor do texto do divisor (geralmente um cinza neutro).
        cor_borda (str): Cor das linhas do divisor e do contorno dos botões sociais.
    """
    
    # === Construção do Divisor ===
    # Cria a quebra visual clássica: [Linha] OU CONTINUE COM [Linha]
    divisor = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            # A propriedade 'expand=True' faz com que a linha estique o máximo possível,
            # empurrando o texto perfeitamente para o centro.
            ft.Container(height=1, bgcolor=cor_borda, expand=True),
            
            # Texto central do divisor
            ft.Text(
                "OU CONTINUE COM", 
                size=12, 
                color=cor_texto_secundario, 
                weight=ft.FontWeight.W_500
            ),
            
            # Linha elástica do lado direito
            ft.Container(height=1, bgcolor=cor_borda, expand=True),
        ]
    )

    # === Estilização dos Botões ===
    # Centraliza as regras de estilo para que todos os botões fiquem uniformes (DRY - Don't Repeat Yourself)
    estilo_botao_social = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=4), # Bordas apenas levemente arredondadas (aspecto mais corporativo)
        side=ft.BorderSide(1, cor_borda),          # Contorno com a mesma cor das linhas do divisor
        padding=ft.padding.symmetric(vertical=15)  # Aumenta a área de clique vertical (padding superior e inferior)
    )

    # === Construção da Linha de Botões ===
    # Botões corrigidos utilizando 'content' no lugar de 'text' e 'icon' para maior flexibilidade de design
    botoes = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Distribui os botões ocupando as extremidades
        controls=[
            # Botão do Google (usando texto estilizado "G" no lugar do ícone nativo)
            ft.OutlinedButton(
                content=ft.Text("G", color="#111827", weight=ft.FontWeight.BOLD), 
                style=estilo_botao_social, 
                expand=True # Faz o botão crescer para preencher a Row (dividindo o espaço igualmente com os outros)
            ),
            
            # Espaçamento fixo entre botões em vez de usar 'spacing' na Row para maior controle
            ft.Container(width=10), 
            
            # Botão da Microsoft
            ft.OutlinedButton(
                content=ft.Icon(ft.Icons.WINDOW, color="#111827"), 
                style=estilo_botao_social, 
                expand=True
            ),
            
            ft.Container(width=10),
            
            # Botão da Apple
            ft.OutlinedButton(
                content=ft.Icon(ft.Icons.APPLE, color="#111827"),
                style=estilo_botao_social, 
                expand=True
            ),
        ]
    )

    # === Empacotamento Final ===
    # Retorna uma Coluna que agrupa o divisor e a fileira de botões
    return ft.Column(
        spacing=20, # Define a distância entre o texto "OU CONTINUE COM" e os botões
        controls=[
            ft.Container(height=10), # Margem de respiro para afastar esta seção do botão principal de Sign In
            divisor, 
            botoes
        ]
    )