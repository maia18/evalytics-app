import flet as ft

def criar_campos_formulario_curso() -> dict[str, ft.TextField]:
    """
    Cria um novo conjunto de campos de formulário para cadastro/edição de curso.

    Uma função separada garante instâncias próprias de TextField por chamada: 
        Compartilhar os mesmos widgets entre os formulários de adicionar e editar faria o texto digitado em um vazar para o outro.
    """
    return {
        # 'dense=True' diminui a altura interna do campo, deixando o formulário mais compacto
        "nome": ft.TextField(label="Nome do Curso", border_color=ft.Colors.BLUE_200, dense=True),
        "departamento": ft.TextField(label="Departamento", border_color=ft.Colors.BLUE_200, dense=True),
        "coordenador": ft.TextField(label="Coordenador Responsável", border_color=ft.Colors.BLUE_200, dense=True),
    }