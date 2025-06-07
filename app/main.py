from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.tournament import router as tournament_router

app = FastAPI(
    title="Tournament System",
    description="A mini tournament system for player registration",
    version="0.1.0",
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity error occurred"},
    )


# Include routers
app.include_router(tournament_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Tournament System API"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
