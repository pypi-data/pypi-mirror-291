# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import requests

from a3exception import errors


def _handle_response(response: requests.Response) -> dict:
    if response.status_code == 200:
        rd = response.json()
        if rd['code'] != 200:
            raise errors.ClientKnownError(f'{rd["code"]}: {rd["message"]}')
        return rd
    else:
        raise errors.ClientKnownError(f'HTTP状态码为:{response.status_code}')


class OCRClient:

    def __init__(self, host: str):
        self._host = host
        self._session = requests.Session()

    def ocr(self, filename: str = None, base64_image: str = None, return_probability: bool = False, charsets: str = None, png_fix: bool = False, **kwargs) -> str:
        url = urljoin(self._host, "/ocr")
        data = {
            'probability': return_probability,
            'charsets': charsets,
            'png_fix': png_fix,
            'image': base64_image
        }

        files = dict()
        if filename is not None:
            files.update({'file': open(filename, 'rb')})

        response = self._session.post(url=url, data=data, files=files, **kwargs)
        rd = _handle_response(response)
        return rd['data']

    def slide_match(
            self, target_filename: str = None, base64_target: str = None, background_filename: str = None, base64_background: str = None, simple_target: bool = False, **kwargs
    ) -> dict:
        url = urljoin(self._host, "/slide_match")
        data = {
            'simple_target': simple_target,
            'target': base64_target,
            'background': base64_background
        }

        files = dict()
        if target_filename is not None:
            files.update({'target_file': open(target_filename, 'rb')})

        if background_filename is not None:
            files.update({'background_file': open(background_filename, 'rb')})

        response = self._session.post(url=url, data=data, files=files, **kwargs)
        rd = _handle_response(response)
        return rd['data']

    def detection(self, filename: str = None, base64_image: str = None, **kwargs) -> str:
        url = urljoin(self._host, "/detection")
        data = {
            'image': base64_image
        }

        files = dict()
        if filename is not None:
            files.update({'file': open(filename, 'rb')})

        response = self._session.post(url=url, data=data, files=files, **kwargs)
        rd = _handle_response(response)
        return rd['data']
