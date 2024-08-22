<template>
  <q-page>
    <div class="q-pa-md">
      <h5>REFORM AREA(S)</h5>
      <q-card v-for="reformArea in reformAreas" :key="reformArea.id" class="q-mb-md">
        <q-card-section class="cursor-pointer" @click="toggleOutcomes(reformArea.id)" style="margin-bottom: 0px;">
          <h5>{{ reformArea.reform_area }}</h5>
        </q-card-section>
        <q-card-section v-if="selectedReformAreaId === reformArea.id" class="selected-reform-area">
          <h6>Outcomes:</h6>
          <div v-for="(outcome, index) in selectedReformAreaOutcomes" :key="index">
            <div class="outcome">
              <h6 @click="toggleIndicators(outcome.id)">{{ outcome.outcomes[0] }}</h6> <!-- Display outcome name here -->
              <div v-if="selectedOutcomeId === outcome.id">
                <q-list bordered separator>
                  <q-item v-for="indicator in outcome.outcome_indicators" :key="indicator.id">
                    <q-item-label @click="showQuestion(outcome.id, indicator.id)">{{ indicator.indicator }}</q-item-label>
                    <div :id="'outcome-section-' + generateUniqueId(outcome.id, indicator.id)">
                      <div class="hint" v-if="outcome.showQuestion && selectedIndicatorId === indicator.id"></div>
                      <div class="table-section" :data-outcome-id="outcome.id" :data-indicator-id="indicator.id" v-if="outcome.showQuestion && selectedIndicatorId === indicator.id && selectedAnswer === 'Yes'">
                        <h5>Outcome indicator targets</h5>
                        <strong>NOTE:</strong> The nature of indicators for the targets is strictly cumulative (stocks)
                        <table>
  <thead>
    <tr>
      <th>Year</th>
      <th>Baseline</th>
      <th>H1 Target</th>
      <th>H2 Target</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{{ currentYear }}/{{ currentYear + 1 }}</td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).baseline" type="number" step="0.01"></td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).H1" type="number" step="0.01" @input="validateTargets(outcome.id, indicator.id)"></td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).H2" type="number" step="0.01" @input="validateTargets(outcome.id, indicator.id)"></td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).total" type="number" step="0.01" readonly></td>
    </tr>

    <!-- Move the error message inside the row -->
    <tr v-if="showErrorMessage">
      <td colspan="5">
        <div class="error-message">
          Subsequent target should always be greater since it's a stock.
        </div>
      </td>
    </tr>

    <tr>
      <td>{{ currentYear + 1 }}/{{ currentYear + 2 }}</td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).baselineYear2" type="number" step="0.01"></td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).H1Year2" type="nu\mber" step="0.01" @input="validateTargets(outcome.id, indicator.id)"></td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).H2Year2" type="number" step="0.01" @input="validateTargets(outcome.id, indicator.id)"></td>
      <td><input v-model="getOutcomeTarget(outcome.id, indicator.id).totalYear2" type="number" step="0.01" readonly></td>
    </tr>
  </tbody>
</table>

                        <div style="text-align:center;">
                          <label for="outcome_MoV">Means of Verification:</label><br>
                          <div v-for="(mov, index) in getOutcomeTarget(outcome.id, indicator.id).MoV" :key="index">
                            <input v-model="mov.value" type="text"><br>
                          </div>
                          <q-btn color="positive" @click="addInput('MoV', outcome.id, indicator.id)" label="Add MoV"></q-btn>
                          <q-btn @click="removeInput('MoV', outcome.id, indicator.id)" label="Remove MoV" style=" color: #ff0000;"></q-btn><br>
                          <label for="outcome_data_collection_instrument">Data Collection Instruments:</label><br>
                          <div v-for="(instrument, index) in getOutcomeTarget(outcome.id, indicator.id).dataCollectionInstrument" :key="index">
                            <input v-model="instrument.value" type="text"><br>
                          </div>
                          <q-btn color="positive" @click="addInput('dataCollectionInstrument', outcome.id, indicator.id)" label="Add Data Collection Instrument"></q-btn>
                          <q-btn @click="removeInput('dataCollectionInstrument', outcome.id, indicator.id)" label="Remove Data Collection Instrument" style=" color: #ff0000;"></q-btn><br>
                          <label for="outcome_critical_success_factor">Critical Success Factor:</label><br>
                          <div v-for="(factor, index) in getOutcomeTarget(outcome.id, indicator.id).criticalSuccessFactor" :key="index">
                            <input v-model="factor.value" type="text"><br>
                          </div>
                          <q-btn color="positive" @click="addInput('criticalSuccessFactor', outcome.id, indicator.id)" label="Add Critical Success Factor"></q-btn>
                          <q-btn @click="removeInput('criticalSuccessFactor', outcome.id, indicator.id)" label="Remove Critical Success Factor" style=" color: #ff0000;"></q-btn><br>
                          <label for="outcome_data_collection_responsibility">Responsible Person for Data Collection<div class="hint">(Position or Office): </div></label>
                          <input v-model="getOutcomeTarget(outcome.id, indicator.id).dataCollectionResponsibility" type="text"><br>
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
      <!-- Move the dialog outside of the loop to ensure it's only rendered once -->
      <q-dialog v-model="showQuestionDialog">
        <q-card>
          <q-card-section>
            <p>Are you expecting this outcome indicator to be realized within {{ currentYear }}/{{ currentYear + 1 }} to {{ currentYear + 1 }}/{{ currentYear + 2 }}?</p>
            <q-radio v-model="selectedAnswer" val="Yes">Yes</q-radio>
            <q-radio v-model="selectedAnswer" val="No">No</q-radio>
          </q-card-section>
        </q-card>
      </q-dialog>
    </div>
    <!-- Success and Error Messages -->
    <div v-if="successMessage || errorMessage" class="message">
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
    <q-btn unelevated color="positive " label="Save" @click="saveOutcomeTargets(selectedOutcomeId, selectedIndicatorId)" style="float: left;"/>
  </q-page>
</template>

<script>
import { ref, watch } from 'vue';
import { api } from '/src/boot/axios'; // Adjust import path as necessary
import { fetchInstitutionData } from '/src/services/institutionAPI'; // Adjust import path as necessary
export default {
  setup() {
    const reformAreas = ref([]);
    const selectedReformAreaOutcomes = ref([]);
    const selectedReformAreaId = ref(null);
    const selectedOutcomeId = ref(null);
    const selectedIndicatorId = ref(null); // Define selectedIndicatorId
    const showQuestionDialog = ref(false);
    const selectedAnswer = ref(null);

    const outcomeFields = ref({});
    const accessToken = localStorage.getItem('accessToken'); // Make sure to set this value on login
    const showErrorMessage = ref(false); // Initialize showErrorMessage as a ref
    const outcomeTargets = ref({}); // Define outcomeTargets
    const errorMessage = ref('');
    const successMessage = ref('');
    const outcome = ref({
      outcome_id: '', // Initialize with appropriate values
      MoV: '',
      dataCollectionInstrument: '',
      criticalSuccessFactor: '',
      dataCollectionResponsibility: '',
      totalEstimatedBudget: 0, // Add this property
    });
    const outcomeIndicators = ref([]); // Initialize with appropriate values
    const currentYear = new Date().getFullYear();
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
          }));
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
       // Define your method to fetch outcomes
       const fetchOutcomes = async (reformAreaId) => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const response = await api.get(`/outcomes/reform_area/${reformAreaId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

       selectedReformAreaOutcomes.value = response.data.map(outcome => ({
          id: outcome.id,
          outcomes: outcome.outcomes,
          outcome_indicators: outcome.outcome_indicators // Assuming outcome_indicators is an array in your response
        }));
        selectedReformAreaId.value = reformAreaId;
      } catch (error) {
        console.error('Error fetching outcomes:', error);
      }
    };
    const toggleOutcomes = async (reformAreaId) => {
      if (reformAreaId === selectedReformAreaId.value) {
        selectedReformAreaId.value = null;
        selectedOutcomeId.value = null;
        selectedIndicatorId.value = null;
        selectedReformAreaOutcomes.value = [];
      } else {
        await fetchOutcomes(reformAreaId);
      }
    };

    const toggleIndicators = (outcomeId) => {
  selectedOutcomeId.value = selectedOutcomeId.value === outcomeId ? null : outcomeId;
  const selectedOutcome = selectedReformAreaOutcomes.value.find(outcome => outcome.id === outcomeId);
  if (selectedOutcome) {
    // Assign outcome indicators here based on your data structure
    outcomeIndicators.value = selectedOutcome.outcome_indicators;
  }
};



const showQuestion = (outcomeId, indicatorId) => {
      selectedOutcomeId.value = outcomeId;
      selectedIndicatorId.value = indicatorId;
      const outcomeIndex = selectedReformAreaOutcomes.value.findIndex(outcome => outcome.id === outcomeId);
      if (outcomeIndex !== -1) {
        selectedAnswer.value = null;
        selectedReformAreaOutcomes.value.forEach((outcome, index) => {
          if (index !== outcomeIndex) {
            outcome.showQuestion = false;
          }
        });
        selectedReformAreaOutcomes.value[outcomeIndex].showQuestion = true;
      }
      showQuestionDialog.value = true;
    };


    const addInput = (field, outcomeId, indicatorId) => {
  const fieldValue = getOutcomeTarget(outcomeId, indicatorId)[field];
  if (!fieldValue) {
    // If the field value is undefined, initialize it as an empty array
    getOutcomeTarget(outcomeId, indicatorId)[field] = [];
  }
  getOutcomeTarget(outcomeId, indicatorId)[field].push({ value: '' });
};
    // Function to remove input field
    const removeInput = (field, outcomeId, indicatorId) => {
      const fieldValue = getOutcomeTarget(outcomeId, indicatorId)[field];
      if (fieldValue.length > 0) {
        fieldValue.pop();
      }
    };

    const validateTargets = (outcomeId, indicatorId) => {
  const targets = getOutcomeTarget(outcomeId, indicatorId);
  showErrorMessage.value = false; // Reset error message

  // Validate Year 1 H1 and H2
  if (targets.H1 !== '' && parseFloat(targets.H1) <= parseFloat(targets.baseline)) {
    console.error("H1 target for the first year should be greater than Baseline");
    showErrorMessage.value = true;
  }
  if (targets.H2 !== '' && parseFloat(targets.H2) <= parseFloat(targets.H1)) {
    console.error("H2 target for the first year should be greater than H1 target");
    showErrorMessage.value = true;
  }

  // Validate Year 2 H1 and H2
  if (targets.H1Year2 !== '' && parseFloat(targets.H1Year2) <= parseFloat(targets.baselineYear2)) {
    console.error("H1 target for the second year should be greater than Baseline for the second year");
    showErrorMessage.value = true;
  }
  if (targets.H2Year2 !== '' && parseFloat(targets.H2Year2) <= parseFloat(targets.H1Year2)) {
    console.error("H2 target for the second year should be greater than H1 target for the second year");
    showErrorMessage.value = true;
  }

  // Calculate maximum value for Year 1
  const maxYear1 = Math.max(
    parseFloat(targets.baseline || 0),
    parseFloat(targets.H1 || 0),
    parseFloat(targets.H2 || 0)
  );

  // Calculate maximum value for Year 2
  const maxYear2 = Math.max(
    parseFloat(targets.baselineYear2 || 0),
    parseFloat(targets.H1Year2 || 0),
    parseFloat(targets.H2Year2 || 0)
  );

  // Set targets.total and targets.totalYear2 to the respective maximum values
  targets.total = maxYear1;
  targets.totalYear2 = maxYear2;
  targets.baselineYear2= maxYear1;

  // Return true if any validation error occurred, false otherwise
  return showErrorMessage.value;
};
const saveOutcomeTargets = async () => {
  try {
    // Loop through all reform areas
    for (const reformArea of reformAreas.value) {
      // Fetch outcomes for the current reform area
      await fetchOutcomes(reformArea.id);

      // Loop through selected reform area outcomes and save their data
      for (const outcome of selectedReformAreaOutcomes.value) {
        for (const indicator of outcome.outcome_indicators) {
          // Get outcome target data
          const outcomeTargetData = getOutcomeTarget(outcome.id, indicator.id);

          // Set default values if all fields are empty or undefined
          if (!outcomeTargetData.H1 && !outcomeTargetData.H2) {
            outcomeTargetData.H1 = 0;
            outcomeTargetData.H2 = 0;
            outcomeTargetData.total = 0;
            outcomeTargetData.dataCollectionResponsibility = 'N/A';
            outcomeTargetData.MoV = [];
            outcomeTargetData.criticalSuccessFactor = [];
            outcomeTargetData.dataCollectionInstrument = [];
          }

          // Save outcome targets for the current year
          const response1 = await api.post('/outcome-targets/', {
            outcome_indicator: indicator.id,
            year: currentYear,
            baseline: outcomeTargetData.baseline || 0,
            H1_target: outcomeTargetData.H1 || 0,
            H2_target: outcomeTargetData.H2 || 0,
            total_target: outcomeTargetData.total || 0,
            responsibility: outcomeTargetData.dataCollectionResponsibility || 'N/A'
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          // Save outcome targets for the next year
          const response2 = await api.post('/outcome-targets/', {
            outcome_indicator: indicator.id,
            year: currentYear + 1,
            baseline: outcomeTargetData.baselineYear2 || 0,
            H1_target: outcomeTargetData.H1Year2 || 0,
            H2_target: outcomeTargetData.H2Year2 || 0,
            total_target: outcomeTargetData.totalYear2 || 0,
            responsibility: outcomeTargetData.dataCollectionResponsibility || 'N/A'
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          // Save Means of Verification (MoVs)
          const movResponse = await saveMoVs(indicator.id, outcomeTargetData.MoV);

          // Save Critical Success Factors (CSFs)
          const csfResponse = await saveCSFs(indicator.id, outcomeTargetData.criticalSuccessFactor);

          // Save Data Collection Instruments
          const instrumentResponse = await saveInstruments(indicator.id, outcomeTargetData.dataCollectionInstrument);

          // Log success message for the current outcome
          console.log(`Data saved successfully for outcome: ${outcome.outcome}`);
        }
      }

      // Log success message for the current reform area
      console.log(`Data saved successfully for reform area: ${reformArea.reform_area}`);
    }

    // Set success message after saving data for all reform areas
    successMessage.value = 'Data saved successfully.';
    hideMessageAfterDelay('successMessage');
  } catch (error) {
    // Handle errors
    console.error('Error saving data:', error);
  }
};

const hideMessageAfterDelay = (messageType) => {
      setTimeout(() => {
        if (messageType === 'successMessage') {
          successMessage.value = '';
        } else if (messageType === 'errorMessage') {
          errorMessage.value = '';
        }
      }, 5000); // 5 seconds
    };


const saveMoVs = async (outcomeIndicatorId, movs) => {
  try {
    // Extracting values from the movs array and joining them into a single string
    const movValues = movs.map(mov => mov.value);

    const response = await api.post('/outcome-movs/', {
      outcome_indicator_id: outcomeIndicatorId,
      movs: movValues // Passing the array of values to the API
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response; // Returning the response
  } catch (error) {
    console.error('Error saving Means of Verification:', error);
    // Handle error, if required
    throw error; // Rethrow the error
  }
};

const saveCSFs = async (outcomeIndicatorId, csfs) => {
  try {
    const csfValues = csfs.map(csf => csf.value);

    const response = await api.post('/outcome-csfs/', {
      outcome_indicator_id: outcomeIndicatorId,
      csfs: csfValues, // Passing the array of values to the API
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response; // Returning the response
  } catch (error) {
    console.error('Error saving Critical Success Factors:', error);
    // Handle error, if required
    throw error; // Rethrow the error
  }
};

const saveInstruments = async (outcomeIndicatorId, instruments) => {
  try {
    const instrumentValues = instruments.map(instrument => instrument.value);

    const response = await api.post('/outcome-instruments/', {
      outcome_indicator_id: outcomeIndicatorId,
      instruments: instrumentValues, // Passing the array of values to the API
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response; // Returning the response
  } catch (error) {
    console.error('Error saving Data Collection Instruments:', error);

    // Handle error, if required
    throw error; // Rethrow the error
  }
};


const generateUniqueId = (outcomeId, indicatorId) => {
  return `outcome_${outcomeId}_indicator_${indicatorId}`;
};

const getOutcomeTarget = (outcomeId, indicatorId) => {
  if (!outcomeTargets.value[outcomeId]) {
    outcomeTargets.value[outcomeId] = {};
  }
  if (!outcomeTargets.value[outcomeId][indicatorId]) {
    outcomeTargets.value[outcomeId][indicatorId] = {
      baseline: '',
      H1: '',
      H2: '',
      total: 0,
      baselineYear2: '',
      H1Year2: '',
      H2Year2: '',
      totalYear2: 0
    };
  }
  return outcomeTargets.value[outcomeId][indicatorId];
};



    fetchReformAreas();
    return {
      reformAreas,
      selectedReformAreaOutcomes,
      selectedReformAreaId,
      selectedOutcomeId,
      toggleOutcomes,
      toggleIndicators,
      showQuestion,
      outcome,
      outcomeIndicators,
      selectedIndicatorId,
      selectedAnswer,
      showQuestionDialog,
      currentYear,

      generateUniqueId,
      outcomeTargets,
      validateTargets,
      getOutcomeTarget,
      outcomeFields,

      addInput,
      removeInput,
      errorMessage,
      showErrorMessage,

      successMessage,
      saveOutcomeTargets
    };
  },
};
</script>

<style scoped>
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

/* Error message styling */
.error-message {
  color: red; /* Set text color to red */
  text-align: center; /* Center align text */
  margin-top: 10px; /* Add some space on top */
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
