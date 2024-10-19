from time import sleep

import googlemaps
from data import GOOGLE_MAPS_API_KEY, LOCATIONS, TOP_100_CITIES, RETAIL_PLACE_TYPES, PLACE_TYPES


class MapsClient:

    def __init__(self):
        self.client = googlemaps.Client(GOOGLE_MAPS_API_KEY)


    def find_nearby(self, keyword, location, place_type, get_max=False):
        find_results = []

        request_results = self.client.places_nearby(keyword=keyword, location=location, type=place_type,
            # radius=50000,   # 50km maximum radius (31 miles)
            rank_by="distance",
            language="en-US")

        find_results = request_results['results']

        if get_max:  # Get up to 40 more places, currently a maximum of 60 by fetching 2 more pages
            while token := request_results.get('next_page_token'):
                sleep(
                    2)  # Google will complain if these happen too fast (googlemaps.exceptions.ApiError: INVALID_REQUEST)
                request_results = self.client.places_nearby(keyword=None, location=None, type=None,
                    page_token=token)

                find_results += request_results['results']

        return find_results

    # print(response)

    def find_nearby_competitors(self, store_name, location, keywords, *args):
        global nearby_competitors, time
        target_stores = self.find_nearby(store_name, location, args)
        others = self.find_nearby(f'{keywords} -{store_name}', location, args, get_max=True)
        stores = []
        origins = []
        competitors = []
        destinations = []
        # """Distance Matrix API:
        #         Maximum of 25 origins or 25 destinations per request.
        #         Maximum 100 elements in the result matrix
        #
        #         So for one store, maximum of 25 "competitors" distance calculated
        #         Maximum of 4 stores at a time (100 resulting distances)
        # """
        # ALSO:  Google Maps has problems with duplicate entries at the same address,
        #        so those need to be removed.  And the "minus" exclusion doesn't work well,
        #        so the target store name will appear in the destination (competitor) results
        STORE_LIMIT = 4
        COMPETITOR_LIMIT = 25
        count = 0
        for site in target_stores:
            count += 1
            if count > STORE_LIMIT:
                break
            if site['vicinity'] not in stores:
                origins.append(f"place_id:{site['place_id']}")
                stores.append(site['vicinity'])
        count = 0
        for site in others:
            count += 1
            if count > COMPETITOR_LIMIT:
                break
            if (f"{site['name']} {site['vicinity']}" not in competitors and
                    store_name.lower() not in site['name'].lower()):
                destinations.append(f"place_id:{site['place_id']}")
                competitors.append(f"{site['name']} {site['vicinity']}")
        # print(json.dumps(origins, indent=4))
        # print(json.dumps(destinations, indent=4))

        if len(origins) == 0:
            print()
            print("Sorry, couldn't find any target stores with the name: " + store_name)
            exit(1)

        if len(destinations) == 0:
            print()
            print("Sorry, couldn't find any competitor stores matching the keywords: " + keywords)
            print("...and the place type of: " + ','.join(args))
            exit(1)

        matrix = self.client.distance_matrix(origins, destinations)
        #    print(json.dumps(matrix, indent=2))
        nearby_competitors = {}
        store_index = 0
        for row in matrix['rows']:
            # print()
            store = f"{store_name} at {matrix['origin_addresses'][store_index]}"
            # print(store)
            store_index += 1
            comp_index = 0
            nearby_competitors[store] = []
            for element in row['elements']:
                competitor = competitors[comp_index]
                distance = element['distance']['text']
                time = element['duration']['text']
                nearby_competitors[store].append({'name': competitor, 'distance': distance, 'time': time})
                # print(f"\t{competitor} - {distance} ({time})")
                comp_index += 1

        return nearby_competitors
