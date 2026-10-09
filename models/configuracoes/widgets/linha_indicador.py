import flet as ft
from typing import Callable
from components.core.constants.constants import (
    CARD,
    BORDA,
    COR_PRIMARIA,
    SUCESSO,
    AVISO,
)

def criar_linha_indicador(
    item: dict,
    abrir_modal_criterios: Callable[..., None],
    abrir_modal_edicao: Callable[..., None],
    preparar_exclusao: Callable[[dict], None],
    cores: dict[str, str],
) -> ft.Container:
    """
    Renderiza um card individual (linha) para um indicador na lista.
        Possui área clicável para abrir critérios e botões de ação isolados (editar/excluir).
    """

    '''
    Lógica de formatação condicional: 
        Determina a cor da "etiqueta" com base no status salvo no banco.
    '''
    cor_status = (
        cores[SUCESSO]
        if item.get("status") == "ATIVO"
        else cores[AVISO]
    )

    return ft.Container(
        padding=15,
        bgcolor=cores[CARD],

        # Borda sutil e arredondada envolvendo toda a linha.
        # Alternativa mais curta do Flet para isso seria: border=ft.border.all(1, cores[BORDA])
        border=ft.Border(
            top=ft.BorderSide(1, cores[BORDA]),
            bottom=ft.BorderSide(1, cores[BORDA]),
            left=ft.BorderSide(1, cores[BORDA]),
            right=ft.BorderSide(1, cores[BORDA]),
        ),
        border_radius=8,

        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                
                # 1. BLOCO DO TÍTULO (Clicável)
                ft.Container(
                    expand=True, # Diz a este contêiner para ocupar todo o espaço horizontal disponível na Row empurrando a tag e os botões para a extremidade direita. 
                    
                    content=ft.Text(
                        item["titulo"],
                        size=15,
                        weight=ft.FontWeight.W_500,
                        color=cores[COR_PRIMARIA],
                    ),
                    
                    # Ao clicar no título, abre o modal de critérios. 
                    on_click=lambda e, i=item: abrir_modal_criterios(e, i), 
                ),

                # 2. ETIQUETA DE STATUS (Badge)
                ft.Container(
                    bgcolor=cor_status,
                    padding=5,
                    border_radius=4,
                    content=ft.Text(
                        item.get("status", "ATIVO"), # Fallback seguro caso 'status' não exista no dict
                        size=12,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),

                # 3. BLOCO DE AÇÕES (Ícones de Edição e Exclusão)
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=cores[COR_PRIMARIA],
                            tooltip="Editar",
                            on_click=lambda e, i=item: abrir_modal_edicao(e, i),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_700,
                            tooltip="Excluir",
                            on_click=lambda e, i=item: preparar_exclusao(i),
                        ),
                    ],
                ),
            ],
        ),
    )