import re
import unicodedata


ALIASES_CURSOS = {
    "eng telecom": "engenharia de telecomunicacoes",
}


def chave_curso(nome: str | None) -> str:
    """Gera uma chave estável para comparar nomes e variações históricas."""
    if not nome:
        return ""

    texto = unicodedata.normalize("NFKD", str(nome).casefold())
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = re.sub(r"[^a-z0-9]+", " ", texto).strip()
    texto = re.sub(r"\s+", " ", texto)
    return ALIASES_CURSOS.get(texto, texto)


def normalizar_nome_curso(
    nome: str | None,
    nomes_cadastrados: list[str] | None = None,
) -> str:
    """Retorna a grafia do cadastro para variações equivalentes do mesmo curso."""
    if not nome or not str(nome).strip():
        return "Curso não informado"

    nome_limpo = " ".join(str(nome).split())
    chave = chave_curso(nome_limpo)

    for cadastrado in nomes_cadastrados or []:
        if chave_curso(cadastrado) == chave:
            return " ".join(str(cadastrado).split())

    if chave == "engenharia de telecomunicacoes":
        return "Engenharia de Telecomunicações"

    return nome_limpo


def listar_nomes_cursos_filtraveis(
    resultados: list[dict],
    cursos_cadastrados: list[dict],
) -> list[str]:
    """Une o catálogo da Gestão de Cursos às grafias encontradas nas avaliações."""
    nomes_cadastrados = [
        str(curso.get("nome", "")).strip()
        for curso in cursos_cadastrados
        if curso.get("nome") and str(curso.get("nome")).strip()
    ]
    nomes_por_chave = {
        chave_curso(nome): normalizar_nome_curso(nome, nomes_cadastrados)
        for nome in nomes_cadastrados
    }

    for resultado in resultados:
        nome = resultado.get("curso_nome", resultado.get("curso", ""))
        if not nome or not str(nome).strip():
            continue
        chave = chave_curso(str(nome))
        nomes_por_chave.setdefault(
            chave,
            normalizar_nome_curso(str(nome), nomes_cadastrados),
        )

    return sorted(set(nomes_por_chave.values()), key=str.casefold)
