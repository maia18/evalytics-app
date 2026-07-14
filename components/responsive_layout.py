"""
Componente de Layout Responsivo Reutilizável
Encapsula a lógica de sidebar, topbar e overlay para responsividade geral
"""

import flet as ft
import urllib.request
import json

def obter_localizacao() -> str:
    """Busca a cidade e estado baseados no IP do usuário."""
    try:
        # Consulta uma API gratuita de geolocalização
        with urllib.request.urlopen("http://ip-api.com/json/", timeout=3) as resposta:
            dados = json.loads(resposta.read().decode())
            if dados.get("status") == "success":
                cidade = dados.get("city", "")
                estado = dados.get("region", "")
                return f"{cidade} - {estado}"
    except Exception:
        # Se estiver sem internet ou a API falhar, usa este valor padrão
        pass
    
    return "Paracuru - CE"


class ResponsiveLayout:
    
    """
    Cria um layout responsivo com sidebar, topbar e conteúdo adaptável a qualquer tamanho de tela.
    """
    
    def __init__(self, page: ft.Page, titulo_pagina: str, subtitulo: str = "", dark_mode: bool = False, mudar_tela=None):
        self.page = page
        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.mudar_tela = mudar_tela
        
        self.dark_mode = getattr(self.page, "is_dark_mode", False) # Lê a preferência salva ou usa falso (Light Mode) por padrão
        
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT # Aplica o tema nativo do Flet
        
        # Paleta de cores dinâmica
        self.COR_FUNDO = "#1E1E1E" if self.dark_mode else "#F9FAFB"
        self.COR_BORDA = "#3C3C3C" if self.dark_mode else "#E5E7EB"
        self.COR_PRIMARIA = "#F59E0B"
        self.COR_CARD = "#2C2C2C" if self.dark_mode else "white"
        self.COR_TEXTO_PRINCIPAL = "white" if self.dark_mode else "black"
        
        # Estado
        self.sidebar_mobile_aberta = False
        self.sidebar_colapsada = False
        self.conteudo_principal = ft.Column()
        
        # Componentes
        self._criar_componentes()
    
    def _criar_componentes(self):
        
        """Cria os componentes básicos do layout"""
        
        # === OVERLAY ===
        self.overlay = ft.Container(
            visible=False,
            expand=True,
            bgcolor="#00000088",
            on_click=lambda e: self._fechar_sidebar(),
        )
        
        # === SIDEBAR MOBILE ===
        self.sidebar_mobile = ft.Container(
            left=-270,
            top=0,
            bottom=0,
            width=250,
            bgcolor=self.COR_CARD,
            animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            border=ft.Border(right=ft.BorderSide(1, self.COR_BORDA)),
            padding=20,
            shadow=ft.BoxShadow(blur_radius=25, spread_radius=2, color="#33000000"),
            content=self._criar_sidebar_content()
        )
        
        # === TOPBAR ===
        self.topbar = ft.Container(
            padding=20,
            bgcolor=self.COR_CARD,
            border=ft.Border(bottom=ft.BorderSide(1, self.COR_BORDA)),
            content=self._criar_topbar_content()
        )
        
        # === SIDEBAR DESKTOP ===
        self.sidebar_desktop = ft.Container(
            width=250,
            bgcolor=self.COR_CARD,
            border=ft.Border(right=ft.BorderSide(1, self.COR_BORDA)),
            padding=20,
            content=self._criar_sidebar_content()
        )
    
    def _criar_sidebar_content(self):
        
        """Retorna o conteúdo da sidebar com suporte a colapsamento"""
        
        # Container para logo/título corrigido (padding usando valor inteiro simples)
        logo_container = ft.Container(
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.ANALYTICS, color=self.COR_PRIMARIA, size=28),
                    ft.Text(
                        "Evalytics", 
                        size=18, 
                        weight="bold", 
                        color=self.COR_TEXTO_PRINCIPAL,
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            height=60
        )
        
        # Função auxiliar para criar itens do menu
        def criar_item_menu(icone: str, texto: str, rota: str) -> ft.Container:
            return ft.Container(
                height=45,
                content=ft.TextButton(
                    content=ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(
                                icone,
                                size=20,
                                color="grey700" if not self.dark_mode else "grey300",
                            ),
                            ft.Text(
                                texto,
                                size=14,
                                weight="w500",
                                color=self.COR_TEXTO_PRINCIPAL,
                            ),
                        ],
                    ),
                    style=ft.ButtonStyle(
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color="#3C3C3C" if self.dark_mode else "#CCCCCC",
                    ),
                    on_click=lambda _: self.mudar_tela(rota) if self.mudar_tela else None,
                ),
            )
        
        return ft.Column([
            logo_container,
            ft.Divider(height=2),
            criar_item_menu(ft.Icons.HOME, "Início", "/inicio"),
            criar_item_menu(ft.Icons.ADD_BOX_OUTLINED, "Avaliação", "/avaliacoes"),
            criar_item_menu(ft.Icons.GRID_VIEW_OUTLINED, "Dashboard", "/dashboard"),
            criar_item_menu(ft.Icons.MENU_BOOK_OUTLINED, "Cursos", "/cursos"),
            criar_item_menu(ft.Icons.PIE_CHART_OUTLINE, "Relatórios", "/relatorios"),
            ft.Divider(height=2),
            criar_item_menu(ft.Icons.SETTINGS_OUTLINED, "Configurações", "/configuracoes"),
        ], scroll=ft.ScrollMode.AUTO, spacing=0, expand=False)
    
    def _criar_sidebar_colapsada(self):
        
        """Retorna conteúdo da sidebar apenas com ícones (modo colapsado)"""
        
        def criar_botao_icon(icone: str, tooltip_text: str, rota: str) -> ft.Container:
            return ft.Container(
                height=45,
                alignment=ft.alignment.center,
                content=ft.TextButton(
                    expand=True,
                    content=ft.Icon(
                        icone,
                        color=self.COR_TEXTO_PRINCIPAL,
                        size=24,
                        tooltip=tooltip_text,
                    ),
                    style=ft.ButtonStyle(
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color="#3C3C3C" if self.dark_mode else "#CCCCCC",
                    ),
                    on_click=lambda _: self.mudar_tela(rota) if self.mudar_tela else None,
                ),
            )
        
        return ft.Column([
            ft.Container(content=ft.Icon(ft.Icons.ANALYTICS, color=self.COR_PRIMARIA, size=28), padding=8, alignment=ft.Alignment.CENTER),
            ft.Divider(height=1),
            criar_botao_icon(ft.Icons.HOME, "Início", "/inicio"),
            criar_botao_icon(ft.Icons.ADD_CIRCLE, "Nova Avaliação", "/avaliacoes"),
            criar_botao_icon(ft.Icons.DASHBOARD, "Dashboard", "/dashboard"),
            criar_botao_icon(ft.Icons.BOOK, "Cursos", "/cursos"),
            criar_botao_icon(ft.Icons.PIE_CHART, "Relatórios", "/relatorios"),
            ft.Divider(height=1),
            criar_botao_icon(ft.Icons.SETTINGS, "Configurações", "/configuracoes"),
        ], scroll=ft.ScrollMode.AUTO, spacing=0, alignment=ft.MainAxisAlignment.START)
    
    def _criar_topbar_content(self):
        """Retorna o conteúdo da topbar"""
        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU, 
            on_click=lambda e: self._toggle_sidebar()
        )
        
        # Função para o botão de tema
        def toggle_dark_mode(e):
            self.dark_mode = not self.dark_mode
            self._atualizar_tema()
            
        # Define se mostra a Lua (modo claro) ou Sol (modo escuro)
        icone_tema = ft.Icons.LIGHT_MODE_OUTLINED if self.dark_mode else ft.Icons.DARK_MODE_OUTLINED
        
        # Busca a localização real de forma automática no momento em que a Topbar é criada
        local_atual = obter_localizacao()

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        self.menu_button,
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(self.titulo_pagina, size=20, weight="bold", color=self.COR_TEXTO_PRINCIPAL),
                                ft.Text(self.subtitulo, size=12, color="grey"),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=18, color=self.COR_PRIMARIA),
                                    ft.Text(local_atual, size=14, weight="w500", color=self.COR_TEXTO_PRINCIPAL),
                                ]
                            ),
                            padding=10, 
                            border_radius=8,
                            bgcolor="#3C3C3C" if self.dark_mode else "#E5E7EB", # Códigos HEX absolutos no lugar do ft.colors

                        ),
                        ft.IconButton(icone_tema, on_click=toggle_dark_mode),
                        ft.IconButton(ft.Icons.NOTIFICATIONS_NONE),
                        ft.CircleAvatar(content=ft.Text("AC"), bgcolor=self.COR_PRIMARIA, radius=18),
                    ]
                ),
            ],
        )
    
    def _toggle_sidebar(self):
        """Abre ou fecha a sidebar mobile"""
        if self.page.width >= 900:
            return
        if self.sidebar_mobile_aberta:
            self._fechar_sidebar()
        else:
            self._abrir_sidebar()
    
    def _abrir_sidebar(self):
        """Abre a sidebar mobile"""
        self.sidebar_mobile_aberta = True
        self.sidebar_mobile.left = 0
        self.overlay.visible = True
        self.page.update()
    
    def _fechar_sidebar(self):
        """Fecha a sidebar mobile"""
        self.sidebar_mobile_aberta = False
        self.sidebar_mobile.left = -270
        self.overlay.visible = False
        self.page.update()
    
    def _atualizar_tema(self):
        """Atualiza as cores e recarrega a tela para aplicar o tema"""
        # Salva o estado atual criando um atributo customizado na página
        self.page.is_dark_mode = self.dark_mode
        
        # Altera o tema base da janela do Flet
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        self.page.update()
        
        # Força o recarregamento da tela atual para as novas cores pegarem nos cards
        if self.mudar_tela and hasattr(self, 'rota_atual'):
            self.mudar_tela(self.rota_atual)
    
    def _ajustar_responsividade(self, e=None):
        """Ajusta a visibilidade, tamanho e conteúdo dos componentes conforme o tamanho da tela"""
        if self.page.width < 700:
            # MOBILE: Sidebar invisível e Menu Hambúrguer VISÍVEL
            self.sidebar_desktop.visible = False
            self.sidebar_desktop.width = 0
            self.menu_button.visible = True
        else:
            # DESKTOP/TABLET: Sidebar visível e Menu Hambúrguer OCULTO
            self.sidebar_desktop.visible = True
            self.menu_button.visible = False
            self._fechar_sidebar()  # Garante que mobile feche ao expandir
            
            if self.page.width >= 1100:
                # DESKTOP: Sidebar expandida (250px) com texto
                self.sidebar_desktop.width = 250
                self.sidebar_colapsada = False
                self.sidebar_desktop.content = self._criar_sidebar_content()
            else:
                # TABLET: Sidebar colapsada (72px) apenas com ícones
                self.sidebar_desktop.width = 72
                self.sidebar_colapsada = True
                self.sidebar_desktop.content = self._criar_sidebar_colapsada()
        
        self.page.update()
    
    def add_content(self, content: ft.Control):
        """Adiciona conteúdo à área principal"""
        self.conteudo_principal = content
    
    def criar_view(self, route: str):
        """Cria e retorna a View com o layout responsivo"""
        self.rota_atual = route
        self.page.on_resize = self._ajustar_responsividade
        self._ajustar_responsividade()
        
        return ft.View(
            route=route,
            padding=0,
            bgcolor=self.COR_FUNDO,
            controls=[
                ft.Stack(
                    expand=True,
                    controls=[
                        ft.Row(
                            expand=True,
                            spacing=0,
                            controls=[
                                self.sidebar_desktop,
                                ft.Column(
                                    expand=True,
                                    spacing=0,
                                    controls=[
                                        self.topbar,
                                        ft.Container(
                                            expand=True,
                                            padding=20,
                                            content=self.conteudo_principal
                                        )
                                    ], 
                                    scroll=ft.ScrollMode.AUTO
                                )
                            ]
                        ),
                        self.overlay,
                        self.sidebar_mobile
                    ]
                )
            ]
        )
