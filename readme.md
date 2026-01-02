# GeoAI Risk Analysis Engine

GeoAI Engine is a powerful tool that combines real-time geospatial data from OpenStreetMap with advanced AI analysis using Google's Gemini models. It helps city planners and risk analysts identify critical infrastructure, assess resilience, and pinpoint potential points of failure in urban environments.

![Dashboard Screenshot](/frontend/public/Screenshot.png)

## Feature Overview

- **🌍 Geospatial Discovery**: Automatically fetches critical infrastructure (Hospitals, Police, Fire Stations, Pharmacies) within a 2km radius of any coordinate using the Overpass API.
- **🤖 AI-Powered Risk Analysis**: Leverages Google Gemini 2.5 Flash to generate comprehensive risk reports, identifying resilience hubs and safety gaps.
- **📍 Interactive Visualization**: Displays infrastructure data on an interactive map using Leaflet and Vue.js.
- **🔍 Specific Point Analysis**: detailed safety and optimization analysis for individual facilities.

## Tech Stack

- **Backend**: FastAPI, Python
- **AI Engine**: Google GenAI (Gemini 2.5 Flash)
- **Data Source**: OpenStreetMap (Overpass API)
- **Frontend**: Vue.js 3, Vite, Leaflet (Vue-Leaflet)

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js & npm
- Google Cloud API Key (for Gemini)

### Backend Setup

1. Navigate to the root directory.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn requests google-genai python-dotenv
   ```
3. Create a `.env` file in the root directory and add your Google API Key:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Start the backend server:
   ```bash
   fastapi dev main.py
   ```
   The API will run at `http://127.0.0.1:8000`.

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:5173`.

## Usage

1. Open the frontend application in your browser.
2. Click on the map to select a location or use the default coordinates.
3. View the fetched infrastructure markers on the map.
4. The AI Risk Report will automatically generate and display key insights about the area's resilience.

## Future ToDos

- [ ] Add user authentication to save analysis history.
- [ ] Implement search functionality for specific locations.
- [ ] Add more infrastructure types to the OSM query.
- [ ] Integrate real-time traffic data for better risk assessment.
- [ ] Deploy to a public cloud provider.
