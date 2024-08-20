import logging
import pprint
import requests
import traceback
from abc import ABC, abstractmethod
from typing import Dict

from artifactory.utils.functools import retry


class RequesterBase(ABC):

    @abstractmethod
    def request(self, method, url, **kwargs) -> requests.Response:
        pass

    def get(self, *args, **kwargs) -> requests.Response:
        return self.request('get', *args, **kwargs)

    def head(self, *args, **kwargs) -> requests.Response:
        return self.request('head', *args, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        return self.request('post', *args, **kwargs)

    def put(self, *args, **kwargs) -> requests.Response:
        return self.request('put', *args, **kwargs)

    def delete(self, *args, **kwargs) -> requests.Response:
        return self.request('delete', *args, **kwargs)

    def patch(self, *args, **kwargs) -> requests.Response:
        return self.request('patch', *args, **kwargs)

    def _raw_request_with_retries(self, method, url, max_retries, sleep_time_s, **kwargs) -> requests.Response:
        def request():
            resp = self._raw_request(method, url, **kwargs)
            try:
                resp.raise_for_status()
            except Exception as error:
                raise RuntimeError(f'{error}. Response body: {resp.text})')
            return resp
    
        def on_error(error: Exception):
            args = {**dict(method=method, url=url), **kwargs}
            self._on_failed_request(error, args)
        
        response = retry(
            fn=request,
            max_retries=max_retries,
            sleep_time_base_s=sleep_time_s,
            sleep_time_factor=1,
            on_error=on_error,
        )
        return response

    def _raw_request(self, method, url, **kwargs) -> requests.Response:
        return requests.request(method, url, **kwargs)

    def _on_failed_request(self, error: Exception, arguments: Dict = None):
        logging.debug(f'Failed to make request: {error}\n',
                      f'Arguments:\n {pprint.pformat(arguments, indent=2)}\n',
                      f'Traceback:\n {traceback.format_exc()}')
