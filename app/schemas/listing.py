# app/schemas/listing.py
from pydantic import BaseModel, Field
from typing import Union

class ListingCreate(BaseModel):
    title: str
    address: str
    zip_code: str = Field(..., alias="zipCode")
    year_built: Union[int, None] = Field(None, alias="yearBuilt")
    square_footage: int = Field(..., alias="squareFootage")
    price: int
    description: Union[str, None] = None
    image_url: Union[str, None] = Field(None, alias="imageUrl")
    arv: Union[int, None] = None
    approved: bool = False
    lat: Union[float, None] = None
    lng: Union[float, None] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }

class ListingRead(ListingCreate):
    id: int
    owner_id: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
