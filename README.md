
# 🐾 POAS - Sistema para Clínica Veterinária

Sistema desenvolvido para a disciplina **POAS**, com o objetivo de gerenciar uma clínica veterinária, permitindo o controle de usuários, clientes, animais, produtos, atendimentos e agendamentos, através de uma API REST desenvolvida em **FastAPI** e uma interface moderna em **React**.

---

## Integrantes
- Kaik Emanuel
- Isaac Fonseca
- Bruno Ildo 
- Weslley Wender

---
# 🚀 Tecnologias Utilizadas

## Backend
- 🐍 Python
- ⚡ FastAPI
- 🔐 JWT (JSON Web Token)
- 🗄️ SQLAlchemy
- 🗃️ SQLite
- 🔒 Pwdlib (Hash de Senhas)
- 📄 Swagger/OpenAPI

## Frontend
- ⚛️ React
- 📡 Axios
- 🎨 CSS
- 📊 Recharts
- ⚡ Vite

---

# 📁 Estrutura do Projeto

```text
POAS---PROJETO/

├── backend/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── schemas/
│   ├── config/
│   ├── database/
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   ├── assets/
│   │   └── App.jsx
│
├── tests/
│
└── README.md
```

---

# ▶️ Como rodar o Backend

## 1. Abra um terminal
- PowerShell
- CMD

---

## 2. Navegue até a pasta do backend

```bash
cd C:\Users\COMPUTER\Documents\POAS---PROJETO\backend
```

---

## 3. Crie e ative um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Instale as dependências

```bash
pip install -r requirements.txt
```

Caso não exista um arquivo `requirements.txt`, instale as principais dependências:

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv pwdlib python-jose python-multipart
```

---

## 5. Inicie a API

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000
```

---

## 📄 Documentação da API (Swagger)

Após iniciar a aplicação, acesse:

```
http://127.0.0.1:8000/docs
```

ou

```
http://127.0.0.1:8000/redoc
```

---

# 💻 Como rodar o Frontend

## 1. Abra outro terminal

- PowerShell
- CMD

---

## 2. Navegue até a pasta do frontend

```bash
cd C:\Users\COMPUTER\Documents\POAS---PROJETO\frontend
```

---

## 3. Instale as dependências

```bash
npm install
```

---

## 4. Execute o projeto

```bash
npm run dev
```

O React será iniciado em:

```
http://localhost:5173
```

---

# 🔐 Funcionalidades

## 👤 Usuários

- ✅ Cadastro
- ✅ Login
- ✅ Logout
- ✅ Autenticação JWT
- ✅ Controle de permissões por perfil

---

## 🐶 Animais

- ✅ Cadastro
- ✅ Consulta
- ✅ Atualização
- ✅ Exclusão

---

## 💉 Vacinas

```
GET    /vacinas
GET    /vacinas/{id}
POST   /vacinas
PUT    /vacinas/{id}
DELETE /vacinas/{id}
```

---

## 💊 Aplicações de Vacinas

```
GET    /aplicacoes-vacina
GET    /aplicacoes-vacina/{id}
POST   /aplicacoes-vacina
PUT    /aplicacoes-vacina/{id}
DELETE /aplicacoes-vacina/{id}
```

---

## 👨‍⚕️ Veterinários

- ✅ Cadastro
- ✅ Controle de acesso

---

## 👥 Clientes

- ✅ Cadastro
- ✅ Atualização
- ✅ Busca
- ✅ Validação de CPF
- ✅ Validação de e-mail

---

## 📅 Agendamentos

- ✅ Cadastro
- ✅ Atualização
- ✅ Cancelamento
- ✅ Consultas futuras

---

## 🩺 Atendimentos

- ✅ Registro de atendimento
- ✅ Histórico

---

## 📦 Produtos

- ✅ Cadastro
- ✅ Controle de estoque
- ✅ Consulta
- ✅ Atualização

---

## 📊 Dashboard

- ✅ Total de usuários
- ✅ Total de clientes
- ✅ Total de animais
- ✅ Total de produtos
- ✅ Total de atendimentos
- ✅ Total de agendamentos
- ✅ Valor total do estoque
- ✅ Produtos sem estoque
- ✅ Produtos com estoque baixo
- ✅ Animal mais velho
- ✅ Cliente com mais animais
- ✅ Média de idade dos animais
- ✅ Agendamentos do dia
- ✅ Agendamentos futuros
- ✅ Gráficos estatísticos

---

# 🔐 Segurança

- 🔒 Autenticação JWT
- 🔑 Senhas criptografadas
- 👥 Controle de acesso por perfil
- 🚫 Rotas protegidas
- ✅ Validação de dados
- 🔒 Logout com revogação de token

---

# 📡 API Endpoints

## Login

```
POST /login
```

---

## Usuários

```
GET    /usuarios
GET    /usuarios/{id}
POST   /usuarios
PUT    /usuarios/{id}
DELETE /usuarios/{id}
```

---

## Clientes

```
GET    /clientes
GET    /clientes/{id}
POST   /clientes
PUT    /clientes/{id}
DELETE /clientes/{id}
```

---

## Animais

```
GET    /animais
GET    /animais/{id}
POST   /animais
PUT    /animais/{id}
DELETE /animais/{id}
```

---

## 💉 Vacinas

```
GET    /vacinas
GET    /vacinas/{id}
POST   /vacinas
PUT    /vacinas/{id}
DELETE /vacinas/{id}
```

---

## 💊 Aplicações de Vacinas

```
GET    /aplicacoes-vacina
GET    /aplicacoes-vacina/{id}
POST   /aplicacoes-vacina
PUT    /aplicacoes-vacina/{id}
DELETE /aplicacoes-vacina/{id}
```

---

## Produtos

```
GET    /produtos
GET    /produtos/{id}
POST   /produtos
PUT    /produtos/{id}
DELETE /produtos/{id}
```

---

## Agendamentos

```
GET    /agendamentos
GET    /agendamentos/{id}
POST   /agendamentos
PUT    /agendamentos/{id}
DELETE /agendamentos/{id}
```

---

## Atendimentos

```
GET    /atendimentos
GET    /atendimentos/{id}
POST   /atendimentos
PUT    /atendimentos/{id}
DELETE /atendimentos/{id}
```

---

## Dashboard

```
GET /dashboard
```

---

# **Cronograma**

## 1º Bimestre – Planejamento e Estruturação do Projeto

**Período:** 12/03/2026 – 18/05/2026

Nesta etapa foi realizado o planejamento do sistema e a organização inicial do projeto.

### 12/03/2026 – 10/04/2026 | Planejamento e Documentação

* Definição do objetivo do sistema;
* Levantamento dos requisitos funcionais;
* Escolha das tecnologias utilizadas;
* Criação do repositório no GitHub;
* Elaboração e atualização do README.md.

### 11/04/2026 – 18/05/2026 | Prototipação e Estrutura Inicial

* Desenvolvimento dos protótipos utilizando Canva;
* Planejamento das telas do sistema;
* Definição do fluxo de navegação;
* Configuração do ambiente de desenvolvimento;
* Estruturação inicial da API REST;



---

## 2º Bimestre – Desenvolvimento dos Módulos Principais

**Período:** 19/05/2026 – 20/07/2026

Nesta fase serão desenvolvidas as principais funcionalidades da clínica veterinária.

### 19/05/2026 – 20/06/2026 | Backend

* Cadastro de usuários;
* Login e logout;
* Cadastro de clientes;
* Cadastro de animais;
* Implementação da autenticação JWT.
* Implementação das regras de negócio;
* Testes dos endpoints.

### 21/06/2026 – 20/07/2026 | Consultas e Serviços

* Agendamento de consultas;
* Agendamento de banho e tosa;
* Registro de atendimentos;
* Histórico de consultas e serviços;
* Correção de erros encontrados.
* Configuração do banco de dados;

---

## 3º Bimestre – Frontend e Módulo Pet Shop

**Período:** 10/08/2026 – 13/10/2026

Nesta etapa serão desenvolvidas as interfaces do sistema e as funcionalidades de venda de produtos.

### 10/08/2026 – 10/09/2026 | Desenvolvimento do Frontend

* Página inicial;
* Tela de login e cadastro;
* Telas de clientes, animais e agendamentos;
* Integração entre frontend e backend.

### 11/09/2026 – 13/10/2026 | Módulo Pet Shop

* Cadastro de produtos;
* Busca e listagem de produtos;
* Implementação do carrinho de compras;
* Integração das funcionalidades de compra;
* Ajustes visuais e responsividade.

---

## 4º Bimestre – Infraestrutura e Entrega Final

**Período:** 14/10/2026 – 18/12/2026

Nesta fase será realizada a implantação da aplicação e a preparação para a entrega final.

### 14/10/2026 – 15/11/2026 | Infraestrutura

* Containerização com Docker;
* Configuração dos containers;
* Criação dos arquivos YAML;
* Implantação utilizando Kubernetes;
* Testes de implantação.

### 16/11/2026 – 18/12/2026 | Finalização

* Testes finais do sistema;
* Correção de bugs;
* Atualização da documentação;
* Organização do repositório;
* Criação dos slides;
* Preparação da apresentação;
* Entrega final do projeto.
