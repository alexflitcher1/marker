from fastapi import HTTPException, status


def generate_401():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )


def generate_404():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Playlist doesn't exist"
    )


def generate_500():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error. Try again later"
    )
