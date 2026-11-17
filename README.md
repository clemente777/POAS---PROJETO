# 🐾 Petonline24h — Sistema de Gerenciamento Veterinário

Sistema web desenvolvido para a disciplina **POAS**, com o objetivo de auxiliar no gerenciamento das atividades de uma clínica veterinária e de um pet shop.

O **Petonline24h** oferece recursos para gerenciamento de usuários, clientes, animais, veterinários, agendamentos, atendimentos, vacinas, produtos, estoque, carrinho de compras e pedidos.

A aplicação utiliza uma arquitetura composta por uma API REST desenvolvida com **Python e FastAPI**, um frontend desenvolvido com **React e Vite** e um banco de dados **MySQL**.

O projeto também conta com autenticação, controle de acesso por perfil, dashboard estatístico, interface responsiva e suporte a Progressive Web App (PWA), permitindo sua instalação em dispositivos compatíveis.

---

## 📑 Sumário

- [Integrantes](#-integrantes)
- [Objetivos do Projeto](#-objetivos-do-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração do Backend](#-configuração-do-backend)
- [Configuração do Frontend](#-configuração-do-frontend)
- [Banco de Dados](#-banco-de-dados)
- [Documentação da API](#-documentação-da-api)
- [Funcionalidades](#-funcionalidades-do-sistema)
- [Autenticação e Segurança](#-autenticação-e-segurança)
- [Acesso pela Rede Local](#-acesso-pela-rede-local-computador-e-celular)
- [Responsividade](#-responsividade-da-interface)
- [Progressive Web App (PWA)](#-progressive-web-app-pwa)
- [Testes Automatizados](#-testes-automatizados)
- [Solução de Problemas](#-solução-de-problemas)
- [Cronograma](#-cronograma-do-projeto)
- [Considerações Finais](#-considerações-finais)

---

## 👥 Integrantes

- Kaik Emanuel
- Isaac Fonseca
- Bruno Ildo
- Weslley Wender

---

## 🎯 Objetivos do Projeto

O Petonline24h foi desenvolvido com o propósito de centralizar e facilitar o gerenciamento das atividades de uma clínica veterinária.

Entre os principais objetivos estão:

- Organizar o cadastro e o gerenciamento de usuários.
- Facilitar o controle de clientes e seus animais.
- Gerenciar agendamentos e atendimentos veterinários.
- Registrar vacinas e aplicações.
- Controlar produtos e estoque.
- Permitir o gerenciamento de carrinhos e pedidos.
- Disponibilizar informações administrativas por meio de dashboards.
- Garantir controle de acesso conforme o perfil do usuário.
- Permitir o acesso por computadores, celulares e tablets.
- Oferecer a possibilidade de instalação como aplicativo web por meio de PWA.

---

## 🚀 Tecnologias Utilizadas

### Backend

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação do backend. |
| FastAPI | Desenvolvimento da API REST. |
| SQLAlchemy | Mapeamento objeto-relacional e comunicação com o banco de dados. |
| MySQL | Armazenamento persistente das informações. |
| Pwdlib | Hash e verificação de senhas. |
| JWT | Autenticação baseada em tokens. |
| Uvicorn | Servidor ASGI utilizado para executar a API. |
| Swagger/OpenAPI | Documentação e testes dos endpoints. |
| Pytest | Execução de testes automatizados. |
| Alembic | Gerenciamento de migrações do banco de dados. |

### Frontend

| Tecnologia | Finalidade |
|---|---|
| React | Construção da interface de usuário. |
| JavaScript | Linguagem utilizada no frontend. |
| Vite | Ferramenta de desenvolvimento e compilação. |
| Axios | Comunicação HTTP com o backend. |
| CSS | Estilização e responsividade. |
| Recharts | Construção de gráficos estatísticos. |
| Lucide React | Biblioteca de ícones. |
| React Router | Gerenciamento das rotas da aplicação. |
| vite-plugin-pwa | Integração dos recursos PWA com o Vite. |
| Workbox | Geração e gerenciamento do cache do Service Worker. |

### Banco de Dados

- MySQL.
- SQLAlchemy.
- Alembic.

---

## 🏗️ Arquitetura do Sistema

O projeto utiliza uma arquitetura dividida em frontend, backend e banco de dados.

Cada parte possui responsabilidades específicas.

### 1. Frontend

Desenvolvido em React, é responsável pela apresentação visual e pela interação com os usuários.

Suas responsabilidades incluem:

- Exibir páginas e componentes.
- Apresentar formulários.
- Realizar validações de interface.
- Enviar requisições HTTP.
- Exibir os dados retornados pela API.
- Controlar a navegação entre as páginas.
- Adaptar a interface a diferentes tamanhos de tela.

### 2. Backend

Desenvolvido com FastAPI, é responsável pelo processamento das solicitações e pelas regras de negócio.

Suas responsabilidades incluem:

- Receber requisições HTTP.
- Validar informações.
- Autenticar usuários.
- Verificar permissões.
- Executar regras de negócio.
- Consultar e atualizar informações no banco de dados.
- Retornar respostas ao frontend.

A estrutura do backend utiliza separação entre rotas, schemas, serviços, implementações de serviços, repositórios e modelos.

### 3. Banco de Dados

O MySQL é responsável pelo armazenamento persistente das informações do sistema.

O acesso aos dados é realizado pelo backend, utilizando SQLAlchemy.

O frontend e os dispositivos dos usuários não acessam diretamente o banco de dados.

### 4. Fluxo de comunicação

O funcionamento geral pode ser representado da seguinte maneira:

```text
┌─────────────────────────────┐
│          USUÁRIO            │
│    Computador ou Celular    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          FRONTEND           │
│         React + Vite        │
│                             │
│  Páginas, formulários,      │
│  componentes e dashboards   │
└──────────────┬──────────────┘
               │
               │ Requisições HTTP
               │ Axios + JWT
               ▼
┌─────────────────────────────┐
│          BACKEND            │
│           FastAPI           │
│                             │
│  Rotas, serviços, regras    │
│  de negócio e repositórios  │
└──────────────┬──────────────┘
               │
               │ SQLAlchemy
               ▼
┌─────────────────────────────┐
│        BANCO DE DADOS       │
│            MySQL            │
└─────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

A organização principal do repositório é apresentada abaixo:

```text
POAS---PROJETO/
│
├── backend/
│   ├── auth/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   │   └── implementations/
│   └── ...
│
├── frontend/
│   ├── public/
│   │   ├── apple-touch-icon.png
│   │   ├── icon-192.png
│   │   ├── icon-512.png
│   │   └── manifest.webmanifest
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── index.css
│   │   ├── responsive.css
│   │   ├── main.jsx
│   │   └── App.jsx
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
└── .env (configuração local, não versionada)
```

**Observação:** a estrutura apresenta os diretórios e arquivos principais. Outros arquivos e subdiretórios podem existir no projeto.

---

## 💻 Pré-requisitos

Antes de executar o sistema, é necessário possuir:

- Python instalado.
- Node.js e npm instalados.
- MySQL instalado e em execução.
- Git para clonar e atualizar o repositório.
- Um navegador moderno.
- Editor de código, como Visual Studio Code.

Também é necessário ter acesso às dependências listadas nos arquivos `requirements.txt` e `frontend/package.json`.

---

## ⚙️ Configuração do Backend

### 1. Obter o projeto

Caso ainda não tenha o repositório em seu computador:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd POAS---PROJETO
```

### 2. Criar o ambiente virtual

Na raiz do projeto, execute:

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

**Windows — PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows — CMD:**

```cmd
venv\Scripts\activate
```

Após a ativação, o terminal deverá indicar que o ambiente virtual está ativo.

### 4. Instalar as dependências

Execute:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configurar as variáveis de ambiente

O backend utiliza configurações externas para acessar o banco de dados e os recursos necessários à aplicação.

Crie o arquivo `.env` na raiz do projeto, conforme as variáveis esperadas pela configuração do backend.

As informações devem corresponder à configuração utilizada no código, incluindo:

- Endereço do servidor MySQL.
- Porta do MySQL.
- Nome do banco de dados.
- Usuário do banco.
- Senha do banco.
- Chave secreta utilizada na autenticação, quando aplicável.

**Importante:** não compartilhe credenciais reais e não envie o arquivo `.env` para o GitHub.

O repositório deve utilizar um `.gitignore` para impedir o versionamento de arquivos de ambiente, credenciais e ambientes virtuais.

### 6. Iniciar o backend

Na raiz do projeto, execute:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O parâmetro `--host 0.0.0.0` permite que o servidor aceite conexões pelas interfaces de rede do computador.

O parâmetro `--reload` reinicia o servidor automaticamente quando são detectadas alterações nos arquivos durante o desenvolvimento.

A API estará disponível em:

```text
http://127.0.0.1:8000
```

Para encerrar o servidor, pressione `CTRL + C`.

---

## 🗄️ Banco de Dados

O projeto utiliza MySQL para armazenar os dados da aplicação.

### Configuração inicial

1. Instale e inicie o MySQL.
2. Crie o banco de dados utilizado pelo projeto.
3. Configure as credenciais no arquivo `.env`.
4. Confira se a URL de conexão do SQLAlchemy está correta.
5. Inicie o backend.

O banco de dados utilizado na configuração do projeto é denominado `veterinaria`.

Exemplo de criação, caso ainda não exista:

```sql
CREATE DATABASE veterinaria
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

A estrutura das tabelas é gerenciada pela configuração de banco de dados e pelos modelos do backend.

Caso o projeto esteja utilizando migrações Alembic, confira a configuração existente antes de executar as migrações:

```bash
alembic upgrade head
```

**Atenção:** não execute comandos de criação ou alteração de tabelas indiscriminadamente em um banco que já contenha dados importantes.

---

## 🌐 Documentação da API

O FastAPI disponibiliza documentação interativa por meio do Swagger e do ReDoc.

Depois de iniciar o backend, acesse:

### Swagger

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

A documentação permite:

- Visualizar os endpoints.
- Consultar os métodos HTTP.
- Verificar parâmetros e schemas.
- Consultar os formatos das requisições.
- Visualizar as respostas da API.
- Realizar testes diretamente pelo navegador.

---

## ⚛️ Configuração do Frontend

### 1. Abrir outro terminal

Mantenha o backend em execução e abra um segundo terminal.

### 2. Acessar a pasta do frontend

```bash
cd frontend
```

Caso esteja na raiz do projeto, esse comando será suficiente.

### 3. Instalar as dependências

```bash
npm install
```

O npm utilizará o `package.json` e o `package-lock.json` para instalar as dependências necessárias.

### 4. Iniciar o frontend

Para executar o servidor de desenvolvimento:

```bash
npm run dev -- --host 0.0.0.0
```

O frontend estará disponível no computador em:

```text
http://localhost:5173
```

O endereço também poderá ser acessado por outros dispositivos conectados à mesma rede, utilizando o IP do computador.

Para encerrar o servidor, pressione `CTRL + C`.

---

## 🐾 Funcionalidades do Sistema

### 🐶 Gerenciamento de Animais

- Cadastro de animais.
- Consulta de animais cadastrados.
- Atualização das informações.
- Exclusão de registros.
- Histórico dos animais.
- Associação dos animais aos clientes.

### 👨‍⚕️ Gerenciamento de Veterinários

- Cadastro de veterinários.
- Controle de acesso por perfil.
- Gerenciamento dos usuários veterinários.
- Associação dos veterinários aos atendimentos e agendamentos, conforme as regras do sistema.

### 👥 Gerenciamento de Clientes

- Cadastro de clientes.
- Consulta de clientes.
- Atualização de informações.
- Busca de registros.
- Validação de CPF.
- Validação de e-mail.
- Associação dos clientes aos animais.

### 📅 Agendamentos

- Cadastro de agendamentos.
- Consulta de horários.
- Atualização de informações.
- Cancelamento de agendamentos.
- Consulta de agendamentos futuros.
- Controle de status.
- Organização dos horários de atendimento.

### 🩺 Atendimentos

- Registro de atendimentos.
- Consulta do histórico.
- Registro de diagnósticos.
- Controle de status.
- Associação dos atendimentos aos animais e veterinários.

### 💉 Vacinas

- Cadastro de vacinas.
- Consulta de vacinas.
- Registro de aplicações.
- Histórico de aplicações.
- Associação das aplicações aos animais.

### 📦 Produtos e Estoque

- Cadastro de produtos.
- Consulta de produtos.
- Atualização de informações.
- Controle de quantidades.
- Gerenciamento de estoque.
- Identificação de produtos com estoque baixo ou zerado.

### 🛒 Carrinho e Pedidos

- Gerenciamento do carrinho.
- Adição de produtos.
- Remoção de produtos.
- Atualização de quantidades.
- Verificação de estoque.
- Finalização de compras.
- Registro de pedidos.

### 📊 Dashboard

O sistema apresenta informações estatísticas para acompanhamento das atividades.

Entre os indicadores disponíveis estão:

- Total de usuários.
- Total de clientes.
- Total de animais.
- Total de produtos.
- Total de atendimentos.
- Total de agendamentos.
- Valor total do estoque.
- Produtos sem estoque.
- Produtos com estoque baixo.
- Animal mais velho.
- Cliente com mais animais.
- Média de idade dos animais.
- Agendamentos do dia.
- Agendamentos futuros.
- Gráficos estatísticos.

As informações apresentadas variam conforme o perfil e as permissões do usuário.

---

## 🔐 Autenticação e Segurança

O Petonline24h possui autenticação e controle de acesso para proteger as funcionalidades e os dados da aplicação.

### Autenticação JWT

A autenticação utiliza tokens JWT para identificar usuários durante as requisições protegidas.

Após o login:

1. O usuário envia suas credenciais.
2. O backend verifica as informações.
3. A API retorna um token de autenticação.
4. O frontend armazena as informações necessárias à sessão.
5. As requisições protegidas enviam o token no cabeçalho HTTP.

Exemplo do cabeçalho:

```http
Authorization: Bearer SEU_TOKEN
```

### Perfis de acesso

O sistema trabalha com os seguintes perfis:

| Perfil | Descrição |
|---|---|
| Administrador | Acesso às funcionalidades administrativas autorizadas. |
| Veterinário | Acesso às funcionalidades veterinárias autorizadas. |
| Cliente | Acesso às funcionalidades destinadas aos clientes. |

### Outros recursos de segurança

- Hash de senhas.
- Validação dos dados recebidos.
- Controle de permissões.
- Proteção de rotas.
- Encerramento de sessão.
- Revogação de tokens, conforme a implementação do backend.
- Separação entre autenticação e regras de negócio.

---

## 📱 Acesso pela Rede Local (Computador e Celular)

O Petonline24h pode ser acessado por outros dispositivos conectados à mesma rede local, como celulares, tablets e computadores.

Essa configuração permite utilizar a aplicação pelo navegador do celular enquanto o frontend e o backend permanecem em execução no computador.

### 1. Como funciona?

O computador funciona como servidor da aplicação.

O celular acessa a interface React por meio do endereço IP do computador. Quando o usuário realiza uma operação, o frontend envia uma requisição ao FastAPI, que processa os dados e se comunica com o MySQL.

O fluxo é:

```text
CELULAR
   |
   | Acesso pelo navegador
   v
FRONTEND REACT
   |
   | Requisições HTTP
   v
BACKEND FASTAPI
   |
   | Consultas e operações
   v
BANCO DE DADOS MYSQL
```

O celular não precisa ter Python, Node.js ou MySQL instalados. Esses serviços continuam sendo executados no computador.

### 2. Configuração do backend

O servidor precisa aceitar conexões externas:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O CORS também precisa autorizar a origem do frontend.

A configuração deve incluir os endereços utilizados durante os testes, por exemplo:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://IP_DO_COMPUTADOR:5173"
]
```

Substitua `IP_DO_COMPUTADOR` pelo endereço IPv4 atual do computador.

A lista deve ser compatível com a configuração real do CORS no projeto.

### 3. Configuração do frontend

No arquivo `frontend/vite.config.js`, o servidor de desenvolvimento utiliza uma configuração equivalente a:

```javascript
server: {
    host: true,
    port: 5173,
}
```

Isso permite que o Vite aceite conexões externas pela rede local.

### 4. Comunicação dinâmica com a API

No arquivo `frontend/src/services/api.js`, foi configurada uma URL dinâmica:

```javascript
export const API_URL =
    import.meta.env.VITE_API_URL ||
    `${window.location.protocol}//${window.location.hostname}:8000`;
```

Essa configuração utiliza o protocolo e o nome do host acessado pelo navegador e define a porta `8000` para a API, quando não existe uma URL específica configurada pela variável de ambiente.

Exemplos:

| Dispositivo | Frontend | Backend |
|---|---|---|
| Computador | `http://localhost:5173` | `http://localhost:8000` |
| Celular | `http://IP_DO_COMPUTADOR:5173` | `http://IP_DO_COMPUTADOR:8000` |

O Axios também é utilizado para enviar as requisições e incluir o token JWT nas operações autenticadas, conforme a configuração da aplicação.

### 5. Como descobrir o IP do computador?

No Windows, abra o PowerShell ou CMD e execute:

```powershell
ipconfig
```

Procure o endereço IPv4 correspondente à conexão Wi-Fi ou Ethernet utilizada.

### 6. Como acessar pelo celular?

1. Conecte o computador à rede Wi-Fi.
2. Conecte o celular à mesma rede Wi-Fi.
3. Inicie o backend.
4. Inicie o frontend com `npm run dev -- --host 0.0.0.0`.
5. Descubra o IPv4 do computador.
6. Abra o navegador do celular.
7. Digite o endereço:

```text
http://IP_DO_COMPUTADOR:5173
```

Para consultar a documentação da API pelo celular:

```text
http://IP_DO_COMPUTADOR:8000/docs
```

### 7. Requisitos e observações

- Os dois dispositivos precisam estar na mesma rede local.
- A rede deve permitir comunicação entre os dispositivos.
- O firewall do Windows precisa permitir as conexões necessárias.
- O IP pode mudar quando o computador se conecta a outra rede ou recebe outro endereço.
- Caso o IP mude, atualize a origem correspondente na configuração do CORS, quando necessário.
- O celular não acessa diretamente o MySQL.
- Os serviços do computador precisam permanecer em execução durante o acesso pela rede local.

**Importante:** o acesso por rede local não representa uma hospedagem pública. Para acessar o sistema de qualquer lugar pela internet, será necessário hospedar o frontend e o backend em servidores acessíveis externamente e configurar a comunicação entre eles.

---

## 📱 Responsividade da Interface

O Petonline24h possui uma interface responsiva, desenvolvida para adaptar a apresentação do sistema a diferentes tamanhos de tela.

O objetivo da responsividade é proporcionar uma experiência adequada tanto em computadores quanto em celulares e tablets.

### 1. Arquivo de responsividade

Foi criado o arquivo:

```text
frontend/src/responsive.css
```

Ele contém regras CSS que modificam a apresentação dos componentes conforme a largura disponível.

O arquivo é importado globalmente pelo ponto de entrada do React:

```javascript
import "./index.css";
import "./responsive.css";
```

Assim, os ajustes responsivos podem ser aplicados às diferentes páginas da aplicação.

### 2. Media Queries

Foram utilizadas media queries para aplicar estilos específicos conforme o tamanho da tela.

Exemplo:

```css
@media (max-width: 768px) {
    /* Ajustes para celulares e tablets */
}
```

Para telas ainda menores:

```css
@media (max-width: 640px) {
    /* Ajustes adicionais */
}
```

As regras permitem reorganizar os elementos, modificar espaçamentos, ajustar larguras e melhorar a navegação em dispositivos móveis.

### 3. Adaptações realizadas

| Elemento | Adaptação |
|---|---|
| Menu lateral | Ajustes para navegação em telas menores. |
| Conteúdo principal | Melhor aproveitamento da largura disponível. |
| Dashboard | Reorganização dos cartões estatísticos. |
| Gráficos | Apresentação em uma única coluna em telas menores. |
| Formulários | Campos adaptados à largura do dispositivo. |
| Botões | Áreas de toque maiores. |
| Modais | Dimensões e posicionamento adaptados. |
| Tabelas | Rolagem horizontal ou apresentação em cartões, conforme o componente. |
| Paginação | Ajustes para facilitar a navegação. |
| Cabeçalhos | Redução e reorganização de espaçamentos. |

### 4. Configuração do viewport

No arquivo `frontend/index.html`, foi utilizada a configuração:

```html
<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, viewport-fit=cover"
/>
```

Essa configuração informa ao navegador que a página deve utilizar a largura real do dispositivo, evitando que o conteúdo seja apresentado como uma página de desktop reduzida.

### 5. Resultado esperado

Em telas maiores, a interface pode apresentar mais elementos lado a lado, como cartões, gráficos e menus.

Em telas menores, os componentes são reorganizados para facilitar a leitura, a navegação e a interação por toque.

A responsividade não cria uma segunda aplicação. O mesmo frontend atende aos diferentes dispositivos, alterando sua apresentação conforme as dimensões da tela.

---

## 📲 Progressive Web App (PWA)

O Petonline24h possui suporte a **Progressive Web App (PWA)**, permitindo que o sistema seja instalado em dispositivos compatíveis e aberto em uma janela independente, semelhante a um aplicativo convencional.

O PWA utiliza recursos do navegador para aproximar a experiência de utilização de uma aplicação instalada.

### 1. Recursos implementados

- Manifesto da aplicação.
- Ícones para dispositivos compatíveis.
- Configuração de exibição em modo `standalone`.
- Service Worker.
- Pré-cache de arquivos estáticos.
- Gerenciamento de cache com Workbox.
- Atualização automática dos recursos da aplicação.
- Configuração da página inicial para direcionar o usuário à autenticação.

### 2. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Vite PWA Plugin | Integração dos recursos PWA com o Vite. |
| Workbox | Gerenciamento de recursos em cache. |
| Service Worker | Intermediação de solicitações e gerenciamento de cache. |
| Web App Manifest | Descrição e configuração da aplicação instalável. |

### 3. Arquivos relacionados

| Arquivo | Finalidade |
|---|---|
| `frontend/public/manifest.webmanifest` | Define os dados da aplicação. |
| `frontend/public/icon-192.png` | Ícone de 192 × 192 pixels. |
| `frontend/public/icon-512.png` | Ícone de 512 × 512 pixels. |
| `frontend/public/apple-touch-icon.png` | Ícone para dispositivos Apple. |
| `frontend/vite.config.js` | Configura a integração PWA e o Workbox. |
| `frontend/index.html` | Referencia o manifesto e os ícones. |
| `frontend/src/pages/Dashboard/Dashboard.jsx` | Verifica a existência da sessão antes de apresentar o dashboard. |

### 4. Manifesto da aplicação

O arquivo:

```text
frontend/public/manifest.webmanifest
```

contém as informações necessárias para identificar e configurar a aplicação instalável.

Entre as propriedades utilizadas estão:

| Propriedade | Finalidade |
|---|---|
| `name` | Nome completo da aplicação. |
| `short_name` | Nome reduzido. |
| `description` | Descrição do sistema. |
| `lang` | Idioma da aplicação. |
| `start_url` | Endereço inicial ao abrir o aplicativo. |
| `scope` | Escopo de navegação. |
| `display` | Modo de exibição. |
| `background_color` | Cor de fundo. |
| `theme_color` | Cor principal do tema. |
| `icons` | Ícones da aplicação. |

O modo `standalone` permite abrir a aplicação sem a apresentação tradicional da barra de endereço do navegador, conforme o suporte do dispositivo.

### 5. Service Worker e cache

O Service Worker é utilizado para gerenciar recursos da aplicação e permitir o armazenamento de arquivos estáticos em cache.

O Workbox auxilia na geração e no gerenciamento desse cache.

Durante a compilação, os recursos estáticos selecionados são preparados para o pré-cache.

Isso permite que partes da interface possam ser carregadas a partir dos arquivos armazenados no dispositivo.

**Limitação importante:** o cache dos arquivos estáticos não significa que todas as funcionalidades funcionam offline. Operações que dependem do backend, da autenticação ou do banco de dados precisam de comunicação com os serviços correspondentes.

### 6. Atualizações automáticas

A integração PWA utiliza a estratégia de registro `autoUpdate`, permitindo que o navegador gerencie a atualização dos recursos do Service Worker conforme a configuração do projeto.

### 7. Autenticação ao abrir o aplicativo

O manifesto utiliza a rota de login como ponto de entrada da aplicação.

Além disso, o dashboard verifica se existe um usuário autenticado e um token armazenado.

Quando a sessão não está disponível, o usuário é redirecionado para a página de login, evitando que a aplicação permaneça indefinidamente na tela de carregamento do dashboard.

### 8. Como gerar a versão de produção

Entre na pasta do frontend:

```bash
cd frontend
```

Gere a compilação:

```bash
npm run build
```

Para testar a versão compilada localmente:

```bash
npm run preview -- --host 0.0.0.0
```

O Vite Preview disponibiliza a versão compilada, normalmente na porta `4173`.

O navegador poderá utilizar o manifesto e o Service Worker gerados para testar a experiência PWA.

### 9. Como instalar

**Em computadores:**

1. Abra o sistema em um navegador compatível.
2. Utilize a opção de instalação disponibilizada pelo navegador.
3. Confirme a instalação.
4. Abra o Petonline24h pelo ícone criado.

**Em dispositivos Android:**

1. Abra o endereço do sistema no navegador compatível.
2. Acesse o menu do navegador.
3. Selecione a opção de instalar aplicativo ou adicionar à tela inicial, conforme o navegador.
4. Confirme a instalação.

**Em dispositivos iPhone:**

1. Abra o sistema no Safari.
2. Selecione o botão de compartilhamento.
3. Escolha a opção de adicionar à tela de início, quando disponível.
4. Confirme a operação.

### 10. Requisitos para disponibilização em produção

Para disponibilizar a instalação PWA pela internet, é necessário:

- Hospedar o frontend em um endereço acessível.
- Utilizar HTTPS.
- Configurar corretamente o manifesto.
- Disponibilizar os ícones.
- Garantir que o Service Worker esteja acessível dentro do escopo da aplicação.
- Configurar a URL de produção da API.
- Autorizar a origem do frontend no CORS do backend.

O acesso por HTTP em endereços de rede local pode ser utilizado para testar a interface, mas não oferece, em geral, o contexto seguro necessário para o Service Worker. `localhost` é uma exceção reconhecida pelos navegadores.

---

## 🧪 Testes Automatizados

Os testes automatizados do backend estão organizados na pasta:

```text
tests/
```

O projeto utiliza Pytest para executar os testes.

### Executar todos os testes

Na raiz do projeto, com o ambiente virtual ativado:

```bash
pytest
```

### Executar com informações detalhadas

```bash
pytest -v
```

### Executar um arquivo específico

```bash
pytest tests/nome_do_arquivo.py -v
```

Os testes auxiliam na verificação do comportamento das funcionalidades, das regras de negócio e dos endpoints da aplicação.

---

## 🛠️ Solução de Problemas

### 1. Erro ao conectar com o MySQL

Verifique:

- Se o servidor MySQL está em execução.
- Se o banco de dados foi criado.
- Se as credenciais estão corretas.
- Se a porta configurada está correta.
- Se a URL de conexão utilizada pelo SQLAlchemy corresponde ao arquivo `.env`.

### 2. Erro ao iniciar o Uvicorn

Confira se o ambiente virtual está ativado e se as dependências foram instaladas:

```bash
pip install -r requirements.txt
```

Verifique também se o comando está sendo executado na raiz correta do projeto:

```bash
uvicorn main:app --reload
```

### 3. Erro de comunicação entre frontend e backend

Verifique:

- Se o backend está em execução.
- Se a API está acessível.
- Se a URL configurada no Axios está correta.
- Se o CORS permite a origem utilizada pelo frontend.
- Se o token JWT está sendo enviado corretamente nas rotas protegidas.

### 4. Frontend não inicia

Entre na pasta `frontend` e execute:

```bash
npm install
npm run dev
```

Caso necessário, confira as mensagens de erro apresentadas pelo Vite.

### 5. Celular não consegue acessar o sistema

Confira:

- Se computador e celular estão na mesma rede.
- Se o endereço IPv4 utilizado está correto.
- Se o frontend foi iniciado com `--host 0.0.0.0`.
- Se o backend está aceitando conexões externas.
- Se o firewall permite as conexões.
- Se o CORS autoriza a origem do celular.

### 6. PWA não apresenta a opção de instalação

Confira:

- Se o manifesto está acessível.
- Se os ícones existem e possuem os caminhos corretos.
- Se o Service Worker foi registrado.
- Se a versão de produção foi compilada.
- Se o sistema está sendo acessado em um contexto seguro, normalmente HTTPS ou localhost.
- Se o navegador oferece suporte aos requisitos de instalação.

---

## 📅 Cronograma do Projeto

O desenvolvimento foi organizado em quatro etapas, distribuídas ao longo dos bimestres.

### 1º Bimestre — Planejamento e Estruturação

**Período:** 12/03/2026 a 18/05/2026

Etapa destinada ao planejamento, levantamento de requisitos e organização inicial do projeto.

#### 12/03/2026 a 10/04/2026 — Planejamento e Documentação

- Definição do objetivo do sistema.
- Levantamento dos requisitos funcionais.
- Escolha das tecnologias.
- Criação do repositório no GitHub.
- Elaboração e atualização da documentação.

#### 11/04/2026 a 18/05/2026 — Prototipação e Estrutura Inicial

- Desenvolvimento dos protótipos utilizando Canva.
- Planejamento das telas.
- Definição dos fluxos de navegação.
- Configuração do ambiente de desenvolvimento.
- Estruturação inicial da API REST.

### 2º Bimestre — Desenvolvimento dos Módulos Principais

**Período:** 19/05/2026 a 20/07/2026

Etapa destinada ao desenvolvimento das funcionalidades principais do backend.

#### 19/05/2026 a 20/06/2026 — Backend

- Cadastro de usuários.
- Login e logout.
- Cadastro de clientes.
- Cadastro de animais.
- Implementação da autenticação JWT.
- Implementação das regras de negócio.
- Testes dos endpoints.

#### 21/06/2026 a 20/07/2026 — Consultas e Serviços

- Agendamento de consultas.
- Agendamento de serviços.
- Registro de atendimentos.
- Histórico de consultas e serviços.
- Configuração do banco de dados.
- Correção de erros encontrados.

### 3º Bimestre — Frontend e Módulo Pet Shop

**Período:** 10/08/2026 a 13/10/2026

Etapa destinada ao desenvolvimento das interfaces e funcionalidades de gerenciamento e venda de produtos.

#### 10/08/2026 a 10/09/2026 — Desenvolvimento do Frontend

- Página inicial.
- Tela de login e cadastro.
- Telas de clientes, animais e agendamentos.
- Integração entre frontend e backend.

#### 11/09/2026 a 13/10/2026 — Módulo Pet Shop

- Cadastro de produtos.
- Busca e listagem de produtos.
- Implementação do carrinho de compras.
- Integração das funcionalidades de compra.
- Ajustes visuais.
- Responsividade.

### 4º Bimestre — Infraestrutura e Entrega Final

**Período:** 14/10/2026 a 18/12/2026

Etapa destinada à infraestrutura, aos testes e à preparação da entrega final.

#### 14/10/2026 a 15/11/2026 — Infraestrutura

- Planejamento da containerização com Docker.
- Configuração dos containers.
- Planejamento dos arquivos YAML.
- Preparação da implantação com Kubernetes.
- Testes de infraestrutura.

#### 16/11/2026 a 18/12/2026 — Finalização

- Testes finais do sistema.
- Correção de bugs.
- Atualização da documentação.
- Organização do repositório.
- Criação dos slides.
- Preparação da apresentação.
- Entrega final do projeto.

**Observação:** as atividades de infraestrutura e implantação devem ser consideradas concluídas somente após sua implementação e validação no projeto.

---

## 📌 Considerações Finais

O **Petonline24h** foi desenvolvido para oferecer uma solução integrada ao gerenciamento de uma clínica veterinária e de um pet shop, reunindo funcionalidades administrativas, veterinárias e comerciais em uma única aplicação.

A utilização de React, FastAPI e MySQL permite separar a interface, o processamento das regras de negócio e o armazenamento das informações, favorecendo a organização e a manutenção do sistema.

A integração entre frontend e backend permite que as operações sejam realizadas por meio de uma API REST, enquanto a autenticação JWT e o controle de permissões organizam o acesso às funcionalidades conforme o perfil do usuário.

As configurações de rede local possibilitam acessar o sistema por computadores, celulares e tablets conectados à mesma rede. A responsividade adapta a interface às dimensões dos dispositivos, proporcionando uma navegação mais adequada em telas menores.

Além disso, a implementação de recursos PWA permite instalar o Petonline24h em dispositivos compatíveis, oferecendo uma experiência semelhante à de um aplicativo, com ícone próprio, abertura independente do navegador e armazenamento em cache dos recursos estáticos.

Dessa forma, o projeto reúne conhecimentos de desenvolvimento frontend, backend, banco de dados, autenticação, arquitetura de software, responsividade, integração de sistemas e tecnologias web modernas.

---

**Projeto acadêmico desenvolvido para a disciplina POAS.**
