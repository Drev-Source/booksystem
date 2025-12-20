import hashlib
import json
import os
import requests

from datetime import datetime
from pydantic import BaseModel
from typing import Any


Response = requests.Response
BASE_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"


class YRUnitMetadata(BaseModel):
    air_pressure_at_sea_level: str
    air_temperature: str
    cloud_area_fraction: str
    relative_humidity: str
    wind_from_direction: str
    wind_speed: str


class YRWeatherData(BaseModel):
    air_pressure_at_sea_level: float
    air_temperature: float
    cloud_area_fraction: float
    relative_humidity: float
    wind_from_direction: float
    wind_speed: float


class YRTimeWeatherData(BaseModel):
    time: str
    data: YRWeatherData


class YRData(BaseModel):
    last_modified: str
    expires: datetime
    units: YRUnitMetadata
    timeseries_data: list[YRTimeWeatherData]


def get_current_timzeone_time(timezone: str) -> None:
    #TODO Implement this
    raise NotImplementedError("Function is not implemented")


class YRClient:

    def get_weather(self, alt: int = 0, lat: float = 56.6759, lon: float = 12.8582) -> YRData:
        filename = self.hash_content(str(alt)+str(lat)+str(lon)) + ".json"
        yr_cache = self.check_cache_isvalid(filename)

        #TODO Incorporate proper check for the expiration
        #if yr_cache:
        #    return yr_cache

        last_modified = yr_cache.last_modified if yr_cache else ""
        headers = {
            "User-Agent": "booksystem/0.1 github.com/Drev-Source/booksystem",
            "If-Modified-Since": last_modified
        }
        params = {
            "altitude": alt,
            "lat": round(lat, 4),
            "lon": round(lon, 4)
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        
        if response.status_code == 200:
            yr_data = self.get_yr_data(response.headers, response.json())
            self.save_cache(filename, yr_data)
            return yr_data
        elif response.status_code == 304:
            return yr_cache
        
        raise Exception(f"Unknown error fetching data, repsonse {response}")


    def get_current_weather(self) -> YRWeatherData | None:
        yr_data = self.get_weather()
        if not yr_data or not yr_data.timeseries_data:
            return None
        
        #TODO return the acutal current weather data based on current time
        #current_gmt_time = get_current_timzeone_time("gmt")
        #for data in yr_data.timeseries_data:
        #    if data.time.hour == current_gmt_time.hour:
        #       return data
        
        return yr_data.timeseries_data[0].data


    def get_units_data(self, data: Any) -> YRUnitMetadata:
        units = data.get("properties", {}).get("meta", {}).get("units", {})

        if not units:
            raise ValueError("Invalid data, couldn't get unit metadata from data.")
        
        return YRUnitMetadata.model_validate(units)
    

    def get_timeseries_data(self, data: Any) -> list[YRTimeWeatherData]:
        timeseries = data.get("properties", {}).get("timeseries", [])
        if not timeseries:
            raise ValueError("Invalid data, couldn't get timeseries from data.")

        timeseries_data = [
                    YRTimeWeatherData(
                        time=t.get("time", ""),
                        data=YRWeatherData.model_validate(t.get("data", {}).get("instant", {}).get("details", {}))
                    )
                    for t in timeseries
                ]

        if not timeseries_data:
            raise ValueError("Invalid data, couldn't get timeseries data from data.")
        
        return timeseries_data


    def get_expire_date(self, headers: dict[Any]) -> datetime:
        date_format = "%a, %d %b %Y %H:%M:%S %Z"
        date = headers.get("Expires", "")

        return datetime.strptime(date, date_format)


    def get_yr_data(self, headers: dict[Any], data: dict[Any]) -> YRData:
        units = self.get_units_data(data)
        timeseries_data = self.get_timeseries_data(data)
        last_modified = headers.get("Last-Modified", "")
        expires = self.get_expire_date(headers)

        return YRData(last_modified=last_modified, expires=expires, units=units, timeseries_data=timeseries_data)


    def check_cache_isvalid(self, filename: str) -> YRData | None:
        data = self.load_cache(filename)

        if not data:
           print("There is no weather data cache")
           return None

        #TODO implement this
        #if data.expiration < get_current_timzeone_time("gmt"):
        #   print("Weather data cache expired")
        #   return None
        #else:
        #   print("Valid weather data cache exists")
        #   return data

        return data


    def save_cache(self, filename: str, yr_data: YRData) -> None:
        if not self.check_cache_isvalid(filename):
            print("Caching weather data")
            with open(filename, "w") as f:
                f.write(yr_data.model_dump_json())


    def load_cache(self, filename: str) -> YRData | None:
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
           return YRData.model_validate(json.load(f))


    def hash_content(self, content: str):
        return hashlib.sha256(content.encode()).hexdigest()
