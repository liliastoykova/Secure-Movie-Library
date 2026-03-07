from routers.movie_router import movie_router
from fastapi import FastAPI
from routers.auth_router import auth_router

app = FastAPI()
app.include_router(movie_router)
app.include_router(auth_router)
