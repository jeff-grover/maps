SELECT
    osm_id,
    latitude,
    longitude,
    MAX(CASE WHEN tag.key = 'amenity' THEN tag.value END) AS amenity,
    MAX(CASE WHEN tag.key = 'shop' THEN tag.value END) AS shop,
    MAX(CASE WHEN tag.key = 'name' THEN tag.value END) AS name,
    MAX(CASE WHEN tag.key = 'brand' THEN tag.value END) AS brand,
    MAX(CASE WHEN tag.key = 'opening_hours' THEN tag.value END) AS opening_hours,
    MAX(CASE WHEN tag.key = 'website' THEN tag.value END) AS website,
    MAX(CASE WHEN tag.key = 'phone' THEN tag.value END) AS phone,
    MAX(CASE WHEN tag.key = 'addr:street' THEN tag.value END) AS addr_street,
    MAX(CASE WHEN tag.key = 'addr:housenumber' THEN tag.value END) AS addr_housenumber,
    MAX(CASE WHEN tag.key = 'addr:postcode' THEN tag.value END) AS addr_postcode,
    MAX(CASE WHEN tag.key = 'addr:city' THEN tag.value END) AS addr_city
FROM (
    SELECT
        osm_id,
        ST_Y(ST_CENTROID(geometry)) AS latitude,
        ST_X(ST_CENTROID(geometry)) AS longitude,
        all_tags
    FROM `bigquery-public-data.geo_openstreetmap.planet_features_points`
    UNION ALL
    SELECT
        osm_id,
        ST_Y(ST_CENTROID(geometry)) AS latitude,
        ST_X(ST_CENTROID(geometry)) AS longitude,
        all_tags
    FROM `bigquery-public-data.geo_openstreetmap.planet_features_multipolygons`
) AS features
JOIN UNNEST(features.all_tags) AS tag ON TRUE
WHERE
    (tag.key = 'amenity' AND tag.value IN ('cafe', 'restaurant', 'fast_food', 'bar', 'pub')) OR
    (tag.key = 'shop') OR
    (tag.key IN ('name', 'brand', 'addr:street', 'addr:housenumber', 'addr:postcode', 'addr:city') AND tag.value IS NOT NULL)
GROUP BY osm_id, latitude, longitude
HAVING 
    MAX(CASE WHEN tag.key = 'amenity' THEN tag.value END) IS NOT NULL OR
    MAX(CASE WHEN tag.key = 'shop' THEN tag.value END) IS NOT NULL;
