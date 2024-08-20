from pydantic import BaseModel, field_validator, model_validator


class OffsetLimitPagination(BaseModel):
    offset: int
    limit: int

    @field_validator('limit')
    @classmethod
    def gt0(cls, v):
        assert v > 0
        return v


class SortOption(BaseModel):
    index: int
    order: str

    @field_validator('index')
    @classmethod
    def gte0(cls, v):
        assert v >= 0
        return v
    
    @field_validator('order')
    @classmethod
    def oneof(cls, v):
        assert v in [O_ASC, O_DESC]
        return v


class SearchOptionContainsAllString(BaseModel):
    contains_all: list[str] | None = None


class SearchOptionEQBool(BaseModel):
    eq: bool | None = None


class SearchOptionEQString(BaseModel):
    eq: str | None = None


class SearchOptionEQ(BaseModel):
    eq: int | None = None


class SearchOptionLE(BaseModel):
    le: int | None = None


class SearchOptionGE(BaseModel):
    ge: int | None = None


class SearchOptionGELE(SearchOptionGE, SearchOptionLE):

    @model_validator(mode='after')
    def is_valid(self):
        ge, le = self.ge, self.le
        if ge is not None and le is not None:
            assert ge < le, f'empty interval ([{ge}, {le}])'
        return self


class SearchOptionGELE(SearchOptionEQ, SearchOptionGE, SearchOptionLE):
    
    @model_validator(mode='after')
    def is_valid(self):
        if self.eq is not None:
            assert self.ge is None, 'eq option can\'t be mixed with ge/le'
            assert self.le is None, 'eq option can\'t be mixed with ge/le'
        return self


O_ASC = "asc"
O_DESC = "_O_DESC"
