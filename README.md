# 📊 Evalytics - Sistema de Avaliação Institucional

O **Evalytics** é uma plataforma web e mobile desenvolvida em Python para gestão e execução de autoavaliações institucionais baseadas nas diretrizes oficiais do **MEC/INEP**. 

O projeto está passando por uma **migração arquitetural estratégica** para adoção de uma interface cross-platform com **Flet** (baseado em Flutter) e um backend serverless escalável em tempo real com **Firebase**.

---

## 🚀 Nova Stack Tecnológica (Em migração)

* **Interface de Usuário (Frontend):** [Flet](https://flet.dev/) (Interface reativa e moderna rodando sobre o motor do Flutter)
* **Banco de Dados (Backend):** [Firebase Firestore](https://firebase.google.com/) (Banco de dados NoSQL orientado a documentos com sincronização em tempo real)
* **Autenticação:** Firebase Auth (Gestão segura de usuários e permissões administrativas)
* **Visualização de Dados:** Flet Charts ou Plotly

---

## 🗺️ Roadmap de Migração (Etapas)

Para garantir a estabilidade do sistema, a transição está dividida nas seguintes fases:

- [x] **Etapa 1: Planejamento e Alinhamento do Repositório** -> Atualização da documentação e definição do escopo.
- [ ] **Etapa 2: Infraestrutura Firebase** -> Criação do projeto no console, ativação do Firestore e geração da chave `firebase_credentials.json`.
- [ ] **Etapa 3: Modelagem NoSQL** -> Desenho das novas coleções (`professores`, `disciplinas`, `indicadores`, `avaliacoes`) e reescrita dos módulos de `services/`.
- [ ] **Etapa 4: Estrutura Base no Flet** -> Criação do arquivo principal com o sistema de rotas (`ft.View`) e tela de Login integrada ao Firebase Auth.
- [ ] **Etapa 5: Migração de Telas** -> Adaptação passo a passo dos formulários de cadastro, do questionário reativo e do dashboard.
- [ ] **Etapa 6: Relatórios e Exportação** -> Reimplementação da exportação de dados (CSV/Excel) e gráficos no novo ecossistema.

---

## ⚙️ Como preparar o ambiente local

Se você deseja colaborar com o desenvolvimento desta nova fase do projeto:

### 1. Clonar o repositório

```
git clone [https://github.com/maia18/evalytics-app.git](https://github.com/maia18/evalytics-app.git)
cd evalytics-app
```
---

### 2. Criar e ativar o Ambiente Virtual

#### Windows:

```
python -m venv venv
.\venv\Scripts\activate
```

#### Linux / Mac:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```
pip install flet firebase-admin
pip freeze > requirements.txt
```

### 4. Credenciais de Segurança


​Por questões de segurança, as chaves do Firebase não são enviadas ao GitHub. 
Você precisará solicitar o arquivo 
```firebase_credentials.json``` à equipe e colá-lo na raiz do projeto (o arquivo já está configurado no .gitignore).

### 5. Executar a aplicação

```
flet run app.py
```

---

## 🔐 Controle de Acesso Temporário (Desenvolvimento)

Enquanto a autenticação via Firebase Auth está sendo implementada, as credenciais administrativas locais são:

- Usuário: admin
- Senha: admin123