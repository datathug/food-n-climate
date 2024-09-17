import geojson
import requests
from overpass import API as Overpass, UnknownOverpassError
from shapely import Point, Polygon

from definitions import PdoLocation

api = Overpass(timeout=60, debug=True)

QUERY_FORM = """
[out:json];
is_in({}, {});
area._
  [boundary=administrative]
  [admin_level~"^({})$"] -> .MyArea;
rel(pivot.MyArea);
out geom;""".strip().replace('\n', '')

# customize

def _as_geojson(elements):
    features = []
    geometry = None
    for elem in elements:
        elem_type = elem.get("type")
        elem_tags = elem.get("tags")
        elem_geom = elem.get("geometry", [])
        if elem_type == "node":
            # Create Point geometry
            geometry = geojson.Point((elem.get("lon"), elem.get("lat")))
        elif elem_type == "way":
            # Create LineString geometry
            geometry = geojson.LineString([(coords["lon"], coords["lat"]) for coords in elem_geom])
        elif elem_type == "relation":
            # Initialize polygon list
            polygons = []
            # First obtain the outer polygons
            for member in elem.get("members", []):
                if member["role"] == "outer":
                    points = [(coords["lon"], coords["lat"]) for coords in member.get("geometry", [])]
                    # Check that the outer polygon is complete
                    # EUGENE: append last if do not match
                    if points and points[-1] == points[0]:
                        polygons.append([points])
                    else:
                        polygons.append([points] + [points[0]])
                        # DO NOT RAISE!  raise UnknownOverpassError("Received corrupt data from Overpass (incomplete polygon).")
            # Then get the inner polygons
            for member in elem.get("members", []):
                if member["role"] == "inner":
                    points = [(coords["lon"], coords["lat"]) for coords in member.get("geometry", [])]
                    # Check that the inner polygon is complete
                    if points and points[-1] == points[0]:
                        # We need to check to which outer polygon the inner polygon belongs
                        point = Point(points[0])
                        check = False
                        for poly in polygons:
                            polygon = Polygon(poly[0])
                            if polygon.contains(point):
                                poly.append(points)
                                check = True
                                break
                        if not check:
                            raise UnknownOverpassError("Received corrupt data from Overpass (inner polygon cannot "
                                                       "be matched to outer polygon).")
                    else:
                        raise UnknownOverpassError("Received corrupt data from Overpass (incomplete polygon).")
            # Finally create MultiPolygon geometry
            if polygons:
                geometry = geojson.MultiPolygon(polygons)
        else:
            raise UnknownOverpassError("Received corrupt data from Overpass (invalid element).")

        if geometry:
            feature = geojson.Feature(
                id=elem["id"],
                geometry=geometry,
                properties=elem_tags
            )
            features.append(feature)

    return geojson.FeatureCollection(features)


class MyOverpass:

    endpoint: str = "https://overpass-api.de/api/interpreter"
    session = requests.Session()
    levels: str = 4     # gets reassigned

    def __init__(self):
        self.levels = '|'.join(self.levels) if not isinstance(self.levels, int) else str(self.levels)

    def get(self, lon, lat):
        q = QUERY_FORM.format(lat, lon, self.levels)
        resp = self.session.get(self.endpoint + "?data=" + q)
        return resp


def get_boundaries(lon: float, lat: float):
    q = f"""
is_in({lat}, {lon});
area._
  [boundary=administrative]
  [admin_level~"^(4|5|6|7)$"] -> .MyArea;
rel(pivot.MyArea);"""
    return api.get(query=q, verbosity='geom')


def parse_geometries(j: dict):
    features = []

    for el in j['elements']:
        coordinates = []
        mismatches = 0
        if el['type'] == 'relation':

            # parse all coordinates
            last_latlon = None
            for member in filter(
                    lambda x: x['type'] == 'way' and 'geometry' in x and x['geometry'],
                    j['elements'][0]['members']
            ):
                if last_latlon:
                    mismatches += 1 if last_latlon != member['geometry'][0] else 0
                else:
                    last_latlon = coordinates
                [coordinates.append((point['lon'], point['lat'])) for point in member['geometry']]


            polygon = geojson.Polygon(
                [
                    coordinates
                ]
            )
            features.append(
                geojson.Feature(geometry=polygon, properties={
                        "level": el['tags']["admin_level"],
                        "name": el["tags"]["name"],
                    }
                )
            )
            print(f"MISMATCHES IN F: {mismatches}")

    return geojson.FeatureCollection(features)