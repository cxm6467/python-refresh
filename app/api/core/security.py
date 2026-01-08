from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from app.utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/store-managers/token")

class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> str:
        auth_credentials = await super().__call__(request)
        access_token = auth_credentials.credentials.split(" ")[1]

        decoded_token = decode_access_token(access_token)
        if decoded_token is None:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")
        return decoded_token


