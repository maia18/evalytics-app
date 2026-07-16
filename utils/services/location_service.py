import urllib.request
import json


def obter_localizacao():

    try:

        with urllib.request.urlopen(
            "http://ip-api.com/json/",
            timeout=3
        ) as resposta:

            dados = json.loads(
                resposta.read().decode()
            )

            if dados.get("status") == "success":

                cidade = dados.get("city", "")
                estado = dados.get("region", "")

                return f"{cidade} - {estado}"

    except Exception:
        pass

    return "Localização indisponível"