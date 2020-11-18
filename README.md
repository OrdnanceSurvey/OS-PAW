# OS-PAW

OS-PAW is the Ordnance Survey Python API Wrapper designed to make data from the OS Data Hub APIs readily accessible to python developers.

## Requirements
Python 3.8 or higher. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install OS-PAW.

```bash
pip install os-paw
```

## Usage

```python
from os_paw.wfs_api import WFS_API

# Generate an API key from https://osdatahub.os.uk/products
API_KEY = 'my_api_key'

# Choose a Spatial Reference System
SRS = 'EPSG:27700'

# Choose an OS Web Feature Service product
TYPE_NAME = 'Zoomstack_RoadsRegional'

# Create Bounding Box
BBOX = '440000, 112000, 443000, 115000'

# Create WFS_API object and run query
wfs_api = WFS_API(api_key=API_KEY)
payload = wfs_api.get_all_features_within_bbox(type_name=TYPE_NAME,
                                               bbox=BBOX,
                                               srs=SRS)
```
## Features
OS-PAW has improved error handling compared to requesting data directly from the OS Data Hub APIs. In particular, the user may search for a product that does not exist such as 'water' and the following message will be returned:
>ValueError: "Water" is not a valid Product.\
>Best matches: ['WaterNetwork_WatercourseLink', 'WaterNetwork_HydroNode', 'Zoomstack_Waterlines', 'Zoomstack_Surfacewater'].

Another advantage of os-paw is that there is no upper bound on the amount of data that can be requested during one method call. The raw API places a limit at 100 features per request, but there is no such limit on the payload here. In order to save time and costs when developing, there are two extra arguments available within the ```get_all_features_within_bbox``` method:
> allow_premium=False ,\
> max_feature_count=1000 .

The former means no premium data requests will be made and the latter means the user can restrict the amount of data returned if they happen to have picked a bounding box with a particularly high feature density. 

The APIs currently accept two Spatial Reference Systems, namely British National Grid (`'EPSG:27700'`) and World Geodetic System 1984 (`'EPSG:4326'`). 

## Tests
There are currently some limited tests of the functionality of the `WFS_API` object. To check that these tests pass, open a command prompt and navigate to the installation of OS-PAW, then run `pytest` from the command line. 

## Limitations
Currently (12/11/2020), there is only a python wrapper for the Web Feature Service (WFS) API. If there is sufficient interest, we shall add similar functionality for the other APIs available on the [OS Data Hub](https://osdatahub.os.uk/products). 

It is currently not possible to filter the results before returning the payload. For example, to return all of the schools within a bounding box, it is first necessary to return all of the buildings and then filter the resulting GeoJSON payload using your preferred method. If pre-filtering is integral to your project, you may wish to refer to the [tutorial](https://labs.os.uk/public/os-data-hub-tutorials/data-science/price-paid-spatial-distribution) on using the raw API, or submit an issue to this project, or feel free to contribute extra functionality yourself.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

