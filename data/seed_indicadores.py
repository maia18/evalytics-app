import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

from indicadores import INDICADORES

# Carrega as variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicializa o cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def popular_banco():
    print("Iniciando o povoamento de Eixos e Indicadores...")

    # 1. Garantir que os 3 Eixos existam
    eixos_iniciais = [
        {"id": 1, "nome": "Organização Didático-Pedagógica"},
        {"id": 2, "nome": "Corpo Docente"},
        {"id": 3, "nome": "Infraestrutura"}
    ]
    
    for eixo in eixos_iniciais:
        try:
            supabase.table("eixos").upsert(eixo).execute()
            print(f"Eixo {eixo['id']} verificado/inserido.")
        except Exception as e:
            print(f"Erro ao inserir eixo {eixo['id']}: {e}")

    # 2. Inserir os Indicadores
    print(f"\nIniciando a inserção de {len(INDICADORES)} indicadores...")
    
    # Dicionário para controlar a ordem dos indicadores dentro de cada eixo
    ordem_por_eixo = {1: 1, 2: 1, 3: 1}
    
    for ind in INDICADORES:
        eixo_id = ind.get("eixo")
        
        # Prepara o payload para o Supabase
        payload = {
            "eixo_id": eixo_id,
            "ordem": ordem_por_eixo[eixo_id],
            "titulo": ind.get("titulo"),
            "descricao": ind.get("descricao", ""),
            "criterios": ind.get("criterios") # O Supabase-py converte dict para JSONB automaticamente
        }
        
        try:
            supabase.table("indicadores").insert(payload).execute()
            print(f"✅ Inserido: Eixo {eixo_id} - {payload['titulo']}")
            ordem_por_eixo[eixo_id] += 1
        except Exception as e:
            print(f"❌ Erro ao inserir '{payload['titulo']}': {e}")

    print("\nPovoamento concluído com sucesso!")

if __name__ == "__main__":
    popular_banco()