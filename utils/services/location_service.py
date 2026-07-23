import urllib.request
import json

def obter_localizacao():
    """
    Tenta descobrir a localização aproximada do usuário (Cidade e Estado) baseada no seu endereço de IP.
    Faz uma requisição HTTP simples e rápida para uma API pública e gratuita.
    
    Returns:
        str: Uma string formatada "Cidade - Estado" se a busca for bem-sucedida, 
             ou "Localização indisponível" caso ocorra qualquer falha (sem internet, timeout, etc).
    """

    try:
        # Abre uma conexão com a API do ip-api.com.
        # O uso do bloco 'with' garante que a conexão de rede seja fechada corretamente após o uso, liberando recursos.
        with urllib.request.urlopen(
            "http://ip-api.com/json/", 
            timeout=3 # Crucial: Aborta a tentativa após 3 segundos para evitar que o aplicativo trave aguardando resposta
        ) as resposta:

            # Lê os dados brutos (em bytes) recebidos do servidor, decodifica para texto (string)
            # e então converte (faz o parse) do formato JSON para um dicionário Python.
            dados = json.loads(
                resposta.read().decode()
            )

            # A API retorna uma chave 'status' que indica se conseguiu mapear o IP
            if dados.get("status") == "success":

                # Extrai a cidade e a região (geralmente a sigla do estado no Brasil)
                # O uso do .get() previne erros caso as chaves não existam no dicionário, retornando uma string vazia por padrão
                cidade = dados.get("city", "")
                estado = dados.get("region", "")

                # Retorna os dados formatados (ex: "Fortaleza - CE")
                return f"{cidade} - {estado}"

    except Exception:
        # Se qualquer coisa der errado (falta de internet, servidor fora do ar, limite de tempo excedido),
        # o código ignora o erro silenciosamente (pass) e segue para o retorno padrão abaixo.
        pass

    # Fallback: Retorno seguro caso o bloco try falhe ou a API não retorne 'success'
    return "Localização indisponível"