<template>
  <div>
    <div>
      <h5>QUARTER AGAINST QUARTER LEVEL OF PERFORMANCE ANALYSIS</h5>
      <label for="quarterSelect">Select Quarter:</label>
      <select id="quarterSelect" v-model="selectedQuarter">
        <option v-for="quarter in quarters" :key="quarter.id" :value="quarter.id">{{ quarter.label }}</option>
      </select>
    </div>
    <canvas id="reformAreaChart" class="chart"></canvas>
    <canvas v-if="showAdditionalChart && outputNames.length > 0" id="additionalChart" class="chart"></canvas>
    <div v-if="showAdditionalChart && outputNames.length > 0">
      <textarea v-model="textAreaContent" rows="4" cols="50" placeholder="Comment on the performance per Output"></textarea>
      <br>

      <q-btn unelevated color="positive" label="Save" @click="saveProgress(selectedReformAreaId)" style="float: left;"/>
    </div>
    <!-- Success and Error Messages -->
    <div v-if="successMessage || errorMessage" class="message">
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { api } from '/src/boot/axios'; // Adjust path as per your project structure
import { fetchInstitutionData } from '/src/services/institutionAPI'; // Adjust import path as necessary
import ChartDataLabels from 'chartjs-plugin-datalabels';


const selectedQuarter = ref(null);
const quarters = [
  { id: 1, label: 'Q1' },
  { id: 2, label: 'Q2' },
  { id: 3, label: 'Q3' },
  { id: 4, label: 'Q4' },
];
const reformAreaACRData = ref([]);
const reformAreaNames = ref([]);
const outputNames = ref([]);
const showAdditionalChart = ref(false);
const textAreaContent = ref('');
const successMessage = ref('');
const errorMessage = ref('');
let chartInstance = null;
let additionalChartInstance = null;
const selectedReformAreaId = ref(null);
const quarterId = ref(null); // Add this reactive variable

// Store the fetched reform areas globally or in a relevant state
let reformAreas = [];

const fetchReformAreas = async (accessToken) => {
  try {
    const institutionId = await getInstitutionId(accessToken);
    const response = await api.get(`/reform-areas/institution/${institutionId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response && response.data && Array.isArray(response.data) && response.data.length > 0) {
      reformAreas = response.data.map(reform => ({
        id: reform.id,
        reform_area: reform.reform_area,
        outputs: [], // Initialize outputs as an empty array
      }));


    } else {
      throw new Error('No reform areas found.');
    }
  } catch (error) {
    console.error('Error fetching reform areas:', error);
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

const fetchReformArea = async (reformAreaId) => {
  try {
    console.log('Fetching reform area with ID:', reformAreaId);

    const accessToken = localStorage.getItem('accessToken');
    console.log('Access token retrieved:', accessToken);

    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    const response = await api.get(`/reform_area/${reformAreaId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    console.log('API response received:', response);

    const reformArea = response.data;
    console.log('Reform area data:', reformArea);

    if (!reformArea || !Array.isArray(reformArea.outcomes)) {
      throw new Error('Invalid or missing reform area data.');
    }

    const outputDetails = reformArea.outcomes.flatMap(outcome =>
      (outcome.outputs || []).map(output => {
        const outputAcrs = output.output_acrs || [];
        console.log(`Processing output ID ${output.id} with ACRs:`, outputAcrs);

        const averageAcr = outputAcrs.length > 0
          ? outputAcrs.reduce((total, acr) => total + acr.average_acr, 0) / outputAcrs.length
          : 0;

        const outputIndicators = output.output_indicators || [];
        const indicatorsDetails = outputIndicators.map(indicator => {
          const indicatorOutputActuals = indicator.output_actual || [];
          const extraAcr = indicatorOutputActuals.extra_acr || 0;

          return {
            indicator_id: indicator.id,
            indicator_name: indicator.indicator,
            extra_acr: extraAcr,
          };
        });

        const extraAvgAcr = indicatorsDetails.length > 0
          ? indicatorsDetails.reduce((total, indicator) => total + indicator.extra_acr, 0) / indicatorsDetails.length
          : 0;

        console.log(`Calculated average ACR: ${averageAcr}, extra average ACR: ${extraAvgAcr} for output ID ${output.id}`);

        return {
          id: output.id,
          name: output.output,
          average_acr: averageAcr,
          extra_avg_acr: extraAvgAcr,
          output_acrs: outputAcrs,
          indicators: indicatorsDetails, // Include indicators with extra_acr for each indicator
        };
      })
    );

    console.log('Output details processed:', outputDetails);

    return {
      reform_area: reformArea.reform_area || 'Unknown',
      outputs: outputDetails,
    };

  } catch (error) {
    console.error('Error fetching reform area details:', error.message);
    throw error;
  }
};



const fetchData = async () => {
  try {
    if (!selectedQuarter.value) return;

    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    quarterId.value = selectedQuarter.value; // Store the selected quarter ID

    // Fetch reform areas to get their IDs using the access token
    await fetchReformAreas(accessToken); // Pass accessToken here

    // Check if we have reform areas
    if (reformAreas.length === 0) {
      throw new Error('No reform areas available to fetch ACR data.');
    }

    // Fetch ACR data for the selected quarter
    const reformAreaACRDataPromises = reformAreas.map(async (reformArea) => {
      const reformAreaACRResponse = await fetchReformAreaACRData(quarterId.value, reformArea.id);
      return reformAreaACRResponse;
    });

    const reformAreaACRResponses = await Promise.all(reformAreaACRDataPromises);

    if (reformAreaACRResponses.length === 0) {
      reformAreaACRData.value = [];
      reformAreaNames.value = [];
      outputNames.value = [];
      createChart();
      return;
    }

    // Flatten the responses if necessary
    reformAreaACRData.value = reformAreaACRResponses.flat();

    const reformAreaDetails = await Promise.all(
      reformAreaACRData.value.map(async (item) => {
        try {
          const details = await fetchReformArea(item.reform_area_id);
          return {
            name: details.reform_area || 'Unknown',
            outputs: details.outputs,
          };
        } catch (error) {
          console.error('Error fetching reform area details:', error);
          return { name: 'Error', outputs: [] };
        }
      })
    );

    reformAreaNames.value = reformAreaDetails.map(detail => detail.name);
    outputNames.value = reformAreaDetails.flatMap(detail => detail.outputs.map(output => output.name));

    createChart();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};


const createChart = () => {
  const ctx = document.getElementById('reformAreaChart').getContext('2d');

  if (chartInstance) {
    chartInstance.destroy();
  }

  const datasets = [
    {
      label: 'Quarterly Target (100%)',
      data: reformAreaACRData.value.map(() => 100),
      backgroundColor: 'orange',
    },
    {
      label: quarters.find(q => q.id === selectedQuarter.value)?.label || 'Selected Quarter',
      data: reformAreaACRData.value.map(item => item.average_acr * 100),
      backgroundColor: 'blue',
      stack: 'combined',
    },
    {
      label: 'EXTRA',
      data: reformAreaACRData.value.map(item => item.extra_avg_acr * 100),
      backgroundColor: 'green',
      stack: 'combined',
    }
  ];

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: reformAreaNames.value,
      datasets: datasets,
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          max: 160,
          stacked: true,
        },
      },
      onClick: async (event, elements) => {
        if (elements.length > 0) {
          const index = elements[0].index;
          selectedReformAreaId.value = reformAreaACRData.value[index].reform_area_id; // Set the selected reform area ID
          const reformAreaId = selectedReformAreaId.value;
          const reformAreaDetails = await fetchReformArea(reformAreaId);

          if (reformAreaDetails.outputs.length > 0) {
            showAdditionalChart.value = true;
            await nextTick();
            createAdditionalChart(reformAreaDetails.outputs);
          } else {
            showAdditionalChart.value = false;
          }
        }
      },
    },
  });
};

const createAdditionalChart = (outputs) => {
  const ctx = document.getElementById('additionalChart').getContext('2d');

  if (additionalChartInstance) {
    additionalChartInstance.destroy();
  }

  if (!outputs.length) {
    showAdditionalChart.value = false;
    return;
  }

  let indicatorCounter = 1;
  const indicatorMapping = {};

  // Combine all extra ACR values into a single dataset
  const indicatorDatasets = outputs.flatMap(output =>
    (output.indicators || [])
      .filter(indicator => indicator.extra_acr > 0 && indicator.indicator_name) // Filter out indicators without a name
      .map(indicator => {
        const indicatorNumber = indicatorCounter++;
        const percentage = indicator.extra_acr * 100;
        indicatorMapping[indicatorNumber] = { name: indicator.indicator_name, percentage };
        return {
          label: ` ${indicatorNumber}: ${indicatorMapping[indicatorNumber].name}`, // Label for the dataset
          data: [{
            x: output.name,
            y: percentage,
            indicatorNumber: indicatorNumber // Store the indicator number in the data point
          }],
          backgroundColor: 'green',
          borderColor: 'darkgreen',
          borderWidth: 1,
          stack: 'acr',
          type: 'bar',
        };
      })
  );

  const datasets = [
    {
      label: 'Quarterly Target (100%)',
      data: outputs.map(output => ({
        x: output.name,
        y: output.output_acrs.length > 0 ? 100 : 0
      })),
      backgroundColor: 'orange',
      stack: 'target',
      type: 'bar',
    },
    {
      label: 'Output ACR',
      data: outputs.map(output => ({
        x: output.name,
        y: output.output_acrs.length > 0 ? output.output_acrs[output.output_acrs.length - 1].average_acr * 100 : 0
      })),
      backgroundColor: 'blue',
      stack: 'acr',
      type: 'bar',
    },
    ...indicatorDatasets
  ];

  additionalChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: outputs.map(output => output.name),
      datasets: datasets,
    },
    options: {
      responsive: true,
      scales: {
        x: {
          beginAtZero: true,
          stacked: true
        },
        y: {
          beginAtZero: true,
          stacked: true,
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const datasetLabel = context.dataset.label || '';
              const value = context.raw.y;
              if (context.dataset.backgroundColor === 'green') {
                // Use the dataset label for the green bars
                return `${datasetLabel} - ${value.toFixed(2)}%`;
              }
              return `${datasetLabel}: ${value.toFixed(2)}%`;
            }
          }
        },

        datalabels: {
          display: true,
          anchor: 'center',
          align: 'center',
          color: 'white',
          font: {
            weight: 'bold',
            size: 12
          },
          formatter: function(value, context) {
            // Show the indicator number and percentage on separate lines for green bars
            if (context.dataset.backgroundColor === 'green') {
              return `${value.indicatorNumber} = ${value.y.toFixed(2)}%`;
            }
            // For other bars, just show the percentage
            return `${value.y.toFixed(2)}%`;
          },
          padding: {
            top: 0,
            bottom: 0,
            left: 0,
            right: 0
          }
        }
      },
    },
    plugins: [ChartDataLabels]
  });

  showAdditionalChart.value = true;
};



const saveProgress = async () => {
  try {
    const reformAreaId = selectedReformAreaId.value;
    const quarterIdToSave = quarterId.value; // Use the stored quarter ID

    console.log('Selected Reform Area ID:', reformAreaId); // Debugging statement
    console.log('Quarter ID to Save:', quarterIdToSave); // Debugging statement

    if (!reformAreaId || !quarterIdToSave) {
      throw new Error('Reform area or quarter not selected.');
    }

    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    await api.post('/output-progress/', {
      reform_area: reformAreaId,
      progress: textAreaContent.value,
      output_reporting_period: quarterIdToSave, // Use the stored quarter ID here
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    successMessage.value = 'Data saved successfully.';
    hideMessageAfterDelay('successMessage');
  } catch (error) {
    console.error('Error saving progress:', error);
    errorMessage.value = 'Failed to save data. Please try again.';
    hideMessageAfterDelay('errorMessage');
  }
};


const hideMessageAfterDelay = (messageType) => {
  setTimeout(() => {
    if (messageType === 'successMessage') {
      successMessage.value = '';
    } else if (messageType === 'errorMessage') {
      errorMessage.value = '';
    }
  }, 3000); // Hide message after 3 seconds
};

watch(selectedQuarter, fetchData);
watch(selectedReformAreaId, fetchData);

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 400px;
}
textarea {
  display: block;
  margin-top: 20px;
  width: 100%;
  box-sizing: border-box;
}
.success-message, .error-message {
  font-size: 1.2rem;
  padding: 10px 20px;
  border-radius: 5px;
  position: relative;
  animation-duration: 0.5s; /* Animation duration */
  animation-fill-mode: forwards; /* Keeps message visible after animation */
}


.message-container {
  margin-top: 20px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 12px;
  border: 1px solid #c3e6cb;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease-in-out;
  transition: opacity 0.5s ease-in-out;
  position: relative;
  font-size: 14px;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease-in-out;
  transition: opacity 0.5s ease-in-out;
  position: relative;
  font-size: 14px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
