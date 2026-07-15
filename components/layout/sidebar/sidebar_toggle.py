def toggle_sidebar(page, sidebar_mobile_aberta, abrir_sidebar, fechar_sidebar):
    if page.width >= 900:
        return sidebar_mobile_aberta
    if sidebar_mobile_aberta:
        fechar_sidebar()
        return False
    else:
        abrir_sidebar()
        return True
