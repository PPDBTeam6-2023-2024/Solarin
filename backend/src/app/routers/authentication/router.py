from fastapi import APIRouter, Depends, HTTPException, status, Query
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy import select
import sqlalchemy.exc
from typing import Union, Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .schemas import UserCreate, Token
from ...database.database import get_db, AsyncSession
from ...database.models.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


@router.post("/add_user")
async def add_user(user: UserCreate, db=Depends(get_db)):
    try:
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=pwd_context.hash(user.password)
        )
        db.add(db_user)
        await db.commit()
        return {
            "username": user.username,
            "email": user.email
        }
    except sqlalchemy.exc.IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=404, detail="Email or username already taken")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add user")


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Union[User, None]:
    user = await session.execute(select(User).where(User.username == username))
    user = user.first()
    if not user:
        return None
    user = user[0]
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return Token(access_token=access_token, token_type="bearer")


def get_my_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id


@router.get("/validate")
def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    success = True
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        success = False
    return {
        "success": success
    }

@router.get("/me")
async def me(user_id: Annotated[int, Depends(get_my_id)], db=Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    scalar = result.scalars().all()[0]
    return {"username": scalar.username, "id": scalar.id, "email": scalar.email, "alliance": scalar.alliance}
