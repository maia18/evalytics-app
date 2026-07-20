import flet as ft

def obter_funcao_alternar(btn_aba_signin, btn_aba_signup, campo_nome, opcoes_extras, btn_login, COR_TEXTO_TITULO, COR_CARD, COR_PRIMARIA):
    
    # Esta é a sua função exata, agora encapsulada
    def alternar_modo(e):
        is_signup = (e.control.data == "signup")
        
        estilo_ativo = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
            color=COR_TEXTO_TITULO,
            bgcolor=COR_CARD,
            side=ft.border.BorderSide(1, COR_PRIMARIA)
        )
        
        estilo_inativo = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
            color=COR_TEXTO_TITULO,
            bgcolor=COR_CARD,
            side=ft.border.BorderSide(1, "transparent")
        )
        
        btn_aba_signin.style = estilo_inativo if is_signup else estilo_ativo
        btn_aba_signup.style = estilo_ativo if is_signup else estilo_inativo
        
        campo_nome.visible = is_signup
        opcoes_extras.visible = not is_signup
        
        btn_login.text = "Create account" if is_signup else "Sign In"
        
        e.page.update()
        
    # Retornamos a função pronta para ser usada no on_click
    return alternar_modo