import dagster as dg
from ..resources import PostgresResource
from ..api_client.geocoding.schemas import LocationRecord

@dg.asset(
        group_name='weather',
        kinds={'postgres'},
        deps=['location_model']
        )
def location(
#     context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    location_model
    ) -> None:
    """write to location table in postgres"""
    postgres_session = postgres.session
    loc_record = LocationRecord(**location_model.model_dump(exclude='postcodes_list'))

    # upsert location record
    postgres_session.merge(loc_record)
    postgres_session.commit()
