from fastapi import FastAPI

app = FastAPI(
    title="Image Agent",
    description="Custom AI product image generation agent",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Image Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
