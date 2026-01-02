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
              <vue-markdown :source="data.riskAnalysis" />
            </div>
            <button @click="data = null" class="clear-btn">Clear Analysis</button>
          </div>
        </Transition>
        <p v-if="!data && !loading" style="color: #7f8c8d;">
          Click anywhere on the map to generate a spatial AI analysis.
        </p>
      </div>
    </div>

    <div style="flex: 1;">
      <l-map ref="map" v-model:zoom="zoom" :center="center" @click="handleMapClick">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <l-geo-json :geojson="data?.infraList" :options="geojsonOptions" />
        <l-marker v-for="(pt, i) in data?.infraList.features" :key="i"
          :lat-lng="[pt.geometry.coordinates[1], pt.geometry.coordinates[0]]">
          <l-popup>{{ pt.properties.name }} ({{ pt.properties.type }})</l-popup>
        </l-marker>
      </l-map>
    </div>
  </div>
</template>


<script setup>

import { ref } from 'vue';
import L from "leaflet";
import VueMarkdown from 'vue-markdown-render';
import { LMap, LTileLayer, LGeoJson, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

const zoom = ref(13);
const center = ref([51.505, -0.09]);
const data = ref(null);
const loading = ref(false);

const handleMapClick = async (event) => {
  const { lat, lng } = event.latlng;
  loading.value = true;
  try {
    const res = await fetch(`http://localhost:8000/api/infrastructures?withRiskAnalysis=true&lat=${lat}&lon=${lng}`);
    data.value = await res.json();
  } catch (err) {
    console.error("Analysis failed", err);
  } finally {
    loading.value = false;
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