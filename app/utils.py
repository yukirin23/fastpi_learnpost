from passlib.context import CryptContext

# setting crypto password for
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashed / generate password
def hash(password: str):
    return pwd_context.hash(password)

#verify / check password

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
