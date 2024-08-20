import requests
from pydantic import BaseModel, ConfigDict
from requests.structures import CaseInsensitiveDict

from .resources import ResourceMeta


class ResponseBase(BaseModel):
    _code: int
    _headers: CaseInsensitiveDict
    
    @property
    def code(self) -> int:
        return self._code

    @property
    def headers(self) -> CaseInsensitiveDict:
        return self._headers

    @classmethod
    def from_response(cls, resp: requests.Response) -> 'ResponseBase':
        obj = cls.parse_obj(resp.json())
        obj._code = resp.status_code
        obj._headers = resp.headers
        return obj


class V1ResourcesIdGETResponse200(ResponseBase, ResourceMeta):
    download_url: str


class V1ResourcesDraftsPOSTResponse200(ResponseBase):
    resource_id: str
    upload_url: str


class V1ResourcesSearchPOSTResponse200(ResponseBase):
    resources: list[ResourceMeta]
