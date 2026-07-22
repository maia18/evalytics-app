from components.layout.sidebar.sidebar_factory import criar_sidebar_desktop 

# Ajusta ativamente o layout da interface se adaptando à largura da janela do usuário
def ajustar_responsividade(page, sidebar_desktop, topbar, fechar_sidebar, dark_mode, mudar_tela): 
    if page.width < 700: # Dispositivos móveis ou telas pequenas
        sidebar_desktop.visible = False # Oculta a sidebar de desktop
        sidebar_desktop.width = 0 # Remove seu preenchimento de largura
        topbar.menu_button.visible = True # Habilita o botão 'hamburguer' da topbar para abrir a versão mobile
    else: # Tablets, Laptops e Monitores
        sidebar_desktop.visible = True # Traz a sidebar de desktop de volta à vista
        topbar.menu_button.visible = False # Esconde o botão de menu mobile
        fechar_sidebar() # Força o fechamento da versão mobile caso estivesse aberta durante o redimensionamento

        # Ajuste adaptativo extra: O menu diminui para modo ícone se a tela for média (entre 700px e 1100px)
        sidebar_desktop.width = 250 if page.width >= 1100 else 72 # 250px normal, 72px 'encolhido'
        sidebar_desktop.content = criar_sidebar_desktop( # Recria o conteúdo interno com as novas larguras
            dark_mode=dark_mode, # Repassa a preferência de cor
            mudar_tela=mudar_tela, # Repassa a função de clique/navegação
            collapsed=page.width < 1100 # Define propriedade collapsed como verdadeira em telas médias
        ).content 

    page.update() # Força a atualização da interface com os novos tamanhos