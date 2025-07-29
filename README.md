# Assignmnent

## Diagram

![Diagram](diagram.png)


## Docker compose

```bash
docker-compose up
```

## Application to show real-time precipitation forecast for next hour

1. Install packages using poetry.
```bash
poetry install

```
2. In the folder weather app run:
```bash
uvicorn main:app --reload
```

3. Call the endpoint:
   http://127.0.0.1:8000/precipitation_now

