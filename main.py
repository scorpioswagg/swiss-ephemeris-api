from fastapi import FastAPI, Header
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime

app = FastAPI()

API_KEY = "cosmicblueprintsecret"

class BirthData(BaseModel):
    year: int
    month: int
    day: int
    hour: float
    latitude: float
    longitude: float

@app.get("/")
def root():
    return {"status": "Swiss Ephemeris API running"}

@app.post("/calculate-chart")
def calculate_chart(data: BirthData, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        return {"error": "Invalid API key"}

    jd = swe.julday(
        data.year,
        data.month,
        data.day,
        data.hour
    )

    sun = swe.calc_ut(jd, swe.SUN)
    moon = swe.calc_ut(jd, swe.MOON)

    return {
        "sun_longitude": sun[0][0],
        "moon_longitude": moon[0][0],
        "julian_day": jd
    }
