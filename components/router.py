from views.login import ViewLogin
from views.dashboard import ViewDashboard
from views.avaliacoes import ViewAvaliacoes
from views.relatorios import ViewRelatorios
from views.cursos import ViewCursos
from views.formulario import ViewFormulario
from views.configuracoes import ViewConfiguracoes

ROTAS = {
    "/": ViewLogin,
    "/dashboard": ViewDashboard,
    "/avaliacoes": ViewAvaliacoes,
    "/relatorios": ViewRelatorios,
    "/cursos": ViewCursos,
    "/formulario": ViewFormulario,
    "/configuracoes": ViewConfiguracoes,
}


def obter_view(rota: str):
    return ROTAS.get(rota, ViewLogin)