from fastapi import FastAPI
from fastapi.responses import JSONResponse
from hoopstats import PlayerScraper

import numpy as np

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthcheck")
def healthcheck():
    return {"status_code": 200, "message": "Healthy API"}


@app.get("/{first_name}/{last_name}")
async def get_player_stats(first_name: str, last_name: str):
    p = PlayerScraper(first_name, last_name)
    df = p.get_stats_by_year(stat_type="per_game")

    # TODO - Create a Issue for Hoop Stats to address cleaning the data to a json object ...
    df = df.replace([np.inf, -np.inf, np.nan], None)

    # Convert DataFrame to JSON
    json_data = df.to_dict(orient="records")

    return JSONResponse(content=json_data)
