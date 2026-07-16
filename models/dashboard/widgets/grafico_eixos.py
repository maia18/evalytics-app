import flet as ft

def criar_coluna_grafico(layout, nome, nota, cor):
    altura_max = 200
    altura_barra = (nota / 5.0) * altura_max
    
    return ft.Column(
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        controls=[
            ft.Text(f"{nota:.1f}", size=12, weight="bold", color="grey"),
            ft.Container(
                width=40,
                height=altura_barra,
                bgcolor=cor,
                border_radius=4,
                tooltip=f"{nome}: {nota:.1f} / 5.0"
            ),
            ft.Text(nome, size=12, weight="w500", color=layout.cores["TEXTO_PRINCIPAL"])
        ]
    )

def criar_grafico_eixos(layout, medias_eixos, nomes_eixos, cores_barras):
    barras_grafico = []
    for i, (eixo_id, nota) in enumerate(medias_eixos.items()):
        nome = nomes_eixos.get(eixo_id, f"Eixo {eixo_id}")
        cor = cores_barras[i % len(cores_barras)]
        barras_grafico.append(criar_coluna_grafico(layout, nome, nota, cor))

    borda_grafico = ft.Border(
        top=ft.BorderSide(1, layout.cores["BORDA"]),
        bottom=ft.BorderSide(1, layout.cores["BORDA"]),
        left=ft.BorderSide(1, layout.cores["BORDA"]),
        right=ft.BorderSide(1, layout.cores["BORDA"])
    )

    return ft.Container(
        bgcolor=layout.cores["CARD"],
        padding=30,
        border_radius=8,
        border=borda_grafico,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text("Desempenho Médio por Eixo", size=18, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
                        ft.Text("Médias das avaliações separadas por categoria (Escala 5.0).", size=14, color="grey"),
                    ]
                ),
                ft.Container(
                    height=260,
                    padding=20,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        controls=barras_grafico
                    )
                )
            ]
        )
    )
