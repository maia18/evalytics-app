import flet as ft

def obter_funcao_alternar(btn_aba_signin, btn_aba_signup, campo_nome, opcoes_extras, btn_login, COR_TEXTO_TITULO, COR_CARD, COR_PRIMARIA):
    """
    Fábrica de função (Closure) que constrói e retorna o callback responsável por alternar
    o estado da tela entre 'Sign In' (Login) e 'Sign Up' (Cadastro).
    
    Args:
        btn_aba_signin: A referência do botão/aba de login.
        btn_aba_signup: A referência do botão/aba de cadastro.
        campo_nome: O campo de texto para o nome do usuário.
        opcoes_extras: O bloco contendo "Lembrar de mim" e "Esqueci a senha".
        btn_login: O botão principal de ação do formulário.
        COR_TEXTO_TITULO, COR_CARD, COR_PRIMARIA: Constantes de cores do tema.
    """
    
    # Esta é a função interna que será de fato atrelada ao evento 'on_click' das abas
    def alternar_modo(e):
        # Descobre qual aba foi clicada verificando o atributo 'data' do controle que disparou o evento
        is_signup = (e.control.data == "signup")
        
        # Define o estilo visual de uma aba SELECIONADA (destaque apenas por fundo/cor de texto, sem borda)
        estilo_ativo = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            color=COR_PRIMARIA,
            bgcolor=ft.Colors.with_opacity(0.1, COR_PRIMARIA),
            side=ft.BorderSide(0, ft.Colors.TRANSPARENT), # Sem contorno
            overlay_color=ft.Colors.TRANSPARENT, # Sem overlay de foco/hover
        )
        
        # Define o estilo visual de uma aba INATIVA (transparente, sem borda)
        estilo_inativo = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            color=COR_TEXTO_TITULO,
            bgcolor=ft.Colors.TRANSPARENT,
            side=ft.BorderSide(0, ft.Colors.TRANSPARENT), # Sem contorno
            overlay_color=ft.Colors.TRANSPARENT, # Sem overlay de foco/hover
        )
        
        # Aplica os estilos dependendo de quem foi clicado usando operadores ternários
        btn_aba_signin.style = estilo_inativo if is_signup else estilo_ativo
        btn_aba_signup.style = estilo_ativo if is_signup else estilo_inativo
        
        # Lógica de interface: 
        # - O campo 'Nome' só faz sentido se o usuário estiver criando uma conta (Sign Up)
        campo_nome.visible = is_signup
        
        # - As opções 'Lembrar de mim' / 'Esqueci a senha' só fazem sentido no Login (Sign In)
        opcoes_extras.visible = not is_signup
        
        # Atualiza a chamada para ação (Call to Action) do botão principal
        btn_login.text = "Create account" if is_signup else "Sign In"
        
        # Comunica à página que os elementos visuais foram alterados e precisam ser redesenhados
        e.page.update()
        
    # Retornamos a função pronta e "abastecida" com as referências, para ser usada no on_click
    return alternar_modo