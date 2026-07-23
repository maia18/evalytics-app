import flet as ft

def criar_card_login(cabecalho_abas, campo_nome, campo_email, campo_senha, opcoes_extras, btn_login, secao_social, COR_CARD):
    """
    Constrói o painel central (Card) que agrupa todos os elementos do formulário de autenticação.
    Atua como um contêiner estilizado para manter a interface limpa e centralizada.
    
    Args:
        cabecalho_abas: O seletor de abas (Sign In / Sign Up).
        campo_nome, campo_email, campo_senha: Os inputs de texto do usuário.
        opcoes_extras: Elementos auxiliares (Lembrar de mim, Esqueci a senha).
        btn_login: O botão principal de submissão do formulário.
        secao_social: A área com botões de login via redes sociais/terceiros.
        COR_CARD: A cor de fundo do cartão, adaptável ao tema claro/escuro.
    """
    return ft.Container(
        width=420, # Define uma largura fixa ideal para formulários de login, evitando que fiquem esticados em monitores grandes
        bgcolor=COR_CARD, # Aplica a cor de fundo adaptativa
        padding=40, # Espaçamento interno generoso (respiro) para afastar os campos das bordas do cartão
        border_radius=12, # Suaviza as quinas do painel com um arredondamento moderno
        
        # Cria uma sombra sutil projetada sob o cartão para dar a sensação de elevação (profundidade/3D)
        shadow=ft.BoxShadow(blur_radius=15, color="black12"), 
        
        # Empilha todos os componentes recebidos verticalmente
        content=ft.Column(
            spacing=20, # Mantém uma distância consistente e harmônica de 20px entre cada bloco do formulário
            controls=[
                cabecalho_abas, 
                campo_nome, 
                campo_email, 
                campo_senha, 
                opcoes_extras, 
                btn_login, 
                secao_social
            ]
        )
    )