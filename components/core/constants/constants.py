"""
Arquivo de Constantes (Constants)
Centraliza todas as dimensões, medidas e paletas de cores da aplicação.
"""
import flet as ft
from typing import Final

# =====================================================================
# DIMENSÕES E MEDIDAS DA INTERFACE
# =====================================================================

WINDOW_WIDTH: Final[int] = 1280  # Largura padrão da janela principal da aplicação (em pixels)
WINDOW_HEIGHT: Final[int] = 720  # Altura padrão da janela principal da aplicação (em pixels)
ALTURA_MAX: Final[int] = 200     # Altura máxima da coluna (utilizada em Gráficos de eixos/barras)
LARGURA_BREAKPOINT_MOBILE = 700   # Define o limite máximo para dispositivos pequenos (celulares e tablets pequenos). Se a largura da tela for menor que 700px, a aplicação adota o modo Mobile.
LARGURA_BREAKPOINT_DESKTOP = 1100  # Define o limite para telas grandes (monitores de notebook e desktop). Acima de 1100px, a aplicação tem espaço de sobra, então adota o modo Desktop completo.

# =====================================================================
# DIMENSÕES DE COMPONENTES (SIDEBAR)
# =====================================================================

LARGURA_SIDEBAR_EXPANDIDA = 250 # Define a largura (em pixels) da barra lateral quando ela está totalmente aberta. 250px é um tamanho padrão excelente, pois oferece espaço suficiente para ícones e textos descritivos longos sem espremer o conteúdo principal da tela.
LARGURA_SIDEBAR_COLAPSADA = 72 # Define a largura (em pixels) da barra lateral quando ela está recolhida (mini-sidebar). 72px é o tamanho exato para mostrar apenas os ícones centralizados, liberando o máximo de espaço útil na tela para o conteúdo principal, ideal para telas médias (tablets) ou quando o usuário prefere focar no dashboard.


# =====================================================================
# PALETA DE CORES
# =====================================================================

# --- Cor da Marca (Brand Color) ---
COR_PRIMARIA: Final[str] = "#4809F4"  # Roxo/Azul vibrante - Cor principal de destaque e seed do tema

# --- Textos: MODO CLARO ---
COR_TEXTO_TITULO: Final[str] = "#111827"      # Cinza muito escuro/quase preto para títulos
COR_TEXTO_SECUNDARIO: Final[str] = "#6B7280"  # Cinza médio para textos secundários e descrições

# --- Textos: MODO ESCURO ---
TEXTO_PRINCIPAL: Final[str] = ft.Colors.WHITE       # Branco absoluto para textos principais
TEXTO_SECUNDARIO: Final[str] = ft.Colors.GREY_300   # Cinza claro para textos secundários

# --- Fundos (Backgrounds) ---
COR_FUNDO: Final[str] = "#F9FAFB"  # Cinza bem claro/off-white - fundo da tela no MODO CLARO
FUNDO: Final[str] = "#1E1E1E"      # Cinza escuro profundo - fundo da tela no MODO ESCURO

# --- Cartões e Painéis (Cards) ---
COR_CARD: Final[str] = "#FFFFFF"   # Branco puro - fundo dos cards no MODO CLARO
CARD: Final[str] = "#2C2C2C"       # Cinza escuro elevado - fundo dos cards no MODO ESCURO

# --- Bordas e Linhas Divisórias ---
COR_BORDA: Final[str] = "#E5E7EB"  # Cinza claro para bordas gerais no MODO CLARO
BORDA: Final[str] = "#3C3C3C"      # Cinza escuro para bordas no MODO ESCURO

# Alias histórico de COR_BORDA (mesmo valor). Mantido por compatibilidade;
# ao confirmar que nenhum outro módulo depende deste nome, pode ser removido.
BORDA_NOT_DARKMODE: Final[str] = COR_BORDA

# --- Elementos de Sobreposição e Interação (MODO ESCURO) ---
OVERLAY_MODAL: Final[str] = "#00000088"  # Preto com transparência (Alpha 88) - fundo de Modais/Popups
HOVER: Final[str] = "#3C3C3C"            # Cor de fundo ao passar o mouse (hover)
SURFACE: Final[str] = "#3C3C3C"          # Cor de superfícies elevadas (menus soltos, tooltips)