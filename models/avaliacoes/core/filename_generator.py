import os
from datetime import datetime

# Gera um caminho de arquivo com timestamp, salvo no diretório de trabalho atual
def gerar_nome_arquivo(base_nome: str = "dados_brutos", extensao: str = "csv") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Extrai o momento atual formatado como Ano-Mês-Dia_Hora-Minuto-Segundo
    
    '''
    Concatena a string criando o nome final. 
        Ex: dados_brutos_20260710_143000.csv
    '''
    nome_arquivo = f"{base_nome}_{timestamp}.{extensao}"
    
    return os.path.join(os.getcwd(), nome_arquivo) # Retorna o caminho absoluto juntando a pasta atual com o nome do arquivo