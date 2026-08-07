import logging
from database.indicadores import INDICADORES # Importa a lista estática local
from database.services.firebase_config import db # Importa o cliente Firestore configurado

def realizar_migracao_inicial():
    """Script temporário para popular o Firestore com os dados do arquivo local."""
    colecao = db.collection("indicadores")
    
    print("Iniciando verificação do banco de dados...")
    
    # Verificação de segurança: checa se já existem dados para evitar duplicatas
    docs_existentes = list(colecao.limit(1).stream())
    if docs_existentes:
        print("Aviso: O banco já possui indicadores. Migração cancelada para evitar duplicatas.")
        return

    sucesso = 0
    erros = 0
    
    print(f"Migrando {len(INDICADORES)} indicadores para a nuvem. Aguarde...")

    for item in INDICADORES:
        try:
            # Garante que a chave status exista, assumindo ATIVO como padrão
            if "status" not in item:
                item["status"] = "ATIVO"
            
            # Dispara a gravação no Firestore usando o client
            colecao.add(item)
            sucesso += 1
            
        except Exception as e:
            erros += 1
            logging.error(f"Erro ao migrar o indicador '{item.get('titulo')}': {e}")
    
    print("-" * 40)
    print("Migração finalizada!")
    print(f"Sucesso: {sucesso} indicadores salvos no Firestore.")
    print(f"Erros: {erros}")

if __name__ == "__main__":
    realizar_migracao_inicial()