# app de mobilidade

🚖 App Mobilidade – Sistema de Caronas e Gestão de Corridas
📌 Sobre o projeto

O App Mobilidade é um projeto fullstack desenvolvido como portfólio, com objetivo de demonstrar minhas habilidades em Ciência de Dados, backend (FastAPI) e frontend (React + TailwindCSS).

A ideia principal é construir um sistema de caronas/gestão de corridas onde usuários possam:

Criar e listar corridas disponíveis 🚗

Gerenciar usuários e interações 👥

Fazer requisições a uma API segura 🔒

No estágio atual, já temos:

✅ Backend com FastAPI rodando (endpoints base configurados)

✅ Banco de dados inicial preparado (SQLAlchemy)

✅ Frontend com React + Vite instalado e funcionando

✅ TailwindCSS configurado para estilização

✅ Integração inicial API ↔ Frontend com Axios

⚙️ Tecnologias utilizadas
🔹 Backend

FastAPI
 – Framework web moderno para Python

SQLAlchemy
 – ORM para modelagem do banco

Uvicorn
 – Servidor ASGI para rodar a API

🔹 Frontend

React
 – Biblioteca para construção de interfaces

Vite
 – Build tool rápida para React

TailwindCSS
 – Framework de CSS utilitário

Axios
 – Cliente HTTP para integração com a API

⚙️ Estrutura do projeto

app-mobilidade/
│── backend/               # Código do backend
│   ├── main.py            # Ponto de entrada da API FastAPI
│   ├── models.py          # Modelos do banco de dados
│   ├── schemas.py         # Definições de schemas (Pydantic)
│   ├── database.py        # Configuração do banco SQLite
│   ├── auth.py            # Funções de autenticação
│   └── ...
│
│── frontend/              # Código do frontend
│   ├── index.html         # Estrutura principal
│   └── src/
│       └── main.js        # Arquivo principal do Vite
│
│── venv/                  # Ambiente virtual (não versionado no GitHub)
│── requirements.txt       # Dependências do Python
│── package.json           # Configuração do frontend


▶️ Como rodar o projeto

Clonar o repositório

git clone https://github.com/Augosto-PS/app-mobilidade
cd app-mobilidade

Rodar o backend (FastAPI)
Criar o ambiente virtual:

python -m venv venv
source venv/Scripts/activate   # Windows
# ou
source venv/bin/activate       # Linux/Mac

Instalar dependências: 
pip install -r requirements.txt

Rodar a API:
uvicorn main:app --reload

A API estará disponível em:  http://127.0.0.1:8000/docs

Rodar o frontend (Vite)
No diretório frontend/:

npm install
npm run dev

O frontend estará disponível em: http://127.0.0.1:5173

🔗 Status do projeto

✅ Backend configurado e rodando com FastAPI.
✅ Banco de dados SQLite conectado.
✅ Frontend inicializado com Vite.
🔄 Próximo passo: conectar frontend com a API (fetch dos dados e integração).

🎯 Objetivo do projeto

O projeto está sendo desenvolvido como portfólio profissional para demonstrar conhecimentos em:

Criação de APIs com FastAPI.

Integração backend + frontend.

Estruturação de projetos escaláveis.

Organização de código e boas práticas.









 
