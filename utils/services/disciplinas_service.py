from database.services.firebase_config import db

# Centralizar o nome da coleção em uma constante evita erros de digitação (typos)
# e facilita futuras manutenções na estrutura do banco de dados.
COLECAO = "disciplinas" 

def criar_disciplina(nome: str, codigo: str, carga_horaria: int):
    """
    Cria uma nova disciplina no banco de dados do Firebase.
    Diferente do método .add() direto, esta função cria a referência primeiro 
    para poder capturar e retornar o ID gerado imediatamente após a gravação.
    
    Args:
        nome (str): Nome completo da disciplina (ex: "Eletromagnetismo Aplicado").
        codigo (str): Código interno ou acadêmico da instituição (ex: "FIS201").
        carga_horaria (int): Total de horas-aula previstas para a disciplina.
        
    Returns:
        str: O ID alfanumérico único gerado pelo Firebase para este documento recém-criado.
    """
    
    # Cria uma nova referência de documento "vazia". 
    # O Firebase gera o ID automaticamente neste momento, mesmo antes de salvar os dados.
    doc_ref = db.collection(COLECAO).document()
    
    # Monta o dicionário com as informações a serem gravadas
    dados = {
        "nome": nome,
        "codigo": codigo,
        "carga_horaria": carga_horaria
    }
    
    # Salva fisicamente os dados na referência criada
    doc_ref.set(dados)
    
    # Retorna o ID gerado, muito útil caso o front-end precise desse ID na mesma hora 
    # (ex: para redirecionar o usuário para a página de detalhes da disciplina recém-criada)
    return doc_ref.id

def listar_disciplinas():
    """
    Busca e retorna todas as disciplinas cadastradas no Firebase.
    
    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma disciplina 
              completamente desempacotada e com seu respectivo ID.
    """
    
    disciplinas = []
    
    # Inicia um fluxo (stream) de leitura de todos os documentos da coleção
    docs = db.collection(COLECAO).stream()
    
    # Itera sobre o objeto retornado pelo banco de dados
    for doc in docs:
        # Converte o documento bruto do Firestore para um dicionário Python padrão
        dados = doc.to_dict()
        
        # Injeta o ID único dentro do dicionário para que a interface de usuário 
        # consiga identificar qual registro é qual na hora de editar ou excluir
        dados["id"] = doc.id
        
        # Adiciona o registro já processado e pronto para uso na lista final
        disciplinas.append(dados)
        
    return disciplinas

def atualizar_disciplina(disciplina_id: str, dados_atualizados: dict):
    """
    Atualiza campos específicos de uma disciplina já existente.
    
    Args:
        disciplina_id (str): O ID único da disciplina que será modificada.
        dados_atualizados (dict): Dicionário contendo APENAS as chaves e valores que devem ser alterados.
        
    Returns:
        bool: True para indicar que o comando foi executado.
    """
    
    # Localiza a referência exata do documento a ser atualizado pelo seu ID
    doc_ref = db.collection(COLECAO).document(disciplina_id)
    
    # O uso do 'merge=True' é a chave aqui! Ele instrui o Firebase a mesclar os novos dados
    # com os dados existentes. Se não usássemos isso, o comando .set() apagaria tudo o que 
    # não foi enviado no dicionário 'dados_atualizados', causando perda de dados.
    doc_ref.set(dados_atualizados, merge=True)
    
    return True

def deletar_disciplina(disciplina_id: str):
    """
    Apaga uma disciplina permanentemente do banco de dados (Hard Delete).
    
    Args:
        disciplina_id (str): O ID único da disciplina que será removida.
        
    Returns:
        bool: True para indicar que o comando foi executado.
    """
    
    # Acessa a coleção, aponta diretamente para o documento específico e aciona a exclusão.
    # Cuidado: esta operação é irreversível no Firebase.
    db.collection(COLECAO).document(disciplina_id).delete()
    
    return True
