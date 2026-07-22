import flet as ft 
from database.indicadores import INDICADORES 
from models.configuracoes.core.indicadores_ui import criar_linha_indicador, criar_pasta_indicador 

def abrir_pasta(page, titulo_pasta, pasta_aberta_atualmente, area_conteudo_aba, abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao): 
    """
    Substitui a visualização das 3 pastas principais pela listagem detalhada de indicadores daquele Eixo específico.
    """
    # De-para identificando qual ID de eixo pertence a qual título de pasta
    mapa_eixos = { 
        "Organização Didático-Pedagógica": 1, 
        "Corpo Docente e Tutorial": 2, 
        "Infraestrutura": 3 
    } 
    
    eixo_id = mapa_eixos.get(titulo_pasta) 
    pasta_aberta_atualmente["titulo"] = titulo_pasta # Salva estado na memória
    pasta_aberta_atualmente["eixo"] = eixo_id 

    # Filtra os dados globais puxando apenas os indicadores do eixo selecionado
    lista_da_pasta = [item for item in INDICADORES if item.get("eixo") == eixo_id] 

    # Monta o cabeçalho superior contendo o botão de voltar e título da pasta
    controles_lista = [ 
        ft.Row( 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            controls=[ 
                ft.Row([ 
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: voltar_para_pastas(page, area_conteudo_aba)), 
                    ft.Text(titulo_pasta, size=22, weight="bold", color="black87") 
                ]), 
                ft.ElevatedButton("Novo Indicador", icon=ft.Icons.ADD, bgcolor="blue700", color="white", on_click=lambda e: abrir_modal_novo()) 
            ] 
        ), 
        ft.Divider(height=20, color="transparent") 
    ] 

    # Laço de repetição (for) preenchendo a lista visual com cada indicador filtrado
    for item in lista_da_pasta: 
        controles_lista.append( 
            criar_linha_indicador( 
                item, 
                lambda e, i=item: abrir_modal_criterios(e, i), 
                lambda e, i=item: abrir_modal_edicao(e, i), 
                lambda i=item: preparar_exclusao(i) 
            ) 
        ) 

    # Injeta a listagem completa dentro do container dinâmico da aba e ativa a barra de rolagem automática
    area_conteudo_aba.content = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15, controls=controles_lista) 
    page.update() 


def voltar_para_pastas(page, area_conteudo_aba): 
    """
    Desfaz a visualização de lista e reconstrói as 3 pastas principais na tela, recalculando a contagem de itens.
    """
    # Recalcula a volumetria em caso de adições ou deleções recentes
    qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1) 
    qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2) 
    qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3) 

    # Reconstrói a estrutura inicial
    layout_pastas = ft.Column( 
        expand=True, 
        spacing=25, 
        controls=[ 
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color="black87"), 
            ft.Column( 
                spacing=15, 
                controls=[ 
                    # Repassa o dicionário de estado "zerado" nas invocações lambdas
                    criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1, lambda t: abrir_pasta(page, t, {"titulo": "", "eixo": 0}, area_conteudo_aba, None, None, None, None)), 
                    criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2, lambda t: abrir_pasta(page, t, {"titulo": "", "eixo": 0}, area_conteudo_aba, None, None, None, None)), 
                    criar_pasta_indicador("Infraestrutura", qtd_eixo_3, lambda t: abrir_pasta(page, t, {"titulo": "", "eixo": 0}, area_conteudo_aba, None, None, None, None)), 
                ] 
            ) 
        ] 
    ) 

    # Redefine a área dinâmica e força a atualização visual
    area_conteudo_aba.content = layout_pastas 
    page.update() 