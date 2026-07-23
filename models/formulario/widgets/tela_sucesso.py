import flet as ft

def criar_tela_sucesso(mudar_tela):
    """
    Renderiza a tela final de agradecimento exibida após o usuário preencher todas as etapas do formulário.
    """
    
    # Retorna uma coluna que empilha os elementos verticalmente e os centraliza na tela
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza os itens no eixo horizontal
        spacing=20, # Define o espaço padrão de 20 pixels entre cada elemento da coluna
        controls=[
            # Container vazio usado apenas como "espaçador" para empurrar o conteúdo um pouco mais para baixo
            ft.Container(height=50), 
            
            # Ícone grande de "Check" (Verificado) em verde para transmitir sucesso e conclusão
            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="green", size=80),
            
            # Título principal de feedback
            ft.Text("Avaliação Enviada!", size=28, weight="bold", color="onSurface"),
            
            # Mensagem de agradecimento com quebra de linha (\n) para melhor legibilidade
            ft.Text(
                "Muito obrigado pelo seu tempo e contribuição.\nSuas respostas foram registradas com sucesso.",
                text_align=ft.TextAlign.CENTER, # Garante que as duas linhas do texto fiquem centralizadas
                color="onSurfaceVariant" # Cor de contraste mais suave definida pelo tema
            ),
            
            # Mais um espaçador vazio antes do botão
            ft.Container(height=20),
            
            # Botão de retorno que aciona o callback de roteamento, levando o usuário de volta à página inicial
            ft.ElevatedButton("Voltar para o Painel", on_click=lambda _: mudar_tela("/inicio"))
        ]
    )