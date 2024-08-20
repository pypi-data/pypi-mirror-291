from abc import abstractmethod
from pydantic import BaseModel, ConfigDict
from requests.structures import CaseInsensitiveDict
from typing import Any

from .resources import NewResourceDraftMeta, ResourcesSearchOptions


class RequestBase(BaseModel):
    _method: str
    
    @property
    def method(self) -> str:
        return self._method
    
    @abstractmethod
    def path(self) -> str:
        pass
    
    def query_str(self) -> str | None:
        if self.query is None:
            return None
        assert issubclass(type(self.query), BaseModel)
        d = self.query.dict()
        q = '&'.join(f'{k}={v}' for k, v in d.items())
        return q 

    def header(self) -> CaseInsensitiveDict | None:
        if self.headers is None:
            return None
        assert issubclass(type(self.headers), CaseInsensitiveDict)
        return self.headers

    def body_json(self) -> Any | None:
        if self.body is None:
            return None
        assert issubclass(type(self.body), BaseModel)
        return self.body.dict()


class RequestPOSTBase(RequestBase):
    def __init__(self, **data):
        super().__init__(**data)
        self._method = 'POST'


class V1ResourcesDraftsPOSTRequest(RequestPOSTBase):
    query: None = None
    headers: None = None
    uri: None = None
    body: NewResourceDraftMeta
    
    model_config = ConfigDict(extra='forbid')
    
    def path(self) -> str:
        return '/v1/resources/drafts'


class V1ResourcesSearchPOSTRequest(RequestPOSTBase):
    class Query(BaseModel):
        q: str | None = None

    query: Query | None = None
    headers: None = None
    uri: None = None
    body: ResourcesSearchOptions
    
    model_config = ConfigDict(extra='forbid')
    
    def path(self) -> str:
        return '/v1/resources/search'
