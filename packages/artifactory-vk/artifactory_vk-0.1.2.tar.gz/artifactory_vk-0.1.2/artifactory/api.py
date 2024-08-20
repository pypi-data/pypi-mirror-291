from typing import IO

import requests
from tusclient.uploader import Uploader as TusUploader

from . import models
from artifactory.utils.requesters import DefaultRequester


class API:
    def __init__(
        self,
        *,
        endpoint: str,
    ):
        self._endpoint = endpoint
        self._requester = DefaultRequester()
        
    def v1_resources_search_POST(
        self,
        request: models.requests.V1ResourcesSearchPOSTRequest,
    ) -> models.responses.V1ResourcesSearchPOSTResponse200:
        resp = self._make_request(request)
        if resp.status_code != 200:
            raise RuntimeError('Got error response:', resp.code, resp.content)
        resp_model = models.responses.V1ResourcesSearchPOSTResponse200.from_response(resp)
        return resp_model

    def v1_resources_drafts_POST(
        self,
        request: models.requests.V1ResourcesDraftsPOSTRequest,
    ) -> models.responses.V1ResourcesDraftsPOSTResponse200:
        resp = self._make_request(request)
        if resp.status_code != 200:
            raise RuntimeError('Got error response:', resp.code, resp.content)
        resp_model = models.responses.V1ResourcesDraftsPOSTResponse200.from_response(resp)
        return resp_model
    
    def tus_upload(
        self,
        reader: IO[bytes],
        byte_size: int,
        *,
        upload_url: str,
        chunk_size: int,
    ) -> None:
        # TODO: wait for PR: https://github.com/tus/tus-py-client/pull/96
        self._declare_length(upload_url, byte_size)
        uploader = TusUploader(
            file_stream=reader,
            url=upload_url,
            chunk_size=chunk_size,
            verify_tls_cert=False,
        )
        uploader.upload()
    
    # TODO: remove when PR is merged: https://github.com/tus/tus-py-client/pull/96
    def _declare_length(self, upload_url: str, length: int):
        headers = {
            'Tus-Resumable': '1.0.0',
        }
        resp = self._requester.head(
            upload_url,
            headers=headers,
        )
        resp.raise_for_status()

        if resp.headers.get('Upload-Defer-Length') == '1':
            headers = {
                'Tus-Resumable': '1.0.0',
                'Content-Type': 'application/offset+octet-stream',
                'Upload-Offset': '0',
                'Upload-Length': str(length),
            }
            resp = self._requester.patch(
                upload_url,
                headers=headers,
            )
            resp.raise_for_status()
            return True

        return False

    def _make_request(self, req: models.requests.RequestBase) -> requests.Response:
        url = self._make_url(req.path(), query=req.query_str())
        resp = self._requester.request(
            req.method,
            url,
            headers=req.header(),
            json=req.body_json(),
        )
        return resp

    def _make_url(self, path: str, *, query: str | None = None):
        if not path.startswith('/'):
            path = '/' + path
        url = f'{self._endpoint}{path}'
        if query is not None:
            url += f'?{query}'
        return url
    