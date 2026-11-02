import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.limits import limiter
from app.routes import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
app = FastAPI(title="CyberLearn API", version="0.1.0", docs_url="/docs" if settings.environment != "production" else None,
              redoc_url=None, openapi_url="/openapi.json" if settings.environment != "production" else None)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True,
                   allow_methods=["GET", "POST", "PATCH", "DELETE"], allow_headers=["Authorization", "Content-Type"])


class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"x-content-type-options", b"nosniff"),
                    (b"x-frame-options", b"DENY"),
                    (b"referrer-policy", b"strict-origin-when-cross-origin"),
                    (b"content-security-policy", b"default-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; img-src 'self' data:; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net"),
                ])
                message["headers"] = headers
            await send(message)
        await self.app(scope, receive, send_with_headers)


app.add_middleware(SecurityHeadersMiddleware)
if settings.environment == "production":
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router)
