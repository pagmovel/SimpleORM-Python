# Manual Completo de Uso e Treinamento - Estrutura ORM com SQLAlchemy e PostgreSQL

## Índice

## Índice Atualizado

- [Introdução](#introdução)
- [Capítulo 1 – Entendendo a Arquitetura do Projeto](#capítulo-1--entendendo-a-arquitetura-do-projeto)
- [Capítulo 2 – Preparando o Ambiente: do caos ao controle](#capítulo-2--preparando-o-ambiente-do-caos-ao-controle)
  - [2.1. Instalação dos pacotes necessários](#21-instalação-dos-pacotes-necessários)
  - [2.2. Entendendo o `config.json`](#22-entendendo-o-configjson)
  - [2.3. Conexão com o banco](#23-conexão-com-o-banco)
- [Capítulo 3 – Gerando os Models automaticamente: menos tédio, mais produtividade](#capítulo-3--gerando-os-models-automaticamente-menos-tédio-mais-produtividade)
  - [3.1. O que o script `generate_models.py` faz por você?](#31-o-que-o-script-generate_modelspy-faz-por-você)
  - [3.2. Executando o gerador com um prefixo](#32-executando-o-gerador-com-um-prefixo)
  - [3.3. Anatomia de um model gerado](#33-anatomia-de-um-model-gerado)
- [Capítulo 4 – O Poder do CRUDMixin, o motor silencioso por trás da mágica: criando, lendo, atualizando e deletando com graça](#capítulo-4--o-poder-do-crudmixin-o-motor-silencioso-por-trás-da-mágica-criando-lendo-atualizando-e-deletando-com-graça)
  - [4.1. all(where=None, or_where=None)](#41-allwherenone-or_wherenone)
  - [4.2. get(where=None, or_where=None)](#42-getwherenone-or_wherenone)
  - [4.3. insert(\*\*kwargs)](#43-insertkwargs)
  - [4.4. create(records)](#44-createrecords)
  - [4.5. update(data=None, \*\*kwargs)](#45-updatedatanone-kwargs)
  - [4.6. delete()](#46-delete)
  - [4.7. findById(id)](#47-findbyidid)
  - [4.8. rawSql(sql_string, params=None, db_key=None)](#48-rawsqlsql_string-paramsnone-db_keynone)
- [Capítulo 5 – QueryChain: a arte de consultar como um mestre zen](#capítulo-5--querychain-a-arte-de-consultar-como-um-mestre-zen)
  - [5.1. O problema: consultas monolíticas, ilegíveis e inflexíveis](#51-o-problema-consultas-monolíticas-ilegíveis-e-inflexíveis)
  - [5.2. A solução: QueryChain](#52-a-solução-querychain)
  - [5.3. Métodos de Encadeamento](#53-métodos-de-encadeamento)
  - [5.4. Métodos de Execução](#54-métodos-de-execução)
  - [5.5. Exemplo prático completo](#55-exemplo-prático-completo)
- [Capítulo 6 – Casos de Uso Reais: quando o banco de dados encontra a vida real](#capítulo-6--casos-de-uso-reais-quando-o-banco-de-dados-encontra-a-vida-real)

  - [6.1. Cenário 1 – Consulta condicional com parâmetros dinâmicos](#61-cenário-1--consulta-condicional-com-parâmetros-dinâmicos)
  - [6.2. Cenário 2 – Gerando relatório com agregações](#62-cenário-2--gerando-relatório-com-agregações)
  - [6.3. Cenário 3 – API paginada com ordenação dinâmica](#63-cenário-3--api-paginada-com-ordenação-dinâmica)
  - [6.4. Cenário 4 – Join com múltiplas tabelas e múltiplas colunas](#64-cenário-4--join-com-múltiplas-tabelas-e-múltiplas-colunas)
  - [6.5. Cenário 5 – Atualização condicional de registros](#65-cenário-5--atualização-condicional-de-registros)

- [Capítulo 7 – Boas Práticas, Armadilhas Comuns e Como Evitar Tragédias Anunciadas](#capítulo-7--boas-práticas-armadilhas-comuns-e-como-evitar-tragédias-anunciadas)
  - [7.1. Fechando sessões corretamente](#71-fechando-sessões-corretamente)
  - [7.2. Use `.select()` com sabedoria](#72-use-select-com-sabedoria)
  - [7.3. Evite `.toList()` se você precisa de dicionários](#73-evite-tolist-se-você-precisa-de-dicionários)
  - [7.4. Cuidado com operadores mal utilizados](#74-cuidado-com-operadores-mal-utilizados)
  - [7.5. Joins sem `label()` podem quebrar sua API](#75-joins-sem-label-podem-quebrar-sua-api)
  - [7.6. Atualizações em massa exigem cuidado](#76-atualizações-em-massa-exigem-cuidado)
  - [7.7. Documente os models gerados automaticamente](#77-documente-os-models-gerados-automaticamente)
  - [7.8. Use `rawSql()` com moderação (mas sem medo)](#78-use-rawsql-com-moderação-mas-sem-medo)
- [Capítulo 8 – Testes, Extensões e o Futuro: adaptando sua arquitetura para crescer com você](#capítulo-8--testes-extensões-e-o-futuro-adaptando-sua-arquitetura-para-crescer-com-você)
  - [8.1. Testes automatizados com SQLAlchemy](#81-testes-automatizados-com-sqlalchemy)
  - [8.2. Como estender o CRUDMixin](#82-como-estender-o-crudmixin)
  - [8.3. Integração com frameworks web](#83-integração-com-frameworks-web)
- [Capítulo 9 – Validação Inteligente com Elegância: erros que explicam, não confundem](#capítulo-9--validação-inteligente-com-elegância-erros-que-explicam-não-confundem)
  - [9.1. O que é o `validate_or_fail`](#91-o-que-é-o-validate_or_fail)
  - [9.2. Declarando regras no seu model](#92-declarando-regras-no-seu-model)
  - [9.3. Validação em Ação: exemplos reais](#93-validação-em-ação-exemplos-reais)
  - [9.4. Regras avançadas: min, max, in, regex](#94-regras-avançadas-min-max-in-regex)
  - [9.5. Capturando erros manualmente (útil em APIs)](#95-capturando-erros-manualmente-útil-em-apis)
  - [9.6. Validação em massa com `.create()`](#96-validação-em-massa-com-create)
  - [9.7. Validar dados sem salvar: uso direto do `validate_or_fail`](#97-validar-dados-sem-salvar-uso-direto-do-validate_or_fail)
  - [9.8. Dicas finais](#98-dicas-finais)
- [Capítulo 10 – Protegendo e Traduzindo Campos com Elegância: fillable, guarded e aliases](#capítulo-10--protegendo-e-traduzindo-campos-com-elegância-fillable-guarded-e-aliases)
  - [10.1. O que é `fillable`](#101-o-que-é-fillable)
  - [10.2. E o `guarded`](#102-e-o-guarded)
  - [10.3. Quando usar `fillable` vs `guarded`](#103-quando-usar-fillable-vs-guarded)
  - [10.4. `aliases`: traduzindo campos amigavelmente](#104-aliases-traduzindo-campos-amigavelmente)
  - [10.5. Aplicação combinada: tudo junto](#105-aplicação-combinada-tudo-junto)
  - [10.6. Dica bônus: compatível com `.update()` também](#106-dica-bônus-compatível-com-update-também)
  - [10.7. Por que isso importa?](#107-por-que-isso-importa)

## Introdução

Parabéns. Se você está lendo este documento, é muito provável que tenha sobrevivido à primeira onda de documentação técnica — aquela mais resumida, prática, cheia de bullet points e exemplos secos como torradas esquecidas no forno. Mas agora é diferente. Você chegou ao **MANUAL**, o verdadeiro compêndio. Este é o seu mapa do tesouro, onde vamos destrinchar com minúcia o funcionamento interno desta arquitetura ORM baseada em SQLAlchemy. E não se preocupe, não será uma jornada solitária: eu estarei com você, passo a passo, sem pressa, e com algumas piadas sutis pelo caminho (prometo não exagerar).

Este manual é ideal para:

- Desenvolvedores iniciantes que querem aprender como estruturar suas aplicações com SQLAlchemy.
- Desenvolvedores experientes que precisam compreender os detalhes do projeto.
- Equipes técnicas que desejam padronizar o uso da camada de dados.

Antes de mergulharmos no código, precisamos responder a uma pergunta essencial:

**Por que usar uma arquitetura ORM (Object Relational Mapping)?**

Se você já teve que escrever dezenas de comandos SQL diretamente dentro do seu código — e pior, repetir os mesmos SELECTs com pequenas variações — sabe bem como isso pode se tornar um pesadelo. A abordagem ORM traz um modelo mais elegante: objetos Python representam suas tabelas, e os métodos que você chama nesses objetos geram automaticamente os SQLs necessários por baixo dos panos. Além disso, a separação entre lógica de negócio e persistência de dados se torna muito mais limpa e testável.

O projeto que você tem em mãos vai além do ORM básico. Ele implementa uma camada intermediária chamada `CRUDMixin`, com suporte a um poderoso encadeamento de consultas via `QueryChain`. Essa combinação permite escrever consultas com um nível de expressividade que beira a poesia — ou quase isso.

Ao final deste manual, você será capaz de:

1. Entender a estrutura do projeto em profundidade.
2. Configurar corretamente o ambiente.
3. Gerar modelos automaticamente a partir do seu banco de dados.
4. Utilizar os métodos CRUD com segurança e clareza.
5. Encadear consultas complexas usando `QueryChain`.
6. Executar comandos SQL personalizados de forma segura.

---

## Capítulo 1 – Entendendo a Arquitetura do Projeto

Imagine o projeto como um prédio modular:

- O **alicerce** é o SQLAlchemy. Ele define a base da comunicação com o banco e representa suas tabelas como classes.
- O **térreo** é o `db.py`, que configura a conexão com o banco e cria a `Base` e o `SessionLocal`, fundamentais para qualquer operação.
- O **primeiro andar** é o `crud.py`, que define `CRUDMixin` (a camada que fornece os métodos insert, update, delete, etc.) e `QueryChain`, a alma do encadeamento de consultas.
- O **segundo andar** é a pasta `models/`, onde ficam os modelos Python que representam suas tabelas no banco.
- No **telhado**, temos arquivos utilitários como `create_tables.py` e `generate_models.py`, que ajudam a construir e manter a estrutura de forma automática.

Nada aqui é aleatório. Cada peça tem sua razão de existir — e todas funcionam em harmonia para oferecer uma interface robusta, escalável e elegante.

---

## Capítulo 2 – Preparando o Ambiente: do caos ao controle

Imagine que você acaba de baixar o projeto, animado para ver tudo funcionando. Você digita um `python script.py` com entusiasmo e... erro. A tela te olha de volta com uma exceção digna de um filme de terror. Calma. Vamos evitar esse cenário.

### 2.1. Instalação dos pacotes necessários

Primeiro passo é garantir que você tenha o ambiente Python corretamente configurado. O projeto foi testado com Python 3.9+, então evite versões muito antigas (ou muito exóticas).

Instale os pacotes necessários:

```bash
pip install sqlalchemy psycopg2-binary
```

Esses dois pacotes são indispensáveis:

- `sqlalchemy`: o ORM principal que usamos.
- `psycopg2-binary`: driver para conectar com bancos PostgreSQL.

Se quiser brincar em modo local com SQLite, o SQLAlchemy também suporta, mas aqui focaremos na estrutura pensada para PostgreSQL.

### 2.2. Entendendo o `config.json`

O `config.json` é o cérebro das configurações de ambiente. Ele informa qual banco usar, credenciais, host e até mesmo o schema (isso mesmo, aquele que alguns esquecem que existe em bancos mais parrudos como o PostgreSQL).

Veja um exemplo de entrada de ambiente:

```json
{
  "environment": "dev",
  "database": {
    "dev": {
      "database": "pgsql",
      "dbname": "meubanco",
      "user": "meuusuario",
      "password": "minhasenha",
      "host": "127.0.0.1",
      "port": "5432",
      "schema": "public"
    },
    "prod": {
      "database": "pgsql",
      "dbname": "postgres",
      "user": "postgres",
      "password": "postgres",
      "host": "192.168.1.21",
      "port": "5432",
      "schema": "public"
    },
    "staging": {
      "database": "pgsql",
      "dbname": "postgres",
      "user": "postgres",
      "password": "postgres",
      "host": "192.168.1.22",
      "port": "5432",
      "schema": "public"
    },
    "autokit": {
      "database": "pgsql",
      "dbname": "postgres",
      "user": "postgres",
      "password": "postgres",
      "host": "192.168.1.23",
      "port": "5432",
      "schema": "public"
    }
  }
}
```

Alguns pontos importantes:

- `environment`: define qual configuração será carregada.
- `database`: agrupa as conexões disponíveis por nome (dev, prod, staging, autokit... você escolhe).

Você pode definir múltiplos ambientes, e mudar entre eles apenas trocando a chave `environment`.

### 2.3. Conexão com o banco

A função `get_engine()` dentro de `db.py` vai ler o `config.json` e montar a string de conexão com base no ambiente ativo. Não é mágica negra — é só leitura de JSON, concatenação e uso da função `create_engine()` do SQLAlchemy.

O `SessionLocal` também é criado ali, e será usado para abrir conexões de sessão de forma segura e isolada.

---

## Capítulo 3 – Gerando os Models automaticamente: menos tédio, mais produtividade

Se você já teve que escrever à mão todos os modelos de um banco com 30, 50 ou 200 tabelas... você sabe: é o tipo de tarefa que testa sua sanidade. Este projeto elimina essa tortura com um script que automatiza toda essa geração com base no schema do banco.

### 3.1. O que o script `generate_models.py` faz por você?

Esse script acessa seu banco de dados, reflete as tabelas e gera um arquivo `.py` para cada tabela, dentro da pasta `models/`. Ele gera:

- A declaração da classe com `Base` e `CRUDMixin`
- Colunas e tipos automaticamente
- Chaves primárias e estrangeiras
- Indexes e restrições únicas, se existirem
- Atribuição de schema

Tudo isso é extraído diretamente da estrutura do banco de dados.

### 3.2. Executando o gerador com um prefixo

A ideia é que você possa gerar apenas os models que começam com um determinado prefixo (por exemplo, `tbl_`, `app_`, `sys_`, etc.):

```bash
python generate_models.py tbl_
```

Esse comando gera apenas os arquivos dos modelos cujos nomes de tabela começam com `tbl_`.

O resultado será algo como:

```
models/
├── tbl_bot_registros.py
├── tbl_bots_control.py
```

Cada arquivo contém uma classe declarada corretamente, pronta para uso.

### 3.3. Anatomia de um model gerado

Vamos analisar um exemplo gerado automaticamente:

```python
from sqlalchemy import Column, Integer, String, Boolean
from .db import Base
from .crud import CRUDMixin

class TblBotsControle(Base, CRUDMixin):
    __tablename__ = 'tbl_bots_control'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
```

Explicando:

- `Base` é a base declarativa do SQLAlchemy, herdada por todos os models.
- `CRUDMixin` traz todos os métodos de acesso ao banco (insert, update, delete, all, get, etc.).
- `__tablename__` define o nome da tabela no banco.
- `__table_args__` define o schema utilizado (importante em PostgreSQL).
- As colunas usam os tipos corretos, extraídos do banco.

Você pode editar livremente os modelos após a geração, inclusive adicionando métodos próprios ou propriedades especiais.

No próximo capítulo, você aprenderá a criar as tabelas no banco com um único comando, e entenderá como isso se conecta com os modelos gerados.

---

## Capítulo 4 – O Poder do CRUDMixin, o motor silencioso por trás da mágica: criando, lendo, atualizando e deletando com graça

Chegamos a um dos pontos mais poderosos — e muitas vezes subestimados — dessa arquitetura: o `CRUDMixin`. Este mixin é responsável por fornecer todos os métodos essenciais para operar sobre os dados. A beleza disso? Você escreve pouquíssimo código e ganha uma capacidade enorme de controle sobre as operações de banco.

Vamos agora destrinchar cada método deste mixin. E não apenas dizer o que ele faz, mas mostrar como, quando, e por que utilizá-lo.

### 4.1. all(where=None, or_where=None)

Este método é o ponto de entrada para iniciar uma consulta complexa, retornando uma instância de `QueryChain`, que permite encadeamento fluente de filtros, ordenações, joins e outros modificadores.

#### Parâmetros:

- `where`: tupla ou lista de tuplas com filtros a serem aplicados com `AND`
- `or_where`: tupla ou lista de tuplas com filtros aplicados com `OR`

#### Retorno:

- Um objeto `QueryChain`, que precisa ser finalizado com um método de execução, como `.toList()`, `.toDict()`, `.first()`, etc.

#### Exemplo:

```python
usuarios = Usuario.all(where=("ativo", True)).orderBy("id", "desc").limit(10).toDict()
```

### 4.2. get(where=None, or_where=None)

Retorna o primeiro registro que satisfaz os critérios passados, convertido automaticamente para um dicionário.

#### Retorno:

- Um `dict` com os campos do model ou `None` se nenhum registro for encontrado.

#### Exemplo:

```python
admin = Usuario.get(where=("email", "admin@empresa.com"))
```

### 4.3. insert(\*\*kwargs)

Cria e persiste um novo registro no banco.

#### Parâmetros:

- Argumentos nomeados, correspondendo às colunas da tabela.

#### Retorno:

- A instância do model recém-criada.

#### Exemplo:

```python
novo_usuario = Usuario.insert(nome="Fernanda", email="fer@empresa.com", ativo=True)
```

### 4.4. create(records)

Cria múltiplos registros em uma única transação.

#### Parâmetros:

- `records`: uma lista de dicionários, cada um representando um novo registro.

#### Retorno:

- Uma lista de dicionários contendo os dados persistidos.

#### Exemplo:

```python
dados = [
    {"nome": "Ana"},
    {"nome": "Bruno"}
]
usuarios = Usuario.create(dados)
```

### 4.5. update(data=None, \*\*kwargs)

Atualiza os campos da instância atual. Pode receber os dados em múltiplos formatos.

#### Formas válidas:

- `data={"campo": valor}`
- `data=[("campo", valor)]`
- `campo=valor` diretamente

#### Exemplo:

```python
usuario.update(nome="João da Silva", ativo=False)
```

### 4.6. delete()

Remove o registro atual do banco. Não há volta, então cuidado com esse botão nuclear.

#### Exemplo:

```python
usuario.delete()
```

### 4.7. findById(id)

Busca um registro pela chave primária.

#### Retorno:

- A instância do model, ou `None` se não encontrar

#### Exemplo:

```python
usuario = Usuario.findById(42)
```

### 4.8. rawSql(sql_string, params=None, db_key=None)

Executa SQL puro diretamente no banco. Deve ser usada com cautela, mas é essencial quando você precisa de consultas mais complexas ou fora do escopo do ORM.

#### Parâmetros:

- `sql_string`: string SQL (use parâmetros nomeados para segurança)
- `params`: dicionário com os valores dos parâmetros
- `db_key`: opcional, permite selecionar outro banco configurado no `config.json`

#### Exemplo:

```python
sql = "SELECT * FROM usuarios WHERE nome ILIKE :nome"
res = Usuario.rawSql(sql, {"nome": "%jo%"})
```

---

No próximo capítulo, vamos nos aprofundar no `QueryChain`, essa maravilha que permite escrever consultas que antes exigiriam várias linhas de SQL, agora com poucas e elegantes instruções Python.

---

## Capítulo 5 – QueryChain: a arte de consultar como um mestre zen

Chegamos ao coração do sistema de consultas desta arquitetura: a classe `QueryChain`. Ela é, para todos os efeitos práticos, o seu melhor amigo quando se trata de extrair dados do banco de maneira expressiva, legível e incrivelmente poderosa. Este capítulo é inteiramente dedicado a te transformar em um verdadeiro mestre zen do encadeamento de consultas.

Mas antes de ir direto ao ponto, vamos entender o **porquê** da existência dessa classe.

### 5.1. O problema: consultas monolíticas, ilegíveis e inflexíveis

Quem já usou SQLAlchemy puro para montar consultas com múltiplos filtros, joins, ordenações e paginações sabe que o código começa a ficar verboso rapidamente. Pior ainda, quando você precisa aplicar condicionais dinâmicas — dependendo de parâmetros recebidos por uma API ou lógica de negócio — manter o código limpo se torna quase impossível sem muita abstração.

### 5.2. A solução: QueryChain

A `QueryChain` resolve exatamente isso. Ela encapsula uma `query` SQLAlchemy e fornece uma interface fluente (inspirada em bibliotecas como jQuery e LINQ) que permite encadear modificadores e só executar a query no final, com um dos métodos de execução.

Vamos olhar para isso em profundidade, analisando cada método que você pode usar e como ele altera o estado da consulta.

---

### 5.3. Métodos de Encadeamento

#### select(\*columns)

Seleciona colunas específicas para retorno. Se não for usado, retorna todas as colunas do model.

```python
usuarios = Usuario.all().select("id", "nome").toDict()
```

Você também pode passar colunas de outro model em joins:

```python
from models.empresa import Empresa
res = Usuario.all().join(Empresa, Usuario.empresa_id == Empresa.id)
          .select(Usuario.nome, Empresa.nome.label("empresa"))
          .toDict()
```

#### where(...)

Aplica um filtro `AND`. Suporta dois formatos:

- `("coluna", valor)` => assume igualdade
- `("coluna", "operador", valor)` => operador explícito (`!=`, `>`, `like`, etc.)

```python
Usuario.all().where("ativo", True).where("idade", ">=", 18)
```

#### whereIn(coluna, lista)

Filtra registros com valores dentro de uma lista:

```python
Usuario.all().whereIn("id", [1,2,3])
```

#### whereNotIn(coluna, lista)

Oposto do anterior:

```python
Usuario.all().whereNotIn("perfil", ["admin", "root"])
```

#### isTrue(coluna) e isFalse(coluna)

Aplica verificação booleana:

```python
Usuario.all().isTrue("ativo")
Usuario.all().isFalse(["confirmado", "validado"])
```

#### empty(coluna) e notEmpty(coluna)

Verifica se os campos estão vazios (nulo ou string vazia):

```python
Usuario.all().empty("data_desativacao")
Usuario.all().notEmpty("nome")
```

#### emptyOrNull(coluna)

Versão mais inteligente que trata strings e outros tipos:

```python
Usuario.all().emptyOrNull("descricao")
```

#### join(model, onclause=None)

Faz inner join:

```python
Usuario.all().join(Empresa, Usuario.empresa_id == Empresa.id)
```

#### leftJoin(model, onclause=None)

Faz left outer join:

```python
Usuario.all().leftJoin(Empresa, Usuario.empresa_id == Empresa.id)
```

#### groupBy(...)

Agrupamento por colunas:

```python
Usuario.all().groupBy(Usuario.perfil).toList()
```

#### orderBy(...)

Aceita duas formas:

- Strings em pares: `("nome", "asc")`
- Expressões SQLAlchemy: `Model.coluna.desc()`

```python
Usuario.all().orderBy("nome", "asc", "id", "desc")
Usuario.all().orderBy(Usuario.id.desc())
```

#### limit(valor) e offset(valor)

Paginação:

```python
Usuario.all().limit(10).offset(20)
```

---

### 5.4. Métodos de Execução

Estes são os métodos que de fato **executam** a query montada.

#### toList()

Retorna uma lista de objetos (instâncias do model). Ideal para lógica interna.

```python
registros = Usuario.all().toList()
for r in registros:
    print(r.nome)
```

#### toDict()

Retorna lista de dicionários. Ideal para APIs e serialização.

```python
dados = Usuario.all().select("id", "nome").toDict()
```

#### first()

Retorna a primeira instância encontrada (ou `None`).

```python
u = Usuario.all().where("email", "fulano@email.com").first()
```

#### firstToDict()

Mesmo que `first()`, mas converte para dicionário.

```python
dados = Usuario.all().where("email", "fulano@email.com").firstToDict()
```

#### count()

Executa um `SELECT COUNT(*)` com os filtros aplicados:

```python
ativos = Usuario.all().isTrue("ativo").count()
```

---

### 5.5. Exemplo prático completo

Vamos construir uma consulta complexa para ilustrar tudo isso:

```python
usuarios = Usuario.all()\
    .leftJoin(Empresa, Usuario.empresa_id == Empresa.id)\
    .select(Usuario.id, Usuario.nome, Empresa.nome.label("empresa"))\
    .where("ativo", True)\
    .notEmpty("email")\
    .orderBy("nome", "asc")\
    .limit(10)\
    .toDict()
```

Você acabou de construir o equivalente a uma query SQL com `JOIN`, `WHERE`, `ORDER BY`, `LIMIT`, projeção de colunas e tratamento de nulls — tudo isso em um encadeamento legível e reaproveitável.

No próximo capítulo, vamos entrar em cenários de uso do mundo real, com casos que exigem lógica condicional, múltiplas tabelas e decisões em tempo de execução.

---

## Capítulo 6 – Casos de Uso Reais: quando o banco de dados encontra a vida real

Até aqui, exploramos ferramentas. Agora é hora de ver essas ferramentas em ação — como um chef de cozinha que conhece suas facas e panelas, mas quer mesmo é saber como preparar um belo risoto de cogumelos.

Este capítulo apresenta cenários reais que vão desde a consulta simples até a manipulação condicional de dados, passando por joins, paginação dinâmica, construção de filtros em tempo de execução, e integração com endpoints REST.

### 6.1. Cenário 1 – Consulta condicional com parâmetros dinâmicos

Imagine que você tem um endpoint de API que aceita múltiplos parâmetros de filtro:

```python
# Parâmetros vindos de uma requisição
params = {
    "ativo": True,
    "perfil": "editor",
    "idade_min": 25,
    "busca": "silva"
}
```

Queremos montar a consulta com base apenas nos parâmetros fornecidos (e ignorar os ausentes). Com QueryChain, isso é simples:

```python
query = Usuario.all()

if "ativo" in params:
    query = query.isTrue("ativo") if params["ativo"] else query.isFalse("ativo")

if "perfil" in params:
    query = query.where("perfil", params["perfil"])

if "idade_min" in params:
    query = query.where("idade", ">=", params["idade_min"])

if "busca" in params:
    query = query.where("nome", "like", f"%{params['busca']}%")

usuarios = query.toDict()
```

Resultado: você construiu dinamicamente uma consulta altamente flexível sem precisar escrever ifs aninhados com SQL literal.

### 6.2. Cenário 2 – Gerando relatório com agregações

Vamos supor que você precise de um relatório que conte o número de usuários por perfil. Aqui entra o `groupBy()`:

```python
from sqlalchemy import func

resumo = Usuario.all()\
    .select(Usuario.perfil, func.count(Usuario.id).label("total"))\
    .groupBy(Usuario.perfil)\
    .orderBy("total", "desc")\
    .toDict()
```

O resultado será uma lista como:

```python
[
  {"perfil": "admin", "total": 12},
  {"perfil": "editor", "total": 7},
  {"perfil": "leitor", "total": 4}
]
```

### 6.3. Cenário 3 – API paginada com ordenação dinâmica

Suponha que você esteja implementando um endpoint REST com suporte a ordenação e paginação:

```python
# Parâmetros de paginação
page = 3
per_page = 20
sort_field = "nome"
sort_order = "asc"

usuarios = Usuario.all()\
    .orderBy(sort_field, sort_order)\
    .limit(per_page)\
    .offset((page - 1) * per_page)\
    .toDict()
```

Resultado: apenas os usuários daquela página serão retornados, ordenados conforme desejado.

### 6.4. Cenário 4 – Join com múltiplas tabelas e múltiplas colunas

Agora imagine que você precisa montar um relatório completo com dados da tabela de usuários, empresas e registros:

```python
from models.empresa import Empresa
from models.registro import Registro

dados = Usuario.all()\
    .join(Empresa, Usuario.empresa_id == Empresa.id)\
    .join(Registro, Registro.usuario_id == Usuario.id)\
    .select(
        Usuario.id, Usuario.nome,
        Empresa.nome.label("empresa"),
        Registro.tipo, Registro.criado_em
    )\
    .where("ativo", True)\
    .orderBy("criado_em", "desc")\
    .limit(50)\
    .toDict()
```

Você acabou de fazer um join triplo com projeção personalizada. E tudo isso com encadeamento limpo.

### 6.5. Cenário 5 – Atualização condicional de registros

Vamos imaginar que você deseja desativar todos os usuários inativos há mais de um ano:

```python
from datetime import datetime, timedelta
limite = datetime.now() - timedelta(days=365)

usuarios = Usuario.all()\
    .where("ativo", True)\
    .where("ultimo_login", "<", limite)\
    .toList()

for usuario in usuarios:
    usuario.update(ativo=False)


# Ou

for usuario in usuarios:
    User.updateWhere(ativo=False, ('id', usuario['id']))
```

---

Esses são apenas alguns exemplos reais que mostram o poder da arquitetura quando aplicada com criatividade e clareza.

No próximo capítulo, vamos tratar de boas práticas, erros comuns e como evitar surpresas desagradáveis em produção.

---

## Capítulo 7 – Boas Práticas, Armadilhas Comuns e Como Evitar Tragédias Anunciadas

Chegamos à parte em que a teoria encontra o campo de batalha. Não importa o quão poderosa seja sua arquitetura: se mal utilizada, ela pode se transformar em um festival de bugs, lentidão e frustração. Este capítulo é um guia de sobrevivência: ele não só revela as boas práticas que você deve seguir, mas também expõe os erros comuns com uma lanterna potente — e, é claro, mostra como evitá-los.

### 7.1. Fechando sessões corretamente

**Problema:** você abriu uma sessão, executou uma query... e nunca a fechou. Isso, em ambientes com muitas requisições simultâneas, é como deixar a torneira da pia aberta durante um racionamento de água.

**Solução:** todos os métodos que executam query no `QueryChain` (como `.toDict()`, `.first()`, `.count()`) já fecham a sessão automaticamente. Mas, se você escrever consultas personalizadas, lembre-se de fechar a sessão manualmente:

```python
session = SessionLocal()
try:
    resultado = session.query(Usuario).all()
finally:
    session.close()
```

### 7.2. Use `.select()` com sabedoria

**Problema:** você precisa retornar só duas colunas, mas esquece de usar `.select()` e retorna todos os campos — incluindo colunas com blobs, JSONs enormes ou logs antigos.

**Solução:** sempre que sua consulta for para API ou relatório, use `.select()` com as colunas exatas. Isso reduz o tráfego, melhora a performance e clareia o código:

```python
Usuario.all().select("id", "nome", "email").toDict()
```

### 7.3. Evite `.toList()` se você precisa de dicionários

**Problema:** você usa `.toList()` e depois tenta serializar as instâncias do model em JSON... e se vê preso escrevendo `vars()` ou `.__dict__`.

**Solução:** se você quer um resultado pronto para serialização, use `.toDict()`. O método já converte internamente os objetos com base nas colunas definidas.

### 7.4. Cuidado com operadores mal utilizados

**Problema:** você tenta usar `>=` diretamente como string no `.where()` e se esquece de passar os três argumentos:

```python
# ERRADO
Usuario.all().where("idade >=", 18)

# CERTO
Usuario.all().where("idade", ">=", 18)
```

**Dica bônus:** se você tiver múltiplos filtros, prefira aplicá-los encadeando `.where()` ou usando listas para clareza.

### 7.5. Joins sem `label()` podem quebrar sua API

**Problema:** você faz um join e usa `.select()` com duas colunas `nome` — uma da tabela `Usuario` e outra da tabela `Empresa`. Resultado: a última sobrescreve a anterior no dicionário.

**Solução:** sempre use `.label("alias")` em colunas de outras tabelas:

```python
.select(Usuario.nome, Empresa.nome.label("empresa"))
```

### 7.6. Atualizações em massa exigem cuidado

**Problema:** você busca múltiplos registros com `.toList()` e faz update em loop, mas esquece que cada `update()` abre e fecha uma sessão separada. Em alguns bancos, isso pode gerar deadlocks.

**Solução:** em updates críticos, use `.rawSql()` ou agrupe as atualizações em uma única transação personalizada com `session.begin()`.

### 7.7. Documente os models gerados automaticamente

**Problema:** o gerador de models cria tudo corretamente, mas você se esquece de adicionar docstrings, comentários ou validações personalizadas depois.

**Solução:** após gerar os arquivos com `generate_models.py`, revise cada um, documente, adicione métodos específicos do domínio e centralize regras de negócio simples ali mesmo.

### 7.8. Use `rawSql()` com moderação (mas sem medo)

**Problema:** você evita `rawSql()` por medo de perder o controle — ou usa demais, burlando toda a abstração ORM.

**Solução:** `rawSql()` é ótimo para relatórios complexos, views materializadas ou queries com CTEs. Use com moderação, mas sem preconceito.

---

Dominar a arquitetura não é apenas aprender como usá-la, mas também como **não** usá-la. Uma arquitetura elegante precisa de disciplina para se manter limpa, segura e eficiente.

No próximo capítulo, fecharemos com orientações sobre testes, extensões futuras e como essa arquitetura pode evoluir junto com seu sistema.

---

## Capítulo 8 – Testes, Extensões e o Futuro: adaptando sua arquitetura para crescer com você

Neste último capítulo, vamos dar um passo além da implementação: vamos falar sobre **manutenção**, **evolução** e, principalmente, como garantir que sua arquitetura continue funcionando à medida que sua aplicação cresce, muda, escala e — inevitavelmente — quebra.

Um código funcional é ótimo. Um código testável, extensível e resiliente é o que diferencia um desenvolvedor pragmático de um desenvolvedor verdadeiramente profissional.

### 8.1. Testes automatizados com SQLAlchemy

Testar é a única forma confiável de dormir tranquilo enquanto o deploy roda na sexta-feira. E o melhor: a arquitetura deste projeto já está preparada para isso.

#### Estratégia recomendada

- Use `pytest` como framework principal de testes.
- Crie um banco de testes separado (pode até ser SQLite em memória para velocidade).
- Use `Base.metadata.create_all()` para criar as tabelas temporariamente antes dos testes.
- Use `session.begin()` ou `session.rollback()` para garantir isolamento dos testes.

#### Exemplo de teste simples

```python
import pytest
from models.usuario import Usuario
from models.db import SessionLocal, Base, get_engine

@pytest.fixture(scope="function")
def session():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

def test_usuario_insert(session):
    novo = Usuario.insert(nome="Teste", email="teste@a.com")
    assert novo.id is not None
```

#### Dica de ouro:

Evite reusar sessões entre testes. Cada teste deve começar com banco limpo.

---

### 8.2. Como estender o CRUDMixin

Embora `CRUDMixin` já cubra as operações básicas (insert, update, delete, get, all, rawSql...), você pode perfeitamente personalizá-lo para as regras do seu sistema.

#### Exemplo: adicionando um método soft delete

```python
class CustomMixin(CRUDMixin):
    def soft_delete(self):
        self.update(ativo=False)
```

Depois, use isso em seus modelos:

```python
class Usuario(Base, CustomMixin):
    ...
```

Você também pode sobrescrever `insert()` ou `update()` para aplicar validações específicas antes do commit.

---

### 8.3. Integração com frameworks web

Essa arquitetura se encaixa perfeitamente com frameworks como Flask, FastAPI e até Django (em projetos com arquitetura hexagonal).

#### Exemplo com FastAPI

```python
@app.get("/usuarios")
def listar():
    return Usuario.all().isTrue("ativo").orderBy("nome").toDict()
```

#### Cuidado:

Use sempre sessões curtas e encapsuladas em rotas para evitar problemas de concorrência.

---

## Capítulo 9 – Validação Inteligente com Elegância: erros que explicam, não confundem

Se você já tentou debugar um formulário que simplesmente “não salva” sem nenhuma mensagem clara, este capítulo é para você.

Agora que você já sabe inserir, atualizar, deletar e consultar com maestria, é hora de elevar a robustez do seu sistema. Vamos adicionar uma camada de proteção aos dados — a validação.

O sistema apresentado aqui já vem com um motor de validação embutido, que você pode ativar com o mínimo de esforço e o máximo de clareza.

---

### 9.1. O que é o `validate_or_fail`?

A função `validate_or_fail` (presente em `validator.py`) é uma validadora genérica que aplica um conjunto de regras simples a qualquer dicionário de dados.

Ela suporta:

- Campos obrigatórios
- Validação de tipo (`string`, `integer`, `email`, etc.)
- Regras de tamanho (`min`, `max`)
- Validação com regex
- Verificação por valores permitidos (`in`, `not_in`)

Se algum erro for encontrado, uma exceção `ValidationError` é lançada, contendo um dicionário explicando exatamente o que deu errado — campo por campo.

---

### 9.2. Declarando regras no seu model

Vamos usar como exemplo o model `User`, que já vem com regras básicas:

```python
class User(Base, CRUDMixin):
    ...

    @classmethod
    def rules(cls):
        return {
            'name': ['required'],
            'email': ['required', 'email'],
            'password': ['required'],
        }
```

Essas regras dizem:

- `name` é obrigatório
- `email` é obrigatório e deve ter formato válido
- `password` é obrigatório

Você pode adicionar quantas regras quiser, e elas serão automaticamente aplicadas ao usar `.insert()`, `.create()` e `.update()`.

---

### 9.3. Validação em Ação: exemplos reais

#### 1. Inserindo um registro com dados inválidos

```python
User.insert(name="", email="errado", password=None)
```

Resultado:

```python
ValidationError: {
  'name': ['Este campo é obrigatório.'],
  'email': ['Formato de e-mail inválido.'],
  'password': ['Este campo é obrigatório.']
}
```

#### 2. Atualizando com segurança

```python
usuario.update(email="sem-arroba", name="  ")
```

Retorno esperado:

```python
ValidationError: {
  'name': ['Este campo é obrigatório.'],
  'email': ['Formato de e-mail inválido.']
}
```

---

### 9.4. Regras avançadas: min, max, in, regex

Você pode usar regras mais elaboradas para validar diferentes tipos de dados:

```python
@classmethod
def rules(cls):
    return {
        'name': ['required', 'min:3', 'max:50'],
        'email': ['required', 'email'],
        'idade': ['integer', 'min:18'],
        'genero': ['in:["M","F","O"]'],
        'cpf': ['regex:^\\d{11}$']
    }
```

Essas regras permitem validar:

- Tamanho mínimo/máximo de strings
- Intervalos de números
- Conjunto de valores permitidos
- Formato de campos específicos com expressões regulares

---

### 9.5. Capturando erros manualmente (útil em APIs)

Você pode capturar os erros de validação e transformá-los em mensagens amigáveis em sua aplicação:

```python
from utils.validator import ValidationError

try:
    User.insert(name="Ok", email="sem-email", password="")
except ValidationError as e:
    print(e.errors)
```

---

### 9.6. Validação em massa com `.create()`

Ao usar `.create()`, cada item da lista será validado individualmente:

```python
dados = [
    {"name": "Alice", "email": "alice@teste.com", "password": "abc"},
    {"name": "", "email": "bob@", "password": None}
]

User.create(dados)
```

Resultado:

```
[VALIDAÇÃO] Erro no registro 2: {
  'name': ['Este campo é obrigatório.'],
  'email': ['Formato de e-mail inválido.'],
  'password': ['Este campo é obrigatório.']
}
```

---

### 9.7. Validar dados sem salvar: uso direto do `validate_or_fail`

Nem sempre você quer inserir ou atualizar imediatamente. Às vezes, você só precisa verificar se os dados **seriam válidos** — por exemplo:

- antes de mostrar uma mensagem de erro no formulário
- antes de chamar uma API externa
- em um `dry-run` de importação em massa
- durante validação em endpoints que ainda não persistem dados

Para isso, você pode usar diretamente a função `validate_or_fail`, passando os dados e as regras:

#### Exemplo 1 – Validação simples (sem salvar)

```python
from utils.validator import validate_or_fail

dados = {
    "name": "",
    "email": "errado",
    "password": "123"
}

# Validando com as regras do próprio model
validate_or_fail(dados, User.rules())
```

Isso lançará:

```python
ValidationError: {
  'name': ['Este campo é obrigatório.'],
  'email': ['Formato de e-mail inválido.']
}
```

---

#### Exemplo 2 – Validação dinâmica em tempo de execução

Você pode até validar campos parciais:

```python
parcial = {"email": "teste@", "idade": 16}

rules = {
    "email": ["required", "email"],
    "idade": ["integer", "min:18"]
}

validate_or_fail(parcial, rules)
```

Resultado:

```python
ValidationError: {
  'email': ['Formato de e-mail inválido.'],
  'idade': ['Valor mínimo permitido é 18.']
}
```

---

#### Exemplo 3 – Usando com `try`/`except` em APIs ou testes

```python
try:
    validate_or_fail({"email": "joao@", "cpf": "123"}, {
        "email": ["required", "email"],
        "cpf": ["regex:^\\d{11}$"]
    })
except ValidationError as e:
    print("Erros:", e.errors)
```

---

### Quando isso é útil?

- Pré-validação antes de salvar no banco
- Validação de etapas intermediárias em formulários
- Conferência de arquivos CSV, JSON ou payloads externos
- Criação de endpoints tipo `POST /validar` que só analisam os dados

---

Validar sem salvar é como fazer um test-drive antes de comprar: você ganha confiança no que está recebendo — e evita levar dor de cabeça pra casa (ou pro banco de dados).

---

### 9.8. Dicas finais

- Toda validação é feita **antes** de persistir no banco
- Regras vivem no próprio model, perto dos dados
- Toda exceção é **descritiva**, nunca genérica
- Você pode customizar os tipos e mensagens, se necessário

---

Com isso, você fecha mais uma camada de robustez no seu sistema. Seu ORM agora não apenas consulta e salva dados — ele **protege** seus dados com validações claras, consistentes e automatizadas.

---

## Capítulo 10 – Protegendo e Traduzindo Campos com Elegância: fillable, guarded e aliases

Você chegou até aqui dominando inserções, consultas, validações e atualizações. Mas e se alguém tentar injetar dados indevidos no seu model? Ou se o frontend envia "nome" enquanto seu banco espera "name"? É aqui que entram os guardiões silenciosos: `fillable`, `guarded` e `aliases`.

Este capítulo mostra como essas ferramentas protegem seu modelo contra atualizações indesejadas e ainda facilitam a comunicação com interfaces externas.

---

### 10.1. O que é `fillable`?

O atributo `fillable` define uma lista **explícita** de campos que podem ser preenchidos via `.insert()`, `.create()` ou `.update()`.

É uma forma de **whitelist** — você declara o que pode entrar, o resto é ignorado.

#### Exemplo:

```python
class User(Base, CRUDMixin):
    ...
    fillable = ['name', 'email', 'password']
```

#### Uso:

```python
User.insert(name="Ana", email="ana@x.com", password="123", role="admin")
```

Se `role` **não** estiver em `fillable`, será automaticamente ignorado — mesmo que esteja presente no dicionário de entrada.

---

### 10.2. E o `guarded`?

Enquanto `fillable` diz o que pode entrar, `guarded` faz o oposto: lista campos que **não podem** ser preenchidos.

Você pode usar um ou outro (não os dois ao mesmo tempo).

#### Exemplo:

```python
class Produto(Base, CRUDMixin):
    ...
    guarded = ['id', 'criado_em']
```

Qualquer tentativa de preencher esses campos será ignorada silenciosamente.

---

### 10.3. Quando usar `fillable` vs `guarded`

| Situação                             | Recomendado |
| ------------------------------------ | ----------- |
| Poucos campos confiáveis             | `fillable`  |
| Muitos campos, poucos proibidos      | `guarded`   |
| Modelos expostos em APIs públicas    | `fillable`  |
| Modelos internos, usados só por devs | Pode omitir |

---

### 10.4. `aliases`: traduzindo campos amigavelmente

Às vezes seu model usa nomes técnicos como `name`, `created_at`, mas você quer permitir que a API ou o admin use nomes mais humanos, como `nome` ou `criadoEm`.

A propriedade `aliases` mapeia esses nomes alternativos para os reais.

#### Exemplo:

```python
class User(Base, CRUDMixin):
    ...
    aliases = {
        'nome': 'name',
        'criadoEm': 'created_at'
    }
```

#### Uso:

```python
User.insert(nome="João", email="joao@email.com", password="123")
```

Internamente, `nome` será convertido para `name`.

---

### 10.5. Aplicação combinada: tudo junto

```python
class User(Base, CRUDMixin):
    ...
    fillable = ['name', 'email', 'password']
    aliases = {'nome': 'name'}
```

Agora você pode chamar:

```python
User.insert(nome="Lia", email="lia@teste.com", password="abc", ativo=True)
```

E o campo `ativo` será ignorado (por não estar em `fillable`), e `nome` será corretamente traduzido para `name`.

---

### 10.6. Dica bônus: compatível com `.update()` também

Tudo isso funciona tanto para `.insert()` quanto `.create()` e `.update()`.

```python
usuario.update(nome="Novo Nome", email="atualizado@a.com")

# Ou

User.updateWhere({"nome":"Novo Nome", "email":"atualizado@a.com"}, ('id', 110))
```

Se os campos estiverem em `fillable` e mapeados em `aliases`, eles passam!

---

### 10.7. Por que isso importa?

- Evita sobrescritas acidentais de colunas sensíveis
- Protege o modelo contra entradas inesperadas
- Permite APIs multilíngues e painéis mais amigáveis
- Deixa o código mais claro e previsível

---

Usar `fillable`, `guarded` e `aliases` é como configurar uma porta de entrada com controle de acesso e recepcionista bilíngue. Elegante, seguro e acolhedor.

Com isso, seus models estão não apenas mais seguros — mas também mais compreensíveis por quem fala a língua dos dados… ou a língua dos usuários.

---

#### Sugestões práticas:

A estrutura atual destas classes funcionam muito bem em projetos médios. Mas, conforme o sistema cresce, é saudável planejar algumas melhorias:

Separe os domínio em módulos para facilitar a manutenção dos seus projetos (ex: `usuario/`, `produto/`, `financeiro/`)

---

Ao longo deste manual, você viu como uma estrutura bem desenhada com SQLAlchemy pode ir muito além do básico. Agora você tem em mãos não apenas uma biblioteca — mas uma base sólida, expressiva e expansível para qualquer aplicação profissional.

Mais do que saber usar, você sabe adaptar, refatorar e evoluir.

Missão cumprida.
