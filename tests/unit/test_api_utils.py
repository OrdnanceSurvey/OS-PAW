import pytest
from os_paw.api_utils import (API_Service, convert_features_to_geojson,
                              convert_single_feature_to_geojson,
                              get_feature_geometry_type, validate_api_key,
                              validate_api_service, validate_bbox,
                              validate_output_format, validate_request_params,
                              validate_srs, validate_type_name)


def test_get_geometry_feature_type_success():
    feature = {"type": "Feature",
                "geometry": {
                "type": "LineString",
                "coordinates": [
                [[0.985674076026689,51.07949125302662],[0.9894006268513168,51.07891028754501]]
                ]
                },
                "properties": {
                "Type": "B Road"}}
    feature_type = get_feature_geometry_type(feature)
    assert feature_type == 'LineString'    


def test_validate_srs_success():
    validate_srs('EPSG:27700')


def test_validate_srs_fail():
    with pytest.raises(AssertionError) as e:
        validate_srs('EPSG:1234')
    expected_error = 'EPSG:1234 is not a valid Spatial Reference System.'
    assert expected_error in e.value.args[0]


def test_validate_output_format_success():
    validate_output_format('gEoJsOn')
    validate_output_format('GeoJSON')


def test_validate_output_format_fail():
    with pytest.raises(AssertionError) as e:
        validate_output_format('shp')
    expected_error = 'shp is not a valid output format.'
    assert expected_error in e.value.args[0]


def test_validate_api_service_success():
    validate_api_service('wfs')



def test_validate_api_service_fail():
    with pytest.raises(TypeError) as e:
        validate_api_service('abc')
    assert e.value.args[0] == f'Please use {[api.name for api in API_Service]}'


def test_validate_type_name_success():
    assert validate_type_name('Zoomstack_RoadsRegional', 'wfs', False)


def test_validate_type_name_fail():
    with pytest.raises(ValueError) as e:
        validate_type_name('water', 'wfs', False)
    expected_matches = {'Zoomstack_Surfacewater', 'WaterNetwork_WatercourseLink', 
                        'WaterNetwork_HydroNode', 'Zoomstack_Waterlines'}
    best_matches_error = e.value.args[0].split('Best matches:')[-1]
    for match in expected_matches:
        assert match in best_matches_error


def test_validate_bbox_success():
    validate_bbox('605621,139199,606621,140199', srs='EPSG:27700')
    validate_bbox('51, -1, 52, 1', srs='EPSG:4326')


def test_validate_bbox_fail_bng():
    with pytest.raises(AssertionError) as e:
        validate_bbox('605621,3139199,606621,140199', srs='EPSG:27700')
    assert e.value.args[0] == 'British Longitude values must be between 0 and 700000. Format bbox as a comma-separated string of the form "Easting_SW, Northing_SW, Easting_NE, Northing_NE".'

def test_validate_bbox_fail_wgs():
    with pytest.raises(AssertionError) as e:
        validate_bbox('30, -1, 52, 1', srs='EPSG:4326')
    assert e.value.args[0] == 'British Latitude values must be between 49 and 61. Format bbox as a comma-separated string of the form "latitude_SW, longitude_SW, latitude_NE, longitude_NE".'


def test_validate_request_params_success():
    validate_request_params('wfs', True, 'WaterNetwork_HydroNode', 
                            '605621,139199,606621,140199', 'EPSG:27700',
                            'GeoJSON')


def test_validate_request_params_fail():
    with pytest.raises(ValueError) as e:
        validate_request_params('wfs', True, 'WaterNetwork_HydroDog', 
                                '605621,139199,606621,140199', 'EPSG:27700',
                                'GeoJSON')
    expected_error = '"WaterNetwork_HydroDog" is not a valid Product.'
    assert expected_error in e.value.args[0].split('Available')[0]


def test_validate_api_key_success():
    validate_api_key('abcdefghijklmnopqrstuvwxyzabcdef')


def test_validate_api_key_fail():
    with pytest.raises(AssertionError) as e:
        validate_api_key('abc')
    assert e.value.args[0] == 'OS Data Hub API Keys are 32 characters.'




