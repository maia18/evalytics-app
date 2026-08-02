import flet as ft

from utils.services.sessions.indicadores_repository import contar_indicadores_por_eixo, listar_indicadores_por_eixo
from models.configuracoes.core.indicadores_ui import criar_linha_indicador, criar_pasta_indicador
from models.configuracoes.core.estado_indicadores import EstadoIndicadores

# Relaciona o título da interface ao ID inteiro do Eixo esperado pelo repositório
MAPA_EIXOS: dict[str, int] = {
    "Organização Didático-Pedagógica": 1,
    "Corpo Docente e Tutorial": 2,
    "Infraestrutura": 3,
}

# Substitui dinamicamente a visualização inicial de Pastas pela listagem de indicadores de um eixo
def abrir_pasta(page: ft.Page, titulo_pasta: str, estado: EstadoIndicadores) -> None:
    eixo_id = MAPA_EIXOS.get(titulo_pasta)
    estado.definir_pasta_aberta(titulo_pasta, eixo_id)

    lista_da_pasta = listar_indicadores_por_eixo(eixo_id) # Acessa os dados reais no repositório de JSON (ou banco futuro)

    ''' Inicia os controles visuais com o cabeçalho (Botão voltar, Título e Botão de Novo) '''
    controles_lista: list[ft.Control] = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas(page, estado)),
                    ft.Text(titulo_pasta, size=22, weight="bold", color=ft.Colors.BLACK87),
                ]),
                ft.ElevatedButton(
                    "Novo Indicador", icon=ft.Icons.ADD, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE,
                    on_click=lambda e: estado.abrir_modal_novo(),
                ),
            ],
        ),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
    ]

    # Adiciona cada item gerado à lista de renderização visual repassando os Callbacks Globais do estado
    for item in lista_da_pasta:
        controles_lista.append(
            criar_linha_indicador(
                item,
                lambda e, i=item: estado.abrir_modal_criterios(e, i),
                lambda e, i=item: estado.abrir_modal_edicao(e, i),
                lambda i=item: estado.preparar_exclusao(i),
            )
        )
        
    # Injete a lista com scroll automático na aba de configuração
    estado.area_conteudo_aba.content = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15, controls=controles_lista) 
    page.update()

def criar_layout_pastas(page: ft.Page, estado: EstadoIndicadores) -> ft.Column:
    """
    Monta a listagem inicial visual de pastas (uma por eixo), buscando as contagens atualizadas no repositório.

    Reutilizada tanto na renderização original da tela quanto ao clicar no botão de 'Voltar'.
    """
    return ft.Column(
        expand=True, spacing=25,
        controls=[
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color=ft.Colors.BLACK87),
            ft.Column(
                spacing=15,
                controls=[
                    criar_pasta_indicador(
                        titulo, contar_indicadores_por_eixo(eixo_id),
                        lambda t: abrir_pasta(page, t, estado),
                    ) # Gera as pastas iterando no dicionário MAPA_EIXOS definido no topo
                    for titulo, eixo_id in MAPA_EIXOS.items()
                ],
            ),
        ],
    )

# Desfaz a visualização interna da lista e reconstrói as pastas principais
def voltar_para_pastas(page: ft.Page, estado: EstadoIndicadores) -> None:
    estado.area_conteudo_aba.content = criar_layout_pastas(page, estado)
    page.update()