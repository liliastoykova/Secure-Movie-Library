from routers.movie_router import movie_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(movie_router)

