from nicegui import ui

import pages.dashboard
import pages.professores
import pages.disciplinas
import pages.nova_avaliacao
import pages.avaliacoes
import pages.relatorios
import pages.eixo
import pages.login

ui.run(
    title="Evalytics",
    reload=True,
    storage_secret="chave-super-secreta-evalytics-2026" 
)