from sqlalchemy.orm import Session
from backend.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


def register_user(db: Session, username: str, email: str, password: str):
    existing = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing:
        return None

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(db, email, password):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if password != user.password:
        return None

    return user