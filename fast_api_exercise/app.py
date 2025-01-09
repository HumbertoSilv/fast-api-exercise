from contextlib import asynccontextmanager

from fastapi import FastAPI

from fast_api_exercise.routers import auth, todos, users
from fast_api_exercise.settings import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting application')
    yield  # Executa a aplicação
    logger.info('Stopping application')


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)
