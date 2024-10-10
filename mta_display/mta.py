from fastapi import FastAPI
import requests

app = FastAPI(
    title="FastAPI MTA Service",
    description="Fetches MTA subway schedule",
    version="0.1.0",
)


@app.get("/")
def health():
    return {"message": "OK"}

@app.get("/stop/")
@app.get("/stop/{stop_id}")
def stop(stop_id: str = 'A14'):
    data = requests.get(f"https://demo.transiter.dev/systems/us-ny-subway/stops/{stop_id}").json()
    station = data['name']
    trains = [ {'line': s['trip']['route']['id'], 'direction': s['headsign'], 'track': s['track'], 'destination': s['trip']['destination']['name'], 'departureTime': s['departure']['time']} for s in data['stopTimes'][0:5]]
    return { 'name': station,
            'trains': trains }

# To run the app, % uvicorn mta:app --reload
# The app uses data from https://github.com/jamespfennell/transiter .