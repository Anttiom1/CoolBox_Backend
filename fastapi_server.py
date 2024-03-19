from fastapi import FastAPI
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
    

