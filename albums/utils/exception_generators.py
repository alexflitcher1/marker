from fastapi import HTTPException, status

def generate_401():
    """ Generate 401 error """
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )

def generate_album_404():
    """ Generate 404 error """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Album doesn't exist"
    )
