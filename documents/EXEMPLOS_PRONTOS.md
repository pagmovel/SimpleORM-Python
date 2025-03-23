# Exemplos Prontos de Uso - ORM com SQLAlchemy e QueryChain

Este documento fornece blocos de código prontos para copiar e colar. Eles estão organizados por tipo de operação e acompanham breves descrições para facilitar o uso imediato.

## 1. Inserção de Dados

### Inserir um único registro
```python
from models.usuario import Usuario

novo_usuario = Usuario.insert(
    nome="João da Silva",
    email="joao@exemplo.com",
    perfil="editor",
    ativo=True
)
```

### Inserir múltiplos registros de uma vez
```python
usuarios = [
    {"nome": "Ana", "email": "ana@teste.com"},
    {"nome": "Carlos", "email": "carlos@teste.com"}
]
Usuario.create(usuarios)
```

---

## 2. Consulta Simples

### Buscar todos os registros ativos
```python
usuarios = Usuario.all().isTrue("ativo").toDict()
```

### Buscar com filtro por campo específico
```python
usuario = Usuario.get(where=("email", "joao@exemplo.com"))
```

### Buscar apenas algumas colunas
```python
usuarios = Usuario.all().select("id", "nome").toDict()
```

---

## 3. Filtros Avançados

### Filtros encadeados com operadores
```python
usuarios = Usuario.all()\
    .where("idade", ">=", 18)\
    .where("perfil", "editor")\
    .notEmpty("email")\
    .orderBy("nome")\
    .toDict()
```

### Filtro por lista de valores
```python
Usuario.all().whereIn("id", [1, 2, 3]).toDict()
```

---

## 4. Join entre Tabelas

```python
from models.empresa import Empresa

usuarios = Usuario.all()\
    .join(Empresa, Usuario.empresa_id == Empresa.id)\
    .select(
        Usuario.id,
        Usuario.nome,
        Empresa.nome.label("empresa")
    )\
    .orderBy("usuario.id")\
    .toDict()
```

---

## 5. Atualização e Exclusão

### Atualizar um registro
```python
usuario = Usuario.get(where=("email", "ana@teste.com"))
if usuario:
    usuario.update(nome="Ana Maria")
```

### Deletar um registro
```python
usuario = Usuario.get(where=("id", 5))
if usuario:
    usuario.delete()
```

---

## 6. SQL Direto (rawSql)

### Consultar usando SQL puro
```python
sql = "SELECT id, nome FROM usuarios WHERE ativo = true"
usuarios = Usuario.rawSql(sql)
for row in usuarios:
    print(row)
```

### SQL com parâmetros nomeados
```python
sql = "SELECT * FROM usuarios WHERE nome LIKE :nome"
params = {"nome": "%silva%"}
usuarios = Usuario.rawSql(sql, params)
```

---

## 7. Paginação e Ordenação Dinâmica

```python
page = 2
limit = 20
usuarios = Usuario.all()\
    .orderBy("nome", "asc")\
    .offset((page - 1) * limit)\
    .limit(limit)\
    .toDict()
```

---

## 8. Relatórios com Agrupamento

```python
from sqlalchemy import func

resumo = Usuario.all()\
    .select(Usuario.perfil, func.count(Usuario.id).label("total"))\
    .groupBy(Usuario.perfil)\
    .orderBy("total", "desc")\
    .toDict()
```

---

Estes blocos cobrem os usos mais comuns da arquitetura ORM apresentada no `MANUAL.md`. Sinta-se à vontade para adaptar conforme as regras do seu domínio.

