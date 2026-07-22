"""
Arquivo de Constantes (Constants)
Centraliza todas as dimensões, medidas e paletas de cores da aplicação.
"""

# =====================================================================
# DIMENSÕES E MEDIDAS DA INTERFACE
# =====================================================================
WINDOW_WIDTH = 1280  # Largura padrão da janela principal da aplicação (em pixels)
WINDOW_HEIGHT = 720  # Altura padrão da janela principal da aplicação (em pixels)
ALTURA_MAX = 200     # Altura máxima da coluna (utilizada em Gráficos de eixos/barras)

# =====================================================================
# PALETA DE CORES
# =====================================================================

# --- Cor da Marca (Brand Color) ---
COR_PRIMARIA = "#4809F4"  # Roxo/Azul vibrante - Usado como cor principal de destaque e seed do tema

# --- Textos ---
# Modo Claro
COR_TEXTO_TITULO = "#111827"      # Cinza muito escuro/quase preto para títulos no modo claro
COR_TEXTO_SECUNDARIO = "#6B7280"  # Cinza médio para textos secundários e descrições no modo claro

# Modo Escuro
TEXTO_PRINCIPAL = "white"         # Branco absoluto para textos principais no modo escuro
TEXTO_SECUNDARIO = "grey300"      # Cinza claro (padrão do Flet) para textos secundários no modo escuro

# --- Fundos (Backgrounds) ---
COR_FUNDO = "#F9FAFB"  # Cinza bem claro/off-white para o fundo da tela no modo claro
FUNDO = "#1E1E1E"      # Cinza escuro profundo para o fundo da tela no modo escuro

# --- Cartões e Painéis (Cards) ---
COR_CARD = "#FFFFFF"   # Branco puro para o fundo dos cards no modo claro
CARD = "#2C2C2C"       # Cinza escuro elevado para o fundo dos cards no modo escuro

# --- Bordas e Linhas Divisórias ---
COR_BORDA = "#E5E7EB"             # Cinza claro para bordas gerais no modo claro
BORDA = "#3C3C3C"                 # Cinza escuro para bordas no modo escuro
BORDA_NOT_DARKMODE = "#E5E7EB"    # Variável específica de borda para modo claro (mesma cor de COR_BORDA)

# --- Elementos de Sobreposição e Interação ---
OVERLAY_MODAL = "#00000088"  # Preto com transparência (Alpha 88) para fundo escurecido de Modais/Popups
HOVER = "#3C3C3C"            # Cor de fundo ao passar o mouse (efeito hover) sobre elementos no modo escuro
SURFACE = "#3C3C3C"          # Cor de superfícies elevadas (como menus soltos ou tooltips) no modo escuro