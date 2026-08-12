import flet as ft

def criar_card_pergunta(page: ft.Page, indicador: dict, estado: dict) -> ft.Container:
    """Constrói o cartão central com opções, rolagem e um campo de justificativa para a pergunta."""
    titulo_ind = indicador["titulo"]
    criterios = indicador.get("criterios", {})

    # Resgata a resposta anterior do usuário (ou usa 3 como padrão inicial)
    valor_inicial = str(estado["respostas"].get(titulo_ind, 3))
    
    # Resgata a justificativa anterior (caso já exista no estado)
    # Certifique-se de inicializar o dicionário "justificativas" no seu estado global se ainda não houver.
    if "justificativas" not in estado:
        estado["justificativas"] = {}
    justificativa_inicial = estado["justificativas"].get(titulo_ind, "")

    # Função disparada quando o usuário clica na bolinha de uma opção
    def ao_mudar_opcao(e: ft.ControlEvent) -> None:
        estado["respostas"][titulo_ind] = int(e.control.value)
        page.update()

    # Função disparada quando o usuário digita algo na justificativa
    def ao_mudar_justificativa(e: ft.ControlEvent) -> None:
        estado["justificativas"][titulo_ind] = e.control.value

    # Cria a lista de opções com as bolinhas e os textos lado a lado
    opcoes_radio = []
    for chave, texto_criterio in sorted(criterios.items(), key=lambda x: str(x[0])):
        label_texto = f"Nível {chave}: {texto_criterio}"
        
        linha_opcao = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Radio(value=str(chave), fill_color="primary"),
                ft.Container(
                    expand=True, 
                    content=ft.Text(
                        label_texto, 
                        color="onSurface", 
                        size=14
                    )
                )
            ]
        )
        opcoes_radio.append(linha_opcao)

    container_opcoes_rolavel = ft.Container(
        content=ft.Column(
            spacing=10, 
            controls=opcoes_radio,
            scroll=ft.ScrollMode.AUTO,
        ),
        height=200, # Reduzido levemente para dar espaço ao campo de texto no card
        padding=5,
    )

    grupo_radio = ft.RadioGroup(
        content=container_opcoes_rolavel,
        value=valor_inicial,
        on_change=ao_mudar_opcao,
    )

    # Campo de texto para a justificativa
    campo_justificativa = ft.TextField(
        label="Justificativa (Opcional)",
        hint_text="Digite aqui os motivos ou evidências...",
        value=justificativa_inicial,
        multiline=True,
        min_lines=2,
        max_lines=3,
        text_size=14,
        on_change=ao_mudar_justificativa,
    )

    # Verifica se existe descrição para evitar criar espaço à toa
    descricao_texto = indicador.get("descricao", "")
    controles_coluna = [ft.Text(titulo_ind, size=18, weight="bold", color="onSurface")]
    
    if descricao_texto:
        controles_coluna.append(ft.Text(descricao_texto, size=14, color="onSurfaceVariant"))
    
    # Adiciona os elementos na coluna principal do card
    controles_coluna.extend([
        grupo_radio,
        ft.Divider(height=10, color="transparent"), # Pequeno espaçamento
        campo_justificativa
    ])

    return ft.Container(
        bgcolor="surface", 
        padding=25, 
        border_radius=12, 
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="shadow"),
        content=ft.Column(
            spacing=10, 
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=controles_coluna,
        ),
    )