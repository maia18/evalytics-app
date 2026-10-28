from fpdf import FPDF

class RelatorioEvalytics(FPDF):
    """
    Documento PDF customizado que estende o FPDF original. 
        Define um cabeçalho e rodapé padrão que serão injetados automaticamente em todas as páginas."""

    def set_font(self, family=None, style="", size=0):
        """Usa a fonte Unicode incorporada no lugar das fontes PDF básicas."""
        if family and str(family).lower() in {"helvetica", "arial"}:
            family = "dejavu"
        super().set_font(family, style, size)

    def header(self) -> None:
        """Imprime o cabeçalho no topo da página atual."""
        
        self.set_font("helvetica", "B", 16)
        self.set_text_color(25, 118, 210)
        self.cell(0, 10, "Evalytics - Avaliação Institucional", ln=True, align="C")
        self.set_font("helvetica", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Relatório Consolidado de Eixos", ln=True, align="C")

        # Linha fina divisória abaixo dos títulos
        self.line(20, 30, 190, 30)
        self.ln(10)

    def footer(self) -> None:
        """Posiciona a quebra a -15mm do final e imprime o número da página centralizado."""
        
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")
