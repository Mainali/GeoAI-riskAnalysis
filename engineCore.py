import requests
from google import genai
from dotenv import load_dotenv
import json
import os

def getOSMData(lat, lon, radius_meters =2000):

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:55];
    ( 

      node["amenity"~"hospital|police|fire_station|pharmacy"](around:{radius_meters},{lat},{lon}); 

      way["amenity"~"hospital|police|fire_station|pharmacy"](around:{radius_meters},{lat},{lon}); 

    ); 

    out center; 
    """
    print("fetching data from overpass api")

    try:
        response = requests.get(overpass_url, params={'data': query})
        data = response.json()
        dataList = []
        #extracting the data
        nodes = data['elements']
        locationName = data['elements'][0]['tags']['addr:city']
        print(len(nodes))
        for node in nodes:
            if node['type'] == 'node':
                tags = node['tags']
                dataList.append({
                    'name': tags.get('name', ''),
                    'amenity': tags.get('amenity', ''),
                    'lat': node['lat'],
                    'lon': node['lon']
                })
            elif node['type'] == 'way':
                tags = node['tags']
                dataList.append({
                    'name': tags.get('name', ''),
                    'amenity': tags.get('amenity', ''),
                    'lat': node['center']['lat'],
                    'lon': node['center']['lon']
                })
        print("Data fetched successfully")
        return locationName, dataList
    except Exception as e:
        print(f"Error fetching data from overpass api: {e}")
        return None


def analyzeInfrastructureRisk(locationName, infraList):
    #using google genai api to analyze the risk
    
    dataContext = "\n".join([f"{infra['name']} {infra['amenity']} {infra['lat']} {infra['lon']}" for infra in infraList])
    prompt = f""" 
    You are a Geospatial Risk Analyst.  
    Analyze the following critical infrastructure found within 2km of {locationName}: 
    {dataContext} 
    Task: 
    1. Identify the 'Primary Resilience Hub' (the most critical facility). 
    2. Identify a 'Single Point of Failure' (what's missing or overloaded?). 
    3. Provide a 2-sentence executive summary for a city planner. 
    Format the response in clean Markdown. 
    """
    #get api key from env file
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )

    return response.text


def analyzePointRisk(amenity: str, name: str):
    prompt =  f"Identify 2 safety risks and 1 optimization for a {amenity} named {name} in an urban setting." 
    #get api key from env file
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )

    return response.text
# infraList = getOSMData(40.7128, -74.0060)
# analyzeRisk("New York", infraList)