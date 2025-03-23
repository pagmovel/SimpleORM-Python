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

name é obrigatório

email é obrigatório e deve ter formato válido

password é obrigatório

Você pode adicionar quantas regras quiser, e elas serão automaticamente aplicadas ao usar .insert(), .create() e .update().

9.3. Validação em Ação: exemplos reais
1. Inserindo um registro com dados inválidos
```
User.insert(name="", email="errado", password=None)
```
Resultado:

```
ValidationError: {
  'name': ['Este campo é obrigatório.'],
  'email': ['Formato de e-mail inválido.'],
  'password': ['Este campo é obrigatório.']
}
```
2. Atualizando com segurança
```
usuario.update(email="sem-arroba", name="  ")
Retorno esperado:

```
ValidationError: {
  'name': ['Este campo é obrigatório.'],
  'email': ['Formato de e-mail inválido.']
}
```
9.4. Regras avançadas: min, max, in, regex
Você pode usar regras mais elaboradas para validar diferentes tipos de dados:

```
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

Tamanho mínimo/máximo de strings

Intervalos de números

Conjunto de valores permitidos

Formato de campos específicos com expressões regulares

9.5. Capturando erros manualmente (útil em APIs)
Você pode capturar os erros de validação e transformá-los em mensagens amigáveis em sua aplicação:

```
from utils.validator import ValidationError

try:
    User.insert(name="Ok", email="sem-email", password="")
except ValidationError as e:
    print(e.errors)
9.6. Validação em massa com .create()
Ao usar .create(), cada item da lista será validado individualmente:

```
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

9.7. Dicas finais
Toda validação é feita antes de persistir no banco

Regras vivem no próprio model, perto dos dados

Toda exceção é descritiva, nunca genérica

Você pode customizar os tipos e mensagens, se necessário

Com isso, você fecha mais uma camada de robustez no seu sistema. Seu ORM agora não apenas consulta e salva dados — ele protege seus dados com validações claras, consistentes e automatizadas. """