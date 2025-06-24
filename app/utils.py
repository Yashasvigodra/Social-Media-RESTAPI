from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"] , deprecated="auto")#all we are doing is we are telling the passlib what is the default hashing algorithm we wanna use aad in this case we are using bcrypt

def hash(password : str):
    return pwd_context.hash(password)


#function to compare it two hashed passwords are equal
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)