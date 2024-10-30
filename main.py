import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from maps_client import MapsClient, GOOGLE_MAPS_API_KEY
from data import CITY_LOOKUP

app = FastAPI(title='FleetCommander Maps API',
              description='<img alt="Fleet Commander Logo" src="/static/fc_logo.jpeg" /><h1>API for MarketDial FleetCommander™ services</h1>')


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

MAPS_CLIENT = None

@app.get("/", response_class=HTMLResponse)
async def upload_csv(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/competitors", response_class=HTMLResponse)
async def show_competitors(request: Request, name: str, city: str, keywords: str, cats: str):
    global MAPS_CLIENT

    types = eval(f"[{cats.replace('\r\n', ',')}]")

    if not MAPS_CLIENT:
        MAPS_CLIENT = MapsClient()

    location = CITY_LOOKUP.get(city.strip())
    if not location:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sorry, I don't know this city (largest 1000 US cities only): " + city)

    parts = location.split(',')
    lat = float(parts[0])
    lng = float(parts[1])

    results, store_ids, comp_ids = MAPS_CLIENT.find_nearby_competitors(name, location, keywords, *types)

    return templates.TemplateResponse(request, "competitors.html",
        {'name': name, 'city': city, 'keywords': keywords, 'types': types,
            'results': results, 'API_KEY': GOOGLE_MAPS_API_KEY, 'store_ids': store_ids,
            'comp_ids': comp_ids, 'latlong': { 'lat': lat, 'lng': lng }})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9898, reload=True, )