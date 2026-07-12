""" Importa as views (páginas) da aplicação """  
from models.login import ViewLogin
from models.inicio import ViewInicio
from models.dashboard import ViewDashboard
from models.avaliacoes import ViewAvaliacoes
from models.relatorios import ViewRelatorios
from models.cursos import ViewCursos
from models.formulario import ViewFormulario
from models.configuracoes import ViewConfiguracoes

# Dicionário que mapeia rotas (strings) para suas respectivas views
ROTAS = {
    "/": ViewLogin,                         # Rota inicial (login)
    "/inicio": ViewInicio,                  # Página principal
    "/dashboard": ViewDashboard,            # Página de Dashboard
    "/avaliacoes": ViewAvaliacoes,          # Página de avaliações
    "/relatorios": ViewRelatorios,          # Página de relatórios
    "/cursos": ViewCursos,                  # Página de cursos
    "/formulario": ViewFormulario,          # Página de formulário
    "/configuracoes": ViewConfiguracoes,    # Página de configurações
}

def obter_view(rota: str):
    """
    Função que retorna a view correspondente à rota informada.
    
    Caso a rota não exista no dicionário ROTAS, retorna a ViewLogin por padrão.
    """
    return ROTAS.get(rota, ViewLogin)