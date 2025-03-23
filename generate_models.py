# generate_models.py

import os
import sys
from sqlalchemy import MetaData, Column, ForeignKey
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

    - Se a coluna for PK (col.primary_key=True), gera primary_key=True
    - Adiciona index=True, unique=True, etc., conforme flags da coluna
    - Inclui ForeignKey('schema.outra_tabela.outra_coluna') se houver FKs
    - Usa import relativo: from .db import Base, from .crud import CRUDMixin
    - Salva o arquivo em /models/<nome_tabela>.py
    """

    class_name = camel_case(table.name)
    columns_lines = []
    need_foreignkey_import = False  # Para saber se precisaremos de 'ForeignKey' no import

    # Percorre colunas refletidas
    for col in table.columns:
        # Se a coluna for 'imagem', usamos LargeBinary para armazenar BLOB
        if col.name == 'imagem':
            col_type = 'LargeBinary'
        else:
            col_type = type(col.type).__name__
        params = [col_type]

        # Se tiver ForeignKey, pegamos a primeira (caso haja várias, adaptar se precisar)
        if col.foreign_keys:
            fk = list(col.foreign_keys)[0]
            # Geralmente virá algo como 'bancos.outra_tabela.outra_coluna'
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

        column_line = f"    {col.name} = Column({', '.join(params)})"
        columns_lines.append(column_line)

    # Se tiver schema definido no config.json, define __table_args__
    table_args = f"    __table_args__ = {{'schema': '{schema}'}}\n\n" if schema else "\n"

    # Coletamos os tipos de colunas usados (String, Integer etc.) para o import
    used_types = {('LargeBinary' if col.name == 'imagem' else type(col.type).__name__) for col in table.columns}
    base_types_import = ', '.join(sorted(used_types))

    # Se houve alguma FK, garantimos que 'ForeignKey' esteja presente no import
    if need_foreignkey_import and 'ForeignKey' not in base_types_import:
        base_types_import += ', ForeignKey'

    # -------------------------------------------------------------------------
    # NOVO: Geração de atributos fillable e método rules()
    # fillable => define campos permitidos para insert/update
    # rules()  => regras de validação automáticas estilo Laravel
    # -------------------------------------------------------------------------

    fillable = [col.name for col in table.columns if not col.primary_key]
    rules_lines = []
    for col in table.columns:
        if col.primary_key:
            continue
        field_rules = []
        if not col.nullable:
            field_rules.append("required")
        col_type = type(col.type).__name__.lower()
        if col_type in ["string", "text"]:
            field_rules.append("string")
        elif col_type in ["integer"]:
            field_rules.append("integer")
        elif col_type in ["boolean"]:
            field_rules.append("boolean")
        elif col_type in ["float", "numeric"]:
            field_rules.append("float")
        elif col_type in ["datetime"]:
            field_rules.append("datetime")
        if field_rules:
            rules_lines.append(f"            '{col.name}': {field_rules},")

    rules_method = f"""    fillable = {fillable}

    @classmethod
    def rules(cls):
        return {{
{chr(10).join(rules_lines)}
        }}
"""

    # Monta o conteúdo do arquivo gerado
    content = f'''from sqlalchemy import Column, {base_types_import}
from .db import Base
from .crud import CRUDMixin

class {class_name}(Base, CRUDMixin):
    __tablename__ = '{table.name}'
{table_args}{chr(10).join(columns_lines)}

{rules_method}
'''

    # Cria a pasta "models" se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Gera o arquivo models/<nome_da_tabela>.py
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

    # Lê engine / schema a partir do config.json
    engine = get_engine()
    schema = get_schema()

    metadata = MetaData()
    # Reflete as tabelas do banco, usando o schema configurado
    metadata.reflect(bind=engine, schema=schema)

    print(f"Tabelas encontradas no schema='{schema}':")
    for tbl_name in metadata.tables:
        print(" -", tbl_name)

    print("\\nGerando modelos...\\n")
    for table in metadata.tables.values():
        if table.name.startswith(prefix):
            generate_model_file(table, schema, output_dir='models')

if __name__ == '__main__':
    main()
