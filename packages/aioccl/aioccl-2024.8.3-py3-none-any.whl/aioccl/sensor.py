from __future__ import annotations

from dataclasses import dataclass
import enum
from typing import TypedDict

class CCLSensor:
    """Class that represents a CCLSensor object in the aioCCL API."""
    
    def __init__(self, key: str):
        """Initialize a CCL sensor."""
        self._value: None | str | int | float
    
        if key in CCL_SENSORS.keys():
            self._key = key
    
    @property
    def key(self) -> str:
        return self._key
    
    @property
    def name(self) -> str:
        return CCL_SENSORS[self._key].name
    
    @property
    def sensor_type(self) -> CCLSensorTypes:
        return CCL_SENSORS[self._key].sensor_type
    
    @property
    def compartment(self) -> str:
        return CCL_SENSORS[self._key].compartment.value
    
    @property
    def binary(self) -> bool:
        return CCL_SENSORS[self._key].binary

    @property
    def value(self):
        if self.sensor_type == CCLSensorTypes.CH_SENSOR_TYPE:
            return CCL_CH_SENSOR_TYPES.get(self._value)
        elif self.sensor_type in CCL_LEVEL_SENSORS:
            return 'Lv ' + self._value
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value

@dataclass
class CCLSensorPreset:
    name: str
    sensor_type: str
    compartment: str = None
    binary: bool = False
    
class CCLSensorTypes(enum.Enum):
    PRESSURE = 1
    TEMPERATURE = 2
    HUMIDITY = 3
    WIND_DIRECITON = 4
    WIND_SPEED = 5
    RAIN_RATE = 6
    RAINFALL = 7
    UVI = 8
    RADIATION = 9
    BATTERY_BINARY = 10
    CONNECTION = 11
    CH_SENSOR_TYPE = 12
    CO = 13
    CO2 = 14
    VOLATILE = 15
    VOC = 16
    PM10 = 17
    PM25 = 18
    AQI = 19
    LEAKAGE = 20
    BATTERY = 21

class CCLDeviceCompartment(enum.Enum):
    ADDITIONAL = 'Additional Sensors'
    STATUS = 'Status'

CCL_CH_SENSOR_TYPES: dict[str, str] = {
    '2': 'Thermo-Hygro',
    '3': 'Pool',
    '4': 'Soil',
}

CCL_SENSORS: dict[str, CCLSensorPreset] = {
    # Main Sensors 12-34
    'abar': CCLSensorPreset('Air Pressure (Absolute)', CCLSensorTypes.PRESSURE),
    'rbar': CCLSensorPreset('Air Pressure (Relative)', CCLSensorTypes.PRESSURE),
    't1dew': CCLSensorPreset('Index: Dew Point', CCLSensorTypes.TEMPERATURE),
    't1feels': CCLSensorPreset('Index: Feels Like', CCLSensorTypes.TEMPERATURE),
    't1heat': CCLSensorPreset('Index: Heat Index', CCLSensorTypes.TEMPERATURE),
    't1wbgt': CCLSensorPreset('Index: WBGT', CCLSensorTypes.TEMPERATURE),
    't1chill': CCLSensorPreset('Index: Wind Chill', CCLSensorTypes.TEMPERATURE),
    'inhum': CCLSensorPreset('Indoor Humidity', CCLSensorTypes.HUMIDITY),
    'intem': CCLSensorPreset('Indoor Temperature', CCLSensorTypes.TEMPERATURE),
    't1solrad': CCLSensorPreset('Light Intensity', CCLSensorTypes.RADIATION),
    't1hum': CCLSensorPreset('Outdoor Humidity', CCLSensorTypes.HUMIDITY),
    't1tem': CCLSensorPreset('Outdoor Temperature', CCLSensorTypes.TEMPERATURE),
    't1rainra': CCLSensorPreset('Rain Rate', CCLSensorTypes.RAIN_RATE),
    't1rainhr': CCLSensorPreset('Rainfall: Hourly ', CCLSensorTypes.RAINFALL),
    't1raindy': CCLSensorPreset('Rainfall: Daily', CCLSensorTypes.RAINFALL),
    't1rainwy': CCLSensorPreset('Rainfall: Weekly', CCLSensorTypes.RAINFALL),
    't1rainmth': CCLSensorPreset('Rainfall: Monthly', CCLSensorTypes.RAINFALL),
    't1rainyr': CCLSensorPreset('Rainfall: Yearly', CCLSensorTypes.RAINFALL),
    't1uvi': CCLSensorPreset('UV Index', CCLSensorTypes.UVI),
    't1wdir': CCLSensorPreset('Wind Direction', CCLSensorTypes.WIND_DIRECITON),
    't1wgust': CCLSensorPreset('Wind Gust', CCLSensorTypes.WIND_SPEED),
    't1ws': CCLSensorPreset('Wind Speed', CCLSensorTypes.WIND_SPEED),
    't1ws10mav': CCLSensorPreset('Wind Speed (10 mins AVG.)', CCLSensorTypes.WIND_SPEED),
    # Additional Sensors 35-77
    't11co': CCLSensorPreset('Air Quality: CO', CCLSensorTypes.CO, CCLDeviceCompartment.ADDITIONAL),
    't10co2': CCLSensorPreset('Air Quality: CO\u2082', CCLSensorTypes.CO2, CCLDeviceCompartment.ADDITIONAL),
    't9hcho': CCLSensorPreset('Air Quality: Formaldehyde', CCLSensorTypes.VOLATILE, CCLDeviceCompartment.ADDITIONAL),
    't8pm10': CCLSensorPreset('Air Quality: PM10', CCLSensorTypes.PM10, CCLDeviceCompartment.ADDITIONAL),
    't8pm10ai': CCLSensorPreset('Air Quality: PM10 AQI', CCLSensorTypes.AQI, CCLDeviceCompartment.ADDITIONAL),
    't8pm25': CCLSensorPreset('Air Quality: PM2.5', CCLSensorTypes.PM25, CCLDeviceCompartment.ADDITIONAL),
    't8pm25ai': CCLSensorPreset('Air Quality: PM2.5 AQI', CCLSensorTypes.AQI, CCLDeviceCompartment.ADDITIONAL),
    't9voclv': CCLSensorPreset('Air Quality: VOC Level', CCLSensorTypes.VOC, CCLDeviceCompartment.ADDITIONAL),
    't234c1tem': CCLSensorPreset('CH1 Temperature', CCLSensorTypes.TEMPERATURE, CCLDeviceCompartment.ADDITIONAL),
    't234c1hum': CCLSensorPreset('CH1 Humidity', CCLSensorTypes.HUMIDITY, CCLDeviceCompartment.ADDITIONAL),
    't234c1tp': CCLSensorPreset('CH1 Type', CCLSensorTypes.CH_SENSOR_TYPE, CCLDeviceCompartment.ADDITIONAL),
    't234c2tem': CCLSensorPreset('CH2 Temperature', CCLSensorTypes.TEMPERATURE, CCLDeviceCompartment.ADDITIONAL),
    't234c2hum': CCLSensorPreset('CH2 Humidity', CCLSensorTypes.HUMIDITY, CCLDeviceCompartment.ADDITIONAL),
    't234c2tp': CCLSensorPreset('CH2 Type', CCLSensorTypes.CH_SENSOR_TYPE, CCLDeviceCompartment.ADDITIONAL),
    't234c3tem': CCLSensorPreset('CH3 Temperature', CCLSensorTypes.TEMPERATURE, CCLDeviceCompartment.ADDITIONAL),
    't234c3hum': CCLSensorPreset('CH3 Humidity', CCLSensorTypes.HUMIDITY, CCLDeviceCompartment.ADDITIONAL),
    't234c3tp': CCLSensorPreset('CH3 Type', CCLSensorTypes.CH_SENSOR_TYPE, CCLDeviceCompartment.ADDITIONAL),
    't234c4tem': CCLSensorPreset('CH4 Temperature', CCLSensorTypes.TEMPERATURE, CCLDeviceCompartment.ADDITIONAL),
    't234c4hum': CCLSensorPreset('CH4 Humidity', CCLSensorTypes.HUMIDITY, CCLDeviceCompartment.ADDITIONAL),
    't234c4tp': CCLSensorPreset('CH4 Type', CCLSensorTypes.CH_SENSOR_TYPE, CCLDeviceCompartment.ADDITIONAL),
    't234c5tem': CCLSensorPreset('CH5 Temperature', CCLSensorTypes.TEMPERATURE, CCLDeviceCompartment.ADDITIONAL),
    't234c5hum': CCLSensorPreset('CH5 Humidity', CCLSensorTypes.HUMIDITY, CCLDeviceCompartment.ADDITIONAL),
    't234c5tp': CCLSensorPreset('CH5 Type', CCLSensorTypes.CH_SENSOR_TYPE, CCLDeviceCompartment.ADDITIONAL),
    't234c6tem': CCLSensorPreset('CH6 Temperature', CCLSensorTypes.TEMPERATURE, CCLDeviceCompartment.ADDITIONAL),
    't234c6hum': CCLSensorPreset('CH6 Humidity', CCLSensorTypes.HUMIDITY, CCLDeviceCompartment.ADDITIONAL),
    't234c6tp': CCLSensorPreset('CH6 Type', CCLSensorTypes.CH_SENSOR_TYPE, CCLDeviceCompartment.ADDITIONAL),
    't234c7tem': CCLSensorPreset('CH7 Temperature', CCLSensorTypes.TEMPERATURE, CCLDeviceCompartment.ADDITIONAL),
    't234c7hum': CCLSensorPreset('CH7 Humidity', CCLSensorTypes.HUMIDITY, CCLDeviceCompartment.ADDITIONAL),
    't234c7tp': CCLSensorPreset('CH7 Type', CCLSensorTypes.CH_SENSOR_TYPE, CCLDeviceCompartment.ADDITIONAL),
    't6c1wls': CCLSensorPreset('Leakage CH1', CCLSensorTypes.LEAKAGE, CCLDeviceCompartment.ADDITIONAL, True),
    # Status 78-119
    't234c1bat': CCLSensorPreset('Battery: CH1', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't234c2bat': CCLSensorPreset('Battery: CH2', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't234c3bat': CCLSensorPreset('Battery: CH3', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't234c4bat': CCLSensorPreset('Battery: CH4', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't234c5bat': CCLSensorPreset('Battery: CH5', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't234c6bat': CCLSensorPreset('Battery: CH6', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't234c7bat': CCLSensorPreset('Battery: CH7', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't11bat': CCLSensorPreset('Battery: CO', CCLSensorTypes.BATTERY, CCLDeviceCompartment.STATUS),
    't10bat': CCLSensorPreset('Battery: CO\u2082', CCLSensorTypes.BATTERY, CCLDeviceCompartment.STATUS),
    'inbat': CCLSensorPreset('Battery: Console', CCLSensorTypes.BATTERY_BINARY, True),
    't9bat': CCLSensorPreset('Battery:Formaldehyde/VOC', CCLSensorTypes.BATTERY, CCLDeviceCompartment.STATUS),
    't6c1bat': CCLSensorPreset('Battery: Leakage CH1', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't1bat': CCLSensorPreset('Battery: Main Sensor Array', CCLSensorTypes.BATTERY_BINARY, CCLDeviceCompartment.STATUS, True),
    't8bat': CCLSensorPreset('Battery: PM2.5/10', CCLSensorTypes.BATTERY, CCLDeviceCompartment.STATUS),
    't234c1cn': CCLSensorPreset('Connection: CH1', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't234c2cn': CCLSensorPreset('Connection: CH2', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't234c3cn': CCLSensorPreset('Connection: CH3', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't234c4cn': CCLSensorPreset('Connection: CH4', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't234c5cn': CCLSensorPreset('Connection: CH5', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't234c6cn': CCLSensorPreset('Connection: CH6', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't234c7cn': CCLSensorPreset('Connection: CH7', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't11cn': CCLSensorPreset('Connection: CO', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't10cn': CCLSensorPreset('Connection: CO\u2082', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't9cn': CCLSensorPreset('Connection: Formaldehyde/VOC', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't6c1cn': CCLSensorPreset('Connection: Leakage CH1', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't1cn': CCLSensorPreset('Connection: Main Sensor Array', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
    't8cn': CCLSensorPreset('Connection: PM2.5/10', CCLSensorTypes.CONNECTION, CCLDeviceCompartment.STATUS, True),
}

CCL_LEVEL_SENSORS = (CCLSensorTypes.VOC, CCLSensorTypes.BATTERY)