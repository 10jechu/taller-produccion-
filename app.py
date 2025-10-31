from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # Ì±à ESTA L√çNEA ES CLAVE

templates = Jinja2Templates(directory="templates")

API_KEY = "de767f30ef707f25df6eccc8813335e7"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "weather": None, "error": None})

@app.post("/clima", response_class=HTMLResponse)
def get_weather(request: Request, ciudad: str = Form(...)):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    res = requests.get(url)
    data = res.json()

    if data.get("cod") != 200:
        return templates.TemplateResponse("index.html", {"request": request, "weather": None, "error": "Ciudad no encontrada"})

    clima = {
        "nombre": data["name"],
        "temp": round(data["main"]["temp"], 1),
        "desc": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"],
    }

    return templates.TemplateResponse("index.html", {"request": request, "weather": clima, "error": None})
