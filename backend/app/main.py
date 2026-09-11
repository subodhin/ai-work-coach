from fastapi import FastAPI

app = FastAPI(title="AI Work Coach")


@app.get("/health")
def health():
    return {"status": "ok"}