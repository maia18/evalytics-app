import flet as ft 
import json 
from database.indicadores import INDICADORES 

def criar_modal_criterios(page, item_alvo_acao): 
    """Gera um popup para gerenciar os 5 graus de avaliação de um indicador."""
    
    # Gera de forma dinâmica os 5 campos de texto que abrigam os critérios
    campos_criterios = [ 
        ft.TextField( 
            label=f"Critério {i+1}", 
            multiline=True, # Habilita múltiplas linhas
            width=600, 
            border_color="blue200", 
        ) for i in range(5) 
    ] 

    def salvar_criterios(e): 
        """Coleta os dados, atualiza a memória e transcreve para o arquivo do banco."""
        # Agrupa o valor preenchido nos inputs num dicionário referenciado por índice 1 a 5
        novos_criterios = {str(i+1): campos_criterios[i].value for i in range(5)} 
        
        # Busca o item correto no banco em memória usando o título e o eixo como identificadores únicos
        for item in INDICADORES: 
            if item.get("titulo") == item_alvo_acao.get("titulo") and item.get("eixo") == item_alvo_acao.get("eixo"): 
                item["criterios"] = novos_criterios 
                break 
                
        # Persiste a lista atualizada reescrevendo o arquivo do banco de dados
        with open("database/indicadores.py", "w", encoding="utf-8") as f: 
            f.write(f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n") 
        
        # Exibe feedback e fecha o modal
        page.snack_bar = ft.SnackBar(ft.Text("Critérios atualizados com sucesso!", color="green")) 
        page.snack_bar.open = True 
        modal.open = False 
        page.update() 

    # 2. Estrutura visual do Modal
    modal = ft.AlertDialog( 
        modal=True, # Trava cliques fora da caixa até o usuário lidar com o formulário
        title=ft.Text("Editar Critérios", size=20, weight="bold"), 
        content=ft.Column( 
            width=600, 
            height=450, 
            scroll=ft.ScrollMode.AUTO, # Evita estourar a tela em monitores menores
            spacing=15, 
            controls=campos_criterios 
        ), 
        actions=[ 
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)), 
            ft.ElevatedButton("Salvar", on_click=salvar_criterios, bgcolor="blue700", color="white"), 
        ], 
    ) 

    # 3. Lógica para carregar os dados ao abrir
    def abrir_modal_criterios(e, indicador_selecionado): 
        """Prepara o modal preenchendo os inputs com os dados existentes do item clicado."""
        item_alvo_acao.clear() # Limpa a memória referenciada anterior
        item_alvo_acao.update(indicador_selecionado) # Seta qual indicador estamos editando
        
        criterios_atuais = indicador_selecionado.get("criterios", {}) 
        
        for i in range(5): 
            # Tenta pegar as chaves tanto como string quanto inteiro para evitar bugs com o JSON
            valor_salvo = criterios_atuais.get(str(i+1), criterios_atuais.get(i+1, "")) 
            campos_criterios[i].value = valor_salvo 
            
        # Adiciona o modal nativo à página se não estiver presente
        if modal not in page.overlay: 
            page.overlay.append(modal) 
        
        modal.open = True 
        page.update()  

    return modal, campos_criterios, abrir_modal_criterios 