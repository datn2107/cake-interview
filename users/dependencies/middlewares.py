from logging import Logger
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: Logger) -> None:
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request, call_next):
        log_infor = {
            "url": request.url,
            "method": request.method,
            "body": await request.body(),
        }
        self.logger.info(log_infor)

        try:
            response = await call_next(request)
        except Exception as e:
            self.logger.error(log_infor, exc_info=e)
            raise HTTPException(status_code=500, detail="Internal server error")

        return response
