import os
import sys
from sqlalchemy import MetaData, Column
from models.db import engine, SCHEMA
from models.crud import CRUDMixin

def camel_case(s):
    """Converte nomes em snake_case para CamelCase (ex.: usuario_detalhe -> UsuarioDetalhe)."""
    return ''.join(word.capitalize() for word in s.split('_'))

def generate_model_file(table, output_dir='models'):
    class_name = camel_case(table.name)
    columns_lines = []
    types_used = set()

    for col in table.columns:
        col_type = type(col.type).__name__
        types_used.add(col_type)
        args = [col_type]
        if col.primary_key:
            args.append("primary_key=True")
        if col.index:
            args.append("index=True")
        if not col.nullable:
            args.append("nullable=False")
        if col.unique:
            args.append("unique=True")
        column_line = f"    {col.name} = Column({', '.join(args)})"
        columns_lines.append(column_line)

    types_import = ', '.join(sorted(types_used))
    table_args = f"    __table_args__ = {{'schema': '{SCHEMA}'}}\n\n" if SCHEMA else "\n"
    content = f"""from sqlalchemy import Column, {types_import}
from models.db import Base
from models.crud import CRUDMixin

class {class_name}(Base, CRUDMixin):
    __tablename__ = '{table.name}'
{table_args}{chr(10).join(columns_lines)}
"""

    file_path = os.path.join(output_dir, f"{table.name}.py")
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Gerado: {file_path}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python generate_models.py <prefixo>")
        sys.exit(1)
    prefix = sys.argv[1]
    
    output_dir = 'models'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Usando schema: {SCHEMA}")

    metadata = MetaData()
    metadata.reflect(bind=engine, schema=SCHEMA)
    print("Tabelas encontradas no banco de dados:")
    for table in metadata.tables.values():
        print(f" - {table.name}")
        if table.name.startswith(prefix):
            generate_model_file(table, output_dir)

if __name__ == '__main__':
    main()
