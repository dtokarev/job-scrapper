from json import JSONDecodeError
from urllib.parse import urlencode

import logging
import requests
from requests import Response

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/59.0.3071.125 Mobile Safari/537.36 '
}
log = logging.getLogger('console')


def get(url: str, headers: dict = default_headers, bearer: str = None, params=None) -> Response:
    if bearer is not None:
        headers['Authorization'] = "Bearer "+bearer

    if params:
        encoded_params = urlencode(params, True)
        url += encoded_params if url.endswith('?') else '?'+encoded_params
    # print(url)
    return requests.get(url, headers=headers)


def validate_response(response: Response, errors: list) -> bool:
    if int(response.status_code) < 400:
        return True
    try:
        error = str(response.json())
    except JSONDecodeError as ex:
        error = '{} ({}) url: {}'.format(response.reason, response.status_code, response.url)

    errors.append(error)
    log.error(error)
    return False


