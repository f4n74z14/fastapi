from fastapi import HTTPException, status

USER_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден.")

