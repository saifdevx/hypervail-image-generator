from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


app = FastAPI(
    title="Image Agent",
    description="Custom AI product image generation agent",
    version="0.2.0",
)


app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }