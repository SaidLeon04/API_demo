from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image 
import os
import json 

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/imagenes/")
async def upload_file(file: UploadFile, fliph: int | None = None, crop: str | None = None, colorize: bool | None = None):
    folder = "static/images"
    destino = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(destino, 'wb') as image:
        content = await file.read()
        image.write(content)

    imagen = Image.open(f"static/images/{file.filename}")
    if colorize:
        r, g, b = imagen.split()
        imagen = Image.merge("RGB", (b, g, r))
        imagen.save("static/images/cambio.jpg")
        ruta_color = "static/images/cambio.jpg"
    else:
        ruta_color = " "

    if fliph:
        out = imagen.rotate(fliph)
        out.save("static/images/giro.jpg") 
        ruta_giro = "static/images/giro.jpg"
    else:
        ruta_giro = " "

    if crop:
        tupla = eval(crop)
        box = (tupla)
        region = imagen.crop(box)
        region.save("static/images/recorte.jpg")
        ruta_corte = "static/images/recorte.jpg"
    else:
        ruta_corte = " "
    

    result = {
        "filename": f"/static/images/{file.filename}",
        "tipo": file.content_type,
        "ruta":f"127.0.0.1:8000/static/images/{file.filename}",
        "ruta_corte": f"127.0.0.1:8000/{ruta_corte}",
        "ruta_color": f"127.0.0.1:8000/{ruta_color}",
        "ruta_giro": f"127.0.0.1:8000/{ruta_giro}"

    }
    return result
