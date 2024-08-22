<template>
  <div>
    <!-- Quarter Selection -->
    <div>
      <h5>QUARTER AGAINST END OF CONTRACT LEVEL OF PERFORMANCE ANALYSIS</h5>
      <label for="quarterSelect">Select Quarter:</label>
      <select id="quarterSelect" v-model="selectedQuarter">
        <option v-for="quarter in quarters" :key="quarter.id" :value="quarter.id">{{ quarter.label }}</option>
      </select>
    </div>

    <!-- Conditional Rendering of Charts or Table -->
    <canvas v-if="!showTable && !showAdditionalChart" id="reformAreaChart" class="chart"></canvas>
    <canvas v-if="showAdditionalChart && !showTable && outputNames.length > 0" id="additionalChart" class="chart"></canvas>



    <!-- Textarea and Save Button -->
    <div v-if="showAdditionalChart && outputNames.length > 0 && !showTable">
      <textarea v-model="textAreaContent" rows="4" cols="50" placeholder="Comment on the performance per Output"></textarea>
      <br>
      <q-btn unelevated color="positive" label="Save" @click="saveProgress(selectedReformAreaId)" style="float: left;" />
    </div>

<!-- Annual ACR Table -->
<div v-if="annualACRTableData.length > 0 && !showTable">
      <h5>Annual Average ACR for Output</h5>
      <table class="acr-table">
        <thead>
          <tr>
            <th>Output Name</th>
            <th>ANNUAL OUTPUT ACR(%)</th> <!-- Ensure "th" is used instead of "h" -->
            <th v-for="header in annualACRTableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in annualACRTableData" :key="index">
            <td>{{ row.outputName }}</td>
            <td>{{ row.end_contract_average_acr }}</td> <!-- Display end_contract_average_acr here -->
            <td v-for="(acr, key) in row.acrValues" :key="key">{{ formatACRValue(acr) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Textarea and Save Button -->
      <div v-if="annualACRTableData.length > 0 && !showAdditionalChart && !showTable">
        <br>
        <textarea v-model="textAreaContent" rows="4" cols="110" placeholder="Comment on the performance per Output"></textarea>
        <br>
        <q-btn unelevated color="positive" label="Save" @click="saveProgress(selectedReformAreaId)" style="float: left;" />
      </div>
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
const annualACRTableHeaders = ref([]);
const annualACRTableData = ref([]);
let chartInstance = null;
let additionalChartInstance = null;
const selectedReformAreaId = ref(null);
const quarterId = ref(null);

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
        outputs: [],
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


// Helper function to get the previous quarter ID
const getPreviousQuarterId = (currentQuarterId) => {
  const currentIndex = quarters.findIndex(q => q.id === currentQuarterId);
  return currentIndex > 0 ? quarters[currentIndex - 1].id : null;
};

// Updated fetchReformAreaACRData function
const fetchReformAreaACRData = async (outputReportingPeriodId, reformAreaId) => {
  try {
    const response = await api.get(`/endcontract-reform-area-acr/${outputReportingPeriodId}/${reformAreaId}/`);
    const data = response.data;

    // If data is empty, try to fetch data for previous quarters
    if (data.length === 0) {
      let previousQuarterId = getPreviousQuarterId(selectedQuarter.value);

      // Attempt to fetch data for previous quarters until data is found or no more quarters are available
      while (previousQuarterId !== null) {
        const previousResponse = await api.get(`/endcontract-reform-area-acr/${previousQuarterId}/${reformAreaId}/`);
        const previousData = previousResponse.data;

        if (previousData.length > 0) {
          // If previous data is found, return it
          return previousData.map(item => ({
            ...item,
            reform_area_id: item.reform_area_id,
            end_contract_output_acrs: item.end_contract_output_acrs || [],
          }));
        }

        // Move to the previous quarter
        previousQuarterId = getPreviousQuarterId(previousQuarterId);
      }

      // If no data is found for any previous quarters, return an empty array
      return [];
    }

    // Return the fetched data
    return data.map(item => ({
      ...item,
      reform_area_id: item.reform_area_id,
      end_contract_output_acrs: item.end_contract_output_acrs || [],
    }));
  } catch (error) {
    console.error('Error fetching reform area ACR data:', error);
    throw error;
  }
};

const fetchReformArea = async (reformAreaId) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    const response = await api.get(`/reform_area/${reformAreaId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    const reformArea = response.data;

    if (!reformArea || !Array.isArray(reformArea.outcomes)) {
      throw new Error('Invalid or missing reform area data.');
    }

    return {
      reform_area: reformArea.reform_area || 'Unknown',
      outputs: reformArea.outcomes || [],
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

    quarterId.value = selectedQuarter.value;

    await fetchReformAreas(accessToken);

    if (reformAreas.length === 0) {
      throw new Error('No reform areas available to fetch ACR data.');
    }

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

    createChart();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const createChart = () => {
  const ctx = document.getElementById('reformAreaChart')?.getContext('2d');

  if (!ctx) {
    console.error('Failed to get 2D context for reformAreaChart.');
    return;
  }

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: reformAreaNames.value,
      datasets: [
        {
          label: 'End of Contract Target (100%)',
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
          label: 'End of Contract Average ACR',
          data: annualACRTableData.value.map(row => row.average_acr * 100),
          backgroundColor: 'green',
          stack: 'combined',
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.dataset.label || '';
              return `${label}: ${context.raw.toFixed(2)}%`;
            },
          },
        },
      },
      onClick: (event, elements) => {
        if (elements.length > 0) {
          const element = elements[0];
          const dataIndex = element.index;
          const reformArea = reformAreaACRData.value[dataIndex];

          if (reformArea && reformArea.end_contract_output_acrs) {
            // Update the displayed data based on the clicked bar
            updateAnnualOutputACRs(reformArea.end_contract_output_acrs);
          }
        }
      },
    },
  });

  nextTick(() => {
    if (showAdditionalChart.value) {
      createAdditionalChart();
    }
  });
};

const fetchOutputName = async (outputId) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    const response = await api.get(`/outputs/${outputId}/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response.data.output[0] || 'Unknown Output';
  } catch (error) {
    console.error(`Error fetching output name for ID ${outputId}:`, error);
    return 'Error fetching output';
  }
};


const updateAnnualOutputACRs = async (annualOutputAcrs) => {
  try {
    // Create an array of promises to fetch output names
    const promises = annualOutputAcrs.map(async (acr) => {
      const outputName = await fetchOutputName(acr.output); // Fetch the output name
      return {
        outputName, // Use the fetched output name
        end_contract_average_acr: acr.end_contract_average_acr * 100, // Add end_contract_average_acr here
        acrValues: [], // Assuming you have other values to show, if not, you can remove this or adjust accordingly
      };
    });

    // Wait for all promises to resolve
    annualACRTableData.value = await Promise.all(promises);

    showTable.value = true; // Show the table with the new data
  } catch (error) {
    console.error('Error updating annual output ACRs:', error);
  }
};



watch(selectedQuarter, fetchData);

onMounted(() => {
  nextTick(() => {
    if (showAdditionalChart.value) {
      createAdditionalChart();
    }
  });
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 400px;
}

.acr-table {
  width: 100%;
  border-collapse: collapse;
}

.acr-table th, .acr-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.success-message {
  color: green;
}

.error-message {
  color: red;
}
</style>
