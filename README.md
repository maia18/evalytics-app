# 📊 Evalytics

O **Evalytics** é uma solução inteligente para a gestão e execução de autoavaliações institucionais, desenhada para alinhar cursos superiores às diretrizes oficiais do **MEC/INEP**.

O sistema transforma o complexo processo de avaliação em uma jornada fluida, utilizando tecnologia de ponta para garantir **performance**, **escalabilidade** e uma **experiência** de usuário impecável para coordenadores e avaliadores.

---

## Stack Tecnológica

O projeto foi modernizado para oferecer uma arquitetura robusta e escalável:

* **Interface (Frontend)**: [Flet](https://flet.dev/) (Interface reativa e moderna rodando sobre o motor do Flutter)
* **Banco de Dados (Backend)**: [Firebase Firestore](https://firebase.google.com/) (Banco de dados NoSQL orientado a documentos com sincronização em tempo real)
* **Segurança**: Firebase Auth (Gestão segura de usuários e permissões administrativas)

---

## Principais Funcionalidades

* **Gerenciamento Hierárquico**: Organização intuitiva de indicadores por eixos temáticos (Pastas).

* **Editor Dinâmico**: Fluxo otimizado para atualização de títulos, descrições e critérios de avaliação com um clique.

* **Interface Cross-Platform**: Experiência consistente em diferentes dispositivos.

* **Dados em Tempo Real**: Sincronização imediata das avaliações entre usuários e base de dados.

---

## Execução local

### 1. Clonar o projeto

```
git clone https://github.com/maia18/evalytics-app.git
cd evalytics-app
```

### 2. Configurar o ambiente

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

### 5. Executar

```
flet run main.py
```

---

## Acesso de Desenvolvimento

Enquanto a autenticação via Firebase Auth está sendo implementada, as credenciais administrativas locais são:

- Usuário: admin
- Senha: admin123
