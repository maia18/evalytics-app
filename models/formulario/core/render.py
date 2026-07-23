import flet as ft
from components.core.constants.texts import NOMES_EIXOS # Importa o dicionário que mapeia o número do eixo ao seu respectivo nome em texto
from models.formulario.widgets.card_pergunta import criar_card_pergunta # Importa a função que gera o bloco visual com a pergunta e as opções de resposta
from models.formulario.widgets.stepper_eixos import criar_stepper_eixos # Importa o indicador visual de etapas (os "pontinhos" ou steps no topo)

# Mixin responsável por construir e atualizar a interface de renderização do formulário.
class FormularioRenderMixin:
    """
    Extensão (Mixin) que lida exclusivamente com a atualização visual do formulário.
    A sua responsabilidade é ler o estado atual do Controller e refleti-lo na tela.
    """
    
    def atualizar_renderizacao(self):
        """
        Reconstrói os elementos visuais da tela (cabeçalho, pergunta atual e rodapé) 
        com base no índice atual do formulário.
        """
        
        # Verificação de segurança: se não houver indicadores a responder, avisa e interrompe
        if not self.indicadores_ativos:
            self.area_dinamica.controls = [ft.Text("Nenhum indicador ativo.", color="onSurfaceVariant")]
            self.page.update()
            return

        # Recupera os dados da pergunta atual com base no índice numérico armazenado no estado
        ind_atual = self.indicadores_ativos[self.estado["indice_atual"]]
        eixo_atual = ind_atual.get("eixo")

        # Filtra a lista completa para descobrir quantas perguntas existem APENAS dentro deste eixo atual
        inds_neste_eixo = [i for i in self.indicadores_ativos if i.get("eixo") == eixo_atual]
        
        # Calcula a posição relativa do usuário dentro deste eixo (ex: Pergunta 2 de 5)
        # O +1 é necessário porque o índice de listas no Python começa em 0
        posicao_neste_eixo = inds_neste_eixo.index(ind_atual) + 1
        total_neste_eixo = len(inds_neste_eixo)

        # Gera a barra de navegação por eixos passando a função de "pulo" como callback
        linha_stepper = criar_stepper_eixos(eixo_atual, self.pular_para_eixo)
        
        # Calcula a porcentagem geral de conclusão de toda a avaliação (para a ProgressBar)
        progresso_geral = (self.estado["indice_atual"] + 1) / len(self.indicadores_ativos)

        # === Montagem do Cabeçalho ===
        cabecalho = ft.Column(
            spacing=15,
            controls=[
                # Linha com o título da seção e os indicadores de bolinhas (Stepper)
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[ft.Text("Progresso da Avaliação", size=18, weight="bold", color="onSurface"), linha_stepper]
                ),
                # Barra de carregamento linear preenchida de acordo com progresso_geral
                ft.ProgressBar(value=progresso_geral, color="primary", bgcolor="surfaceVariant"),
                # Linha com o nome do eixo por extenso e o contador local (Pergunta X de Y)
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        # Tenta pegar o nome pelo ID, se falhar, escreve "Eixo X"
                        ft.Text(NOMES_EIXOS.get(eixo_atual, f"Eixo {eixo_atual}"), size=16, weight="bold", color="primary"),
                        ft.Text(f"Pergunta {posicao_neste_eixo} de {total_neste_eixo}", size=14, color="onSurfaceVariant")
                    ]
                ),
                ft.Divider(height=10, color="outlineVariant")
            ]
        )

        # === Montagem do Cartão Principal ===
        # Chama a função que desenha a pergunta em si e as opções, passando o estado para
        # que respostas anteriores possam ser recarregadas caso o usuário volte uma página
        card = criar_card_pergunta(self.page, ind_atual, self.estado)

        # === Montagem do Rodapé (Botões) ===
        # Botão de cancelamento destacado com cor de alerta (vermelho/error)
        btn_cancelar = ft.TextButton("Cancelar", icon=ft.Icons.CANCEL, icon_color="error", style=ft.ButtonStyle(color="error"), on_click=lambda _: self.mudar_tela("/inicio"))
        
        # Botão para recuar. A lógica `disabled=(self.estado["indice_atual"] == 0)` 
        # impede que o usuário tente voltar se já estiver na primeira pergunta.
        btn_anterior = ft.ElevatedButton("Anterior", icon=ft.Icons.ARROW_BACK, bgcolor="surfaceVariant", color="onSurface", disabled=(self.estado["indice_atual"] == 0), on_click=self.anterior)
        
        # Lógica condicional: Se for o último índice, o botão vira "Finalizar" e fica verde
        eh_ultima_pergunta = (self.estado["indice_atual"] == len(self.indicadores_ativos) - 1)
        
        btn_avancar = ft.ElevatedButton(
            "Finalizar" if eh_ultima_pergunta else "Avançar", 
            icon=ft.Icons.CHECK if eh_ultima_pergunta else ft.Icons.ARROW_FORWARD, 
            bgcolor="green" if eh_ultima_pergunta else "primary", 
            color="white" if eh_ultima_pergunta else "onPrimary", 
            on_click=self.avancar
        )

        # Envolve os botões em um container elegante estilo "painel inferior" com sombra
        rodape = ft.Container(
            padding=20,
            bgcolor="surface",
            border_radius=8,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="shadow"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                controls=[
                    btn_cancelar, 
                    ft.Row([btn_anterior, btn_avancar], spacing=10) # Agrupa os botões de navegação à direita
                ]
            )
        )

        # === Atualização da Interface ===
        # Substitui todo o conteúdo antigo da área pela nova renderização completa
        self.area_dinamica.controls = [cabecalho, card, rodape]
        self.page.update()