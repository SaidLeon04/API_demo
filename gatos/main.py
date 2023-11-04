from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/gatos/{parametro}")
async def get_gato(parametro: str):
    numero = random.randint(1, 5)
    ruta = f"127.0.0.1:8000/static/images/{parametro}/{numero}.jpg"
    return ruta