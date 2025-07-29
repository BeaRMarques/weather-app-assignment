# PostgreSQL
POSTGRES_USER = "weather_app_user"
POSTGRES_PASSWORD = "weather_app_pass"
POSTGRES_DB = "weather_app"
POSTGRES_PORT = "5432"
POSTGRES_TABLE = "precipitation_location"
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgresql:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_URL_LOCAL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"

# Kafka
KAFKA_TOPIC_NAME = "weather_topic"
KAFKA_PORT = "9092"
KAFKA_BOOTSTRAP_SERVER = f"kafka:{KAFKA_PORT}"
KAFKA_BOOTSTRAP_SERVER_LOCAL = f"localhost:{KAFKA_PORT}"
KAKFA_NUMBER_PARTITIONS = 1
KAFKA_REPLICATION_FACTOR = 1

# Latitude and longitude coordinates
LOCATIONS: list[tuple[float, float]] = [
    (52.084516, 2.084516),
    (52.1, 5.0),
    (52.1, 5.1),
    (52.1, 5.2),
    (52.1, 5.3),
    (52.1, 5.4),
    (52.1, 5.5),
    (52.1, 5.6),
    (52.2, 5.0),
    (52.2, 5.1),
    (52.2, 5.2),
    (52.2, 5.3),
    (52.2, 5.4),
    (52.2, 5.5),
    (52.2, 5.6),
    (52.3, 5.0),
    (52.3, 5.1),
    (52.3, 5.2),
    (52.3, 5.3),
    (52.3, 5.4),
    (52.3, 5.5),
    (52.3, 5.6),
    (52.4, 5.0),
    (52.4, 5.1),
    (52.4, 5.2),
    (52.4, 5.3),
    (52.4, 5.4),
    (52.4, 5.5),
    (52.4, 5.6),
    (52.5, 5.0),
    (52.5, 5.1),
    (52.5, 5.2),
    (52.5, 5.3),
    (52.5, 5.4),
    (52.5, 5.5),
    (52.5, 5.6),
    (52.6, 5.0),
    (52.6, 5.1),
    (52.6, 5.2),
    (52.6, 5.3),
    (52.6, 5.4),
    (52.6, 5.5),
    (52.6, 5.6),
    (52.7, 5.0),
    (52.7, 5.1),
    (52.7, 5.2),
    (52.7, 5.3),
    (52.7, 5.4),
    (52.7, 5.5),
    (52.7, 5.6),
]
