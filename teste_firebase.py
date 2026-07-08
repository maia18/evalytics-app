from database.firebase_client import db

print("A tentar conectar ao Firebase e criar um documento...")

try:
    # Vamos criar uma coleção chamada "professores" e adicionar um documento
    doc_ref = db.collection("professores").document()
    doc_ref.set({
        "nome": "Professor Teste",
        "departamento": "Engenharia Informática",
        "ativo": True
    })
    
    print("Sucesso! Documento adicionado.")
    print(f"ID do documento criado: {doc_ref.id}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")