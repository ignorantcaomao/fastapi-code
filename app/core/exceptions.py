from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from loguru import logger

class NotFoundException(HTTPException):
  def __init__(self, detail: str = "Resource Not Found"):
    super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class AlreadyExistsException(HTTPException):
  def __init__(self, detail: str = "Resource Already Exists"):
    super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UnauthorizedException(HTTPException):
  def __init__(self, detail: str = "Unauthorized access"):
    super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
  def __init__(self, detail: str = "Access Forbidden"):
    super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
  logger.exception(f"unhandled exception at {request.url.path}: {exc}")
  return JSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={"detail": "Internal Server Error"},
  )