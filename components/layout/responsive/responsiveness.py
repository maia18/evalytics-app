from components.layout.sidebar.sidebar_factory import criar_sidebar_desktop

def ajustar_responsividade(page, sidebar_desktop, topbar, fechar_sidebar, dark_mode, mudar_tela):
    if page.width < 700:
        sidebar_desktop.visible = False
        sidebar_desktop.width = 0
        topbar.menu_button.visible = True
    else:
        sidebar_desktop.visible = True
        topbar.menu_button.visible = False
        fechar_sidebar()

        sidebar_desktop.width = 250 if page.width >= 1100 else 72
        sidebar_desktop.content = criar_sidebar_desktop(
            dark_mode=dark_mode,
            mudar_tela=mudar_tela,
            collapsed=page.width < 1100
        ).content

    page.update()
