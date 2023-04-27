from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from src.schemas import settings
from src.settings import CustomMiddleware
from src.routers import mem
from src.db import init_db
from src.utils import system_usage_scheduler


def create_app() -> FastAPI:
    """
    Create app instance
    """
    current_app = FastAPI(
        title='System Usage',
        version='0.0.1',
        description='System Usage manager',
        debug=True)
    return current_app


app = create_app()

middleware = CustomMiddleware(app=app)

# hook by using request and response


@app.middleware('http')
async def check_header_middleware(request: Request, call_next):
    """

    Middleware function that checks the API key in the request header for requests that start with '/v1'.
    If the API key is valid, the request is passed to the main application.
    If the API key is invalid, an HTTPException is raised with a 400 Bad Request status code.
    If the request does not start with '/v1', the middleware is skipped.

    Parameters:
    request (fastapi.Request): Incoming HTTP request.
    call_next (Callable[[Request], Awaitable[Response]]): A callable that passes the request\
        to the next middleware or the main application.

    Returns:
        fastapi.Response: The HTTP response returned by the next middleware or the main application.

    Raises:
        HTTPException: If the API key is invalid, an HTTPException is raised with a 400 Bad Request status code.

    """
    try:
        if request.url.path.startswith("/v1"):
            # verification api_key from headers and apply middleware
            await middleware.verify_api_key(request)
            response = await call_next(request)
            return response
        else:
            # do not apply middleware
            response = await call_next(request)
        return response
    except HTTPException as exc:
        return JSONResponse(content={"detail": str(exc.detail)}, status_code=exc.status_code)


# including routers
app.include_router(router=mem, prefix='/v1')

# startup event working while service start running
@app.on_event('startup')
async def start_up_service():
    init_db()  # initializing database
    if settings.LOCAL_EXECUTOR:
        system_usage_scheduler()  # while we want using none specific scheduler

# shutdown event working while service stopped or terminated
@app.on_event('shutdown')
async def start_up_service():
    if settings.LOCAL_EXECUTOR:
        system_usage_scheduler(0)  # cancel threading which started by timer


if __name__ == "__main__":
    import uvicorn as uv
    uv.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        limit_concurrency=500,
        limit_max_requests=1000,
        # workers=8,
        proxy_headers=True
        )
