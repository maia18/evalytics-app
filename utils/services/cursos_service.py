from database.services.firebase_config import db

def listar_cursos():
    """
    Busca e retorna todos os cursos cadastrados na coleção 'cursos' do Firebase.
    Ideal para popular as listas, menus suspensos (Dropdowns) e tabelas da interface.
    
    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um curso 
              com seus dados e o seu 'id' único gerado pelo banco.
    """
    
    try:
        # Cria um fluxo de leitura (stream) eficiente para buscar todos os documentos da coleção "cursos"
        docs = db.collection("cursos").stream()
        
        # Utiliza compreensão de lista (List Comprehension) para montar o retorno.
        # O operador ** desempacota os dados do documento (to_dict()) e os mescla com o ID nativo do Firebase.
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
        
    except Exception as e:
        # Em caso de falha de conexão ou erro de leitura, exibe o erro no terminal
        # e retorna uma lista vazia para evitar que a aplicação quebre ao tentar renderizar os dados na tela.
        print(f"Erro ao buscar cursos: {e}")
        return []

def criar_curso(nome, modalidade):
    """
    Cadastra um novo curso no banco de dados da nuvem (Firestore).
    
    Args:
        nome (str): O nome oficial do curso (ex: "Sistemas de Informação").
        modalidade (str): O formato de ensino oferecido (ex: "Presencial", "EAD", "Híbrido").
    """
    
    try:
        # Monta o dicionário (pacote de dados) que representa o documento a ser salvo
        novo_curso = {
            "nome": nome,
            "modalidade": modalidade, # Ex: Presencial, EAD, Híbrido
            
            # Flag booleana inicializada como True por padrão. 
            # Permite ocultar cursos do sistema no futuro sem perder o histórico de dados já salvos.
            "ativo": True 
        }
        
        # Acessa a coleção "cursos" e insere o novo registro.
        # O Firebase gerará um ID alfanumérico único automaticamente para este documento.
        db.collection("cursos").add(novo_curso)
        
        # Log de feedback positivo no terminal do servidor
        print("Curso criado com sucesso!")
        
    except Exception as e:
        # Intercepta e exibe qualquer erro ocorrido durante a tentativa de gravação (ex: queda de rede)
        print(f"Erro ao criar curso: {e}")