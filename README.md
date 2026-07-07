# 📊 Evalytics - Sistema de Avaliação Institucional

O **Evalytics** é uma plataforma web desenvolvida em Python para gestão e execução de autoavaliações institucionais. O sistema é baseado nas diretrizes oficiais do instrumento de avaliação de cursos de graduação do **MEC/INEP**, permitindo a geração de relatórios detalhados e gráficos de radar para análise de desempenho por eixos.

## 🚀 Tecnologias Utilizadas

* **Backend & Frontend:** [Python](https://www.python.org/) com [NiceGUI](https://nicegui.io/)
* **Banco de Dados:** [Supabase](https://supabase.com/) (PostgreSQL)
* **Visualização de Dados:** [Plotly](https://plotly.com/)
* **Exportação:** Geração nativa de relatórios em CSV

## ⚙️ Como executar o projeto localmente

Se você deseja rodar este projeto no seu computador, siga o passo a passo abaixo:

### 1. Pré-requisitos
Certifique-se de ter o [Python 3.x](https://www.python.org/downloads/) e o [Git](https://git-scm.com/) instalados na sua máquina.

### 2. Clonar o repositório
Abra o seu terminal e baixe o código para a sua máquina:
```
git clone [https://github.com/maia18/evalytics-app.git](https://github.com/SEU-USUARIO/evalytics-app.git)
cd evalytics-app
```

### 3. Criar e ativar o Ambiente Virtual

#### Windows:

```
python -m venv venv
.\venv\Scripts\activate
```

#### Linux / Mac::

```
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar as dependências

```
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente:

```
SUPABASE_URL=[https://sua-url-do-supabase.supabase.co](https://sua-url-do-supabase.supabase.co)
SUPABASE_KEY=sua-chave-anon-public-do-supabase
```
