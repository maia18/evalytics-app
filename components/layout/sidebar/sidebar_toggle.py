def toggle_sidebar(page, sidebar_mobile_aberta, abrir_sidebar, fechar_sidebar): 
    """
    Executa a inversão (toggle) de estado da visibilidade do menu Mobile, chamando os respectivos callbacks (funções passadas como argumento).
    """
    
    # Bloqueio de comportamento indesejado se a tela atual for classificada como Larga
    if page.width >= 900: 
        return sidebar_mobile_aberta # Devolve o estado inalterado
        
    # Quando o menu está à vista e o gatilho é disparado, solicitamos fechamento
    if sidebar_mobile_aberta: 
        fechar_sidebar() # Aciona animação de fechar
        return False # Confirmação que agora está oculto
        
    # Vice-versa: Puxa o menu para a tela caso não esteja visível
    else: 
        abrir_sidebar() # Aciona animação de abrir e fundo modal cinza
        return True # Confirmação de que está visível