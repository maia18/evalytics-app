import flet as ft 
from typing import Callable 
from utils.services.sessions.indicadores_repository import adicionar_indicador 
from models.configuracoes.core.estado_indicadores import EstadoIndicadores 

# Cria o modal de cadastro de um novo indicador
def criar_modal_novo( 
    page: ft.Page, 
    estado: EstadoIndicadores, 
    abrir_pasta: Callable[[str], None], 
) -> tuple[ft.AlertDialog, ft.TextField, ft.TextField, Callable]:
    
    # Instancia os campos de entrada de dados vazios.
    campo_titulo = ft.TextField(label="Título do Indicador", border_color=ft.Colors.BLUE_200) 
    campo_desc = ft.TextField(label="Descrição", multiline=True, border_color=ft.Colors.BLUE_200) 
    
    # Cria e persiste um novo indicador no eixo da pasta atualmente aberta
    def salvar_novo(e: ft.ControlEvent) -> None: 
        
        ''' 
        Chama a função do repositório para salvar no banco de dados.
            Usa 'estado.pasta_eixo' (resgatado do estado global) para garantir que oo indicador seja salvo exatamente no eixo (pasta) em que o usuário está navegando.
        '''
        adicionar_indicador(campo_titulo.value or "", estado.pasta_eixo, campo_desc.value or "") 

        '''
        Limpa os campos após salvar. Se não fizermos isso, o modal vai abrir com os textos do indicador anterior na próxima vez que o usuário clicar em "Novo".
        '''
        campo_titulo.value = "" 
        campo_desc.value = "" 

        # Exibe o feedback visual de sucesso na parte inferior da tela.
        page.snack_bar = ft.SnackBar(ft.Text("Novo indicador criado!", color=ft.Colors.GREEN)) 
        page.snack_bar.open = True 
        
        modal.open = False # Fecha o popup.
        
        '''
        Força a lista visual a recarregar, fazendo com que o novo item recém-criado apareça instantaneamente na interface sem precisar atualizar a página inteira.
        '''
        abrir_pasta(estado.pasta_titulo) 
        page.update() 

    # Constrói a estrutura visual do alerta flutuante (AlertDialog).
    modal = ft.AlertDialog( 
        title=ft.Text("Novo Indicador", size=18, weight="bold"), 
        content=ft.Column(width=400, height=200, spacing=15, controls=[campo_titulo, campo_desc]), 
        actions=[ 
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)), 
            ft.ElevatedButton("Salvar", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=salvar_novo), 
        ], 
        actions_alignment=ft.MainAxisAlignment.END, 
    ) 
    
    # Exibe o modal com os campos limpos, pronto para um novo cadastro.
    def abrir_modal_novo() -> None: 
        '''
        O framework Flet exige que componentes flutuantes (como diálogos e modais) sejam explicitamente adicionados à camada de sobreposição (overlay) da página.
        '''
        if modal not in page.overlay: 
            page.overlay.append(modal) 
            
        modal.open = True 
        page.update() 

    return modal, campo_titulo, campo_desc, abrir_modal_novo 