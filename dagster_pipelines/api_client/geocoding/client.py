from ..rest_adapter import RestAdapter
from ..exceptions import ApiDataException
from json import JSONDecodeError
from .models import Location

class GeocodingClient:
    def __init__(self):
        self._rest_adapter = RestAdapter(api='geocoding-api')
        self.endpoint = '/v1/search'
    
    def search(self, name: str, count: int=10) -> list[Location]:
        params = {'name': name, 'count': count} # default format is json
                                                # try using protobuf
        resp = self._rest_adapter.get(endpoint=self.endpoint, params=params)
        try:
            results = resp.json().get('results')
        except (ValueError, JSONDecodeError) as e:
            raise ApiDataException('error while deserializing json response') from e
        return [Location(**result) for result in results]
