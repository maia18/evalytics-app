# Alterna entre os temas claro e escuro (Dark Mode/Light Mode) da aplicação.
def toggle_dark_mode(page, dark_mode, mudar_tela, rota_atual, configurar_tema):
    dark_mode = not dark_mode # Inverte o estado atual (se for True vira False, e vice-versa)
    
    page.is_dark_mode = dark_mode # Aplica o novo estado na propriedade da página (atualizando a flag interna)
    
    configurar_tema(page, dark_mode) # Chama a função auxiliar para configurar as cores e estilos baseados no novo tema
    
    page.update()

    # Verifica se a função de mudança de tela e a rota atual foram fornecidas
    if mudar_tela and rota_atual:
        '''
        Recarrega ou navega para a tela atual para garantir que os componentes sejam recriados/atualizados com o novo tema
        '''
        mudar_tela(rota_atual)

    return dark_mode # Retorna o novo estado para que possa ser armazenado/atualizado na variável externa