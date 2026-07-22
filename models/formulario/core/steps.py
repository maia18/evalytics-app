from models.formulario.widgets.tela_sucesso import criar_tela_sucesso

# Contém as funções de navegação (steps) do formulário.
class FormularioStepsMixin:
    
    def pular_para_eixo(self, eixo_alvo):
        self.area_dinamica.opacity = 0
        self.page.update()
        
        for i, ind in enumerate(self.indicadores_ativos):
            if ind.get("eixo") == eixo_alvo:
                self.estado["indice_atual"] = i
                break
                
        self.atualizar_renderizacao()
        self.area_dinamica.opacity = 1
        self.page.update()

    def avancar(self, e=None):
        if self.estado["indice_atual"] < len(self.indicadores_ativos) - 1:
            self.area_dinamica.opacity = 0
            self.page.update()
            
            self.estado["indice_atual"] += 1
            self.atualizar_renderizacao()
            
            self.area_dinamica.opacity = 1
            self.page.update()
        else:
            self.area_central.content = criar_tela_sucesso(self.mudar_tela)
            self.page.update()

    def anterior(self, e=None):
        if self.estado["indice_atual"] > 0:
            self.area_dinamica.opacity = 0
            self.page.update()
            
            self.estado["indice_atual"] -= 1
            self.atualizar_renderizacao()
            
            self.area_dinamica.opacity = 1
            self.page.update()