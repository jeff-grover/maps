#!/usr/bin/env python

import json
from maps_client import MapsClient
from data import CITY_LOOKUP, RETAIL_PLACE_TYPES
from sys import argv

if __name__ == '__main__':
    if len(argv) < 3:
        print()
        print("USAGE:")
        print()
        print("  nearby.py STORE_NAME CITY_NAME [STORE_KEYWORDS] [STORE_TYPE STORE_TYPE STORE_TYPE... etc.]")
        print()
        print("    Where STORE_TYPEs are zero or more of the following: ")
        print("      " + '\n      '.join(RETAIL_PLACE_TYPES))
        print()
        exit()

    location = CITY_LOOKUP.get(argv[2])
    if not location:
        print()
        print("Sorry, I don't know this city (largest 1000 US cities only): " + argv[2])
        print()
        exit()

    client = MapsClient()

    if len(argv) > 4:
        place_type = argv[4]
    else:
        place_type = 'store'

    if len(argv) > 3:
        keywords = argv[3]
    else:
        keywords = 'store'


    # nearby_competitors = client.find_nearby_competitors(store_name="Maverik", location=location, keywords="convenience", place_type=["store", "gas_station"])
    nearby_competitors = client.find_nearby_competitors(argv[1], location, keywords, 'store', 'gas_station')

    print()
    print()
    print(json.dumps(nearby_competitors, indent=4))