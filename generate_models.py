# generate_models.py

import os
import sys
import re
<<<<<<< HEAD
from sqlalchemy import MetaData, Column, ForeignKey, text
=======
from sqlalchemy import MetaData, Column, ForeignKey
>>>>>>> 77bba562c619e00c66c854c39d39e3f8affae1de
from models.db import get_engine, get_schema
from models.crud import CRUDMixin


def camel_case(s: str) -> str:
    """
    Converte snake_case em CamelCase (ex.: usuario_detalhe -> UsuarioDetalhe).
    """
    return ''.join(word.capitalize() for word in s.split('_'))


def generate_model_file(table, schema, output_dir='models'):
    """
    Gera um arquivo .py com o modelo SQLAlchemy para a tabela informada.
<<<<<<< HEAD

=======
    
>>>>>>> 77bba562c619e00c66c854c39d39e3f8affae1de
    - Se a coluna for PK, gera primary_key=True.
    - Adiciona index, unique, etc., conforme flags da coluna.
    - Insere ForeignKey se houver.
    - Usa import relativo: from .db import Base e from .crud import CRUDMixin.
    - Se a coluna possuir default definido no banco (server_default),
      insere-o no modelo, substituindo chamadas nextval() para usar a variável SCHEMA.
    - Se houver schema, cria uma variável SCHEMA no início do arquivo e
      usa-a em __table_args__.
    """

    class_name = camel_case(table.name)
    columns_lines = []
    need_foreignkey_import = False  # Indica se é necessário importar ForeignKey
    need_expression_import = False  # Indica se é necessário importar expression (ex.: para boolean)
<<<<<<< HEAD
    needs_text_import = False       # Indica se é necessário importar text() para server_default numérico
    need_array_import = False       # Indica se é necessário importar ARRAY do PostgreSQL
=======
>>>>>>> 77bba562c619e00c66c854c39d39e3f8affae1de

    # Percorre as colunas refletidas
    for col in table.columns:
        # Tratamento especial para coluna 'imagem'
        if col.name == 'imagem':
            col_type = 'LargeBinary'
        # Se o tipo da coluna for ARRAY, ajusta para ARRAY(<tipo_interno>)
        elif type(col.type).__name__ == "ARRAY":
            # Obtém o tipo dos itens armazenados no ARRAY
            inner_type = type(col.type.item_type).__name__
            col_type = f"ARRAY({inner_type})"
            need_array_import = True
        else:
            col_type = type(col.type).__name__
        params = [col_type]

        # Se houver ForeignKey, pega a primeira (ajuste se necessário)
        if col.foreign_keys:
            fk = list(col.foreign_keys)[0]
            params.append(f"ForeignKey('{fk.target_fullname}')")
            need_foreignkey_import = True

        if col.primary_key:
            params.append("primary_key=True")
        if col.index:
            params.append("index=True")
        if not col.nullable:
            params.append("nullable=False")
        if col.unique:
            params.append("unique=True")

        # Se houver server_default, insere no modelo
        if col.server_default is not None:
            if col_type.lower() in ["boolean"]:
                params.append("default=False")
                params.append("server_default=expression.false()")
                need_expression_import = True
            else:
                default_val = None
                if col.server_default.arg is not None and hasattr(col.server_default.arg, "text"):
                    default_val = col.server_default.arg.text
                if default_val is not None:
                    # Se for uma chamada nextval(), substitui o schema fixo pela variável SCHEMA
                    if default_val.startswith("nextval("):
                        default_val = re.sub(r"nextval\('([^\.]+)", "nextval('{SCHEMA}", default_val)
                        params.append(f"server_default=f{repr(default_val)}")
                    else:
                        if default_val.isdigit():
<<<<<<< HEAD
                            params.append(f"server_default=text('{default_val}')")
                            needs_text_import = True
=======
                            params.append(f"server_default={default_val}")
>>>>>>> 77bba562c619e00c66c854c39d39e3f8affae1de
                        else:
                            params.append(f"server_default={repr(default_val)}")

        column_line = f"    {col.name} = Column({', '.join(params)})"
        columns_lines.append(column_line)

    # Define __table_args__ utilizando a variável SCHEMA se schema estiver definido
    table_args = f"    __table_args__ = {{'schema': SCHEMA}}\n\n" if schema else "\n"

    # Coleta os tipos de colunas usados para o import
    used_types = {('LargeBinary' if col.name == 'imagem' else type(col.type).__name__) for col in table.columns}
    # Se houver colunas ARRAY, já incluímos "ARRAY" nelas; mas queremos importá-lo do dialeto
    if need_array_import:
        used_types.discard("ARRAY")
    base_types_import = ', '.join(sorted(used_types))
    if need_foreignkey_import and 'ForeignKey' not in base_types_import:
        base_types_import += ', ForeignKey'

<<<<<<< HEAD
    # Monta o cabeçalho com os imports, utilizando imports absolutos para os módulos do projeto.
    header_lines = [f"from sqlalchemy import Column, {base_types_import}"]
    if need_array_import:
        header_lines.append("from sqlalchemy.dialects.postgresql import ARRAY")
    if need_expression_import:
        header_lines.append("from sqlalchemy.sql import expression")
    if needs_text_import:
        header_lines.append("from sqlalchemy import text")
    header_lines.extend([
        "from models.db import Base",
        "from models.crud import CRUDMixin",
        "from models.utils.validator import validate_or_fail",
=======
    # Monta o cabeçalho com os imports
    header_lines = [f"from sqlalchemy import Column, {base_types_import}"]
    if need_expression_import:
        header_lines.append("from sqlalchemy.sql import expression")
    header_lines.extend([
        "from .db import Base",
        "from .crud import CRUDMixin",
>>>>>>> 77bba562c619e00c66c854c39d39e3f8affae1de
        ""
    ])
    header = "\n".join(header_lines)

    # Se houver schema, define a variável SCHEMA no início do arquivo
    schema_variable = f"SCHEMA = {repr(schema)}\n\n" if schema else ""

    # Geração dos atributos fillable e do método rules()
    fillable = [col.name for col in table.columns if not col.primary_key]
    rules_lines = []
    for col in table.columns:
        if col.primary_key:
            continue
        field_rules = []
<<<<<<< HEAD
        # Não adiciona a regra "required" se o nome da coluna for created_at, updated_at ou deleted_at
        if col.name not in ["created_at", "updated_at", "deleted_at"]:
            if not col.nullable:
                field_rules.append("required")
=======
        if not col.nullable:
            field_rules.append("required")
>>>>>>> 77bba562c619e00c66c854c39d39e3f8affae1de
        col_type_name = type(col.type).__name__.lower()
        if col_type_name in ["string", "text"]:
            field_rules.append("string")
        elif col_type_name in ["integer"]:
            field_rules.append("integer")
        elif col_type_name in ["boolean"]:
            field_rules.append("boolean")
        elif col_type_name in ["float", "numeric"]:
            field_rules.append("float")
        elif col_type_name in ["datetime"]:
            field_rules.append("datetime")
        if field_rules:
            rules_lines.append(f"            '{col.name}': {field_rules},")
<<<<<<< HEAD
=======
    
>>>>>>> 77bba562c619e00c66c854c39d39e3f8affae1de
    rules_method = f"""    fillable = {fillable}

    @classmethod
    def rules(cls):
        return {{
{chr(10).join(rules_lines)}
        }}
"""

    # Monta o conteúdo final do arquivo
    content = f'''{header}{schema_variable}class {class_name}(Base, CRUDMixin):
    __tablename__ = '{table.name}'
{table_args}{chr(10).join(columns_lines)}

{rules_method}
'''

    # Cria a pasta "models" se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f"{table.name}.py")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Gerado: {file_path}")


def main():
    """
    Uso:
      python generate_models.py <prefixo>

    Lê do config.json o ambiente (ex.: dev, prod), descobre o schema,
    reflete as tabelas e gera modelos apenas para as que começam com <prefixo>.
    """
    if len(sys.argv) < 2:
        print("Uso: python generate_models.py <prefixo>")
        sys.exit(1)

    prefix = sys.argv[1]
    engine = get_engine()
    schema = get_schema()

    metadata = MetaData()
    metadata.reflect(bind=engine, schema=schema)

    print(f"Tabelas encontradas no schema='{schema}':")
    for tbl_name in metadata.tables:
        print(" -", tbl_name)

    print("\nGerando modelos...\n")
    for table in metadata.tables.values():
        if table.name.startswith(prefix):
            generate_model_file(table, schema, output_dir='models')


if __name__ == '__main__':
    main()
    