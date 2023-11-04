from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import csv
import json  

app = FastAPI()
# validacón con pydantic
class Contacto(BaseModel):
    id_contacto: int
    nombre: str
    primer_apellido: str 
    segundo_apellido: str
    email: str
    telefono: str


# metodo GET para contactos
@app.get(
    "/contactos",
    status_code=status.HTTP_200_OK,
    summary="Endpoint GET"    
)
async def root():
    """
    # Endpoint del método GET contactos
    ## 1- Status codes:
    * 200- EXITO
    """
    with open("contactos.csv", "r") as file:
        contactos = list(csv.DictReader(file))

    json_data = json.dumps(contactos)
    
    with open("contactos.json", "w") as json_file:
        json_file.write(json_data)
 
    response = json_data
    return response

# metodo POST para contactos 
@app.post("/contactos", 
        status_code=status.HTTP_201_CREATED,
        summary="Endpoint POST")
async def insertar_contacto(contacto: Contacto):
    """
    # Endpoint del método }POST contactos
    ## 1- Status codes:
    * 201- CREADO
    """
    with open("contactos.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([contacto.id_contacto, contacto.nombre, 
        contacto.primer_apellido, contacto.segundo_apellido, 
        contacto.email, contacto.telefono])
    return contacto

@app.put("/contactos/{id_contacto}", response_model=Contacto, 
         status_code=status.HTTP_202_ACCEPTED,
        summary="Endpoint PUT")
async def update_contacto(id_contacto: int, contacto: Contacto):
    """
    # Endpoint del método PUT contactos
    ## 1- Status codes:
    * 202- ACCEPTED
    """
    contactos = []
    with open('contactos.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contactos.append(row)
    id_contacto -= 1
    contactos[id_contacto]['nombre'] = contacto.nombre
    contactos[id_contacto]['primer_apellido'] = contacto.primer_apellido
    contactos[id_contacto]['segundo_apellido'] = contacto.segundo_apellido
    contactos[id_contacto]['email'] = contacto.email
    contactos[id_contacto]['telefono'] = contacto.telefono

    with open("contactos.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id_contacto', 'nombre', 'primer_apellido','segundo_apellido','email','telefono'])
        writer.writeheader()
        writer.writerows(contactos)
    
    return contacto

# busqueda por nombre
@app.get("/contacto/{nombre}", status_code=status.HTTP_200_OK,
        summary="Endpoint GET")
async def get_contacto(nombre: str):
    """
    # Endpoint del método GET contactos para buscar contactos 
    ## 1- Status codes:
    * 200- OK
    """
    with open('contactos.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['nombre']) == nombre:
                return row
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    
@app.delete("/contactos/{id_contacto}", status_code=status.HTTP_200_OK,
        summary="Endpoint DELETE")
async def delete_contacto(id_contacto: int):
    """
    # Endpoint del método DELETE contactos para buscar contactos 
    ## 1- Status codes:
    * 200- OK
    """
    with open('contactos.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if int(row['id_contacto']) == id_contacto:
                rows.remove(row)
                with open('contactos.csv', 'w', newline='') as file:
                    fieldnames = ['id_contacto', 'nombre', 'primer_apellido', 'segundo_apellido', 'email', 'telefono']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                    return {"message": "Contacto eliminado "}

    raise HTTPException(status_code=404, detail="Contacto no encontrado")