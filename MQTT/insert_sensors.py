
import json

from sqlalchemy import text

from dp import get_db


try:
    with open ("CoolBox_metadata.json", "r", encoding="UTF-8") as config_file:
        metadata = json.loads(config_file.read())
        with get_db() as _db:
            try:
                devices = metadata["devices"]
                device_ids = devices.keys()
                for device_id in device_ids:
                    device = devices.get(device_id)
                    device_name = device["sd"]
                    sensors = device["sensors"]
                    if sensors == {}:
                        continue
                    sensor_ids = sensors.keys()
                    for sensor_id in sensor_ids:
                        sensor = sensors.get(sensor_id)
                        if "unit" not in sensor:
                            continue
                    
                        #print(f"INSERT INTO sensor_dim(device_id, device, sensor, unit) VALUES({device_id}, {device_name}, {sensor_id}, {sensor["sd"]}, {sensor["unit"]})")
                        _query_str = "INSERT INTO sensor_dim(device_id, device_name, sensor_id, unit_name, unit_value) \
                            VALUES(:device_id, :device_name, :sensor_id, :unit_name, :unit_value)"
                        
                        _db.execute(text(_query_str), {"device_id": device_id, "device_name": device_name,"sensor_id": sensor_id, "unit_name": sensor["sd"], "unit_value": sensor["unit"]})    
                _db.commit()
                

            except Exception as e:
                print(e)
                _db.rollback()
                raise e
except Exception as e:
    print(e)
