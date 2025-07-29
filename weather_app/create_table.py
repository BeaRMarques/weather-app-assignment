"""Creates table `precipitation_location` in PostgreSQL database."""

import logging
import sys
import time

from constants import POSTGRES_TABLE, POSTGRES_URL
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

Base = declarative_base()


class PrecipitationLocation(Base):
    __tablename__ = POSTGRES_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    lat = Column(Float)
    lon = Column(Float)
    total_precipitation = Column(Float)
    ingestion_time = Column(String)


for n in range(5):
    try:
        engine = create_engine(POSTGRES_URL)
        conn = engine.connect()
        conn.close()
        break
    except Exception as e:
        logging.warning("Postgres database not ready.")
        time.sleep((2**n) + 1)
else:
    logging.error("Could not connect to Postgres database.")

try:
    Base.metadata.create_all(engine)
    logger.info("Table `precipitation_location` was created successfully.")
except Exception as e:
    logger.error(f"Error when creating table `precipitation_location`: {e}.")
