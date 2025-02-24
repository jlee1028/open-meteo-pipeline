from pydantic import BaseModel, Field, computed_field
from typing import Optional

class Location(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = None
    feature_code: Optional[str] = None
    country_code: Optional[str] = None
    admin1_id: Optional[int] = None
    admin2_id: Optional[int] = None
    admin3_id: Optional[int] = None
    admin4_id: Optional[int] = None
    timezone: Optional[str] = None
    population: Optional[int] = None
    postcodes_list: Optional[list[str]] = Field(alias='postcodes', default=None)
    country_id: Optional[int] = None
    country: Optional[str] = None
    admin1: Optional[str] = None
    admin2: Optional[str] = None
    admin3: Optional[str] = None
    admin4: Optional[str] = None
    
    @computed_field
    def postcodes(self) -> str:
        return ','.join(self.postcodes_list)
