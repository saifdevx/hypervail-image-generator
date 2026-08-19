from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import init_database, get_database_status


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


# --------------------------------------------------
# APPLICATION LIFESPAN
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Runs when the application starts.
    init_database()

    yield

    # Later, shutdown logic can go here if needed.


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Image Agent",
    description="Custom AI product image generation agent",
    version="0.3.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(str(STATIC_DIR / "index.html"))


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# DATABASE STATUS
# --------------------------------------------------

@app.get("/api/database/status")
def database_status():
    return get_database_status()