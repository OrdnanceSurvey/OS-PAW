from enum import Enum

from geojson import Feature, LineString

from os_paw import products


class API_Service(Enum):
    wfs = 1
    wmts = 2
    vts = 3
    zxy = 4

VALID_SPATIAL_REFERENCE_SYSTEMS = ('EPSG:4326',
                                   'EPSG:27700')
VALID_OUTPUT_FORMATS = ('geojson')
                        # no longer valid 'xml')


def get_feature_geometry_type(feature):
    try:
        feature_type = feature['geometry']['type']
        return feature_type
    except KeyError:
        raise Exception('Feature is not in standard GeoJSON format.')


def convert_features_to_geojson(features):
    return [convert_single_feature_to_geojson(feat) for feat in features]


def convert_single_feature_to_geojson(single_feature: Feature, 
                                      geometry_type=LineString):
    new_coordinates = single_feature['geometry']['coordinates'][0]
    new_linestring = geometry_type(new_coordinates)
    new_feature = Feature(geometry=new_linestring,
                          properties=single_feature['properties'])
    return new_feature


def validate_api_service(api_service):
    if not hasattr(API_Service, api_service): 
        raise TypeError(f'Please use {[api.name for api in API_Service]}')


def validate_srs(srs_string):
    assert srs_string in VALID_SPATIAL_REFERENCE_SYSTEMS, (f'{srs_string} is '
                                    'not a valid Spatial Reference System.\n'
                                    'Valid Spatial Reference Systems are: '
                                    f'{VALID_SPATIAL_REFERENCE_SYSTEMS}.')


def validate_output_format(output_format_string):
    assert output_format_string.lower() in VALID_OUTPUT_FORMATS, (''
                                                f'{output_format_string} is '
                                                'not a valid output format. \n'
                                                'Valid output formats are: '
                                                f'{VALID_OUTPUT_FORMATS}.')


def validate_type_name(type_name, api_service, allow_premium=False):
    api_service = api_service.lower()
    validate_api_service(api_service)
    product_dict = getattr(products, f'{api_service}_products')
    open_products = product_dict['Open']
    premium_products = product_dict['Premium']
    all_products = open_products | premium_products
    suggestions = find_most_similar_products(type_name, all_products)
    if not allow_premium:
        if type_name not in open_products and type_name in premium_products:
            raise ValueError((f'"{type_name}" is only available as a '
                        f'Premium Product. \n\n Best matches: {suggestions}'))
        elif type_name not in all_products:
            raise ValueError((f'"{type_name}" is not a valid Product. \n\n'
                f'Available Products: \n{all_products}\n\n'
                f'Best matches: {suggestions}'))
        else:
            return type_name in open_products
    elif allow_premium:
        if type_name not in all_products:
            raise ValueError((f'"{type_name}" is not a valid Product. \n\n'
                f'Available Products: \n{all_products}\n\n'
                f'Best matches: {suggestions}'))
    return True


def find_most_similar_products(type_name, all_products):
    return [product for product in all_products 
            if type_name.lower() in product.lower()]


def _validate_bbox(bbox_string, srs, min_x, max_x, min_y, max_y):
    bbox_list = bbox_string.split(',')
    if srs == 'EPSG:4326':
        msg = ('Format bbox as a comma-separated string of the form '
                '"latitude_SW, longitude_SW, latitude_NE, longitude_NE".')
    elif srs == 'EPSG:27700':
        msg = ('Format bbox as a comma-separated string of the form '
               '"Easting_SW, Northing_SW, Easting_NE, Northing_NE".')
    assert (float(bbox_list[0]) > min_y and float(bbox_list[0]) < max_y) and \
           (float(bbox_list[2]) > min_y and float(bbox_list[2]) < max_y), (''
                                f'British Latitude values must be between '
                                f'{min_y} and {max_y}. {msg}')
    assert (float(bbox_list[1]) > min_x and float(bbox_list[1]) < max_x) and \
           (float(bbox_list[3]) > min_x and float(bbox_list[3]) < max_x), (''
                                f'British Longitude values must be between '
                                f'{min_x} and {max_x}. {msg}')


def validate_bbox(bbox_string, srs='EPSG:4326'):
    """N.B. Top Left and Bottom Right coordinates can be interchanged. 
    Whitespace is immaterial."""
    validate_srs(srs)
    if srs == 'EPSG:4326':
        _validate_bbox(bbox_string, srs='EPSG:4326', min_x=-7, max_x=2, 
                                                     min_y=49, max_y=61)
    elif srs == 'EPSG:27700':
        _validate_bbox(bbox_string, srs='EPSG:27700', min_x=0, max_x=700000, 
                                                      min_y=0, max_y=1250000)


def validate_request_params(api_service, allow_premium, type_name, 
                            bbox, srs, output_format):
    validate_type_name(type_name, api_service, allow_premium)
    validate_srs(srs)
    validate_bbox(bbox, srs)
    validate_output_format(output_format)

def validate_api_key(api_key):
    assert len(str(api_key)) == 32, 'OS Data Hub API Keys are 32 characters.'





