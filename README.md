# POAS---PROJETO

Sistema para clínica veterinária que permite agendamento de consultas online, gerenciamento de pacientes, históricos e comunicação com tutores. A aplicação usa API REST, autenticação JWT e arquitetura stateless, com frontend moderno e backend integrado.

O projeto é executado em containers e orquestrado com Kubernetes, usando infraestrutura como código para garantir escalabilidade, organização e facilidade de deploy.
- **Backend:** API REST em Flask  
- **Frontend:** Interface web consumindo  `fetch`  
- **Persistência:** Arquivo JSON (`pizzas.json`)  

---

## Tecnologias Utilizadas
### backend
-  Node.js
- API REST
- JWT (JSON Web Token)
### frontend
- Next.js
- JavaScript (Fetch API)
- HTML
- CSS
### infraestrutura e DevOps
- Docker
- Podman
- Containerd
- Kubernetes
- Rancher Desktop
- YAML (Infraestrutura como Código)

---

## Integrantes
- Kaik Emanuel
- Isaac Fonseca
- Bruno Ildo 
- Weslley Wender
 
 # Cronograma
 ## Parte 1 – Configuração Inicial do Projeto
Período: 25/03/2026 – 06/04/2026
Nesta etapa, foi realizada a preparação do ambiente de desenvolvimento e a criação da
estrutura inicial da API da Clínica Veterinária utilizando o framework FastAPI.

Instalação das Dependências
Foram instaladas as bibliotecas necessárias para o funcionamento do projeto
- FastAPI → criação da API
- Uvicorn → servidor para executar a aplicação
- MySQL Connector / SQLAlchemy → conexão com o banco de dados

Planejamento
- Definir o objetivo do sistema
- Listar funcionalidades principais:
- Cadastro de clientes
- Cadastro de animais
- Agendamento/atendimentos

Atualização do README.md
Foi criado e atualizado o arquivo README.md no repositório do GitHub, com o objetivo de
documentar o projeto.
Foram incluídas as seguintes informações:
- Descrição do projeto
- Objetivo da API
- Tecnologias a ser utilizadas
- Instruções de execução
- Estrutura inicial do sistema

## Parte 2 – Prototipação da Interface (Canva)
Período: 10/04/2026 – 24/04/2026
Nesta etapa, foi realizada a criação de um protótipo visual da aplicação, utilizando a
ferramenta Canva, com o objetivo de simular a interface do sistema da Clínica
Veterinária antes do desenvolvimento completo.

Planejamento das Telas
Inicialmente, foram definidas as principais telas que o sistema deve possuir:
- Tela inicial (home)
- Tela de cadastro de clientes
- Tela de cadastro de animais
- Tela de atendimentos
- Tela de listagem de dados

Foi utilizado o Canva para desenvolver um modelo visual do sistema, simulando um
site/sistema real.
Foram criados layouts com:
- Botões
- Campos de formulário
- Listas de informações
- Estrutura de navegação

Organização da Navegação
Foi definida a forma de navegação entre as telas, pensando na experiência do
usuário:
- Menu principal
- Acesso rápido às funcionalidades
- Fluxo entre cadastro → listagem → edição