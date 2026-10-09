import flet as ft
from components.core.constants.constants import (
    COR_PRIMARIA, 
    CARD_SECUNDARIO, 
    TEXTO_PRINCIPAL,


)
def criar_abas(
    page: ft.Page,
    area_dinamica_indicadores: ft.Container,
    painel_seguranca: ft.Container,
    painel_banco: ft.Container,
    cores: dict[str, str],
) -> tuple[ft.Row, ft.Container]:
    """
    Cria uma estrutura customizada de navegação por abas.
        O segredo desta abordagem é ter um 'Container Alvo' (area_conteudo_aba) que apenas troca o seu conteúdo interno quando um botão é clicado.
    """
    
    # Define qual será o componente inicial renderizado
    area_conteudo_aba = ft.Container(
        content=area_dinamica_indicadores, 
        expand=True, 
        padding=20,
    )

    def mudar_aba(
        e: ft.ControlEvent,
        painel_selecionado: ft.Control,
        btn_indicadores: ft.TextButton,
        btn_seguranca: ft.TextButton,
        btn_banco: ft.TextButton,
    ) -> None:
        """Lida com a lógica de troca de painel e atualização visual dos botões."""
        
        # 1. Substitui o conteúdo visual pelo painel associado à aba clicada
        area_conteudo_aba.content = painel_selecionado

        # 2. Dicionário vinculando cada botão ao seu respectivo painel
        botoes = {
            btn_indicadores: area_dinamica_indicadores,
            btn_seguranca: painel_seguranca,
            btn_banco: painel_banco,
        }

        # 3. Varre todos os botões e atualiza a cor deles
        for botao, painel in botoes.items():
            ativo = (painel_selecionado == painel) # Retorna True ou False

            botao.style = ft.ButtonStyle(
                # Muda a cor da letra e do fundo se a aba for a atual
                color=cores[COR_PRIMARIA] if ativo else cores[TEXTO_PRINCIPAL],
                bgcolor=cores[CARD_SECUNDARIO] if ativo else ft.Colors.TRANSPARENT,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=15,
            )

        # Força o Flet a redesenhar a tela inteira para aplicar as novas cores e painel
        page.update()

    # Estilo base padrão (quando o botão não está selecionado)
    estilo_btn_aba = ft.ButtonStyle(
        color=cores[TEXTO_PRINCIPAL],
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
    )
    
    # Instanciação dos botões usando um lambda para injetar seus respectivos painéis e referências
    btn_indicadores = ft.TextButton(
        "Indicadores", icon=ft.Icons.RULE, style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, area_dinamica_indicadores, btn_indicadores, btn_seguranca, btn_banco),
    )
    btn_seguranca = ft.TextButton(
        "Segurança", icon=ft.Icons.SECURITY, style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, painel_seguranca, btn_indicadores, btn_seguranca, btn_banco),
    )
    btn_banco = ft.TextButton(
        "Banco de Dados", icon=ft.Icons.STORAGE, style=estilo_btn_aba,
        on_click=lambda e: mudar_aba(e, painel_banco, btn_indicadores, btn_seguranca, btn_banco),
    )

    menu_abas = ft.Row([btn_indicadores, btn_seguranca, btn_banco], spacing=10)
    
    return menu_abas, area_conteudo_aba # Retorna o cabeçalho (menu) e o contêiner de conteúdo para o Layout Principal organizar