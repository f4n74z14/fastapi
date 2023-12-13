from fastapi import responses

USER_DELETED_SUCCESSFULLY = responses.JSONResponse(content={"message": "Пользователь успешно удален."})
UNKNOWN_API_RESPONSE = responses.JSONResponse(content={"message": "Пожалуйста, используйте API для доступа к данным, "
                                                                  "документация по ссылке /redoc"})
