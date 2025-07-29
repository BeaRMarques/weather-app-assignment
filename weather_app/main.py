from fastapi import FastAPI
import json
from sqlalchemy import create_engine, text
from constants import POSTGRES_URL_LOCAL

app = FastAPI()
engine = create_engine(POSTGRES_URL_LOCAL)


@app.get("/precipitation_now")
def get_precipitation_now():
    """Returns the most recent precipitation forecast for the next hour, for each location."""
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
            SELECT p.lat, p.lon, p.total_precipitation, p.ingestion_time
            FROM precipitation_location as p
            JOIN (
                SELECT lat, lon, MAX(ingestion_time) as latest_ingestion_time
                FROM precipitation_location
                GROUP BY lat, lon
            ) as m
            ON p.lat = m.lat
            AND p.lon = m.lon
            AND p.ingestion_time = m.latest_ingestion_time;
            """
            )
        )
        return [
            {
                "lat": row.lat,
                "lon": row.lon,
                "total_precipitation": row.total_precipitation,
            }
            for row in result
        ]
