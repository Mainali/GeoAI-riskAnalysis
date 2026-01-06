from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engineCore import getOSMData, analyzeInfrastructureRisk, analyzePointRisk

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/infrastructures")
async def getInfrastructures(lat: float, lon: float, withRiskAnalysis: bool = False):
    osm_data = getOSMData(lat, lon)
    if not osm_data:
        return {"location": "Unknown", "infraList": None, "riskAnalysis": "cannot get data for the location", "error": True}
    
    location, infraList = osm_data
    riskAnalysis = None
    if infraList and withRiskAnalysis:
        riskAnalysis = analyzeInfrastructureRisk(location, infraList)

    #convert infraList to geojson
    if infraList:
        geojson = { 
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [item['lon'], item['lat']]},
                "properties": {"name": item['name'], "type": item['amenity']}
                } for item in infraList
            ]
        }
    else:
        geojson = None

    return {"location": location, "infraList": geojson, "riskAnalysis": riskAnalysis}

@app.get("/api/analyzePoint")   
async def analyzePoint(amenity: str, name: str):
    riskAnalysis = analyzePointRisk(amenity, name)
    return {"riskAnalysis": riskAnalysis} 


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
