import plotly.graph_objects as go

def salvar_grafico_radar(medias: dict, nomes_eixos: dict, caminho_imagem: str) -> None:
    """Gera um gráfico de radar (Plotly) e o salva como imagem no disco."""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        # Extrai os dados garantindo que eles estão ordenados pelas mesmas chaves numéricas
        r=[medias[i] for i in sorted(medias.keys())],
        theta=[nomes_eixos[i] for i in sorted(medias.keys())],
        fill='toself', fillcolor='rgba(33, 150, 243, 0.3)', line_color='rgb(33, 150, 243)', marker=dict(size=8),
    ))
    
    # Trava a escala do radar (teia de aranha) para o limite máximo de nota 5
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
    
    # Salva silenciosamente a imagem compilada pelo Plotly em disco
    fig.write_image(caminho_imagem)