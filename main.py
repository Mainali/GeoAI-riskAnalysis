from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engineCore import getOSMData, analyzeRisk  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/infrastructures")
def getInfrastructures(lat: float, lon: float, withRiskAnalysis: bool = False):
    location, infraList = getOSMData(lat, lon)
    riskAnalysis = None
    if withRiskAnalysis:
        riskAnalysis = analyzeRisk(location, infraList)
    return {"location": location, "infraList": infraList, "riskAnalysis": riskAnalysis}



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
