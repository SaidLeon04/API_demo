from PIL import Image 
from PIL import ImageEnhance

im = Image.open("imagen.jpg") # carga la imagen
im.show() # abre la imagen 
print(im.format, im.size, im.mode) # imprime info de la imagen 

# recorta la imagen con valores de una tupla
box = (0, 0, 400, 400)
region = im.crop(box)
region.save("recorte.jpg")

# invierte los colores de la imagen
r, g, b = region.split()
region = Image.merge("RGB", (b, g, r))
region.save("cambio.jpg")

# gira la imagen 45 grados
out = region.rotate(45)
out.save("giro.jpg") 