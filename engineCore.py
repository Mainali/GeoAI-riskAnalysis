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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(overpass_url, params={'data': query}, headers=headers, timeout=60)
        
        # Check for HTTP errors
        if response.status_code != 200:
            print(f"Overpass API Error: {response.status_code} - {response.text}")
            return None, None
            
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from Overpass API. Response text: {response.text[:500]}")
            return None, None

        dataList = []
        if not data or 'elements' not in data:
            print("No elements found in Overpass response")
            return None, None

        #extracting the data
        nodes = data['elements']
        if not nodes:
             print("Empty elements list from Overpass")
             return None, None

        # Safer way to get location name
        locationName = "Unknown Location"
        if nodes and 'tags' in nodes[0] and 'addr:city' in nodes[0]['tags']:
            locationName = nodes[0]['tags']['addr:city']
        
        print(len(nodes))
        for node in nodes:
            if node['type'] == 'node':
                tags = node.get('tags', {})
                dataList.append({
                    'name': tags.get('name', 'Unknown'),
                    'amenity': tags.get('amenity', 'Unknown'),
                    'lat': node['lat'],
                    'lon': node['lon']
                })
            elif node['type'] == 'way':
                tags = node.get('tags', {})
                if 'center' in node:
                    dataList.append({
                        'name': tags.get('name', 'Unknown'),
                        'amenity': tags.get('amenity', 'Unknown'),
                        'lat': node['center']['lat'],
                        'lon': node['center']['lon']
                    })
        print("Data fetched successfully")
        return locationName, dataList
    except Exception as e:
        print(f"Error fetching data from overpass api: {e}")
        return None, None


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