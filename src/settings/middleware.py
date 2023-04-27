'''
Custom middleware file
'''
from fastapi import HTTPException, Request, status, Request
from starlette.exceptions import HTTPException
from src.schemas import settings
from fastapi.middleware.cors import CORSMiddleware





class CustomMiddleware:
    ORIGINS = [
        "*"
        ]

    def __init__(self, app) -> None:
        self.app = app

    async def verify_api_key(self, request: Request):
        api_key = request.headers.get('X-Token')
        if api_key != settings.API_TOKEN:
            raise HTTPException(
                detail="Invalid API KEY",
                status_code=status.HTTP_400_BAD_REQUEST
                )
            
    def cors_origins(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
