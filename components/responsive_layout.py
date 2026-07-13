"""
Componente de Layout Responsivo Reutilizável
Encapsula a lógica de sidebar, topbar e overlay para responsividade geral
"""

import flet as ft


class ResponsiveLayout:
    """
    Cria um layout responsivo com sidebar, topbar e conteúdo adaptável a qualquer tamanho de tela.
    
    Uso:
        layout = ResponsiveLayout(page, "Página Título", "Subtítulo")
        layout.add_content(seu_conteudo)
        view = layout.criar_view("/rota")
    """
    
    def __init__(self, page: ft.Page, titulo_pagina: str, subtitulo: str = "", dark_mode: bool = False):
        self.page = page
        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.dark_mode = dark_mode
        
        # Paleta de cores
        self.COR_FUNDO = "#1E1E1E" if dark_mode else "#F9FAFB"
        self.COR_BORDA = "#3C3C3C" if dark_mode else "#E5E7EB"
        self.COR_PRIMARIA = "#F59E0B"
        self.COR_CARD = "#2C2C2C" if dark_mode else "white"
        self.COR_TEXTO_PRINCIPAL = "white" if dark_mode else "black"
        
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
        
        # Função auxiliar para criar itens do menu COM ícones
        def criar_item_menu(icone: str, texto: str) -> ft.Container:
            return ft.Container(
                content=ft.Row(
                    spacing=12,
                    controls=[
                        ft.Icon(icone, size=20, color="grey700" if not self.dark_mode else "grey300"),
                        ft.Text(
                            texto,
                            size=14,
                            weight="w500",
                            color=self.COR_TEXTO_PRINCIPAL,
                        ),
                    ]
                ),
                padding=10,
                height=45,
                border_radius=8,
            )
        
        # Labels de seção corrigidos (padding usando valor inteiro simples)
        label_menu = ft.Container(
            content=ft.Text("Menu Principal", size=12, weight="bold", color=self.COR_TEXTO_PRINCIPAL),
            padding=10,
            height=40,
        )
        
        label_config = ft.Container(
            content=ft.Text("Configurações", size=12, weight="bold", color=self.COR_TEXTO_PRINCIPAL),
            padding=10,
            height=40,
        )
        
        return ft.Column([
            logo_container,
            ft.Divider(height=2),
            label_menu,
            criar_item_menu(ft.Icons.HOME, "Início"),
            criar_item_menu(ft.Icons.ADD_BOX_OUTLINED, "Nova Avaliação"),
            criar_item_menu(ft.Icons.GRID_VIEW_OUTLINED, "Dashboard"),
            criar_item_menu(ft.Icons.SCHOOL_OUTLINED, "Professores"),
            criar_item_menu(ft.Icons.MENU_BOOK_OUTLINED, "Cursos"),
            criar_item_menu(ft.Icons.PIE_CHART_OUTLINE, "Relatórios"),
            ft.Divider(height=2),
            label_config,
            criar_item_menu(ft.Icons.SETTINGS_OUTLINED, "Configurações"),
        ], scroll=ft.ScrollMode.AUTO, spacing=0, expand=False)
    
    def _criar_sidebar_colapsada(self):
        """Retorna conteúdo da sidebar apenas com ícones (modo colapsado)"""
        def criar_botao_icon(icone: str, tooltip_text: str) -> ft.Container:
            return ft.Container(
                content=ft.Icon(
                    icone, 
                    color=self.COR_TEXTO_PRINCIPAL, 
                    size=24,
                    tooltip=tooltip_text
                ),
                padding=8,
                alignment=ft.Alignment.CENTER,
            )
        
        return ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.ANALYTICS, color=self.COR_PRIMARIA, size=28),
                padding=8,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Divider(height=1),
            criar_botao_icon(ft.Icons.HOME, "Início"),
            criar_botao_icon(ft.Icons.ADD_CIRCLE, "Nova Avaliação"),
            criar_botao_icon(ft.Icons.DASHBOARD, "Dashboard"),
            criar_botao_icon(ft.Icons.SCHOOL, "Professores"),
            criar_botao_icon(ft.Icons.BOOK, "Cursos"),
            criar_botao_icon(ft.Icons.PIE_CHART, "Relatórios"),
            ft.Divider(height=1),
            criar_botao_icon(ft.Icons.SETTINGS, "Configurações"),
        ], scroll=ft.ScrollMode.AUTO, spacing=0, alignment=ft.MainAxisAlignment.START)
    
    def _criar_topbar_content(self):
        """Retorna o conteúdo da topbar"""
        menu_button = ft.IconButton(
            icon=ft.Icons.MENU, 
            on_click=lambda e: self._toggle_sidebar()
        )
        
        def toggle_dark_mode(e):
            self.dark_mode = not self.dark_mode
            self._atualizar_tema()
        
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        menu_button,
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(
                                    self.titulo_pagina, 
                                    size=20, 
                                    weight="bold", 
                                    color=self.COR_TEXTO_PRINCIPAL
                                ),
                                ft.Text(
                                    self.subtitulo, 
                                    size=12, 
                                    color="grey"
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Dropdown(
                            width=200, 
                            height=40, 
                            value="San Francisco HQ",
                            options=[ft.dropdown.Option("San Francisco HQ")]
                        ),
                        ft.IconButton(ft.Icons.DARK_MODE_OUTLINED, on_click=toggle_dark_mode),
                        ft.IconButton(ft.Icons.NOTIFICATIONS_NONE),
                        ft.CircleAvatar(
                            content=ft.Text("AC"), 
                            bgcolor=self.COR_PRIMARIA, 
                            radius=18
                        ),
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
        """Atualiza as cores ao mudar tema"""
        self.COR_FUNDO = "#1E1E1E" if self.dark_mode else "#F9FAFB"
        self.COR_BORDA = "#3C3C3C" if self.dark_mode else "#E5E7EB"
        self.COR_CARD = "#2C2C2C" if self.dark_mode else "white"
        self.COR_TEXTO_PRINCIPAL = "white" if self.dark_mode else "black"
        self.page.update()
    
    def _ajustar_responsividade(self, e=None):
        """Ajusta a visibilidade, tamanho e conteúdo dos componentes conforme o tamanho da tela"""
        if self.page.width < 700:
            # MOBILE: Sidebar invisível
            self.sidebar_desktop.visible = False
            self.sidebar_desktop.width = 0
        else:
            self.sidebar_desktop.visible = True
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
                                # Coluna que abraça toda a direita
                                ft.Column(
                                    expand=True,
                                    spacing=0, # Garante que a Topbar cole no topo e no conteúdo
                                    controls=[
                                        self.topbar, # Topbar sem margens externas
                                        # Conteúdo principal com o padding correto de 20px
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
