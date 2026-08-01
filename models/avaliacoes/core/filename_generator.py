import os
from datetime import datetime

def gerar_nome_arquivo(base_nome: str = "dados_brutos", extensao: str = "csv") -> str:
    """Gera um caminho de arquivo com timestamp, salvo no diretório de trabalho atual.
    
        NOTA: usa os.getcwd(), que pode variar conforme onde o processo foi iniciado (especialmente em builds empacotados). Mantido como estava; considerar um diretório fixo (ex: pasta de Downloads do usuário) numa futura revisão consciente deste comportamento.
    """
    
    # Extrai o momento atual formatado como Ano-Mês-Dia_Hora-Minuto-Segundo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    
    '''
    Concatena a string criando o nome final. 
        Ex: dados_brutos_20260710_143000.csv
    '''
    nome_arquivo = f"{base_nome}_{timestamp}.{extensao}"
    
    # Retorna o caminho absoluto juntando a pasta atual com o nome do arquivo
    return os.path.join(os.getcwd(), nome_arquivo)