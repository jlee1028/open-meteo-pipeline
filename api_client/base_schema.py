from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func
from datetime import datetime, timezone

Base = declarative_base()

class TimestampMixin:
    db_create_timestamp = Column(DateTime, server_default=func.now())
    db_update_timestamp = Column(DateTime, server_default=func.now(), onupdate=datetime.now(timezone.utc))
