import flet as ft

def criar_linha(item: dict) -> ft.DataRow:
    """Constrói uma linha visual da tabela (DataRow) a partir de um dicionário de dados brutos"""
    
    '''
    Lógica condicional (If/Else inline) para a exibição de comentários.
        Se houver texto no campo "comentario", renderiza um ícone interativo de balão de chat.
        Ao passar o mouse sobre o ícone, o conteúdo real do texto é revelado através da propriedade 'tooltip'.
        Se estiver vazio (None ou ""), exibe apenas um discreto traço cinza para manter o alinhamento da coluna.
    '''
    celula_comentario = (
        ft.DataCell(
            ft.Icon(
                ft.Icons.CHAT_BUBBLE_OUTLINE, 
                size=18, 
                color=ft.Colors.BLUE_700,
                tooltip=item["comentario"]
        ))
        if item["comentario"] else
        ft.DataCell(ft.Text("-", color=ft.Colors.GREY_400))
    )

    '''
    Retorna o objeto oficial de linha do Flet (DataRow).
        As células (DataCell) precisam ser declaradas na exata mesma ordem das colunas (DataColumn) definidas na tabela principal para que os dados não fiquem trocados.
    '''
    return ft.DataRow(cells=[
        ft.DataCell(ft.Text(item["id"], color=ft.Colors.GREY_700)),
        ft.DataCell(ft.Text(item["data"])),
        ft.DataCell(ft.Text(item["curso"])),
        ft.DataCell(ft.Text(item["eixo"])),        
        ft.DataCell(ft.Text(item["nota"], weight="bold", color=item["cor_nota"])), # Aplica dinamicamente a cor da nota previamente calculada durante a extração dos dados do Firestore.
        
        celula_comentario, # Injeta a célula condicional de comentário montada no bloco anterior.
    ])