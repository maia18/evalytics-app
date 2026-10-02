import flet as ft
from components.core.constants.constants import (
    COR_PRIMARIA,
)

def criar_campos_formulario_curso(
    cores: dict[str, str],
) -> dict[str, ft.TextField]:
    """
    Cria um novo conjunto de campos de formulário para cadastro/edição de curso.

    Uma função separada garante instâncias próprias de TextField por chamada: 
        Compartilhar os mesmos widgets entre os formulários de adicionar e editar faria o texto digitado em um vazar para o outro.
    """
    return {
        # 'dense=True' diminui a altura interna do campo, deixando o formulário mais compacto
        "nome": ft.TextField(label="Nome do Curso", border_color=cores[COR_PRIMARIA], dense=True),
        "departamento": ft.TextField(label="Departamento", border_color=cores[COR_PRIMARIA], dense=True),
        "coordenador": ft.TextField(label="Coordenador Responsável", border_color=cores[COR_PRIMARIA], dense=True),
    }