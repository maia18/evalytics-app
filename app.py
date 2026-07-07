import os

from nicegui import ui

import pages.dashboard
import pages.professores
import pages.disciplinas
import pages.nova_avaliacao
import pages.avaliacoes
import pages.relatorios
import pages.eixo
import pages.login

# Pega a porta que o servidor vai exigir (ou usa a 8080 localmente)
porta = int(os.environ.get('PORT', 8080))

ui.run(
    title="Evalytics",
    host='0.0.0.0', # Necessário para servidores externos acessarem
    port=porta,     # Necessário para o Render
    reload=True,
    storage_secret="chave-super-secreta-evalytics-2026"
)