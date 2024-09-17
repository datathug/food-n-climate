import json

from PyQt5.QtCore import QVariant
from geopy import Location
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim


class NoResultsException(Exception):
    pass


class OsmQgisGeocoder(Nominatim):

    id_counter = 1
    layer: QgsVectorLayer = None
    fields: list[QgsField] = None
    cache: list = None
    add_layer_to_map = QgsProject.instance().addMapLayer

    def __init__(self):
        super().__init__(user_agent="nonsense")
        self.cache = []

    def set_layer(self):
        self.fields = [
            QgsField('name', QVariant.String),
            QgsField("raw", QVariant.String),
            QgsField("importance", QVariant.Double),
        ]
        self.layer = QgsVectorLayer("point?crs=epsg:4326",     # "point?crs=epsg:4326&field=id:integer"
                                      "Geocoded results",
                                      "memory")
        self.layer.startEditing()
        [self.layer.addAttribute(f) for f in self.fields]
        self.layer.commitChanges()

        # self.qfields = QgsFields()
        # [self.qfields.append(f) for f in self.fields]

        self.add_layer_to_map(self.layer)
        self.layer.updateExtents()

    def visualize(self, resp: Location, drop_features):

        new_feature_id = self.id_counter
        subset_string = ''
        self.layer.startEditing() if not self.layer.isEditable() else None

        if drop_features and self.layer.featureCount() != 0:
            fids = [f.id() for f in self.layer.getFeatures()]
            self.layer.deleteFeatures(fids)

        elif not drop_features:
            # filter
            subset_string = f'$id={new_feature_id}'

        feat = QgsFeature()

        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(resp.longitude, resp.latitude)))
        feat.setFields(self.layer.fields())

        loc_name = str(resp.raw['name']) if resp.raw is not None else ''
        importance = float(resp.raw['importance']) if 'importance' in resp.raw else -1
        feat.setAttributes([
                loc_name,
                json.dumps(resp.raw),
                importance
            ]
        )
        print(feat.attributes())
        assert feat.geometry().isGeosValid(), 'geom invalid'

        self.id_counter += 1 if self.layer.dataProvider().addFeatures([feat]) else None

        self.layer.commitChanges()
        self.layer.setSubsetString(subset_string) if subset_string else None  # will not work in editing mode
        self.layer.updateExtents()
        return feat

    def get_location(self, place: str, country: str = None, drop_features=True):

        place = f"{place}, {country}" if country else place
        try:
            resp: Location = self.geocode(query=place)
        except GeocoderUnavailable:
            print(f'Geocoder unavailable, better wait')
            return

        if not resp:
            raise NoResultsException(f"received no response for '{place} {country}'")

        self.cache.append(resp)
        feat = None
        if self.layer:
            feat = self.visualize(resp, drop_features=drop_features)
        return resp, feat
