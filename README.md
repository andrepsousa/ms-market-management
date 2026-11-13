# ms-market-management

API para gestão de estoque e vendas de pequenos mercados, desenvolvida em equipe como projeto acadêmico. Implementada com **Python, Flask e PostgreSQL**, reúne cadastro de vendedores, ativação de conta via WhatsApp, autenticação JWT e gerenciamento de produtos vinculados ao vendedor autenticado.

## Funcionalidades

- Cadastro de vendedores com nome, CNPJ, e-mail, telefone e senha.
- Verificação de e-mail e CNPJ já cadastrados.
- Envio de código de ativação por WhatsApp, via Twilio.
- Login de vendedores ativos e emissão de token JWT com validade de uma hora.
- Criação, consulta, atualização, ativação e inativação de produtos.
- Listagem separada de produtos ativos e inativos por vendedor.
- Registro de vendas com quantidade, preço unitário no momento da venda e atualização do estoque.
- Validações de venda: produto pertencente ao vendedor, produto ativo, quantidade positiva e estoque suficiente.

Este repositório contém o backend da aplicação. Dashboard, relatórios e interface React não estão implementados aqui.

## Minha participação — Frank Ribeiro (@FrankRibe)

Participei do desenvolvimento em equipe, com foco na API de produtos, na integração com WhatsApp e em ajustes de validação e ambiente. As entregas abaixo estão registradas no histórico da minha conta:

| Área | Contribuição | Registro |
| --- | --- | --- |
| Gerenciamento de produtos | Implementação de rotas, controller, serviços, entidade de domínio e modelo de persistência para criar, consultar, listar, atualizar e inativar produtos vinculados ao vendedor autenticado. | [Implementação de produtos](https://github.com/andrepsousa/ms-market-management/commit/fd35b347bb25b92cfbb70c6922195b3f67ded9e9) |
| Ativação de produtos | Inclusão da operação de ativação nas camadas de domínio, serviço, controller e rota, com filtro por vendedor. | [Ativação de produto](https://github.com/andrepsousa/ms-market-management/commit/dc974579d009f66ba01556ea45fba6ef25b3e6a1) |
| Integração externa | Contribuições à integração com Twilio para envio de códigos de ativação pelo WhatsApp e ajustes no fluxo de ativação de vendedores. | [Integração Twilio](https://github.com/andrepsousa/ms-market-management/commit/62991131a8d8f27b411f3eea41ad9f38062c2e38) |
| Validação de cadastro | Verificação de CNPJ já cadastrado, com retorno de erro para o cliente da API. | [Validação de CNPJ duplicado](https://github.com/andrepsousa/ms-market-management/commit/3bc7a97893234171dc6a5f240dd50d62a1f62afd) |
| Integração da API | Ajustes nas rotas de criação de vendedores e produtos, inclusão de Flask-CORS e atualização de dependências. | [Rotas e CORS](https://github.com/andrepsousa/ms-market-management/commit/dbcb87e5ce2f9c1d58eef2c73af0149e9e68c68d) |
| Ambiente local | Ajustes nas portas de conexão com o banco de dados. | [Conexão com PostgreSQL](https://github.com/andrepsousa/ms-market-management/commit/8f5dee21c08e9dd72b138b316ac924aeacb80d67) |

Essas contribuições envolveram construção de endpoints autenticados, separação de responsabilidades, persistência de dados e integração com um serviço externo.

O projeto é coletivo. Esta seção delimita minha participação, sem atribuir a mim a autoria de todas as funcionalidades.

[Ver histórico de contribuições de FrankRibe](https://github.com/andrepsousa/ms-market-management/commits/master/?author=FrankRibe)

## Tecnologias e organização

| Finalidade | Tecnologias |
| --- | --- |
| API | Python, Flask e Blueprints |
| Persistência | PostgreSQL, SQLAlchemy e Flask-SQLAlchemy |
| Autenticação | Flask-JWT-Extended e hash de senhas com Werkzeug |
| Integração externa | Twilio WhatsApp |
| Configuração | python-dotenv e Flask-CORS |
| Banco local | Docker Compose |

```text
ms-market-management/
├── src/
│   ├── Application/
│   │   ├── Controllers/   # Requisições, validações e respostas HTTP
│   │   └── Service/       # Operações da aplicação
│   ├── Config/            # Configuração do banco
│   ├── Domain/            # Objetos de domínio
│   ├── Infrastructure/
│   │   ├── Models/        # Modelos de persistência
│   │   └── http/          # Integração com WhatsApp
│   ├── routes.py          # Vendedores e login
│   ├── product_routes.py
│   └── sale_routes.py
├── docker-compose.yml     # Serviço PostgreSQL
├── requirements.txt
└── run.py                 # Inicialização da API
```

## Executar localmente

### Requisitos

- Git e Python com suporte às dependências de `requirements.txt`.
- Docker com Docker Compose.
- Conta Twilio com WhatsApp Sandbox configurado e destinatário autorizado para testar o envio de códigos.

### 1. Obter o código e instalar as dependências

```bash
git clone https://github.com/andrepsousa/ms-market-management.git
cd ms-market-management
python -m venv .venv
```

Ative o ambiente no Linux/macOS:

```bash
source .venv/bin/activate
```

Ou no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### 2. Configurar as chaves da aplicação

Crie um arquivo `.env` na raiz:

```dotenv
SECRET_KEY=substitua_por_uma_chave_aleatoria
JWT_SECRET_KEY=substitua_por_outra_chave_aleatoria
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
```

Use chaves aleatórias distintas e credenciais próprias. Não publique o arquivo `.env`.

O remetente do WhatsApp está definido diretamente em `src/Infrastructure/http/whats_app.py`. Confira se corresponde ao Sandbox da sua conta: a classe atual não usa `TWILIO_PHONE_NUMBER` para configurar o remetente.

### 3. Iniciar o banco

```bash
docker compose up -d db
docker compose logs db
```

Aguarde o PostgreSQL informar que está pronto para aceitar conexões.

O Compose inicia **apenas o banco de dados**, exposto na porta local **5433**. A conexão usada pela API está definida diretamente em `src/Config/data_base.py` e corresponde às credenciais locais do Compose; atualmente ela não é lida de `DATABASE_URL`.

### 4. Iniciar a API

```bash
python run.py
```

A API atende em [http://localhost:5000](http://localhost:5000). Verifique a rota de saúde:

```bash
curl http://localhost:5000/api
```

Na inicialização, `run.py` chama `db.create_all()` para criar tabelas ausentes. Isso não atualiza automaticamente a estrutura de tabelas existentes.

### 5. Encerrar

Interrompa a API com Ctrl+C e encerre o banco:

```bash
docker compose down
```

Os dados permanecem no volume `data_db`.

## Rotas da API

Rotas protegidas recebem `Authorization: Bearer SEU_TOKEN`.

| Método | Caminho | Uso | JWT |
| --- | --- | --- | --- |
| GET | `/api` | Verificar disponibilidade da API | Não |
| POST | `/api/sellers/criar` | Cadastrar vendedor | Não |
| POST | `/api/sellers/<phone>/activate/<activation_code>` | Ativar vendedor | Não |
| POST | `/api/auth/login` | Login por e-mail e senha | Não |
| GET | `/api/sellers` | Listar vendedores | Sim |
| GET | `/api/sellers/<seller_id>` | Consultar vendedor | Sim |
| PUT | `/api/sellers/<seller_id>/update` | Atualizar vendedor | Sim |
| DELETE | `/api/sellers/<seller_id>/delete` | Excluir vendedor | Sim |
| POST | `/api/products/criar` | Criar produto | Sim |
| GET | `/api/products` | Listar produtos ativos do vendedor | Sim |
| GET | `/api/products/inactivated` | Listar produtos inativos do vendedor | Sim |
| GET | `/api/products/<product_id>` | Consultar produto | Sim |
| PUT | `/api/products/atualizar/<product_id>` | Atualizar produto | Sim |
| PATCH | `/api/products/<product_id>/inactivate` | Inativar produto | Sim |
| PATCH | `/api/products/<product_id>/ativar` | Ativar produto | Sim |
| POST | `/api/sales` | Registrar venda | Sim |

A exigência de JWT não equivale, por si só, à autorização para operar sobre qualquer vendedor. As permissões dessas rotas precisam de revisão.

## Exemplo de uso

Os valores abaixo são ilustrativos. Para receber o código, substitua o telefone por um número autorizado no seu Sandbox.

### Cadastrar e ativar um vendedor

```bash
curl -X POST http://localhost:5000/api/sellers/criar \
  -H "Content-Type: application/json" \
  -d '{"name":"Mercado Exemplo","cnpj":"12345678000190","email":"mercado@example.com","phone":"+5511999999999","password":"senha_local_de_exemplo"}'
```

O CNPJ é enviado sem pontuação; a validação atual verifica tamanho, caracteres numéricos e duplicidade, sem validar os dígitos verificadores.

Após receber o código pelo WhatsApp, informe telefone e código na URL:

```bash
curl -X POST "http://localhost:5000/api/sellers/+5511999999999/activate/SEU_CODIGO"
```

### Obter o token

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"mercado@example.com","password":"senha_local_de_exemplo"}'
```

Copie o campo `access_token` da resposta para as próximas chamadas.

### Criar um produto

```bash
curl -X POST http://localhost:5000/api/products/criar \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Arroz","preco":10.50,"quantidade":100,"imagem_url":"https://example.com/arroz.jpg"}'
```

O vendedor é obtido do JWT e o produto é criado ativo.

### Registrar uma venda

Substitua `1` pelo ID do produto criado:

```bash
curl -X POST http://localhost:5000/api/sales \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"produtoId":1,"quantidade":2}'
```

## Estado atual e próximos passos

Projeto acadêmico, com funcionalidades presentes no código e pontos de evolução antes de uso em produção:

- Adicionar testes de autenticação, isolamento entre vendedores e regras de estoque.
- Revisar autorização nas operações de consulta, atualização e exclusão de vendedores.
- Validar tipos e limites dos campos numéricos, inclusive estoque zero e valores negativos.
- Tratar vendas simultâneas para evitar inconsistências de estoque.
- Revisar expiração, limite de tentativas e exposição dos códigos de ativação em URLs e logs.
- Revisar credenciais presentes no histórico e substituir eventuais credenciais ainda válidas; remover um arquivo do estado atual não o apaga dos commits antigos.
- Externalizar a conexão com o banco e o remetente do WhatsApp.
- Fixar a versão da imagem PostgreSQL e validar as dependências em uma versão documentada do Python.
- Padronizar respostas e documentar a API com OpenAPI.
- Revisar a atualização de vendedores, incluindo o fluxo de alteração de senha.

O servidor inicia com `debug=True` e CORS sem restrição de origem configurada, destinados a revisão antes de publicação. A configuração atual é voltada ao desenvolvimento local.

As instruções e exemplos deste README foram conferidos com os arquivos do repositório. A execução completa e o envio de mensagens não foram validados nesta revisão de documentação.

## Equipe e licença

Projeto acadêmico desenvolvido em equipe, hospedado no repositório de [andrepsousa](https://github.com/andrepsousa), com participação de [FrankRibe](https://github.com/FrankRibe) e demais colaboradores.

Distribuído sob a [licença MIT](LICENSE), com os créditos preservados no arquivo de licença.
