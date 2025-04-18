from ..base_schema import Base, TimestampMixin
from sqlalchemy import Column, Integer, Float, String

class LocationRecord(Base, TimestampMixin):
    __tablename__ = 'weather__location'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    feature_code = Column(String)
    country_code = Column(String)
    admin1_id = Column(Integer)
    admin2_id = Column(Integer)
    admin3_id = Column(Integer)
    admin4_id = Column(Integer)
    timezone = Column(String)
    population = Column(Integer)
    postcodes = Column(String)
    country_id = Column(Integer)
    country = Column(String)
    admin1 = Column(String)
    admin2 = Column(String)
    admin3 = Column(String)
    admin4 = Column(String)
