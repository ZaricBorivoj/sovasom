import secrets
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text

from office.accounts.routes import CSRF_COOKIE, router
from office.config import Settings
from office.database import session_factory


def create_app(settings: Settings | None = None, clock=None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.state.sessions = session_factory(settings.database_url)
    app.state.now = clock or (lambda: datetime.now(UTC))

    @app.middleware("http")
    async def protect_requests(request: Request, call_next):
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            token = request.headers.get("x-csrf-token", "")
            valid = (
                request.headers.get("origin") == settings.public_origin
                and bool(token)
                and secrets.compare_digest(token, request.cookies.get(CSRF_COOKIE, ""))
            )
            if not valid:
                return JSONResponse({"detail": "Refresh the page and try again."}, status_code=403)
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(RequestValidationError)
    async def invalid_input(request, exc):
        return JSONResponse({"detail": "Check the supplied values."}, status_code=422)

    @app.get("/api/health")
    def health():
        with app.state.sessions() as db:
            db.execute(text("SELECT 1"))
        return {"status": "ok"}

    app.include_router(router)
    return app
