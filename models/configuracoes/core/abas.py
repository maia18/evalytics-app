import flet as ft 

def criar_abas(page, area_dinamica_indicadores, painel_seguranca, painel_banco): 
    """
    Cria a barra de navegação superior (tabs) e o container que exibirá os painéis correspondentes.
    """
    # Container dinâmico cujo 'content' será substituído ao clicar nas abas
    area_conteudo_aba = ft.Container(content=area_dinamica_indicadores, expand=True, padding=20) 

    def mudar_aba(e, painel_selecionado, btn_indicadores, btn_seguranca, btn_banco): 
        """Callback que injeta o novo painel no container e atualiza a cor dos botões para indicar a aba ativa."""
        area_conteudo_aba.content = painel_selecionado 
        
        # Aplica um fundo azul clarinho ('blue50') apenas no botão que corresponde ao painel selecionado
        btn_indicadores.bgcolor = "blue50" if painel_selecionado == area_dinamica_indicadores else "transparent" 
        btn_seguranca.bgcolor = "blue50" if painel_selecionado == painel_seguranca else "transparent" 
        btn_banco.bgcolor = "blue50" if painel_selecionado == painel_banco else "transparent" 
        page.update() 

    # Estilo base compartilhado entre todos os botões de aba
    estilo_btn_aba = ft.ButtonStyle( 
        color={"": "blue900"}, # Cor do texto azul escuro
        shape=ft.RoundedRectangleBorder(radius=8), # Bordas arredondadas
        padding=15 
    ) 

    # Instanciação dos três botões principais da navegação interna
    btn_indicadores = ft.TextButton( 
        "Indicadores", 
        icon=ft.Icons.RULE, 
        style=estilo_btn_aba, 
        on_click=lambda e: mudar_aba(e, area_dinamica_indicadores, btn_indicadores, btn_seguranca, btn_banco) 
    ) 

    btn_seguranca = ft.TextButton( 
        "Segurança", 
        icon=ft.Icons.SECURITY, 
        style=estilo_btn_aba, 
        on_click=lambda e: mudar_aba(e, painel_seguranca, btn_indicadores, btn_seguranca, btn_banco) 
    ) 

    btn_banco = ft.TextButton( 
        "Banco de Dados", 
        icon=ft.Icons.STORAGE, 
        style=estilo_btn_aba, 
        on_click=lambda e: mudar_aba(e, painel_banco, btn_indicadores, btn_seguranca, btn_banco) 
    ) 

    # Agrupa os botões em uma linha horizontal
    menu_abas = ft.Row([btn_indicadores, btn_seguranca, btn_banco], spacing=10) 

    return menu_abas, area_conteudo_aba 