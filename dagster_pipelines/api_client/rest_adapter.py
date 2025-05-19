import requests
import logging
from .exceptions import ApiRequestException

class RestAdapter:
    def __init__(self, api: str, logger: logging.Logger=None): # no auth required for open-meteo
        '''Low-level REST adapter for the open-meteo API'''
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(name='rest_logger')
            log_format = logging.Formatter('%(asctime)-15s %(levelname)-2s %(message)s')
            log_handler = logging.StreamHandler()
            log_handler.setFormatter(fmt=log_format)
            self.logger.addHandler(hdlr=log_handler)
        self.base_url = f'https://{api}.open-meteo.com'
        self.default_headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
            }
    
    def _do(self, method: str, endpoint: str, headers: dict={}, params: dict={}, body: dict={}) -> requests.Response:
        url = self.base_url + endpoint
        if not headers:
            headers = self.default_headers
        
        # make request
        try:
            resp = requests.request(method=method, url=url, headers=headers, params=params, json=body)
        except requests.exceptions.RequestException as e:
            self.logger.error(msg=e)
            raise ApiRequestException('request failed') from e
        
        # check response status
        if 200 >= resp.status_code <= 299:
            return resp
        else:
            self.logger.error(msg=f'http error: {resp.status_code} - {resp.reason} - {resp.text}')
            raise ApiRequestException(f'http error: {resp.status_code} - {resp.reason} - {resp.text}')
        
    def get(self, endpoint: str, headers: dict={}, params: dict={}):
        return self._do(method='GET', endpoint=endpoint, headers=headers, params=params)

    # read-only API, no other methods implemented
