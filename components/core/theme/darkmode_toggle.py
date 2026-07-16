def toggle_dark_mode(page, dark_mode, mudar_tela, rota_atual, configurar_tema):
    dark_mode = not dark_mode
    page.is_dark_mode = dark_mode
    configurar_tema(page, dark_mode)
    page.update()

    if mudar_tela and rota_atual:
        mudar_tela(rota_atual)

    return dark_mode
