import flet as ft

def criar_estilo_aba(ativo: bool, cor_primaria: str, cor_texto_inativo: str) -> ft.ButtonStyle:
    """
    Configura o estilo (Design System) compartilhado das abas Sign In / Sign Up.
        Retorna o estilo configurado dependendo se a aba está 'selecionada' (ativa) ou não.
    """
    
    return ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        
        # Cor da Fonte: Se estiver ativo ganha a cor primária, caso contrário ganha cinza
        color=cor_primaria if ativo else cor_texto_inativo,
        
        # Cor de Fundo: Se ativo, ganha a cor primária translúcida (10% de opacidade). 
        #   Se inativo, fica completamente transparente (misturando-se ao card)
        bgcolor=ft.Colors.with_opacity(0.1, cor_primaria) if ativo else ft.Colors.TRANSPARENT,
        
        # Zera qualquer borda padrão de botões do Material UI
        side=ft.BorderSide(0, ft.Colors.TRANSPARENT),
        
        # Remove o efeito de "ripple" (a ondinha cinza) ao passar o mouse ou segurar o clique.
        #   Para garantir um visual mais limpo, similar ao web design tradicional.
        overlay_color=ft.Colors.TRANSPARENT,
    )