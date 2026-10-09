import flet as ft
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    SURFACE, 
    COR_PRIMARIA,
)
from components.layout.topbar.core.notifications.notifications import (
    listar_notificacoes,
    contar_nao_lidas,
    marcar_todas_como_lidas,
)

def criar_componentes_notificacoes(page: ft.Page, cores: dict[str, str]):
    """
    Constrói a interface completa do sistema de notificações superior (Sino + Painel).
        Retorna múltiplos componentes que serão ancorados na Topbar pelo Layout Principal.
    """
    
    # Busca o estado inicial do banco de dados/memória
    notificacoes = listar_notificacoes()
    quantidade_nao_lidas = contar_nao_lidas()

    # 1. O Badge (Bolinha vermelha com o número de mensagens)
    badge_notificacoes = ft.Container(
        width=16, height=16, 
        right=1, top=1, # Posicionamento absoluto (só funciona porque estará dentro de um Stack)
        bgcolor="#EF4444", 
        border_radius=8,
        alignment=ft.Alignment.CENTER, 
        visible=quantidade_nao_lidas > 0, # Só aparece se houver mensagens não lidas
        content=ft.Text(str(quantidade_nao_lidas), size=9, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    )

    # 2. O Painel Flutuante (Caixa onde a lista de notificações aparece)
    painel_notificacoes = ft.Container(
        width=320, height=500, 
        visible=False, # Nasce escondido
        top=66, right=66, # Fica ancorado próximo ao canto superior direito da tela
        bgcolor=cores[SURFACE], 
        border_radius=12, padding=0,
        shadow=ft.BoxShadow(blur_radius=20, spread_radius=1, color="#33000000")
    )

    botao_notificacoes = ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE, tooltip="Notificações")

    '''
    # =========================================================================
    # LÓGICA DE INTERAÇÃO (ABRIR/FECHAR)
    # =========================================================================
    '''

    def fechar_painel(e=None):
        painel_notificacoes.visible = False
        botao_notificacoes.icon = ft.Icons.NOTIFICATIONS_NONE
        page.update()

    def alternar_painel(e=None):
        painel_notificacoes.visible = not painel_notificacoes.visible
        botao_notificacoes.icon = ft.Icons.NOTIFICATIONS if painel_notificacoes.visible else ft.Icons.NOTIFICATIONS_NONE # Muda o ícone do sino de "vazado" para "preenchido" quando o painel está aberto
        page.update()

    botao_notificacoes.on_click = alternar_painel

    '''
    # =========================================================================
    # RENDERIZAÇÃO DA LISTA DE ITENS
    # =========================================================================
    '''

    def criar_itens_notificacoes(notificacoes_atualizadas: list[dict]) -> list[ft.Control]:
        """Gera as linhas visuais (cards) para cada notificação recebida."""
        itens = []
        for notificacao in notificacoes_atualizadas:
            itens.append(
                ft.Container(
                    padding=12,
                    content=ft.Row(
                        spacing=12, 
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            # Ícone circular estilizado da notificação
                            ft.Container(
                                width=34, height=34, border_radius=8, bgcolor=cores[SURFACE],
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(notificacao["icone"], size=18, color=COR_PRIMARIA)
                            ),
                            # Textos (Título, Descrição truncada e Tempo)
                            ft.Column(
                                spacing=2, expand=True,
                                controls=[
                                    ft.Text(notificacao["titulo"], size=13, weight=ft.FontWeight.BOLD, color=cores[TEXTO_PRINCIPAL]),
                                    ft.Text(notificacao["descricao"], size=11, color=ft.Colors.GREY, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(notificacao["tempo"], size=10, color=ft.Colors.GREY),
                                ]
                            )
                        ]
                    )
                )
            )
        return itens

    lista_notificacoes = ft.Column(spacing=0, controls=criar_itens_notificacoes(notificacoes))

    def atualizar_lista_notificacoes(novas_notificacoes: list[dict]) -> None:
        """Permite que o sistema injete novas mensagens na UI em tempo real."""
        lista_notificacoes.controls = criar_itens_notificacoes(novas_notificacoes)

    def marcar_como_lidas(e=None):
        marcar_todas_como_lidas()
        badge_notificacoes.visible = False
        badge_notificacoes.content = ft.Text("0", size=9, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        fechar_painel()

    # Preenche o esqueleto do painel criado no passo 2
    painel_notificacoes.content = ft.Column(
        expand=True, spacing=0,
        controls=[
            # Cabeçalho do Painel
            ft.Container(
                padding=16,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Notificações", size=15, weight=ft.FontWeight.BOLD, color=cores[TEXTO_PRINCIPAL]),
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_size=18, tooltip="Fechar", on_click=fechar_painel)
                    ]
                )
            ),
            ft.Divider(height=1),
            ft.ListView(expand=True, spacing=0, controls=[lista_notificacoes], scroll=ft.ScrollMode.AUTO), # Corpo rolável com as mensagens
            ft.Divider(height=1),
            ft.Container(padding=12, alignment=ft.Alignment.CENTER, content=ft.TextButton("Marcar como lidas", on_click=marcar_como_lidas)) # Rodapé com ação
        ]
    )

    '''
    O Stack permite colocar o Badge exatamente por cima do botão de Sino (eixo Z)
        clip_behavior=NONE garante que, se o badge passar da borda do stack, ele não será cortado invisível.
    '''
    area_notificacoes = ft.Stack(
        width=40, height=40, clip_behavior=ft.ClipBehavior.NONE,
        controls=[botao_notificacoes, badge_notificacoes]
    )

    return area_notificacoes, painel_notificacoes, badge_notificacoes, atualizar_lista_notificacoes