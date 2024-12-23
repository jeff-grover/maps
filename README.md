# maps
Experimentation with Google Maps for site management tools

# FastAPI server version:

As usual, set up python, PDM install, then run `main.py`

The UI is available at:

http://0.0.0.0:9898/

SwaggerUI available at:

http://0.0.0.0:9898/docs



# Command-line version:

To get help, try executing `./nearby.py` with no arguments:

```
COMMAND-LINE USAGE:

  nearby.py STORE_NAME CITY_NAME [STORE_KEYWORDS] [STORE_TYPE STORE_TYPE STORE_TYPE... etc.]

    Where STORE_TYPEs are zero or more of the following: 
      bakery
      beauty_salon
      bicycle_store
      book_store
      cafe
      car_dealer
      clothing_store
      convenience_store
      department_store
      drugstore
      electronics_store
      florist
      funeral_home
      furniture_store
      gas_station
      home_goods_store
      insurance_agency
      jewelry_store
      liquor_store
      pet_store
      pharmacy
      restaurant
      shoe_store
      shopping_mall
      store
      supermarket

```
Example command lines:

```
> ./nearby.py "Maverik" "South Jordan" "" "gas_station" "convenience_store" "store"

> ./nearby.py "Dick's" "Salt Lake City" "Sporting Goods" "store"
```
