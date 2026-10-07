import flet as ft
from typing import Callable
from datetime import datetime
from components.core.constants.constants import COR_PRIMARIA
from components.widgets.card.card_base import criar_card_base
from models.avaliacoes.core.feedback import mostrar_feedback
from database.services.firestore_avaliacoes import obter_respostas_tabela

def criar_card_controle_ciclo(layout, mudar_tela: Callable[[str], None], page: ft.Page) -> ft.Container:
    """Cartão que exibe o status do ciclo de avaliação e os botões de ação principais."""
    
    # Cria uma etiqueta de status (Tag / Pill) estilizada
    status_ciclo = ft.Container(
        content=ft.Text("EM ANDAMENTO", color=ft.Colors.WHITE, size=12, weight="bold"),
        bgcolor=ft.Colors.GREEN_600,
        padding=8,
        border_radius=15,  # Bordas arredondadas, estilo pílula
    )
    
    dados_tabela = obter_respostas_tabela()
    total_respostas = len(dados_tabela)
    
    def obter_semestre_atual() -> str:
        """Retorna o semestre acadêmico correspondente à data atual."""

        agora = datetime.now()

        semestre = "1" if agora.month <= 6 else "2"

        return f"{agora.year}.{semestre}"
    
    semestre_atual = obter_semestre_atual()
    
    '''Estrutura principal dividida em Parte Superior e Parte Inferior, separadas por um Divider'''
    conteudo = ft.Column(
        spacing=14,
        controls=[
            # =====================================================================
            #                           PARTE SUPERIOR
            # =====================================================================
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Ciclo de Avaliação Ativo", size=14, color=ft.Colors.GREY_600),
                            ft.Row([
                                ft.Text(
                                    f"Semestre {semestre_atual}",
                                    size=22,
                                    weight="bold",
                                    color=COR_PRIMARIA,
                                ),
                                status_ciclo,
                            ]),
                        ],
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.ElevatedButton(
                                "Nova Avaliação",
                                icon=ft.Icons.OPEN_IN_NEW,
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                                on_click=lambda _: mudar_tela("/formulario"),
                            ),
                            ft.ElevatedButton(
                                "Copiar Link",
                                icon=ft.Icons.CONTENT_COPY,
                                bgcolor=ft.Colors.BLUE_50,
                                color=ft.Colors.BLUE_700,
                                on_click=lambda _: mostrar_feedback(page, "Link copiado para a área de transferência!", sucesso=True),
                            ),
                        ],
                    ),
                ],
            ),
            ft.Divider(color=ft.Colors.GREY_200), # Separador visual
            
            # =====================================================================
            #                           PARTE INFERIOR
            # =====================================================================
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        f"{total_respostas} respostas coletadas até o momento.",
                        size=14,
                        color=ft.Colors.BLACK87,
                    ),
                    ft.TextButton(
                        "Encerrar Ciclo",
                        icon=ft.Icons.STOP_CIRCLE,
                        style=ft.ButtonStyle(color=ft.Colors.RED_700), # Ação destrutiva destacada em vermelho
                    ),
                ],
            ),
        ],
    )

    return criar_card_base(layout.cores, conteudo) # Empacota o layout criado na nossa "casca" de UI padrão