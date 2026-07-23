from database.services.firebase_config import db

def listar_indicadores():
    """
    Busca e retorna todos os indicadores de avaliação cadastrados no Firebase.
    Útil para preencher os formulários de avaliação de forma dinâmica.
    
    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um indicador 
              com seus dados (nome, categoria, status) e o seu 'id' único.
    """
    
    try:
        # Abre um fluxo de leitura contínuo (stream) para buscar todos os documentos da coleção
        docs = db.collection("indicadores").stream()
        
        # Desempacota os dados de cada documento e mescla com o ID nativo gerado pelo Firebase
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
        
    except Exception as e:
        # Tratamento de erro seguro: em caso de falha de conexão, loga o erro e retorna uma lista vazia,
        # impedindo que a aplicação trave ao tentar renderizar elementos nulos.
        print(f"Erro ao buscar indicadores: {e}")
        return []

def criar_indicador(nome, categoria):
    """
    Cadastra um novo indicador (pergunta/critério) para as avaliações no Firebase.
    
    Args:
        nome (str): O texto descritivo do indicador (ex: "Clareza na exposição do conteúdo").
        categoria (str): O eixo ao qual este indicador pertence (ex: "Didática", "Infraestrutura").
    """
    
    try:
        # Monta a estrutura de dados a ser salva na nuvem
        novo_indicador = {
            "nome": nome,
            "categoria": categoria,
            # Flag booleana (Soft Delete) permitindo que o indicador seja desativado em semestres 
            # futuros sem quebrar o histórico de relatórios passados.
            "ativo": True
        }
        
        # Adiciona o registro à coleção "indicadores". O ID é gerado automaticamente.
        db.collection("indicadores").add(novo_indicador)
        print("Indicador criado com sucesso!")
        
    except Exception as e:
        # Intercepta e exibe problemas de gravação
        print(f"Erro ao criar indicador: {e}")
        
def atualizar_indicador(id_indicador, novo_nome):
    """
    Atualiza especificamente o nome/texto de um indicador já existente.
    
    Args:
        id_indicador (str): O ID único do indicador que será alterado.
        novo_nome (str): O novo texto que substituirá o valor atual.
    """
    
    try:
        # Acessa o documento específico pelo seu ID e utiliza o método .update().
        # Diferente do .set(), o .update() modifica apenas o campo especificado (neste caso, "nome")
        # e falha propositalmente se o documento não existir, evitando a criação de registros "fantasmas".
        db.collection("indicadores").document(id_indicador).update({
            "nome": novo_nome
        })
        
    except Exception as e:
        # Loga falhas como IDs inválidos ou falta de permissão de escrita
        print(f"Erro ao atualizar indicador: {e}")