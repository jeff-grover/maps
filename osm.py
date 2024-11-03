import pyrosm
import pandas as pd

# Load the OSM data
osm = pyrosm.OSM("north-america-latest.osm.pbf")

# Get all points of interest (POIs)
pois = osm.get_pois()

# Filter for commercial places by selecting relevant categories in `amenity`, `shop`, etc.
commercial_pois = pois[pois['amenity'].isin([
    'cafe', 'restaurant', 'bar', 'fast_food', 'pub', 'fuel',  # common commercial amenities
] or pois['shop'])]
# Additionally, filter for shops (e.g., retail stores)
commercial_pois = pd.concat([
    commercial_pois,
    pois[pois['shop'].notna()]  # this includes all types of shops (clothing, convenience, etc.)
])

# Save to Parquet
commercial_pois.to_parquet("commercial_pois.parquet")
