from models.formulario.widgets.tela_sucesso import criar_tela_sucesso

# Contém as funções de navegação (steps) do formulário.
class FormularioStepsMixin:
    """
    Extensão (Mixin) que concentra a lógica de transição entre as etapas do formulário.
    Gerencia o índice atual da pergunta e orquestra as animações de troca de tela.
    """
    
    def pular_para_eixo(self, eixo_alvo):
        """
        Navega diretamente para a primeira pergunta de um eixo específico.
        Útil para quando o usuário clica nos marcadores superiores (steppers).
        """
        
        # Efeito de esmaecimento (fade out): Deixa a área invisível antes de trocar o conteúdo
        self.area_dinamica.opacity = 0
        self.page.update()
        
        # Percorre a lista de indicadores ativos para encontrar o primeiro que pertença ao eixo desejado
        for i, ind in enumerate(self.indicadores_ativos):
            if ind.get("eixo") == eixo_alvo:
                # Atualiza o estado central com o novo índice ao encontrar a correspondência
                self.estado["indice_atual"] = i 
                break # Interrompe o laço assim que encontra a primeira ocorrência
                
        # Aciona o renderizador (do FormularioRenderMixin) para montar o visual da nova pergunta
        self.atualizar_renderizacao()
        
        # Efeito de surgimento (fade in): Devolve a opacidade após o novo conteúdo estar pronto
        self.area_dinamica.opacity = 1
        self.page.update()

    def avancar(self, e=None):
        """Avança para a próxima pergunta ou encerra o formulário se for a última etapa."""
        
        # Verifica se ainda existem perguntas pela frente na lista
        if self.estado["indice_atual"] < len(self.indicadores_ativos) - 1:
            
            # Transição: Fade out
            self.area_dinamica.opacity = 0
            self.page.update()
            
            # Incrementa o índice em +1 (avança a etapa)
            self.estado["indice_atual"] += 1
            
            # Remonta a interface com a próxima pergunta
            self.atualizar_renderizacao() 
            
            # Transição: Fade in
            self.area_dinamica.opacity = 1
            self.page.update()
            
        else:
            # Se for o último índice, o botão 'Avançar' atuou como 'Finalizar'.
            # Substitui toda a área central da tela pelo componente de sucesso final.
            self.area_central.content = criar_tela_sucesso(self.mudar_tela)
            self.page.update()

    def anterior(self, e=None):
        """Retorna para a pergunta anterior, garantindo que não ocorram erros de índice."""
        
        # Trava de segurança para não tentar acessar índices negativos
        if self.estado["indice_atual"] > 0:
            
            # Transição: Fade out
            self.area_dinamica.opacity = 0
            self.page.update()
            
            # Decrementa o índice em -1 (retrocede a etapa)
            self.estado["indice_atual"] -= 1
            
            # Remonta a interface com a pergunta anterior
            self.atualizar_renderizacao() 
            
            # Transição: Fade in
            self.area_dinamica.opacity = 1
            self.page.update()