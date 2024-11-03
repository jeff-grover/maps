import html

import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from maps_client import MapsClient, GOOGLE_MAPS_API_KEY
from data import CITY_LOOKUP
import duckdb

app = FastAPI(title='FleetCommander Maps API',
              description='<img alt="Fleet Commander Logo" src="/static/fc_logo.jpeg" /><h1>API for MarketDial FleetCommander™ services</h1>')


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

MAPS_CLIENT = None

@app.get("/google", response_class=HTMLResponse)
async def google_maps_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/", response_class=HTMLResponse)
async def duckdb_home_page(request: Request):
    return templates.TemplateResponse(request=request, name="search.html")

@app.get("/search", response_class=JSONResponse)
async def search(request: Request, name: str, type: str):
    # Connect to a database (in-memory in this case)
    con = duckdb.connect('osm_stores', read_only=True)

    if type == '(all store types)':
        result = con.execute(f"SELECT * FROM stores WHERE name LIKE '{name.replace("'", "''")}%' OR brand LIKE '{name.replace("'","''")}%' LIMIT 1000;").fetchall()
    elif type == '(restaurant, cafe, bar, etc.)':
        result = con.execute(f"SELECT * FROM stores WHERE (name LIKE '{name.replace("'", "''")}%' OR brand LIKE '{name.replace("'","''")}%') AND shop IS NULL LIMIT 1000;").fetchall()
    else:
        result = con.execute(f"SELECT * FROM stores WHERE (name LIKE '{name.replace("'", "''")}%' OR brand LIKE '{name.replace("'","''")}%') AND shop = '{type}' LIMIT 1000;").fetchall()

    json_result=[]
    for row in result:
        name = row[5] or row[6]
        type = row[4] or row[3]
        if row[0]:
            name += f' ({row[0]})'
        if row[7] and row[8] and row[9] and row[10]:
            address = f'{row[8]} {row[7]} {row[10]}  {row[9]}'
        else:
            address = '(no address)'
        json_result.append({'lat': row[1], 'lng': row[2], 'name': html.escape(name),
            'type': type, 'address': html.escape(address) })
    # dict_result = [dict(row) for row in result]

    return JSONResponse({'coordinates': json_result})


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