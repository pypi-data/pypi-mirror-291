from pydantic import BaseModel, ConfigDict, field_validator

from .units import MB


class ClientConfig(BaseModel):
    artifactory_endpoint: str = 'https://artifactory.test-kaizen.idzn.ru'  # TODO: update default endpoint
    upload_chunk_size: int = 50 * MB
    upload_retries: int = 5
    
    model_config = ConfigDict(extra='forbid')
    
    @field_validator('upload_chunk_size')
    @classmethod
    def gt0(cls, v: int) -> int:
        assert v > 0
        return v
    
    @field_validator('upload_retries')
    @classmethod
    def gte0(cls, v: int) -> int:
        assert v >= 0
        return v
