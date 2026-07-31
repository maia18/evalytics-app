import flet as ft

def obter_icone_tema(dark_mode: bool) -> str:
    """Retorna o ícone oposto ao estado atual da interface.

    Ex: se estiver no modo escuro, exibe a silhueta do modo claro como
    sugestão de mudança.
    """
    return ft.Icons.LIGHT_MODE_OUTLINED if dark_mode else ft.Icons.DARK_MODE_OUTLINED