import flet as ft

def criar_rodape_termos(cor_texto_secundario: str, cor_primaria: str) -> ft.Container:
    """Rodapé de conformidade (Termos de Serviço e Política de Privacidade)."""
    return ft.Container(
        margin=ft.Margin.only(top=10),
        content=ft.Text(
            text_align=ft.TextAlign.CENTER, size=12,
            spans=[
                ft.TextSpan("By signing up, you agree to our ", ft.TextStyle(color=cor_texto_secundario)),
                ft.TextSpan("Terms of Service", ft.TextStyle(color=cor_primaria, weight=ft.FontWeight.W_500)),
                ft.TextSpan(" and ", ft.TextStyle(color=cor_texto_secundario)),
                ft.TextSpan("Privacy Policy", ft.TextStyle(color=cor_primaria, weight=ft.FontWeight.W_500)),
            ],
        ),
    )