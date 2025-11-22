from boats_routes import router as boats_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models
from auth_routes import router as auth_router

# Create tables (runs at startup; fine for early stages)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeSkipper Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SafeSkipper backend running successfully"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Auth routes (mobile login)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(boats_router, prefix="/boats", tags=["boats"])
from auth_routes import router as auth_router
from boats_routes import router as boats_router

# ... Base.metadata.create_all and app definition ...

@app.get("/")
def root():
    return {"message": "SafeSkipper backend running successfully"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(boats_router, prefix="/boats", tags=["boats"])
