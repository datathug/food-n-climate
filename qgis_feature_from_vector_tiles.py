from qgis.core import QgsFeature, QgsVectorTileLayer, QgsJsonExporter
from qgis.utils import iface

# _feature_exporter = QgsJsonExporter.exportFeature([x for x in wine.selectedFeatures()][0])

# never provide second argument, created once at import
def serialize_feature(feat: QgsFeature | list[QgsFeature], exporter=QgsJsonExporter()):
    
    print(id(exporter))
    """ Returns a GeoJSON string representation of a feature. """
    if isinstance(feat, QgsFeature):
        return exporter.exportFeature(feat)
    else:
        return [exporter.exportFeature(f) for f in feat]
    

def retrieve_features_within_map_extent(layer: QgsVectorTileLayer | str, scale: int | float, ctx = QgsSelectionContext()):
    assert scale > 0, 'invalid value for scale'
    
    # layer is either name or layer object
    
    # prepare
    layer.removeSelection()
    ctx.setScale(scale)
    
    # perform selection
    wine.selectByGeometry(QgsGeometry.fromRect(iface.mapCanvas().extent()), ctx)
    features = [x for x in wine.selectedFeatures()]
    print(
        "Selected {} features from layer '{}'".format(len(features), layer.name())
    )
    layer.removeSelection()
    return features
