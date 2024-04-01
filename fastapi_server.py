from fastapi import Depends, FastAPI
from sqlalchemy import text
from db import DB

app = FastAPI()

#Sisälämpötila on aina noin 18c joten turha sitä erikkeen hakea. Jätän nämä tähän jos jostain syystä niitä tarvitsee
"""
@app.get("/api/temperature/indoors/latest"
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
        AND sensor_dim.unit_name = 'lämpötila'\
        AND timestamp_dim.year = 2024 \
        AND timestamp_dim.week = :week" 
    rows = db.execute(text(_query_str), {"week": week})  
    data = rows.mappings().all()
    return {"data": data}

@app.get("/api/temperature/indoors/{month}/{day}")
async def get_daily_temperature_indoors(month: int, day: int, db: DB):
    _query_str = f"\
        SELECT device_name, unit_name, value, unit_value, year, month, day, hour, minute, sec FROM measurement_fact \
        JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
        JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id \
        WHERE sensor_dim.device_name = 'sisäilma' \
        AND sensor_dim.unit_name = 'lämpötila'\
        AND timestamp_dim.year = 2024 \
        AND timestamp_dim.month = :month\
        AND timestamp_dim.day = :day" 
    rows = db.execute(text(_query_str), {"month": month, "day": day})  
    data = rows.mappings().all()
    return {"data": data}
"""


@app.get("/api/temperature/outdoors/latest")
async def get_latest_temperature_outdoors(db: DB):
    _query_str = "\
        SELECT device_name, unit_name, value, unit_value, year, month, day, hour, minute, sec \
        FROM `measurement_fact`\
        JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id \
        JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
        WHERE device_name = 'Sääasema masto' \
        AND unit_value = '°C' \
        AND measurement_fact.timestamp_key = \
        (   SELECT MAX(timestamp_dim.timestamp_key) FROM measurement_fact \
            JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
            JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id  \
            WHERE sensor_dim.device_name = 'Sääasema masto'\
            AND sensor_dim.unit_name = 'Lämpötila'\
        )" 
    rows = db.execute(text(_query_str))
    data = rows.mappings().all()
    return {"data" : data}

@app.get("/api/temperature/outdoors/{week}")
async def get_weekly_temperature_outdoors(week: int, db: DB):
    _query_str = f"\
        SELECT device_name, unit_name, value, unit_value, year, month, day, hour, minute, sec FROM measurement_fact \
        JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
        JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id \
        WHERE sensor_dim.device_name = 'Sääasema masto' \
        AND sensor_dim.unit_name = 'Lämpötila'\
        AND timestamp_dim.year = 2024 \
        AND timestamp_dim.week = :week" 
    rows = db.execute(text(_query_str), {"week": week})  
    data = rows.mappings().all()
    return {"data": data}

@app.get("/api/temperature/outdoors/{month}/{day}")
async def get_daily_temperature_outdoors(month: int, day: int, db: DB):
    _query_str = f"\
        SELECT device_name, unit_name, value, unit_value, year, month, day, hour, minute, sec FROM measurement_fact \
        JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
        JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id \
        WHERE sensor_dim.device_name = 'Sääasema masto' \
        AND sensor_dim.unit_name = 'Lämpötila'\
        AND timestamp_dim.year = 2024 \
        AND timestamp_dim.month = :month\
        AND timestamp_dim.day = :day" 
    rows = db.execute(text(_query_str), {"month": month, "day": day})  
    data = rows.mappings().all()
    return {"data": data}


@app.get("/api/energy/{month}/{day}")
async def get_energy_consumption_by_day(month: int, day: int, db: DB):
    _query_str = f"\
    WITH ConsumedAmounts AS (\
    SELECT device_name, unit_name, ROUND(value - LAG(value) OVER (PARTITION BY sensor_dim.sensor_id ORDER BY year, month, day, hour, minute, sec), 2) \
    AS consumed_amount,unit_value, year, month, day, hour, minute, sec \
    FROM measurement_fact \
    JOIN timestamp_dim ON measurement_fact.timestamp_key = timestamp_dim.timestamp_key \
    JOIN sensor_dim ON measurement_fact.sensor_id = sensor_dim.sensor_id  \
    WHERE sensor_dim.unit_value = 'kWh'\
    AND sensor_dim.unit_name = 'Energiakulutus')\
    SELECT year, month, day, SUM(consumed_amount) AS total_consumed_amount\
    FROM ConsumedAmounts\
    WHERE consumed_amount > 0 AND month = :month AND day = :day\
    GROUP BY year, month, day"
    rows = db.execute(text(_query_str), {"month": month, "day": day})  
    data = rows.mappings().all()
    return {"data": data}
