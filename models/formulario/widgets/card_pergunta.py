import flet as ft

def criar_card_pergunta(page: ft.Page, indicador: dict, estado: dict, rodape: ft.Container) -> ft.Container:
    """Constrói o cartão central com opções, rolagem e um campo de justificativa para a pergunta."""
    
    titulo_ind = indicador["titulo"]
    criterios = indicador.get("criterios", {})

    # Busca a resposta salva (se houver), sem forçar um falso positivo no Nível 3
    valor_inicial = str(estado["respostas"].get(titulo_ind, ""))
    
    # Resgata a justificativa anterior (caso já exista no estado)
    # Certifique-se de inicializar o dicionário "justificativas" no seu estado global se ainda não houver.
    # if "justificativas" not in estado:
    #     estado["justificativas"] = {}
    # justificativa_inicial = estado["justificativas"].get(titulo_ind, "")

    # Função disparada quando o usuário clica na bolinha de uma opção
    def ao_mudar_opcao(e: ft.ControlEvent) -> None:
        estado["respostas"][titulo_ind] = int(e.control.value)

    # Função disparada quando o usuário digita algo na justificativa
    # def ao_mudar_justificativa(e: ft.ControlEvent) -> None:
    #     estado["justificativas"][titulo_ind] = e.control.value

    # Cria a lista de opções com as bolinhas e os textos lado a lado
    opcoes_radio = []
    for chave, texto_criterio in sorted(criterios.items(), key=lambda x: str(x[0])):
        linha_opcao = ft.Container(
            padding=ft.Padding.symmetric(vertical=4),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Radio(value=str(chave), active_color=ft.Colors.BLUE_700),
                    ft.Container(
                        expand=True, 
                        padding=ft.Padding.only(top=12),
                        content=ft.Text(f"Nível {chave}: {texto_criterio}", color=ft.Colors.BLACK87, size=14)
                    )
                ]
            )
        )
        opcoes_radio.append(linha_opcao)

    grupo_radio = ft.RadioGroup(
        content=ft.Column(spacing=0, controls=opcoes_radio),
        value=valor_inicial,
        on_change=ao_mudar_opcao,
    )

    campo_justificativa = ft.TextField(
        label="Justificativa (Opcional)",
        multiline=True,
        min_lines=1,
        max_lines=3,
        border_color=ft.Colors.GREY_300,
        text_size=14,
        content_padding=15,
    )
    
    # Verifica se existe descrição adicional
    descricao_texto = indicador.get("descricao", "")
    
    # Constrói os elementos da coluna principal
    controles_coluna = [
        ft.Text(titulo_ind, size=20, weight="bold", color=ft.Colors.BLACK87),
    ]
    if descricao_texto:
        controles_coluna.append(ft.Text(descricao_texto, size=14, color="onSurfaceVariant", italic=True))
        
    controles_coluna.extend([
        ft.Divider(height=1, color=ft.Colors.GREY_200),
        grupo_radio,
        ft.Container(height=10),
        campo_justificativa,
        ft.Divider(height=1, color=ft.Colors.GREY_200),
        rodape 
    ])
    
    # 1. CABEÇALHO FIXO
    descricao_texto = indicador.get("descricao", "")
    cabecalho_card = [
        ft.Text(titulo_ind, size=20, weight="bold", color=ft.Colors.BLACK87),
    ]
    if descricao_texto:
        cabecalho_card.append(ft.Text(descricao_texto, size=14, color="onSurfaceVariant", italic=True))
    cabecalho_card.append(ft.Divider(height=1, color=ft.Colors.GREY_200))

    # 2. ÁREA CENTRAL ROLÁVEL
    # Isolamos as opções e a justificativa em uma coluna separada que expande e rola.
    area_rolavel = ft.Column(
        expand=True, # Empurra o rodapé para baixo, ocupando o espaço livre
        scroll=ft.ScrollMode.AUTO, # A barra de rolagem só vai aparecer AQUI dentro
        spacing=10,
        controls=[
            grupo_radio,
            ft.Container(height=10),
            campo_justificativa,
        ]
    )

    return ft.Container(
        bgcolor=ft.Colors.WHITE, 
        padding=30, 
        border_radius=12, 
        border=ft.Border.all(1, ft.Colors.GREY_200),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4)),
        expand=True,
        content=ft.Column(
            spacing=15, 
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                *cabecalho_card,
                area_rolavel,
                ft.Divider(height=1, color=ft.Colors.GREY_200),
                rodape # Fica ancorado no final, imune ao scroll!
            ],
        ),
    )