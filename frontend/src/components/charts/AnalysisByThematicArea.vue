<template>
  <div>
    <div>
      <h5>ANALYSIS BY THEMATIC AREA</h5>
      <label for="quarterSelect">Select Quarter:</label>
      <select id="quarterSelect" v-model="selectedQuarter">
        <option v-for="quarter in quarters" :key="quarter.id" :value="quarter.id">{{ quarter.label }}</option>
      </select>
    </div>
    <canvas id="thematicAreaChart" class="chart"></canvas>
    <canvas v-if="showAdditionalChart && outputNames.length > 0" id="additionalChart" class="chart"></canvas>
    <div v-if="showAdditionalChart && outputNames.length > 0">
      <textarea v-model="textAreaContent" rows="4" cols="50" placeholder="Comment on the performance per Output"></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { api } from '/src/boot/axios'; // Adjust path as per your project structure
import { fetchInstitutionData } from '/src/services/institutionAPI'; // Adjust import path as necessary


// State variables
const selectedQuarter = ref(null);
const quarters = [
  { id: 1, label: 'Q1' },
  { id: 2, label: 'Q2' },
  { id: 3, label: 'Q3' },
  { id: 4, label: 'Q4' },
];
const thematicAreaData = ref([]);
const thematicAreaNames = ref([]);
const thematicAreaNameMap = ref(new Map());
const outputNames = ref([]);
const showAdditionalChart = ref(false);
const textAreaContent = ref('');
let chartInstance = null;
let additionalChartInstance = null;
let additionalChartData = ref([]);

// Cache for thematic area data and reform area data
const thematicAreaCache = new Map();
const reformAreaCache = new Map();
const processedThematicAreaIds = new Set();

const fetchReformAreas = async (accessToken) => {
  try {
    const institutionId = await getInstitutionId(accessToken);
    const response = await api.get(`/reform-areas/institution/${institutionId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response && response.data && Array.isArray(response.data) && response.data.length > 0) {
      // Returning the reform areas data to be used later
      return response.data.map(reform => ({
        id: reform.id,
        reform_area: reform.reform_area,
        outputs: [], // Initialize outputs as an empty array
      }));
    } else {
      throw new Error('No reform areas found.');
    }
  } catch (error) {
    console.error('Error fetching reform areas:', error);
    return []; // Return an empty array in case of error
  }
};


const getInstitutionId = async (accessToken) => {
  try {
    const institutionData = await fetchInstitutionData(accessToken);
    return institutionData.id;
  } catch (error) {
    console.error('Error fetching institution ID:', error);
  }
};

const fetchReformAreaACRData = async (outputReportingPeriodId, reformAreaId) => {
  try {
    // Construct the URL with both parameters
    const response = await api.get(`/reform-area-acr/output-reporting-period/${outputReportingPeriodId}/reform-area/${reformAreaId}/`);

    // Map the response data to include reform_area_id
    return response.data.map(item => ({
      ...item,
      reform_area_id: item.reform_area_id,
    }));
  } catch (error) {
    console.error('Error fetching reform area ACR data:', error);
    throw error;
  }
};


// Fetch thematic area details using the ID
const fetchThematicAreaDetails = async (thematicAreaId) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) throw new Error('Access token not found. User is not authenticated.');

    const response = await api.get(`/thematic-areas/${thematicAreaId}/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    thematicAreaNameMap.value.set(thematicAreaId, response.data.thematic_area);
    return response.data;
  } catch (error) {
    console.error(`Error fetching thematic area details for ${thematicAreaId}:`, error.message);
    return null;
  }
};



// Fetch thematic area data based on thematic area ID
const fetchThematicAreaACRData = async (thematicAreaId) => {
  if (thematicAreaCache.has(thematicAreaId)) {
    console.log(`Cache hit for ID: ${thematicAreaId}`);
    return thematicAreaCache.get(thematicAreaId);
  }

  try {
    console.log(`Fetching data for ID: ${thematicAreaId}`);
    const response = await api.get(`/thematic-area-acr/${thematicAreaId}/`);
    console.log(`Response data for ID ${thematicAreaId}:`, response.data);
    const data = response.data;
    thematicAreaCache.set(thematicAreaId, data);
    return data;
  } catch (error) {
    console.error(`Error fetching thematic area ACR data for ${thematicAreaId}:`, error.message);
    return [];
  }
};


// Fetch reform area details and thematic area data
const fetchReformArea = async (reformAreaId) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) throw new Error('Access token not found. User is not authenticated.');

    const response = await api.get(`/reform_area/${reformAreaId}`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    const reformAreaData = response.data;

    const thematicAreaId = reformAreaData.thematic_area_id;

    if (thematicAreaId) {
      const thematicAreaDataResponse = await fetchThematicAreaACRData(thematicAreaId);
      await fetchThematicAreaDetails(thematicAreaId);
      return {
        reformAreaData,
        thematicAreaData: thematicAreaDataResponse,
        thematicAreaId: thematicAreaId,
      };
    } else {
      console.error('Thematic area ID not found in reform area details.');
      return {
        reformAreaData,
        thematicAreaData: null,
        thematicAreaId: null,
      };
    }
  } catch (error) {
    console.error('Error fetching reform area details:', error.message);
    return {
      reformAreaData: { reform_area: 'Error', thematic_area_id: null, outputs: [] },
      thematicAreaData: null,
      thematicAreaId: null,
    };
  }
};

const fetchData = async () => {
  try {
    if (!selectedQuarter.value) return;

    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Fetch reform areas using the access token
    const reformAreas = await fetchReformAreas(accessToken); // reformAreas now contains the data

    // If reformAreas is empty, return early
    if (!reformAreas.length) return;

    // Fetch reform area ACR data for each reform area ID and selected quarter
    const thematicAreaResponses = await Promise.all(
      reformAreas.map(async (reformArea) => {
        const reformAreaACRData = await fetchReformAreaACRData(selectedQuarter.value, reformArea.id);
        const thematicAreaDetails = await fetchReformArea(reformArea.id);

        // Avoid processing thematic areas that have been processed already
        if (thematicAreaDetails.thematicAreaId && !processedThematicAreaIds.has(thematicAreaDetails.thematicAreaId)) {
          thematicAreaNames.value.push(thematicAreaDetails.thematicAreaId);
          processedThematicAreaIds.add(thematicAreaDetails.thematicAreaId);
        }

        return thematicAreaDetails.thematicAreaData;
      })
    );

    thematicAreaData.value = thematicAreaResponses.flat();
    createChart();
  } catch (error) {
    console.error('Error fetching data:', error.message);
  }
};

// Create the chart using combined data
const createChart = () => {
  const ctx = document.getElementById('thematicAreaChart').getContext('2d');

  if (chartInstance) {
    chartInstance.destroy();
  }

  const removeDuplicates = (data) => {
    const uniqueLabels = new Set();
    const filteredData = data.filter(item => {
      if (uniqueLabels.has(item.thematic_area_id)) {
        return false;
      } else {
        uniqueLabels.add(item.thematic_area_id);
        return true;
      }
    });
    return filteredData;
  };

  const filteredThematicAreaData = removeDuplicates(thematicAreaData.value);

  if (filteredThematicAreaData.length === 0) {
    document.getElementById('thematicAreaChart').style.display = 'none';
    return;
  } else {
    document.getElementById('thematicAreaChart').style.display = 'block';
  }

  const datasets = [
    {
      label: 'Quarterly Target (100%)',
      data: filteredThematicAreaData.map(() => 100),
      backgroundColor: 'orange',
    },
    {
      label: 'Average ACR',
      data: filteredThematicAreaData.map(item => item.average_acr * 100),
      backgroundColor: 'blue',
      stack: 'combined',
    },
    {
      label: 'Extra',
      data: filteredThematicAreaData.map(item => item.extra_avg_acr * 100),
      backgroundColor: 'green',
      stack: 'combined',
    },
  ];

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: filteredThematicAreaData.map(item => thematicAreaNameMap.value.get(item.thematic_area_id) || item.thematic_area_id),
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return `${tooltipItem.dataset.label}: ${tooltipItem.raw.toFixed(2)}%`;
            },
          },
        },
      },
      scales: {
        y: {
          stacked: true,
        },
      },
    },
  });

  // Add event listener for click events on the chart
  ctx.onclick = async (event) => {
    const activePoints = chartInstance.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
    if (activePoints.length > 0) {
      const clickedElementIndex = activePoints[0].index;
      const clickedElement = activePoints[0].element;
      const thematicAreaId = filteredThematicAreaData[clickedElementIndex].thematic_area_id;
      const clickedDatasetLabel = chartInstance.data.datasets[activePoints[0].datasetIndex].label;

      if (thematicAreaId) {
        if (clickedDatasetLabel === 'Average ACR' || clickedDatasetLabel === 'Extra') {
          showAdditionalChart.value = true;
          await nextTick();
          fetchAndRenderAdditionalChart(thematicAreaId, clickedDatasetLabel);
        }
      }
    }
  };
};


// Fetch and render additional chart for the selected thematic area
const fetchAndRenderAdditionalChart = async (thematicAreaId, datasetLabel) => {
  try {
    // Fetch ACR data for the selected thematic area
    const reformAreaACRData = await fetchReformAreaACRData(selectedQuarter.value, thematicAreaId);

    // Process the data according to the clicked dataset
    const chartData = reformAreaACRData.map(item => ({
      label: `Reform Area ${item.reform_area_id}`,
      data: datasetLabel === 'Average ACR' ? [item.average_acr * 100] : [item.extra_avg_acr * 100],
      backgroundColor: datasetLabel === 'Average ACR' ? 'blue' : 'green',
    }));

    // Create a new chart
    const ctx = document.getElementById('additionalChart').getContext('2d');

    if (additionalChartInstance) {
      additionalChartInstance.destroy();
    }

    additionalChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: reformAreaACRData.map(item => `Reform Area ${item.reform_area_id}`),
        datasets: chartData,
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          tooltip: {
            callbacks: {
              label: function(tooltipItem) {
                return `${tooltipItem.dataset.label}: ${tooltipItem.raw.toFixed(2)}%`;
              },
            },
          },
        },
        scales: {
          y: {
            stacked: true,
          },
        },
      },
    });
  } catch (error) {
    console.error('Error fetching and rendering additional chart:', error.message);
  }
};

// Watch for changes in selected quarter to fetch new data
watch(selectedQuarter, (newQuarter) => {
  if (newQuarter) {
    fetchData();
  }
});

// Initialize chart on component mount
onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 400px;
}
</style>
