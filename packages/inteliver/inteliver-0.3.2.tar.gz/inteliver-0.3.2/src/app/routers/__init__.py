""" Routers Module.

    This module is responsible for registering different API routes.

"""

from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.config import settings
from app.image.router import router as image_router
from app.storage.router import router as storage_router
from app.users.router import router as users_router
from app.utils.i18n import _
from app.versioning.router import router as version_router


def register_routers(app: FastAPI):
    app.include_router(image_router, prefix=f"{settings.api_prefix}/image")

    app.include_router(storage_router, prefix=f"{settings.api_prefix}/storage")

    app.include_router(auth_router, prefix=f"{settings.api_prefix}/auth")

    app.include_router(users_router, prefix=f"{settings.api_prefix}/users")

    app.include_router(
        version_router, prefix=f"{settings.api_prefix}/inteliver-api", tags=["version"]
    )

    # Root endpoint
    @app.get("/")
    async def root():
        return {"message": _("API is up and ok.")}
