from fastapi import Depends, FastAPI
from sqlalchemy import text
from db import DB

app = FastAPI()

@app.get("/api/hello")
async def hello():
    return {"hello" : "hello"}

@app.get("/api/measurements")
async def get_all_measurements(db: DB):
    _query_str = "\
        SELECT device_name, unit_name, value, unit_value, year, month, day, hour, minute, sec FROM `measurement_fact` \
        JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id \
        JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key"
    rows = db.execute(text(_query_str))
    data = rows.mappings().all()
    return {"data" : data}

@app.get("/api/temperature/indoors/latest")
async def get_latest_temperature_indoors(db: DB):
    _query_str = "\
    SELECT device_name, unit_name, value, unit_value, year, month, day, hour, minute, sec \
    FROM `measurement_fact`\
    JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id \
    JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
    WHERE device_name = 'sisäilma' \
    AND unit_value = '°C' \
    AND measurement_fact.timestamp_key = \
        (   SELECT MAX(timestamp_dim.timestamp_key) FROM measurement_fact \
            JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
            JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id  \
            WHERE sensor_dim.device_name = 'sisäilma'\
            AND sensor_dim.unit_name = 'lämpötila'\
        )"
    rows = db.execute(text(_query_str))
    data = rows.mappings().all()
    return {"data" : data}
    
@app.get("/api/temperature/indoors/{week}")
async def get_weekly_temperature_indoors(week: int, db: DB):
    _query_str = f"\
        SELECT device_name, unit_name, value, unit_value, year, month, day, hour, minute, sec FROM measurement_fact \
        JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
        JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id \
        WHERE sensor_dim.device_name = 'sisäilma' \
        AND sensor_dim.unit_name = 'lämpötila' \
        AND timestamp_dim.year = 2024 \
        AND timestamp_dim.week = :week" 
    rows = db.execute(text(_query_str), {"week": week})  
    data = rows.mappings().all()
    return {"data": data}