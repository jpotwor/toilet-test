from fastapi import FastAPI

app = FastAPI(title="Toilet Test")


@app.get("/")
def root():
    return {"message": "Hello from Toilet Test!"}


@app.get("/health")
def health():
    return {"status": "ok"}