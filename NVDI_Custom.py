import ee
import folium
import io
import json
from PIL import Image


def reverse_cords(land_cords):
    new_list = []
    for pair in land_cords[0]:
        new_list.append((pair[1], pair[0]))
    return new_list


def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

def get_nvdi_map_of_area(path_to_json):
    #creating layer for image
    folium.Map.add_ee_layer = add_ee_layer

    service_account = 'ndvi-107@ndvi-356009.iam.gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(service_account, 'private-key.json')
    ee.Initialize(credentials)

    #Opening requested map and packing all cords to list
    with open(path_to_json) as content:
        json_data = json.load(content)
        for feature in json_data['features']:
                land_cords = feature['geometry']['coordinates']

    #Put cords at EE geometry
    bounds = ee.Geometry.Polygon(land_cords)


    imageCollection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    image = ee.Image(imageCollection.filterBounds(bounds).sort('CLOUD_COVER').first())
    ndvi_area = image.normalizedDifference(['SR_B5', 'SR_B4']).clip(bounds)
    ndvi_visualisation_scale = {'min': -1, 'max': 1,
                                'palette': ["770000", "880000", '990000',
                                            "AA0000", 'BB0000', 'CC0000',
                                            'DD0000', 'EE0000', 'FF0000',
                                            'FF0000','FF0000', 'FFCC00',
                                            'FFFF00', '00FF00', '008800',
                                            '006600', '006600']}

    y, x, *_ = bounds.centroid().getInfo()['coordinates']
    center_point = [x, y]

    folium_map = folium.Map(location=center_point)
    #Customizing start zoom, here we have folium method called fit_bounds(but we need to reverse cords from geojson.io)
    folium_map.fit_bounds(reverse_cords(land_cords))
    folium_map.add_ee_layer(ndvi_area, ndvi_visualisation_scale, 'NDVI')

    #Saving map to png(Reason thy we import selenium and io is here, there is no simple way to save as png, at this case
    # we use protected method with dependenses(in general, protected methods not supposed to be used.))
    png_bytes = folium_map._to_png(7)
    map_image = Image.open(io.BytesIO(png_bytes))#Decoding bytes
    map_image.save('imgs/map.png')
    return True

