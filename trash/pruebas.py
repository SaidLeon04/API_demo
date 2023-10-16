from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv

app = FastAPI()

# Modelo Pydantic para datos de entrada
class Item(BaseModel):
    nombre: str
    edad: int

# Rutas para operaciones CRUD

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    with open("data.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item.nombre, item.edad])
    return item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    with open("data.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['id']) == item_id:
                return row
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100):
    items = []
    with open("data.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    return items[skip:skip + limit]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    items = []
    with open("data.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    items[item_id]['nombre'] = item.nombre
    items[item_id]['edad'] = item.edad
    
    with open("data.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'nombre', 'edad'])
        writer.writeheader()
        writer.writerows(items)
    
    return item

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    items = []
    with open("data.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items.pop(item_id)
    
    with open("data.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'nombre', 'edad'])
        writer.writeheader()
        writer.writerows(items)
    
    return deleted_item

