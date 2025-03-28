from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.infrastructure import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
# from app.api.v1 import users, payments, wallets
# app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
# app.include_router(payments.router, prefix=settings.API_V1_STR, tags=["payments"])
# app.include_router(wallets.router, prefix=settings.API_V1_STR, tags=["wallets"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Payment Gateway API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 