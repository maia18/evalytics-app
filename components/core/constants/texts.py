"""
Arquivo de Constantes de Texto (Text/Labels Constants)
Centraliza todos os textos estáticos, títulos e rótulos usados na interface do usuário.
"""
from typing import Final, NamedTuple

# Textos da tela inicial (Home). Continua acessível por índice (compatibilidade).
class TextoPaginaInicio(NamedTuple):
    titulo_menu: str      # [0] Título da aba/menu
    titulo_principal: str  # [1] Título principal da página
    subtitulo: str         # [2] Subtítulo ou descrição
    cta: str                # [3] Texto de botão ou Call-to-Action

# Textos padrão (título + subtítulo) de uma tela. Continua acessível por índice.
class TextoPagina(NamedTuple):
    titulo: str      # [0] Título da aba/menu/página
    subtitulo: str   # [1] Subtítulo ou descrição da funcionalidade

APP_TITLE: Final[str] = "Evalytics - Avaliação Institucional"  # Título principal do app, exibido na janela

# Mapeia o número do eixo (ID) para o seu respectivo nome
NOMES_EIXOS: Final[dict[int, str]] = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}

# Textos utilizados na tela inicial (Home)
TXTS_INICIO: Final[TextoPaginaInicio] = TextoPaginaInicio(
    titulo_menu="Início",
    titulo_principal="Bem-vindo ao Evalytics",
    subtitulo="Sistema de Avaliação Institucional",
    cta="Iniciar nova avaliação",
)

# Textos utilizados na tela de Dashboard (Painel de Controle)
TXTS_DASHBOARD: Final[TextoPagina] = TextoPagina(
    titulo="Dashboard",
    subtitulo="Visão geral dos indicadores.",
)

# Textos utilizados na tela de Nova Avaliação / Formulários
TXTS_AVALIACAO: Final[TextoPagina] = TextoPagina(
    titulo="Avaliações",
    subtitulo="Acessar histórico de avaliações",
)

# Textos utilizados na tela de Gestão de Cursos
TXTS_CURSOS: Final[TextoPagina] = TextoPagina(
    titulo="Cursos",
    subtitulo="Consultar e organizar cursos.",
)

# Textos utilizados na tela de Relatórios
TXTS_RELATORIOS: Final[TextoPagina] = TextoPagina(
    titulo="Relatórios",
    subtitulo="Gerar relatórios.",
)

# Textos utilizados na tela de Configurações
TXTS_CONFIGS: Final[TextoPagina] = TextoPagina(
    titulo="Configurações",
    subtitulo="Acessar configurações do sistema",
)