import flet as ft

def criar_linha(item: dict) -> ft.DataRow:
    """
    Constrói uma linha da tabela a partir de um item de dados.
    
    Se houver texto, mostra um ícone que revela o conteúdo em formato de balão (tooltip) ao passar o mouse.
    """
    celula_comentario = (
        ft.DataCell(ft.Icon(
            ft.Icons.CHAT_BUBBLE_OUTLINE, size=18, color=ft.Colors.BLUE_700,
            tooltip=item["comentario"]
        ))
        if item["comentario"] else
        ft.DataCell(ft.Text("-", color=ft.Colors.GREY_400))
    )

    # Retorna o objeto oficial de linha com as células preenchidas na ordem correta
    return ft.DataRow(cells=[
        ft.DataCell(ft.Text(item["id"], color=ft.Colors.GREY_700)),
        ft.DataCell(ft.Text(item["data"])),
        ft.DataCell(ft.Text(item["curso"])),
        ft.DataCell(ft.Text(item["eixo"])),
        
        # Aplica a cor da nota que foi definida na carga de dados
        ft.DataCell(ft.Text(item["nota"], weight="bold", color=item["cor_nota"])),
        celula_comentario,
    ])