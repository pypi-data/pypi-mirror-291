from enum import Enum
from pydantic import BaseModel, field_validator, model_validator

from .utility import (
    OffsetLimitPagination,
    SortOption,
    SearchOptionContainsAllString,
    SearchOptionEQBool,
    SearchOptionEQString,
    SearchOptionGELE,
)


class ResourcesSearchFilters(BaseModel):
    file_name: SearchOptionEQString | None = None
    tags: SearchOptionContainsAllString | None = None
    creation_ts: SearchOptionGELE | None = None
    is_removed: SearchOptionEQBool | None = None


class ResourcesSorting(BaseModel):
    creation_ts: SortOption | None = None
    
    @model_validator(mode='after')
    def is_valid(self):
        opts = [self.creation_ts]
        opts = filter(opts, lambda opt: opt != None)
        opts = sorted(opts, lambda opt: opt.index)
        for i in range(len(opts)):
            assert opts[i].index == i, f'{i} index is missing ({opts[i]})'
        return self
    

class ResourcesSearchOptions(BaseModel):
    filters: ResourcesSearchFilters | None = None
    sorting: ResourcesSorting | None = None
    pagination: OffsetLimitPagination


class ResourceBase(BaseModel):
    file_name: str | None = None
    checksum_md5: str | None = None
    context: dict | None = None


class ResourceMutable(BaseModel):
    description: str | None = None
    tags: list[str] | None = None


class ResourceTTL(BaseModel):
    soft_ttl_s: int | None = None
    hard_ttl_s: int | None = None
    
    @field_validator('soft_ttl_s', 'hard_ttl_s')
    @classmethod
    def gt0_or_None(cls, v):
        assert (v is None or v > 0)
        return v


class StorageType(str, Enum):
    S3 = 'S3'
    YT = 'YT'


class ResourceS3Storage(BaseModel):
    endpoint: str
    region: str
    bucket: str
    key: str


class ResourceYTStorage(BaseModel):
    proxy: str
    path: str


class ResourceStorage(BaseModel):
    storage_type: StorageType
    s3_storage_info: ResourceS3Storage | None = None
    yt_storage_info: ResourceYTStorage | None = None
    
    @model_validator(mode='after')
    def is_valid(self):
        if self.storage_type == StorageType.S3:
            assert self.s3_storage_info is not None
        if self.storage_type == StorageType.YT:
            assert self.yt_storage_info is not None
        return self


class NewResourceDraftMeta(ResourceBase, ResourceMutable, ResourceTTL):
    byte_size: int | None = None
    
    @field_validator('byte_size')
    @classmethod
    def gt0(cls, v: int) -> int:
        assert (v is None or v > 0)
        return v


class ResourceMeta(ResourceBase, ResourceMutable, ResourceStorage, ResourceTTL):
    resource_id: str
    byte_size: int
    creation_ts: int
    has_ownership: bool
    draft_creation_ts: int | None = None
    last_access_ts: int
    is_removed: bool
