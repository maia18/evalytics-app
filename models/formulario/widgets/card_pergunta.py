import flet as ft

def criar_card_pergunta(page: ft.Page, indicador: dict, estado: dict) -> ft.Container:
    """Constrói o cartão central com todas as opções listadas, seleção única e rolagem vertical se necessário."""
    titulo_ind = indicador["titulo"]
    criterios = indicador.get("criterios", {})

    # Resgata a resposta anterior do usuário (ou usa 3 como padrão inicial)
    valor_inicial = str(estado["respostas"].get(titulo_ind, 3))

    # Função disparada quando o usuário clica na bolinha de uma opção
    def ao_mudar_opcao(e: ft.ControlEvent) -> None:
        estado["respostas"][titulo_ind] = int(e.control.value)
        page.update()

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

<<<<<<< HEAD
    # Envolvemos a coluna de opções em um Container com altura máxima (height) 
    # e ativamos o scroll automático caso ultrapasse o limite.
<<<<<<< HEAD
    # Se preferir que o card inteiro tenha scroll, você pode ajustar conforme sua necessidade.
=======
    # Se preferir que o card inteiro tenha scroll, você pode ajustar conforme sua necessidade
>>>>>>> bcf34a3 ("card_pergunta atualizações")
=======
    
    # scroll automático caso ultrapasse o limite.
    
>>>>>>> 6538c14 (Salva alteracoes locais antes do pull)
    container_opcoes_rolavel = ft.Container(
        content=ft.Column(
            spacing=10, 
            controls=opcoes_radio,
            scroll=ft.ScrollMode.AUTO, # Ativa a rolagem vertical automática se passar do tamanho
        ),
        height=280, # Altura máxima opcional para limitar o card na tela e forçar a barra de rolagem
        padding=5,
    )


    grupo_radio = ft.RadioGroup(
        content=container_opcoes_rolavel,
        value=valor_inicial,
        on_change=ao_mudar_opcao,
    )

    # Verifica se existe descrição para evitar criar espaço à toa

    descricao_texto = indicador.get("descricao", "")
    controles_coluna = [
        ft.Text(titulo_ind, size=18, weight="bold", color="onSurface"),
    ]
    
    if descricao_texto:
        controles_coluna.append(ft.Text(descricao_texto, size=14, color="onSurfaceVariant"))
    
    controles_coluna.append(grupo_radio)

    return ft.Container(
        bgcolor="surface", padding=25, border_radius=12, 
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="shadow"),
        content=ft.Column(
            spacing=10, 
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=controles_coluna,
        ),
    )