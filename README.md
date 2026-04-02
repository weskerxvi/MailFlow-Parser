# MailFlow Parser

API e automacao simples para ler emails em texto, extrair pedidos, normalizar os dados e salvar os resultados em um banco SQLite.

Este projeto foi construido como estudo de backend com Python e mostra um fluxo completo de:

- leitura de entrada textual
- parser com regex
- normalizacao de dados
- persistencia com SQLAlchemy
- exposicao via FastAPI
- testes com pytest
- geracao de relatorios

## Objetivo do projeto

O projeto simula um pequeno sistema de RPA/email processing. A ideia e receber mensagens com um formato padrao, identificar os dados do pedido e transformar essa entrada nao estruturada em registros organizados para consulta e relatorio.

Exemplo de linha processada:

```text
Pedido #123 - Cliente Joao Silva - Valor R$250,42
```

## Stack utilizada

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest
- Regex

## Como o sistema funciona

O fluxo principal e este:

1. O sistema le o conteudo do arquivo `emails.txt`.
2. O parser procura linhas no formato `Pedido #<numero> - Cliente <nome> - Valor <valor>`.
3. Cada item extraido e normalizado.
4. Os pedidos sao gravados no banco `rpa.db`.
5. A API permite consultar os pedidos e gerar um resumo.
6. O modulo de relatorios tambem pode gerar arquivos `.txt` e `.csv`.

## Estrutura do projeto

```text
rpa-email-system/
|-- app/
|   |-- api/
|   |   `-- routes.py
|   |-- reports/
|   |   `-- generator.py
|   |-- services/
|   |   |-- normalize_order.py
|   |   |-- process_email.py
|   |   `-- reports.py
|   |-- database.py
|   |-- email_reader.py
|   |-- main.py
|   |-- models.py
|   |-- parser.py
|   `-- schemas.py
|-- tests/
|-- emails.txt
|-- requirements.txt
`-- rpa.db
```

## Papel de cada arquivo principal

- `app/main.py`: cria a aplicacao FastAPI e registra as rotas.
- `app/api/routes.py`: define os endpoints para processar emails, listar pedidos e gerar resumo.
- `app/parser.py`: extrai numero, cliente e valor a partir do texto bruto.
- `app/services/normalize_order.py`: limpa e padroniza os dados extraidos.
- `app/database.py`: configura engine, sessao e conexao com SQLite.
- `app/models.py`: define o modelo `Order`.
- `app/schemas.py`: define o schema de resposta da API.
- `app/services/reports.py`: calcula metricas agregadas dos pedidos.
- `app/reports/generator.py`: gera arquivos de relatorio em TXT e CSV.
- `app/services/process_email.py`: executa o fluxo fora da API, diretamente por script.

## Como executar localmente

### 1. Criar e ativar ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Iniciar a API

```powershell
uvicorn app.main:app --reload
```

A API ficara disponivel em:

- `http://127.0.0.1:8000`
- Documentacao Swagger: `http://127.0.0.1:8000/docs`

## Como usar

Antes de processar, coloque no arquivo `emails.txt` uma ou mais linhas no formato esperado.

Exemplo:

```text
Pedido #123 - Cliente Joao Silva - Valor 250
Pedido #124 - Cliente Maria Souza - Valor R$320,90
Pedido #125 - Cliente Pedro Lima - Valor
```

### Endpoints disponiveis

#### `POST /process`

Le o arquivo `emails.txt`, extrai os pedidos, normaliza os dados e grava no banco.

Resposta esperada:

```json
{
  "message": "Emails processed successfully.",
  "created": 2,
  "duplicates": 1
}
```

#### `GET /orders`

Lista os pedidos salvos no banco.

#### `GET /reports`

Retorna um resumo com:

- quantidade total de pedidos
- valor total somado
- quantidade de pedidos sem valor

## Geracao de relatorios em arquivo

O modulo `app/reports/generator.py` gera relatorios em TXT e CSV com base nos pedidos salvos no banco.

Para executar manualmente:

```powershell
python -m app.reports.generator
```

Arquivos gerados:

- `reports-dd-mm-aaaa.txt`
- `reports-dd-mm-aaaa.csv`

## Executando os testes

```powershell
pytest
```

Ou, se estiver usando o executavel do ambiente virtual:

```powershell
.\venv\Scripts\pytest.exe
```

## Pontos tecnicos demonstrados neste projeto

- criacao de API REST com FastAPI
- uso de ORM com SQLAlchemy
- modelagem simples de dados
- parser de texto com regex
- tratamento basico de dados inconsistentes
- testes unitarios e de integracao
- separacao em camadas (`api`, `services`, `reports`, `models`)

## Melhorias planejadas

Estas sao melhorias naturais para evoluir o projeto:

- mover configuracoes para variaveis de ambiente
- melhorar validacao dos dados com Pydantic
- adicionar logs estruturados
- evitar arquivos de exemplo e banco versionados no repositorio
- adicionar migracoes com Alembic
- melhorar a documentacao de deploy
- tratar melhor duplicidade diretamente no banco
- reforcar cobertura de testes de API

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo `LICENSE` para mais detalhes.
