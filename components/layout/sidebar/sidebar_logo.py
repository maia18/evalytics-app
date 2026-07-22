import flet as ft 
from components.core.constants.constants import * 

# Cria logo da sidebar
def criar_logo(cores, compact=False): 
    """
    Cria o cabeçalho da marca na parte superior do menu.
    Responde à flag de menu compactado para omitir o texto da marca se necessário.
    """
    
    if compact: 
        # Retorna apenas o ícone principal sem textos extras
        return ft.Container( 
            content=ft.Icon(ft.Icons.ANALYTICS, color=COR_PRIMARIA, size=28), # Define o ícone representativo (Analytics) no tom primário roxo da marca
            padding=8, 
            alignment=ft.Alignment.CENTER, # Centraliza no pequeno espaço de 72px disponível
        ) 
    else: 
        # Retorna a logo padrão em layout horizontal
        return ft.Container( 
            content=ft.Row( 
                spacing=10, # Separa as letras do símbolo
                controls=[ 
                    ft.Icon(ft.Icons.ANALYTICS, color=COR_PRIMARIA, size=28), # Ícone marca
                    ft.Text("Evalytics", size=18, weight="bold", color=cores[TEXTO_PRINCIPAL]), # Nome renderizado com peso em negrito para destacar
                ], 
                vertical_alignment=ft.CrossAxisAlignment.CENTER, # Ambos, texto e ícone, ficam no mesmo centro geométrico na vertical
            ), 
            padding=15, 
            height=60, # Tranca a altura do logo para manter a proporção da gaveta
        ) 