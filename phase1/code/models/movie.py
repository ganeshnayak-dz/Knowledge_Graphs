from pydantic import BaseModel,field_validator
from typing import List,Optional
import math


class MovieModel(BaseModel):
    movie_id:str
    movie_name:str
    year:Optional[int]=None
    overview:str
    director:str
    genre:List[str]
    cast:List[str]

    @field_validator("genre","cast",mode="before")
    @classmethod
    def split_values(cls,value):
        if isinstance(value,str):
            return [v.strip() for v in value.split(',')]
        return value
    
    @field_validator("year", mode="before")
    @classmethod
    def coerce_year(cls, v):
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return None
        if isinstance(v, str):
            digits = "".join(c for c in v if c.isdigit())
            return int(digits) if digits else None
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

