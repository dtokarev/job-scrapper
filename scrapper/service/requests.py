from urllib.parse import urlencode

import requests
from requests import Response

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/59.0.3071.125 Mobile Safari/537.36 '
}


def get(url: str, headers: dict = default_headers, bearer: str = None, params = None, json: bool = True) -> Response:
    if bearer is not None:
        headers['Authorization'] = "Bearer "+bearer

    if params:
        encoded_params = urlencode(params, True)
        url += encoded_params if url.endswith('?') else '?'+encoded_params

    return requests.get(url, headers=headers)


