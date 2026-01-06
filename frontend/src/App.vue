<template>
  <div style="display: flex; height: 100vh;">
    <div style="display: flex; width: 30%; height: 100vh; font-family: sans-serif;">
      <div style="width: 100%; padding: 20px; overflow-y: auto; border-right: 1px solid #ccc; background: #fafafa;">
        <h1 style="color: #2c3e50;">Geo-AI Engine</h1>
        <div v-if="loading" class="loading-bar"></div>
        <Transition name="slide-fade">
          <div v-if="data" class="report-container">
            <h3 style="margin-top: 0;">AI Risk Report</h3>
            <div class="analysis-box">
              <p v-if="data.error" style="color: #e74c3c; font-weight: bold;">{{ data.riskAnalysis }}</p>
              <vue-markdown v-else :source="data.riskAnalysis" />
            </div>
          </div>
        </Transition>

        <Transition name="slide-fade">
          <div v-if="pointAnalysisLoading" class="analysis-box" style="margin-top: 20px; border-left-color: #3498db;">
            <p style="margin: 0; color: #3498db;">Running detailed analysis on specific point...</p>
          </div>
        </Transition>

        <Transition name="slide-fade">
          <div v-if="pointAnalysis" class="report-container" style="margin-top: 20px;">
            <h3 style="margin-top: 0;">Point Analysis: {{ pointAnalysis.name }}</h3>
            <div class="analysis-box" style="border-left-color: #3498db;">
              <vue-markdown :source="pointAnalysis.analysis" />
            </div>
            <button @click="pointAnalysis = null" class="clear-btn" style="background: #95a5a6;">Close Point
              Analysis</button>
          </div>
        </Transition>

        <div v-if="(data || pointAnalysis) && !loading && !pointAnalysisLoading" style="margin-top: 20px;">
          <button @click="{ data = null; pointAnalysis = null; }" class="clear-btn">Clear All Analysis</button>
        </div>

        <p v-if="!data && !loading" style="color: #7f8c8d;">
          Click anywhere on the map to generate a spatial AI analysis.
        </p>
      </div>
    </div>

    <div style="flex: 1;">
      <l-map ref="map" v-model:zoom="zoom" :center="center" :use-global-leaflet="false"
        style="height: 100%; width: 100%" @click="handleMapClick">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <l-marker v-for="(pt, i) in data?.infraList.features" :key="i"
          :lat-lng="[pt.geometry.coordinates[1], pt.geometry.coordinates[0]]">
          <l-popup>
            <div style="min-width: 200px;">
              <h3 style="margin: 0 0 5px;">{{ pt.properties.name }}</h3>
              <p style="margin: 0 0 10px; color: #666;">{{ pt.properties.type }}</p>

              <button @click="analyzeSpecificPoint(pt)"
                style="background: #42b983; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                Analyze Risks
              </button>
            </div>
          </l-popup>
        </l-marker>
      </l-map>
    </div>
  </div>
</template>


<script setup>

import { ref } from 'vue';
import L from "leaflet";
import VueMarkdown from 'vue-markdown-render';
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

const zoom = ref(4);
const center = ref([39.8283, -98.5795]);
const data = ref(null);
const loading = ref(false);
const pointAnalysis = ref(null);
const pointAnalysisLoading = ref(false);

const handleMapClick = async (event) => {
  const { lat, lng } = event.latlng;
  loading.value = true;
  data.value = null; // Reset previous data
  pointAnalysis.value = null; // Reset point analysis
  try {
    const res = await fetch(`http://localhost:8000/api/infrastructures?withRiskAnalysis=true&lat=${lat}&lon=${lng}`);
    data.value = await res.json();
  } catch (err) {
    console.error("Analysis failed", err);
  } finally {
    loading.value = false;
  }
};

const analyzeSpecificPoint = async (feature) => {
  pointAnalysisLoading.value = true;
  pointAnalysis.value = null;
  try {
    const res = await fetch(`http://localhost:8000/api/analyzePoint?amenity=${feature.properties.type}&name=${feature.properties.name}`);
    const result = await res.json();
    pointAnalysis.value = {
      name: feature.properties.name,
      type: feature.properties.type,
      analysis: result.riskAnalysis
    };
  } catch (err) {
    console.error("Point analysis failed", err);
  } finally {
    pointAnalysisLoading.value = false;
  }
};

</script>

<style scoped>
/* 1. Define the Slide-Fade Animation */
.slide-fade-enter-active {
  transition: all 0.5s ease-out;
}


.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

/* 2. Professional Styling */
.analysis-box {
  background: white;
  padding: 15px;
  border-left: 4px solid #42b983;
  /* Vue Green */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  line-height: 1.6;
  font-size: 14px;
}

.loading-bar {
  height: 4px;
  width: 100%;
  background: #42b983;
  animation: loading 1.5s infinite;
  margin-bottom: 10px;
}

@keyframes loading {
  0% {
    opacity: 0.2;
  }

  50% {
    opacity: 1;
  }

  100% {
    opacity: 0.2;
  }
}

.clear-btn {
  margin-top: 15px;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}
</style>