from fastapi import HTTPException, status

def generate_401():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )

def generate_artist_404():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Artist doesn't exist"
    )
