from fastapi import HTTPException, status

def generate_401():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": "Invalid token", "code": 1}
    )

def generate_mail_400():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "User with this email already exists", "code": 3}
    )

def generate_login_400():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "User with this login already exists", "code": 3}
    )

def generate_code_400():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "Mail code is not valid", "code": 6}
    )

def generate_token_400():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "Login or password is not valid", "code": 7}
    )