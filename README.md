# Documentação do Projeto ORM/CRUD (SQLAlchemy + PostgreSQL)

Este projeto fornece uma estrutura ORM reutilizável com operações CRUD e filtros encadeáveis, usando SQLAlchemy com suporte a PostgreSQL. Ele é ideal para quem deseja produtividade e flexibilidade ao interagir com bancos relacionais.

---

## 📁 Estrutura dos Arquivos

| Arquivo              | Função                                                                 |
|----------------------|------------------------------------------------------------------------|
| `crud.py`            | Implementa a lógica de CRUD e filtros encadeáveis (`CRUDMixin`, `QueryChain`) |
| `db.py`              | Gerencia conexão com o banco e instância da `Session`                  |
| `config.json`        | Configurações de ambiente e banco (dev, prod, etc.)                    |
| `create_tables.py`   | Cria as tabelas a partir dos models gerados                            |
| `generate_models.py` | Reflete o banco de dados e gera os arquivos Python dos models          |

---

## 🔧 Requisitos

- Python 3.9+
- SQLAlchemy
- PostgreSQL

```bash
pip install sqlalchemy psycopg2-binary
```

---

## ⚙️ Configuração do Ambiente

1. Abra o arquivo `config.json` e configure os dados do banco:

```json
{
  "ambiente": "dev",
  "database": {
    "dev": {
      "database": "pgsql",
      "dbname": "postgres_dev",
      "user": "nem_a_pau",
      "password": "nem_a_pau_mesmo",
      "host": "192.168.1.20",
      "port": "5432",
      "schema": "public"
    },
    "prod": {
      "database": "pgsql",
      "dbname": "postgres_prod",
      "user": "nem_a_pau",
      "password": "nem_a_pau_mesmo",
      "host": "192.168.1.21",
      "port": "5432",
      "schema": "public"
    },
    "auxiliar": {
      "database": "pgsql",
      "dbname": "postgres_prod",
      "user": "nem_a_pau",
      "password": "nem_a_pau_mesmo",
      "host": "192.168.1.22",
      "port": "5433",
      "schema": "public"
    }
  }
}
```

2. O valor em "ambiente" define qual conexão será usada por padrão.

---

## 🛠️ Gerando os Models Automaticamente

1. Certifique-se de que o banco e tabelas existem.
2. Rode o gerador passando o prefixo das tabelas:

```bash
python generate_models.py tbl_bb
```

Isso criará os arquivos dentro do diretório `models/`. Cada model terá:
- Classe herdando de `Base` e `CRUDMixin`
- Colunas refletidas automaticamente

Exemplo de model gerado:
```python
class TblBbBotsControle(Base, CRUDMixin):
    __tablename__ = 'tbl_bb_bots_controle'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
```

---

## 🧱 Criando as Tabelas no Banco

Após gerar os models, execute:

```bash
python create_tables.py
```

Esse script importa os models e executa `Base.metadata.create_all()`.

---

## 🧩 Entendendo a Estrutura dos Models

Todo model precisa:
- Herdar de `Base` e `CRUDMixin`
- Declarar `__tablename__` e, opcionalmente, `__table_args__`
- Utilizar colunas do SQLAlchemy normalmente

Exemplo:
```python
from sqlalchemy import Column, Integer, String
from .db import Base
from .crud import CRUDMixin

class Usuario(Base, CRUDMixin):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
```

---

## 🚀 Usando o CRUDMixin na Prática

### Métodos de Acesso Rápido

#### `Usuario.all(...)`
- Retorna um `QueryChain` que permite encadear filtros e modificadores (ex: ordenação, limite).
- Pode receber filtros via `where`, `or_where`.
- Só é executado quando um dos métodos de execução é chamado (ex: `.toDict()`, `.toList()`, `.first()`).

#### `Usuario.get(...)`
- Recebe os mesmos filtros que `all()`.
- Retorna o primeiro resultado como um `dict`, ou `None`.

#### `Usuario.insert(**kwargs)`
- Cria um novo registro no banco com os valores fornecidos.
- Retorna a instância criada (objeto do model).

#### `Usuario.create([dicts])`
- Insere vários registros em uma única operação.
- Retorna uma lista de dicionários com os dados inseridos.

#### `registro.update(...)`
- Atualiza os campos da instância atual. Pode receber:
  - dicionário (`data={}`)
  - lista de tuplas (`data=[(...)]`)
  - argumentos nomeados (`campo=valor`)
- Retorna a instância atualizada.

#### `registro.delete()`
- Remove o registro atual do banco de dados.

#### `Usuario.findById(id)`
- Retorna a instância com a chave primária fornecida.

---

## 🧠 Métodos de Execução (QueryChain)

Estes métodos executam a query e retornam os resultados:

### `.toDict()`
- Retorna uma lista de dicionários com os dados encontrados.
- Se `.select(...)` foi usado, retorna apenas as colunas selecionadas.
- Caso contrário, retorna todos os campos de cada registro.

### `.toList()`
- Retorna uma lista de objetos (instâncias da classe do model).

### `.first()`
- Retorna a primeira instância encontrada (objeto).

### `.firstToDict()`
- Retorna o primeiro resultado como dicionário (ou `None` se não houver resultado).

### `.count()`
- Retorna o número total de registros encontrados.

---

## 🔁 Encadeando Consultas com `QueryChain`

### Exemplo completo com JOIN, filtro e colunas nomeadas:
```python
from models.tbl_bb_bot_registros_primeira_sentenca import TblBbBotRegistros1Sentenca

resultado = TblBbBotRegistros1Sentenca.all()\
    .join(TblBbBotsControle, TblBbBotsControle.id == TblBbBotRegistros1Sentenca.bot_controle_id)\
    .select('id', 'sentenca', TblBbBotsControle.nome.label('nome_bot'))\
    .where('sentenca', 'like', '%despacho%')\
    .notEmpty('sentenca')\
    .orderBy('id', 'desc')\
    .limit(10)\
    .offset(0)\
    .toDict()
```

### Métodos encadeáveis disponíveis:

| Método         | Descrição |
|----------------|-----------|
| `.select(...)` | Define colunas específicas a serem retornadas |
| `.where(...)` | Filtro com igualdade ou operador customizado |
| `.whereIn(...)`, `.whereNotIn(...)` | Filtragem por lista de valores |
| `.isTrue(...)`, `.isFalse(...)` | Filtra campos booleanos |
| `.empty(...)`, `.notEmpty(...)`, `.emptyOrNull(...)` | Verifica campos vazios/nulos |
| `.orderBy(...)` | Ordena resultados por colunas |
| `.groupBy(...)` | Agrupa os resultados |
| `.limit(...)`, `.offset(...)` | Paginação |

---

## 📜 Executando SQL Bruto

Você pode executar comandos SQL diretamente:

```python
sql = "SELECT id, nome FROM public.tbl_bb_bots_controle WHERE ativo = true"
resultado = TblBbBotsControle.rawSql(sql)

for linha in resultado:
    print(linha)
```

Com parâmetros nomeados:
```python
sql = "SELECT * FROM usuarios WHERE nome LIKE :nome"
params = {"nome": "%fulano%"}
res = Usuario.rawSql(sql, params)
```

---

## 📚 Exemplos Avançados

### 🔎 Filtros combinados com múltiplas regras
```python
res = Usuario.all()\
    .whereIn('id', [1, 2, 3])\
    .isFalse('ativo')\
    .empty('encerrado_em')\
    .toDict()
```

### 🧠 Atualizar com lista de tuplas
```python
usuario.update(data=[("nome", "Novo"), ("ativo", True)])
```

### 📥 Inserção em massa
```python
dados = [
    {"nome": "Ana", "email": "a@a.com"},
    {"nome": "João", "email": "j@j.com"}
]
Usuario.create(dados)
```

---

## ⚠️ Observações Importantes

- Sempre chame um método de execução (`.toDict()`, `.first()`, etc.) para rodar a consulta.
- `select()` aceita strings (nomes das colunas do model atual) ou objetos (`Model.coluna`).
- Para JOINs, use colunas com `.label()` para evitar conflitos de nome.
- `update()` pode receber dicionário, lista de tuplas ou parâmetros nomeados.
- `rawSql()` é útil para consultas muito customizadas, mas não retorna dicionários.

---

## 👨‍💻 Autor

Desenvolvido por Marcos Ronaldo.

Para dúvidas, consulte as docstrings em `crud.py`, especialmente:
- `CRUDMixin`
- `QueryChain`

Você encontrará instruções detalhadas, exemplos e explicações de cada método.

