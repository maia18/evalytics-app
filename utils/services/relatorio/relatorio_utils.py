def obter_semestre(data_iso: str) -> str:
    """
    Converte uma data ISO para o semestre acadêmico.
    Exemplos:
        2026-02-15 -> 2026.1
        2026-08-20 -> 2026.2
    """
    if not data_iso:
        return ""

    try:
        ano = int(data_iso[:4])
        mes = int(data_iso[5:7])
        semestre = "1" if mes <= 6 else "2"
        return f"{ano}.{semestre}"
    except (ValueError, TypeError):
        return ""

def filtrar_resultados(
    resultados: list[dict],
    semestre: str | None = None,
    eixo: int | None = None,
) -> list[dict]:
    """
    Filtra os resultados consolidados por semestre e/ou eixo em memória.
    """
    filtrados: list[dict] = []

    for resultado in resultados:

        # --------------------------------------------------
        # FILTRO DE SEMESTRE
        # --------------------------------------------------
        if semestre:
            data_avaliacao = resultado.get("data_avaliacao", "")
            if not data_avaliacao:
                continue

            semestre_resultado = obter_semestre(data_avaliacao)
            if semestre_resultado != semestre:
                continue

        # --------------------------------------------------
        # FILTRO DE EIXO
        # --------------------------------------------------
        if eixo is not None:
            eixos = resultado.get("eixos", {})
            if not isinstance(eixos, dict):
                continue

            nota_eixo = eixos.get(eixo)
            if nota_eixo is None:
                continue

            try:
                nota_eixo = float(nota_eixo)
            except (TypeError, ValueError):
                continue

            # Sem resposta para o eixo selecionado.
            if nota_eixo <= 0:
                continue

        filtrados.append(resultado)

    return filtrados