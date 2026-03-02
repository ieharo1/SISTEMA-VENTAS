from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.database import connect_to_mongodb, close_mongodb_connection
from app.routes import auth, sales


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="Sistema de Ventas - FastAPI",
    description="A comprehensive sales management system with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(sales.router)

templates = Jinja2Templates(directory="app/templates")
