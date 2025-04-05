# from models.usuario import Usuario
from utils.validator import ValidationError
from sqlalchemy import text
from .models.users import User



try:
    novo_usuario = User.insert(
        nome="João F. Roberto da Silva II",
        email="joaofroberto2@exemplo.com",
    )

    print(novo_usuario.to_dict())
except ValidationError as e:
    print("[VALIDAÇÃO]", e.errors)