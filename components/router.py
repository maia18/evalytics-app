from models.login import ViewLogin
from models.dashboard import ViewDashboard
from models.avaliacoes import ViewAvaliacoes
from models.relatorios import ViewRelatorios
from models.cursos import ViewCursos
from models.formulario import ViewFormulario
from models.configuracoes import ViewConfiguracoes

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