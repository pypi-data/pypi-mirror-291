"""
Necessary middlewares for the app.
"""
from jose import jwt
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth_vpetrov import User as UserModel
from user_vpetrov.schemas import User, Admin
from . import exceptions
from .config import get_auth_config



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8001/create/user")


def require_admin_user(token: Annotated[str, Depends(oauth2_scheme)],):
    """
    Middleware to require an admin user.
    """
    # Request user from auth app.
    print(token)
    # Mock
    admin = {
        "id": 1,
        "is_admin": True,
        "name": "Admin User",
        "email": "admin@domain.com"
    }
    if not admin:
        raise exceptions.AuthorizationException()
    return Admin(**admin)


def require_user(token: Annotated[str, Depends(oauth2_scheme)],
                 db: Session = Depends(get_auth_config().get_db)):
    """
    Middleware to require a user.
    """
    # Request user from auth app.
    print(token)
    # Mock
    # user = {
    #     "id": 1,
    #     "name": "Name",
    #     "last_name": "Last Name",
    #     "email": "email@domain.com",
    #     "password": "passwordM@12",
    #     "gender": "F",
    #     "phone": "+56 9 1234 5678",
    #     "rut": "11.111.111-1",
    #     "birth_date": "1990-01-01"
    # }
      # Decodificar el token JWT
    try:
        data = jwt.decode(
            token, get_auth_config().secret_key, algorithms=["HS256"])
        print(data)
        user_id = data.get("id")
        if user_id is None:
            raise exceptions.AuthorizationException()
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthorizationException("Token has expired")
    except jwt.InvalidTokenError:
        raise exceptions.AuthorizationException("Invalid token")

    # Realizar consulta a la base de datos para obtener el usuario
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise exceptions.AuthorizationException("User not found")

    # Convertir el modelo SQLAlchemy a Pydantic
    return User(**user)
    # if not user:
    #     raise exceptions.AuthorizationException()
    # return User(**user)
