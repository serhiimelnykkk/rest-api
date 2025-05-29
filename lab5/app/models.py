from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository, PydanticObjectId

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: int

class BookCreate(BookBase):
    pass 
class BookDB(BookBase):
    id: PydanticObjectId = Field(default=None, alias="_id") 

    class Config:
        json_encoders = {
            PydanticObjectId: str 
        }
        allow_population_by_field_name = True 