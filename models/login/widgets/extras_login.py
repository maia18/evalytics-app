import flet as ft

def criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA):
    """
    Cria a linha auxiliar de opções do formulário de login, contendo o checkbox 
    para "Lembrar-me" (Keep me signed in) e o link de recuperação de senha.
    
    Args:
        COR_TEXTO_SECUNDARIO (str): Cor do texto do checkbox (geralmente um tom neutro/cinza).
        COR_PRIMARIA (str): Cor de destaque (brand color) usada para preencher o checkbox e colorir o link.
    """
    
    # Retorna uma linha (Row) para organizar os elementos lado a lado horizontalmente
    return ft.Row(
        # SPACE_BETWEEN empurra o primeiro controle para a extrema esquerda 
        # e o último para a extrema direita, ocupando o espaço vazio no meio
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            # Controle interativo de caixa de seleção (Checkbox)
            ft.Checkbox(
                label="Lembrar-me", # Texto exibido ao lado da caixa
                label_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO, size=14), # Define o tamanho e a cor do texto do label
                fill_color=COR_PRIMARIA # Cor interna aplicada na caixa quando ela é clicada/marcada
            ),
            
            # Botão de texto simples (sem preenchimento de fundo) atuando como um link/hyperlink
            ft.TextButton(
                "Esqueceu a senha?", 
                style=ft.ButtonStyle(color=COR_PRIMARIA) # Aplica a cor primária para indicar que o texto é clicável
            )
        ]
    )
