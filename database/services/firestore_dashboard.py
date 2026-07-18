from configurations.firebase_config import db

# Calcula médias das avaliações para o dashboard
def obter_medias_dashboard():
    try:
        docs = db.collection("avaliacoes_institucionais").stream()
        soma = {"infra": 0, "didatica": 0, "atend": 0, "mat": 0, "inov": 0}
        total_avaliacoes = 0

        for doc in docs:
            dados = doc.to_dict()
            if "notas" in dados:
                soma["infra"] += dados["notas"].get("infraestrutura", 0)
                soma["didatica"] += dados["notas"].get("didatica", 0)
                soma["atend"] += dados["notas"].get("atendimento", 0)
                soma["mat"] += dados["notas"].get("material", 0)
                soma["inov"] += dados["notas"].get("inovacao", 0)
                total_avaliacoes += 1

        if total_avaliacoes == 0:
            return None

        return {
            "infraestrutura": round(soma["infra"] / total_avaliacoes, 1),
            "didatica": round(soma["didatica"] / total_avaliacoes, 1),
            "atendimento": round(soma["atend"] / total_avaliacoes, 1),
            "material": round(soma["mat"] / total_avaliacoes, 1),
            "inovacao": round(soma["inov"] / total_avaliacoes, 1),
        }
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None