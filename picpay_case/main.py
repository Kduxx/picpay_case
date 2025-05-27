from fastapi import FastAPI
from picpay_case.api.endpoints import users

app = FastAPI(
    title="Picpay Case - User CRUD API",
    description="Simple user CRUD api with FasAPI and SQLAlchemy",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
            "message": "Welcome to the User CRUD API",
            "docs": "/docs",
            "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/ping")
def ping_pong():
    return {"message": "pong"}


# Add user router
app.include_router(users.router)


def start():
    import uvicorn
    uvicorn.run("picpay_case.main:app", host="0.0.0.0", port=8000, reload=True)
