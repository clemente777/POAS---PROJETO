# 🐾 POAS - Petonline24h | Sistema para Clínica Veterinária

Sistema desenvolvido para a disciplina **POAS**, com o objetivo de gerenciar uma clínica veterinária, permitindo o controle de usuários, clientes, animais, produtos, atendimentos, agendamentos, vacinas e pedidos.

O projeto utiliza uma API REST desenvolvida em **FastAPI** e uma interface web moderna desenvolvida em **React**, proporcionando uma solução integrada para o gerenciamento das atividades de uma clínica veterinária.

Além das funcionalidades administrativas e veterinárias, o sistema conta com recursos de autenticação, controle de acesso por perfil, gerenciamento de estoque, dashboard estatístico e adaptação para dispositivos móveis.

---

## 👥 Integrantes

- Kaik Emanuel
- Isaac Fonseca
- Bruno Ildo
- Weslley Wender

---

# 🚀 Tecnologias Utilizadas

## Backend

- 🐍 Python
- ⚡ FastAPI
- 🔗 SQLAlchemy
- 🗄️ MySQL
- 🔐 Pwdlib (Hash de Senhas)
- 🔑 JWT (Autenticação por tokens)
- 🚀 Uvicorn
- 📄 Swagger/OpenAPI
- 🧪 Pytest
- 🛠️ Alembic (Migrações do banco de dados)

## Frontend

- ⚛️ React
- 📡 Axios
- 🎨 CSS
- 📊 Recharts
- ⚡ Vite
- JavaScript
- Lucide React

---

# 📁 Estrutura do Projeto

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
│   └── vite.config.js
│
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
└── .env
```

---

# ▶️ Como Rodar o Backend

## 1. Abra um terminal

Utilize um dos seguintes terminais:

- PowerShell
- CMD
- Terminal integrado do VS Code

## 2. Navegue até a pasta principal do projeto

```bash
cd C:\Users\COMPUTER\Documents\POAS---PROJETO
```

## 3. Crie e ative um ambiente virtual

Crie o ambiente virtual:

```bash
python -m venv venv
```

### Windows - PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows - CMD

```cmd
venv\Scripts\activate
```

## 4. Instale as dependências

```bash
pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` não esteja disponível, será necessário instalar as dependências de acordo com as utilizadas pelo projeto.

## 5. Configure o banco de dados

O projeto utiliza **MySQL** para armazenar as informações do sistema.

Antes de iniciar a aplicação:

1. Instale e inicie o servidor MySQL.
2. Crie o banco de dados utilizado pelo projeto.
3. Configure as variáveis de ambiente no arquivo `.env`.
4. Confira as credenciais e a URL de conexão utilizadas pelo backend.

O arquivo `.env` deve conter as configurações necessárias para a conexão com o banco de dados e demais recursos da aplicação.

**Importante:** não envie o arquivo `.env` para o GitHub, pois ele pode conter informações confidenciais.

## 6. Inicie a API

Para permitir o acesso pela rede local, execute:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível localmente em:

```text
http://127.0.0.1:8000
```

---

## 📄 Documentação da API (Swagger)

Após iniciar o backend, acesse:

```text
http://127.0.0.1:8000/docs
```

Ou utilize a documentação alternativa:

```text
http://127.0.0.1:8000/redoc
```

O Swagger permite visualizar os endpoints disponíveis, consultar parâmetros, enviar requisições e testar as funcionalidades da API.

---

# 💻 Como Rodar o Frontend

## 1. Abra outro terminal

Mantenha o backend em execução e abra um segundo terminal.

## 2. Navegue até a pasta do frontend

```bash
cd C:\Users\COMPUTER\Documents\POAS---PROJETO\frontend
```

## 3. Instale as dependências

```bash
npm install
```

## 4. Execute o projeto

Para permitir o acesso por outros dispositivos da rede local:

```bash
npm run dev -- --host 0.0.0.0
```

O frontend estará disponível no computador em:

```text
http://localhost:5173
```

---

# 📱 Acesso pela Rede Local (Computador e Celular)

O Petonline24h recebeu configurações para permitir o acesso por diferentes dispositivos conectados à mesma rede local, como computadores, celulares e tablets.

Essa funcionalidade possibilita utilizar o sistema pelo navegador do celular, enquanto o frontend e o backend permanecem em execução no computador.

## 1. Alterações realizadas

| Arquivo | Alteração | Finalidade |
|---|---|---|
| `main.py` | Configuração do CORS e do servidor Uvicorn com `host="0.0.0.0"` | Permitir conexões externas com a API. |
| `frontend/vite.config.js` | Configuração de `host: true` e porta `5173` | Permitir acesso ao frontend pela rede local. |
| `frontend/src/services/api.js` | Implementação de URL dinâmica da API | Identificar automaticamente o endereço do backend. |

## 2. Configuração do backend

No arquivo `main.py`, foi configurado o CORS para autorizar as origens utilizadas durante os testes:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://10.144.8.227:5173"
]
```

Também foi configurado o servidor Uvicorn:

```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=True
)
```

O parâmetro `host="0.0.0.0"` permite que o servidor receba conexões pelas interfaces de rede do computador.

## 3. Configuração do frontend

No arquivo `frontend/vite.config.js`, foi acrescentada a configuração:

```javascript
server: {
  host: true,
  port: 5173,
}
```

Essa configuração permite que o servidor de desenvolvimento Vite aceite conexões de outros dispositivos da rede.

## 4. Comunicação entre frontend e backend

No arquivo `frontend/src/services/api.js`, foi implementada uma URL dinâmica:

```javascript
export const API_URL =
    import.meta.env.VITE_API_URL ||
    `${window.location.protocol}//${window.location.hostname}:8000`;
```

Essa configuração identifica o endereço utilizado para acessar o frontend e utiliza o mesmo endereço para localizar o backend, alterando a porta para `8000`.

Exemplos:

| Dispositivo | Frontend | Backend |
|---|---|---|
| Computador | `http://localhost:5173` | `http://localhost:8000` |
| Celular | `http://10.144.8.227:5173` | `http://10.144.8.227:8000` |

O restante da configuração do Axios mantém o envio automático do token JWT nas requisições autenticadas.

## 5. Como acessar pelo celular

1. Conecte o computador e o celular à mesma rede Wi-Fi.
2. Inicie o backend com o comando configurado para a rede local.
3. Inicie o frontend utilizando `--host 0.0.0.0`.
4. No computador, execute:

```bash
ipconfig
```

5. Localize o endereço IPv4 da conexão Wi-Fi.
6. No navegador do celular, acesse:

```text
http://IP_DO_COMPUTADOR:5173
```

Endereço utilizado durante os testes:

```text
http://10.144.8.227:5173
```

Para consultar a API pelo celular:

```text
http://10.144.8.227:8000/docs
```

**Observações:**

- Os dois dispositivos precisam estar na mesma rede, com comunicação entre eles permitida.
- O firewall do Windows precisa permitir as conexões necessárias.
- O endereço IP pode mudar de acordo com a rede utilizada.
- Caso o IP seja alterado, será necessário verificar a configuração do CORS.
- O celular não acessa diretamente o MySQL: a comunicação com o banco é realizada pelo backend.

---

# 📱 Responsividade da Interface

Foi desenvolvido o arquivo `frontend/src/responsive.css` para adaptar a interface do Petonline24h a diferentes tamanhos de tela.

O arquivo é importado globalmente no ponto de entrada do React, por meio de:

```javascript
import "./index.css";
import "./responsive.css";
```

## 1. Melhorias implementadas

- Adaptação do conteúdo para ocupar melhor a largura disponível.
- Ajustes nos cabeçalhos e títulos.
- Botões com áreas de toque maiores.
- Melhorias nos campos de formulários.
- Prevenção do zoom automático do iPhone em campos de texto.
- Adaptação dos modais para telas menores.
- Redimensionamento dos cartões do dashboard.
- Organização dos gráficos em uma única coluna.
- Melhorias na paginação.
- Possibilidade de apresentação de determinadas tabelas em formato de cartões.
- Rolagem horizontal para tabelas que não utilizam o formato de cartões.

## 2. Pontos de quebra

Foram utilizadas media queries para aplicar estilos conforme a largura da tela:

```css
@media (max-width: 768px) {
    /* Ajustes para celulares e tablets */
}
```

```css
@media (max-width: 640px) {
    /* Ajustes adicionais para telas menores */
}
```

Essas configurações permitem que os componentes da interface sejam reorganizados para melhorar a navegação em dispositivos móveis.

---

# 📲 Preparação para Instalação como Aplicativo (PWA)

O projeto recebeu configurações iniciais para oferecer uma experiência semelhante à de um aplicativo instalado no dispositivo.

Foram adicionados metadados no arquivo `frontend/index.html`, um manifesto da aplicação e arquivos de ícones.

## 1. Alterações no HTML

No arquivo `frontend/index.html`, foram adicionadas configurações como:

- `viewport`: ajusta a página à largura do dispositivo.
- `theme-color`: define a cor do tema.
- `manifest`: referencia o manifesto da aplicação.
- `apple-touch-icon`: referencia o ícone para dispositivos Apple.
- `apple-mobile-web-app-capable`: indica a intenção de utilizar uma experiência de abertura semelhante à de um aplicativo.
- `mobile-web-app-capable`: informa a capacidade de utilização em dispositivos móveis compatíveis.

## 2. Manifesto da aplicação

Foi criado o arquivo:

```text
frontend/public/manifest.webmanifest
```

O manifesto define informações utilizadas pelo navegador:

| Propriedade | Finalidade |
|---|---|
| `name` | Nome completo da aplicação. |
| `short_name` | Nome reduzido. |
| `description` | Descrição do sistema. |
| `lang` | Idioma da aplicação. |
| `start_url` | Página inicial ao abrir a aplicação. |
| `scope` | Escopo de navegação. |
| `display` | Modo de exibição `standalone`. |
| `background_color` | Cor de fundo. |
| `theme_color` | Cor principal do tema. |
| `icons` | Ícones utilizados pela aplicação. |

## 3. Ícones adicionados

Os seguintes arquivos estão localizados em `frontend/public/`:

- `apple-touch-icon.png`: ícone destinado a dispositivos Apple.
- `icon-192.png`: ícone de 192 × 192 pixels.
- `icon-512.png`: ícone de 512 × 512 pixels.

Esses arquivos fornecem os recursos gráficos utilizados na apresentação da aplicação em dispositivos compatíveis.

**Observação:** essas alterações representam a preparação inicial para PWA. A instalação efetiva depende da disponibilização correta do manifesto e dos ícones, dos requisitos do navegador e da configuração de HTTPS em produção. Também é necessário verificar a implementação de um Service Worker para oferecer recursos adicionais, como funcionamento offline.

---

# 🐾 Funcionalidades do Sistema

## 🐶 Animais

- Cadastro de animais.
- Consulta de animais.
- Atualização de informações.
- Exclusão de registros.
- Histórico dos animais.

## 👨‍⚕️ Veterinários

- Cadastro.
- Controle de acesso.
- Gerenciamento conforme o perfil de usuário.

## 👥 Clientes

- Cadastro.
- Atualização.
- Busca.
- Validação de CPF.
- Validação de e-mail.

## 📅 Agendamentos

- Cadastro.
- Atualização.
- Cancelamento.
- Consulta de agendamentos futuros.
- Gerenciamento dos horários de atendimento.

## 🩺 Atendimentos

- Registro de atendimento.
- Histórico de atendimentos.
- Registro de diagnóstico.
- Controle de status dos atendimentos.

## 💉 Vacinas

- Cadastro de vacinas.
- Consulta de vacinas.
- Registro de aplicações.
- Histórico de aplicações de vacinas.

## 📦 Produtos

- Cadastro.
- Controle de estoque.
- Consulta.
- Atualização.
- Gerenciamento de produtos.

## 🛒 Carrinho e Pedidos

- Gerenciamento do carrinho.
- Adição de produtos.
- Remoção de produtos.
- Controle de quantidades.
- Verificação de estoque.
- Finalização de compras.
- Registro de pedidos.

## 📊 Dashboard

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

---

# 🔐 Segurança e Controle de Acesso

O sistema possui recursos de autenticação e controle de permissões para proteger as funcionalidades e os dados da aplicação.

Entre os recursos utilizados estão:

- Autenticação baseada em tokens JWT.
- Hash de senhas com Pwdlib.
- Controle de acesso conforme o perfil do usuário.
- Proteção de rotas.
- Validação dos dados enviados à API.
- Controle de sessões e encerramento de autenticação.
- Controle de permissões para administradores, clientes e veterinários.

---

# 🧪 Testes Automatizados

Os testes automatizados estão organizados na pasta:

```text
tests/
```

Para executar os testes, utilize:

```bash
pytest
```

Os testes permitem verificar o funcionamento dos recursos do backend e identificar possíveis falhas durante o desenvolvimento.

---

# 📌 Considerações Finais

O **Petonline24h** tem como objetivo oferecer uma solução integrada para o gerenciamento de uma clínica veterinária, reunindo funcionalidades administrativas, atendimento veterinário, controle de animais, agendamentos, vacinas, produtos e pedidos.

As melhorias de acesso pela rede local permitem utilizar o sistema em outros dispositivos conectados à mesma rede, enquanto os ajustes de responsividade proporcionam uma interface mais adequada para celulares e tablets.

Além disso, as configurações iniciais de PWA preparam o projeto para uma futura experiência de instalação como aplicativo web, ampliando as possibilidades de utilização do sistema.

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
