import os
from datetime import datetime

def gerar_nome_arquivo(base_nome="dados_brutos", extensao="csv"):
    
    """Gera nome de arquivo com timestamp"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{base_nome}_{timestamp}.{extensao}"
    return os.path.join(os.getcwd(), nome_arquivo)
