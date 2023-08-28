import uvicorn
import os

from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from core.db import (
    init,
    redis_cache_client,
    redis_chat_client,
    redis_general,
    redis_session_client,
    redis_throttle_client,
)
from api import router
import sentry_sdk


sentry_sdk.init(
    dsn="https://527e3a8500ad33d6e62969821b9b9fa9@o4505557691858944.ingest.sentry.io/4505739463360512",
    traces_sample_rate=1.0,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    #openapi_url=f"{settings.API_V1_STR}/openapi.json",
   # docs_url=None,
)

templates = Jinja2Templates(directory="templates")

# Your other app code remains the same

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render the index.html template
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
async def startup():
    await redis_cache_client.initialize()
    await redis_chat_client.initialize()
    await redis_throttle_client.initialize()
    await redis_session_client.initialize()
    await redis_general.initialize()
    init.init_db()


@app.on_event("shutdown")
async def shutdown():
    await redis_cache_client.close()
    await redis_chat_client.close()
    await redis_throttle_client.close()
    await redis_session_client.close()
    await redis_general.close()


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Documentaion",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"{settings.STATIC_URL_BASE}/static/swagger-ui-bundle.js",
        swagger_css_url=f"{settings.STATIC_URL_BASE}/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    pass

app.include_router(router, prefix=settings.API_V1_STR)


def run():
    reload_blacklist = ["tests", ".pytest_cache"]
    reload_dirs = os.listdir()

    for dir in reload_blacklist:
        try:
            reload_dirs.remove(dir)
        except:
            pass

    uvicorn.run(
        "app:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEV_MODE,
        reload_dirs=reload_dirs,
        debug=settings.DEV_MODE,
        workers=4,
    )


if __name__ == "__main__":
    run()

    