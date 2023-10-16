from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    app.mount("/static/", StaticFiles(directory="static"), name="static")
    with open(file.filename, 'wb') as image:
        content = await file.read()
        image.write(content)
        image.close()
        return {f"filename": "/static/images/{file.filename}", "tipo": {file.content_type}}