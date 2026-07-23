from database.services.firebase_config import db
from datetime import datetime

def salvar_avaliacao(curso_id, curso_nome, respostas):
    """
    Salva o formulário de avaliação preenchido no banco de dados do Firebase (Firestore).
    
    Args:
        curso_id (str/int): O identificador único do curso avaliado.
        curso_nome (str): O nome em texto do curso para facilitar a leitura humana no banco.
        respostas (dict): Um dicionário contendo as notas dadas no formato { id_do_indicador : nota }.
        
    Returns:
        bool: Retorna True se a gravação for bem-sucedida, ou False em caso de erro.
    """
    
    try:
        # Monta o pacote de dados (documento) que será gravado na nuvem
        nova_avaliacao = {
            "curso_id": curso_id,
            "curso_nome": curso_nome,
            # Grava o momento exato do envio usando o formato ISO 8601 (ex: 2026-07-23T14:30:00)
            # Este formato é universal e excelente para ordenar dados cronologicamente no banco
            "data_avaliacao": datetime.now().isoformat(),
            "respostas": respostas
        }
        
        # Acessa a coleção "avaliacoes" (se não existir, o Firebase cria na hora)
        # e adiciona o novo documento, gerando um ID alfanumérico único automaticamente
        db.collection("avaliacoes").add(nova_avaliacao)
        
        # Log de sucesso no terminal do servidor/console
        print(f"Avaliação do curso {curso_nome} salva com sucesso!")
        return True
        
    except Exception as e:
        # Intercepta qualquer falha (queda de internet, erro de permissão) e exibe o motivo
        print(f"Erro ao salvar a avaliação: {e}")
        return False
    
def listar_avaliacoes():
    """
    Busca e retorna todas as avaliações concluídas e armazenadas na coleção do Firebase.
    
    Returns:
        list: Uma lista de dicionários, onde cada dicionário é uma avaliação completa 
              incluindo o seu ID gerado pelo banco.
    """
    
    try:
        # O método stream() cria um fluxo de leitura eficiente para buscar todos os documentos da coleção
        docs = db.collection("avaliacoes").stream()
        
        # Utiliza List Comprehension (compreensão de lista) para iterar sobre os resultados.
        # A sintaxe **doc.to_dict() "desempacota" os dados salvos e os junta com a chave "id" em um novo dicionário.
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
        
    except Exception as e:
        # Caso falhe ao tentar ler os dados, exibe o erro e retorna uma lista vazia
        # para evitar que a interface do usuário (como a tabela) quebre tentando iterar sobre 'None'
        print(f"Erro ao buscar avaliações: {e}")
        return []