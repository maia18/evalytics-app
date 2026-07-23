import flet as ft
from components.core.constants.constants import *

def criar_coluna_grafico(layout, nome, nota, cor):
    """
    Desenha uma barra vertical individual do gráfico, calculando sua altura baseada na nota.
    """
    
    # Cálculo matemático para descobrir a altura em pixels: 
    # Divide a nota pela nota máxima (5.0) para obter a porcentagem, e multiplica pela Altura Máxima definida nas constantes.
    altura_barra = (nota / 5.0) * ALTURA_MAX
    
    return ft.Column(
        alignment=ft.MainAxisAlignment.END, # Empurra os itens para o fundo (faz as barras crescerem de baixo para cima)
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza os rótulos em relação à barra
        spacing=8,
        controls=[
            # Exibe o valor numérico acima da barra com uma casa decimal
            ft.Text(f"{nota:.1f}", size=12, weight="bold", color="grey"),
            
            # O "corpo" da barra do gráfico
            ft.Container(
                width=40, # Largura fixa da barra
                height=altura_barra, # Altura calculada dinamicamente
                bgcolor=cor, # Cor recebida por parâmetro
                border_radius=4, # Bordas levemente arredondadas no topo e na base
                tooltip=f"{nome}: {nota:.1f} / 5.0" # Exibe dica interativa ao passar o mouse por cima da barra
            ),
            
            # Rótulo com o nome do eixo abaixo da barra
            ft.Text(nome, size=12, weight="w500", color=layout.cores[TEXTO_PRINCIPAL])
        ]
    )

def criar_grafico_eixos(layout, medias_eixos, nomes_eixos, cores_barras):
    """
    Constrói o painel completo do gráfico, incluindo o título e iterando sobre os dados para gerar as barras.
    """
    barras_grafico = []
    
    # Laço de repetição percorrendo os dados simulados recebidos
    for i, (eixo_id, nota) in enumerate(medias_eixos.items()):
        # Pega o nome no dicionário ou usa um fallback genérico "Eixo X
        nome = nomes_eixos.get(eixo_id, f"Eixo {eixo_id}")
        # Aplica a cor garantindo que não vai dar erro de índice se houver mais barras do que cores mapeadas (usando módulo %)
        cor = cores_barras[i % len(cores_barras)]
        
        # Gera a barra visual e anexa na lista de controles
        barras_grafico.append(criar_coluna_grafico(layout, nome, nota, cor))

    # Configuração explícita das 4 bordas para desenhar o quadrado ao redor do painel do gráfico
    borda_grafico = ft.Border(
        top=ft.BorderSide(1, layout.cores[BORDA]),
        bottom=ft.BorderSide(1, layout.cores[BORDA]),
        left=ft.BorderSide(1, layout.cores[BORDA]),
        right=ft.BorderSide(1, layout.cores[BORDA])
    )

    return ft.Container(
        bgcolor=layout.cores[CARD], # Usa a cor dinâmica do tema
        padding=30,
        border_radius=8,
        border=borda_grafico, # Aplica o contorno criado acima
        content=ft.Column(
            spacing=20,
            controls=[
                # Cabeçalho interno do gráfico
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text("Desempenho Médio por Eixo", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
                        ft.Text("Médias das avaliações separadas por categoria (Escala 5.0).", size=14, color="grey"),
                    ]
                ),
                # Área de plotagem (desenho) das barras
                ft.Container(
                    height=260, # Limita a altura total dessa caixa de desenho
                    padding=20,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND, # Distribui as barras com espaço igual ao redor delas
                        vertical_alignment=ft.CrossAxisAlignment.END, # Alinha todas as colunas pela sua base
                        controls=barras_grafico # Injeta a lista gerada no for loop
                    )
                )
            ]
        )
    )
