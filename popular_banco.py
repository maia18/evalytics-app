from config.firebase_config import db
from indicadores import INDICADORES

def popular_indicadores():
    print("🚀 Iniciando a importação dos indicadores para o Firebase...\n")
    
    colecao = db.collection("indicadores")
    
    # Mapeamento para traduzir o número do eixo para texto
    nomes_eixos = {
        1: "Organização Didático-Pedagógica",
        2: "Corpo Docente e Tutorial",
        3: "Infraestrutura"
    }

    contador = 0
    for ind in INDICADORES:
        
        # A MÁGICA AQUI: Converte as chaves (1, 2, 3...) de número para texto ("1", "2", "3"...)
        criterios_formatados = {str(chave): valor for chave, valor in ind["criterios"].items()}
        
        # Prepara o documento no formato que o nosso sistema usa
        novo_doc = {
            "nome": ind["titulo"],
            "categoria": nomes_eixos.get(ind["eixo"], "Geral"),
            "eixo": ind["eixo"],
            "descricao": ind["descricao"],
            "criterios": criterios_formatados, # Salva com as chaves convertidas
            "ativo": True
        }
        
        # Envia para a nuvem
        colecao.add(novo_doc)
        contador += 1
        print(f"✅ Adicionado: {ind['titulo']} (Eixo {ind['eixo']})")

    print(f"\n🎉 Sucesso! {contador} indicadores foram cadastrados no banco de dados.")

if __name__ == "__main__":
    popular_indicadores()