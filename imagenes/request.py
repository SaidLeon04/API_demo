import requests

URI = "http://localhost:8000/"

response = requests.get(URI)
print(f"GET: {response.text}")
print(f"GET: {response.status_code}")

data = {"nombre":"Prueba", "correo":"prueba@gmail.com"}
response = requests.post(URI, json=data)
print(f"POST: {response.text}")
print(f"POST: {response.status_code}")