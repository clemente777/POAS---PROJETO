# Testes automatizados — POAS / Petonline24h

## Atenção: compatibilidade com a implementação

Este pacote foi montado com base no README funcional do POAS e nas informações já compartilhadas sobre o projeto. O README não especifica todos os caminhos HTTP, os campos obrigatórios dos schemas nem os formatos de resposta. Por isso, os testes de integração/funcionais incluem verificações de contrato e alguns caminhos convencionais que precisam ser conferidos em `/openapi.json`.

**Não considere os testes aprovados nem a cobertura completa antes de executá-los e ajustar os contratos às rotas reais.** Os testes unitários deste pacote verificam regras auxiliares isoladas; eles não substituem testes diretos de cada método dos serviços reais.

## Estrutura

- `unitarios/`: validações e regras isoladas.
- `integracao/`: disponibilidade da API, contrato OpenAPI e autenticação.
- `funcionais/`: fluxo de autenticação e verificações dos módulos expostos.

## Instalação

Na raiz do repositório, com o ambiente virtual ativado:

```cmd
python -m pip install pytest requests pytest-cov pytest-mock
```

## Configuração

Inicie a API em outro terminal. Por padrão os testes chamam `http://127.0.0.1:8000`.

Opcionalmente, configure:

```cmd
set POAS_API_URL=http://127.0.0.1:8000
set POAS_TEST_EMAIL=email_de_teste
set POAS_TEST_PASSWORD=senha_de_teste
set POAS_ADMIN_TOKEN=token_admin_de_teste
set POAS_VETERINARIO_TOKEN=token_veterinario_de_teste
set POAS_CLIENTE_TOKEN=token_cliente_de_teste
```

Use somente contas e dados descartáveis de teste. Não use credenciais reais ou tokens de produção.

## Execução

```cmd
python -m pytest tests/unitarios -v
python -m pytest tests/integracao -v
python -m pytest tests/funcionais -v
python -m pytest tests -v
```

Cobertura:

```cmd
python -m pytest tests/unitarios --cov=backend --cov-report=term-missing
```

## Banco de dados

Os testes HTTP deste pacote não criam nem limpam o banco de dados. Aponte a API para um banco de testes separado antes de executar operações que alterem dados. Nunca execute testes destrutivos contra o banco de desenvolvimento ou produção.

## Próxima etapa para fechar a suíte

Compare os caminhos e schemas em `http://127.0.0.1:8000/openapi.json` com os testes em `integracao/` e `funcionais/`. Para transformar todos os cenários em testes completos de CRUD e fluxos ponta a ponta, os payloads devem refletir os schemas reais e a fixture de banco deve sobrescrever a dependência de sessão do FastAPI usada pelo POAS.
