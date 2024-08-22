<template>
  <q-page>
    <div class="q-pa-md">
      <h4>Reform Areas</h4>
      <q-card v-for="reformArea in reformAreas" :key="reformArea.id" class="q-mb-md">
        <q-card-section class="cursor-pointer" @click="toggleOutputs(reformArea.id)" style="margin-bottom: 0px;">
          <h5>{{ reformArea.reform_area }}</h5>
        </q-card-section>

        <q-card-section v-if="isSelectedReformArea(reformArea.id)" class="selected-reform-area">
          <h6>Outputs:</h6>
          <div v-for="(output, index) in selectedReformAreaOutputs" :key="output.id">
            <div class="output">
              <h6 @click="toggleIndicators(output.id)">{{ output.output }}</h6>
              <div v-if="isSelectedOutput(output.id)">
                <q-list bordered separator>
                  <q-item v-for="indicator in output.output_indicators" :key="indicator.id">
                    <q-item-label @click="showTable(output.id, indicator.id)">{{ indicator.indicator }}</q-item-label>
                    <div :id="'output-section-' + generateUniqueId(output.id, indicator.id)">
                      <div class="table-section" :data-output-id="output.id" :data-indicator-id="indicator.id" v-if="isSelectedIndicator(indicator.id)">
                        <!-- Display "Reporting for the results of Quarter" and input fields -->
                        <h5>Reporting for the results of Quarter</h5>
                        <div class="quarter-inputs">
                          <div v-for="period in getActivePeriods()" :key="period.id">
                            <q-input
                              class="hint"
                              filled
                              v-model="getOutputActual(output.id, indicator.id, period.output_label.toLowerCase()).actual"
                              :label="period.output_label"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </q-item>
                </q-list>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
    <!-- Success and Error Messages -->
    <div v-if="successMessage || errorMessage" class="message">
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>

    <q-btn unelevated color="positive" label="Save" @click="saveOutputActuals()" style="float: left;" />
  </q-page>
</template>

<script>
import { ref } from 'vue';
import { api } from '/src/boot/axios'; // Adjust import path as necessary
import { fetchInstitutionData } from '/src/services/institutionAPI'; // Adjust import path as necessary

export default {
  setup() {
    const thematicAreasMap = ref({});
    const reformAreas = ref([]);
    const selectedReformAreaOutputs = ref([]);
    const selectedReformAreaId = ref(null);
    const selectedOutputId = ref(null);
    const selectedIndicatorId = ref(null);
    const outputActuals = ref({});
    const accessToken = localStorage.getItem('accessToken'); // Make sure to set this value on login

    const errorMessage = ref('');
    const successMessage = ref('');

    const activeOutputPeriods = ref([]);

    const fetchReformAreas = async () => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const institutionId = await getInstitutionId();
        const response = await api.get(`/reform-areas/institution/${institutionId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response && response.data && Array.isArray(response.data) && response.data.length > 0) {
          reformAreas.value = response.data.map(reform => ({
            id: reform.id,
            reform_area: reform.reform_area,
            outputs: [], // Initialize outputs as an empty array
          }));

          // Map the thematic area IDs to their corresponding IDs
          thematicAreasMap.value = response.data.reduce((map, reform) => {
            map[reform.id] = reform.id; // Adjust mapping logic if necessary
            return map;
          }, {});
        } else {
          throw new Error('No reform areas found.');
        }
      } catch (error) {
        console.error('Error fetching reform areas:', error);
      }
    };


    const getInstitutionId = async () => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const institutionData = await fetchInstitutionData();
        return institutionData.id;
      } catch (error) {
        console.error('Error fetching institution ID:', error);
      }
    };


    const fetchOutputs = async (reformAreaId) => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const response = await api.get(`/outputs/reform_area/${reformAreaId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        const reformAreaIndex = reformAreas.value.findIndex(reform => reform.id === reformAreaId);
        if (reformAreaIndex !== -1) {
          reformAreas.value[reformAreaIndex].outputs = response.data;
        }

        if (response.data.length === 0) {
          reformAreas.value = reformAreas.value.filter(reform => reform.id !== reformAreaId);
        } else {
          selectedReformAreaOutputs.value = response.data.map(output => ({
            ...output,
            output_indicators: output.output_indicators.map(indicator => ({
              ...indicator,
            }))
          }));
          selectedReformAreaId.value = reformAreaId;
        }

        await fetchActiveOutputPeriods();

      } catch (error) {
        console.error('Error fetching outputs:', error);
      }
    };

    const toggleOutputs = async (reformAreaId) => {
      if (reformAreaId === selectedReformAreaId.value) {
        clearSelection();
      } else {
        await fetchOutputs(reformAreaId);
      }
    };

    const toggleIndicators = (outputId) => {
      selectedOutputId.value = (selectedOutputId.value === outputId) ? null : outputId;
    };

    const isSelectedReformArea = (reformAreaId) => {
      return selectedReformAreaId.value === reformAreaId;
    };

    const isSelectedOutput = (outputId) => {
      return selectedOutputId.value === outputId;
    };

    const isSelectedIndicator = (indicatorId) => {
      return selectedIndicatorId.value === indicatorId;
    };

    const showTable = (outputId, indicatorId) => {
      selectedOutputId.value = outputId;
      selectedIndicatorId.value = indicatorId;
    };

    const generateUniqueId = (outputId, indicatorId) => {
      return `output_${outputId}_indicator_${indicatorId}`;
    };

    const getOutputActual = (outputId, indicatorId, periodLabel) => {
      if (!outputActuals.value[outputId]) {
        outputActuals.value[outputId] = {};
      }
      if (!outputActuals.value[outputId][indicatorId]) {
        outputActuals.value[outputId][indicatorId] = {};
      }
      if (!outputActuals.value[outputId][indicatorId][periodLabel]) {
        outputActuals.value[outputId][indicatorId][periodLabel] = {
          actual: null,
        };
      }

      return outputActuals.value[outputId][indicatorId][periodLabel];
    };

    const getActivePeriods = () => {
      return activeOutputPeriods.value;
    };

    const fetchActiveOutputPeriods = async () => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const response = await api.get(`/output-reporting-period/active`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        activeOutputPeriods.value = response.data;
      } catch (error) {
        console.error('Error fetching active output periods:', error);
      }
    };


// Validation functions
const validateForm = () => {
      if (selectedReformAreaOutputs.value.length === 0) {
        errorMessage.value = 'Please select a Reform Area with Outputs.';
        return false;
      }

      for (const output of selectedReformAreaOutputs.value) {
        if (output.output_indicators.length === 0) {
          errorMessage.value = 'Each Output must have at least one Indicator.';
          return false;
        }

        for (const indicator of output.output_indicators) {
          for (const period of getActivePeriods()) {
            const actual = getOutputActual(output.id, indicator.id, period.output_label.toLowerCase()).actual;
            if (actual === null || actual === '') {
              errorMessage.value = 'Please fill out all the reporting fields for all output indicators under each output.';
              return false;
            }
          }
        }
      }

      errorMessage.value = '';
      return true;
    };

    const saveOutputActuals = async () => {
  if (!validateForm()) {
    return;
  }

  try {
    const institutionId = await getInstitutionId();
    const year = new Date().getFullYear();

    // Iterate through all reform areas
    for (const reformArea of reformAreas.value) {
      const reformAreaOutputs = reformArea.outputs;

      // Check if the reform area has any filled outputs
      const outputsWithActuals = reformAreaOutputs.filter(output => {
        return output.output_indicators.some(indicator => {
          return getActivePeriods().some(period => {
            return getOutputActual(output.id, indicator.id, period.output_label.toLowerCase()).actual !== null;
          });
        });
      });

      // Process each output with actuals
      for (const output of outputsWithActuals) {
        const indicatorsWithReportedActuals = output.output_indicators.filter(indicator => {
          return getActivePeriods().some(period => {
            return getOutputActual(output.id, indicator.id, period.output_label.toLowerCase()).actual !== null;
          });
        });

        for (const indicator of indicatorsWithReportedActuals) {
          for (const period of getActivePeriods()) {
            const outputActual = getOutputActual(output.id, indicator.id, period.output_label.toLowerCase()).actual;

            if (outputActual !== null) {
              const response = await api.post(
                '/output-actual/',
                {
                  institution_id: institutionId,
                  output_indicator_id: indicator.id,
                  output_actual: parseInt(outputActual), // Ensure it is an integer
                  year: year,
                  reporting_period: period.output_label // Sending the period to the backend
                },
                {
                  headers: {
                    Authorization: `Bearer ${accessToken}`,
                  },
                }
              );

              if (response.status === 200 || response.status === 201) {
                successMessage.value = 'Data saved successfully!';
                errorMessage.value = '';

                // Call SaveOutputACR after saving output actual
                await SaveOutputACR(output.id, year);

                await saveEndContractOutputACR(output.id, year);
              } else {
                throw new Error('Failed to save data.');
              }
            }
          }
        }
      }
    }

  } catch (error) {
    successMessage.value = '';
    errorMessage.value = `Error saving data: ${error.message}`;
    console.error('Error saving output actuals:', error);
  }
};

    const SaveOutputACR = async (outputId, year) => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const response = await api.post(`/output-acr/`, {
          output: outputId,
          year: year,
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response.status === 200 || response.status === 201) {
          successMessage.value = 'Data saved successfully!';
          errorMessage.value = '';

          // Save Reform Area ACR
              // Get Reform Area ID from selectedReformAreaId directly or from template
              const reformAreaId = selectedReformAreaId.value; // Adjust as per how you get the reform area ID

              // Call SaveReformAreaACR after saving output actual
              await SaveReformAreaACR(reformAreaId, year);
              await saveAnnualReformACR (reformAreaId, year);


        } else {
          throw new Error('Failed to post output ACR.');
        }
      } catch (error) {
        successMessage.value = '';
        errorMessage.value = `Error posting output ACR: ${error.message}`;
        console.error('Error posting output ACR:', error);
      }
    };

    const SaveReformAreaACR = async (reformAreaId, year) => {
  try {
    const response = await api.post(
      '/reform-area-acr/create/',
      {
        reform_area: reformAreaId,
        year: year,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      successMessage.value = 'Reform Area ACR saved successfully!';
      errorMessage.value = '';

      // Call SaveThematicAreaACR after saving Reform Area ACR
      const thematicAreaId = thematicAreasMap.value[reformAreaId];
      if (thematicAreaId) {
        await SaveThematicAreaACR(thematicAreaId, year);
      } else {
        throw new Error('Thematic Area ID not found.');
      }
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    console.error('Error saving Reform Area ACR:', error.response ? error.response.data : error.message);
    errorMessage.value = error.response ? `Failed to save Reform Area ACR: ${error.response.data.detail}` : 'Failed to save Reform Area ACR. Please try again later.';
  }
};



const SaveThematicAreaACR = async (thematicAreaId, year) => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const response = await api.post(`/thematic-area-acr/`, {
          thematic_area: thematicAreaId,
          year: year,
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response.status === 200 || response.status === 201) {
          successMessage.value = 'Output Actual saved successfully!';
          errorMessage.value = '';
        } else {
          throw new Error('Failed to save Thematic Area ACR.');
        }
      } catch (error) {
        successMessage.value = '';
        errorMessage.value = `Error saving Thematic Area ACR: ${error.message}`;
        console.error('Error saving Thematic Area ACR:', error);
      }
    };

    // Save Annual Output ACR
    const saveAnnualOutputACR = async (outputId, year) => {
      try {
        const response = await api.post(
          '/annual-output-acr/',
          {
            output: outputId,
            year: year
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        if (response.status === 200 || response.status === 201) {
          console.log('Output ACR saved successfully!');
        } else {
          throw new Error('Failed to save Output ACR.');
        }
      } catch (error) {
        console.error('Error saving Output ACR:', error);
      }
    };

    const saveAnnualReformACR = async (reformAreaId, year) => {
  try {
    const response = await api.post(
      '/annual-reform-area-acr/create/',
      {
        reform_area_id: reformAreaId,
        year: year,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      console.log('Annual Reform ACR saved successfully!');
    } else {
      throw new Error('Failed to save Annual Reform ACR.');
    }
  } catch (error) {
    console.error('Error saving Annual Reform ACR:', error);
  }
};

const saveEndContractOutputACR = async (outputId, year) => {
  try {
    const response = await api.post(
      '/endof-contract-output-acr/',
      {
        output: outputId,
        year: year,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      console.log('End Contract Output ACR saved successfully!');
    } else {
      throw new Error('Failed to save End Contract Output ACR.');
    }
  } catch (error) {
    console.error('Error saving End Contract Output ACR:', error);
  }
};

const saveEndContractReformAreaACR = async (year, outputReportingPeriodId) => {
  try {
    const response = await api.post(
      '/end-contract-reform-area-acr/create/',
      {
        year: year,
        output_reporting_period_id: outputReportingPeriodId,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      console.log('End Contract Reform Area ACR saved successfully!');
    } else {
      throw new Error('Failed to save End Contract Reform Area ACR.');
    }
  } catch (error) {
    console.error('Error saving End Contract Reform Area ACR:', error);
  }
};


    const validateAndSave = () => {
      if (validateForm()) {
        saveOutputActuals();
      }
    };


    const clearSelection = () => {
      selectedReformAreaId.value = null;
      selectedOutputId.value = null;
      selectedIndicatorId.value = null;
      selectedReformAreaOutputs.value = [];
    };

    // Fetch reform areas when component is mounted
    fetchReformAreas();


    return {
      reformAreas,
      selectedReformAreaOutputs,
      selectedReformAreaId,
      selectedOutputId,
      selectedIndicatorId,
      toggleOutputs,
      toggleIndicators,
      isSelectedReformArea,
      isSelectedOutput,
      isSelectedIndicator,
      showTable,
      generateUniqueId,
      getOutputActual,
      saveOutputActuals,
      getActivePeriods,
      errorMessage,
      successMessage,
      validateForm,
      validateAndSave
    };
  },
};
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
.selected-reform-area {
  padding: 10px;
  background-color: #f5f5f5;
}
.output {
  margin-bottom: 10px;
}
.table-section {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f5f5;
}
.message {
  margin-top: 20px;
}
.success-message {
  color: green;
}
.error-message {
  color: red;
}
.hint {
  padding: 4px;
}

/* Shared CSS for selected reform area and cursor pointer */
.selected-reform-area {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-top: 10px;
  background-color: #f9f9f9;
}

.selected-reform-area h6 {
  margin-top: 0;
  color: #333;
}

.cursor-pointer {
  cursor: pointer;
}

.hint {
  color: #666;
  font-size: 14px;
  border-left: 6px solid #ff0000; /* Change color as needed */
  padding: 10px;
  margin-bottom: 3px; /* Reduce margin-bottom to 3px */

}


/* CSS for table styling */
.table-section {
  margin-top: 10px;
  margin-left: 0;
  text-align: left;
  width: 100%;
}

.table-section table {
  width: 100%;
  border-collapse: collapse;
}

.table-section th,
.table-section td {
  padding: 8px;
  border: 1px solid #ccc;
}

.table-section th {
  background-color: #f2f2f2;
}

.table-section input[type="number"],
.table-section input[type="text"] {
  width: 100%;
  box-sizing: border-box;
}

/* Center align content within the div */
.table-section div {
  text-align: center;
}

/* CSS for activities */
.activities {
  margin-top: 20px;
}

.activities table {
  width: 100%;
}

.activities th,
.activities td {
  padding: 8px;
}

.activities th {
  text-align: left;
  background-color: #f2f2f2;
}


.total-reform-area-budget {
  margin-top: 20px;
  font-weight: bold;
}
.red-text {
  color: red;
}

.green-text {
  color: green;
}
message-container {
  position: fixed;
  bottom: 20px; /* Adjust the bottom position */
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
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
