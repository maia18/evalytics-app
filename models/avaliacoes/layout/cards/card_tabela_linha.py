import flet as ft


def criar_linha(item: dict) -> ft.DataRow:
    """Constrói uma linha da tabela a partir de uma resposta real."""

    celula_comentario = (
        ft.DataCell(
            ft.Icon(
                ft.Icons.CHAT_BUBBLE_OUTLINE,
                size=18,
                color=ft.Colors.BLUE_700,
                tooltip=item["comentario"],
            )
        )
        if item.get("comentario")
        else ft.DataCell(
            ft.Text(
                "-",
                color=ft.Colors.GREY_400,
            )
        )
    )

    return ft.DataRow(
        cells=[
            ft.DataCell(
                ft.Text(
                    item["id"],
                    color=ft.Colors.GREY_700,
                )
            ),

            ft.DataCell(
                ft.Text(item["data"])
            ),

            ft.DataCell(
                ft.Text(item["curso"])
            ),

            ft.DataCell(
                ft.Text(item["eixo"])
            ),

            ft.DataCell(
                ft.Text(
                    item.get(
                        "indicador",
                        "-",
                    )
                )
            ),

            ft.DataCell(
                ft.Text(
                    item["nota"],
                    weight="bold",
                    color=item["cor_nota"],
                )
            ),

            celula_comentario,
        ],
    )