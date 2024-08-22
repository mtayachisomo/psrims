<template>
  <q-page>
    <div class="q-pa-md">
      <h5>REFORM AREA(S)</h5>
      <q-card v-for="reformArea in reformAreas" :key="reformArea.id" class="q-mb-md">
        <q-card-section class="cursor-pointer reform-area-item" @click="toggleOutputs(reformArea.id)" style="margin-bottom: 0px;">
          <h5>{{ reformArea.reform_area }}</h5>
        </q-card-section>
        <q-card-section v-if="selectedReformAreaId === reformArea.id" class="selected-reform-area">
          <h6>Outputs:</h6>
          <div v-for="(output, index) in selectedReformAreaOutputs" :key="index">
            <div class="output">
              <h6 @click="toggleIndicators(output.id)">{{ output.output[0] }}</h6> <!-- Display output name here -->
              <div v-if="selectedOutputId === output.id">
                <q-list bordered separator>
                  <q-item v-for="indicator in output.output_indicators" :key="indicator.id">
                    <q-item-label @click="showQuestion(output.id, indicator.id)">{{ indicator.indicator }}</q-item-label>
                    <div :id="'output-section-' + generateUniqueId(output.id, indicator.id)">
                      <div  v-if="output.showQuestion && selectedIndicatorId === indicator.id"></div>
                      <div class="table-section" :data-output-id="output.id" :data-indicator-id="indicator.id" v-if="output.showQuestion && selectedIndicatorId === indicator.id && selectedAnswer === 'Yes'">
                        <h5>Output Indicator Targets</h5>
                        <div class="hint" style="color: green;"><strong>NOTE:</strong> The nature of indicators for the targets is strictly cumulative (stocks) </div>

                        <table>
                          <thead>
                            <tr>
                              <th>Year</th>
                              <th>Baseline</th>
                              <th>Q1 Target</th>
                              <th>Q2 Target</th>
                              <th>Q3 Target</th>
                              <th>Q4 Target</th>
                              <th>Total</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>{{ currentYear }}/{{ currentYear + 1 }}</td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).baseline" type="number" step="0.01"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q1" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q2" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q3" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q4" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).total" type="number" step="0.01" readonly></td>
                            </tr>
                                                   <!-- Inside the table section -->
<div v-if="showErrorMessage" class="error-message">
  Subsequent target should always be greater since it's a stock.
</div>
                            <tr>
                              <td>{{ currentYear + 1 }}/{{ currentYear + 2 }}</td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).baselineYear2" type="number" step="0.01" readonly></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q1Year2" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q2Year2" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q3Year2" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).q4Year2" type="number" step="0.01" @input="validateTargets(output.id, indicator.id)"></td>
                              <td><input v-model="getOutputTarget(output.id, indicator.id).totalYear2" type="number" step="0.01" readonly></td>
                            </tr>
                          </tbody>
                        </table>
                         <!-- Invoke the outputIndicatorImplementationPeriod function -->
<div v-if="outputIndicatorImplementationPeriod()">
  <strong>Output Indicator Implementation Period:</strong>
  <span>{{ outputIndicatorImplementationPeriod() }}</span>
</div>
                        <div style="text-align:center;">
      <label for="output_MoV">Means of Verification:</label><br>
      <div v-for="(mov, index) in getOutputTarget(output.id, indicator.id).MoV" :key="index">
        <input v-model="mov.value" type="text"><br>
      </div>
      <q-btn unelevated color="positive" @click="addInput('MoV', output.id, indicator.id)" label="Add MoV"></q-btn>
      <q-btn @click="removeInput('MoV', output.id, indicator.id)" label="Remove MoV" style=" color: #ff0000;"></q-btn><br>

      <label for="output_data_collection_instrument">Data Collection Instruments:</label><br>
      <div v-for="(instrument, index) in getOutputTarget(output.id, indicator.id).dataCollectionInstrument" :key="index">
        <input v-model="instrument.value" type="text"><br>
      </div>
      <q-btn unelevated color="positive" @click="addInput('dataCollectionInstrument', output.id, indicator.id)" label="Add Data Collection Instrument"></q-btn>
      <q-btn @click="removeInput('dataCollectionInstrument', output.id, indicator.id)" label="Remove Data Collection Instrument" style=" color: #ff0000;"></q-btn><br>

      <label for="output_critical_success_factor">Critical Success Factor:</label><br>
      <div v-for="(factor, index) in getOutputTarget(output.id, indicator.id).criticalSuccessFactor" :key="index">
        <input v-model="factor.value" type="text"><br>
      </div>
      <q-btn unelevated color="positive" @click="addInput('criticalSuccessFactor', output.id, indicator.id)" label="Add Critical Success Factor"></q-btn>
      <q-btn @click="removeInput('criticalSuccessFactor', output.id, indicator.id)" label="Remove Critical Success Factor" style=" color: #ff0000;"></q-btn><br>

      <label for="output_data_collection_responsibility">Responsible Person for Data Collection<div class="hint">(Position or Office): </div></label>
      <input v-model="getOutputTarget(output.id, indicator.id).dataCollectionResponsibility" type="text"><br>
    </div>
  </div>

                    </div>
                  </q-item>
                </q-list>
<!-- Activities -->
<div class="activities" v-if="selectedAnswer !== 'No'">
  <h5>Activities for {{ output.output[0] }}</h5>
  <table>
    <thead>
      <tr>
        <th>Activity</th>
        <th>Estimated Budget (MWK)</th>
        <th>Source of Fund</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(activity, activityIndex) in output.activities " :key="activityIndex">
        <td>{{ activity.activity }}</td>
        <td><input type="number" v-model="activity.estimated_budget" class="budget-input" @change="saveActivityBudget(output.id, activity.id, activity.estimated_budget)"></td>
        <td><textarea v-model="activity.source_of_fund" class="source-input" rows="2" style="width: 500px;" @change="saveActivitySource(output.id, activity.id, activity.source_of_fund)"></textarea></td>
      </tr>
    </tbody>
  </table>
  <div class="total-output-budget red-text">
    <strong>Total Estimated Budget for {{ output.output[0] }}</strong>:
    <span>{{ getTotalOutputBudget(output.activities).toFixed(2) }}</span>
  </div>
</div>

              </div>
            </div>
          </div>
          <!-- Total estimated budget for reform area -->
          <div class="total-reform-area-budget green-text" v-if="selectedReformAreaId">
            <strong>Total Estimated Budget for {{ reformArea.reform_area }}</strong>:
            <span>{{ getTotalReformAreaBudget(selectedReformAreaId) }}</span>
          </div>
 <!-- Display reform area implementation period -->
 <div v-if="reformAreaImplementationPeriod"><strong>REFORM AREA IMPLEMENTATION PERIOD: {{ reformAreaImplementationPeriod }}</strong></div>
        </q-card-section>

      </q-card>
      <!-- Move the dialog outside of the loop to ensure it's only rendered once -->
      <q-dialog v-model="showQuestionDialog">
        <q-card>
          <q-card-section>
            <p>Are you expecting this output indicator to be realized within {{ currentYear }}/{{ currentYear + 1 }} to {{ currentYear + 1 }}/{{ currentYear + 2 }}?</p>
            <q-radio v-model="selectedAnswer" val="Yes">Yes</q-radio>
            <q-radio v-model="selectedAnswer" val="No">No</q-radio>
          </q-card-section>
        </q-card>
      </q-dialog>


    </div>
      <!-- Display the implementation period -->
<p v-if="implementationPeriod"><strong>IMPLEMENTATION PERIOD:{{ implementationPeriod }}</strong></p>

      <!-- Success and Error Messages -->
    <div v-if="successMessage || errorMessage" class="message">
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>

    <q-btn unelevated color="positive" label="Save" @click="saveOutputTargets(selectedOutputId, selectedIndicatorId)" style="float: left;"/>
  </q-page>
</template>


<script>
import { ref, computed, watch } from 'vue';
import { api } from '/src/boot/axios'; // Adjust import path as necessary
import { fetchInstitutionData } from '/src/services/institutionAPI'; // Adjust import path as necessary

export default {
  setup() {
    const reformAreas = ref([]);
    const selectedReformAreaOutputs = ref([]);
    const selectedReformAreaId = ref(null);
    const selectedOutputId = ref(null);
    const selectedIndicatorId = ref(null); // Define selectedIndicatorId
    const showQuestionDialog = ref(false);
    const selectedAnswer = ref(null);
    const outputFields = ref({});
    const accessToken = localStorage.getItem('accessToken'); // Make sure to set this value on login

    const showErrorMessage = ref(false); // Initialize showErrorMessage as a ref
    const reformAreaBudgets = ref({}); // Store reform area budgets
    const outputBudgets = ref({}); // Store output budgets
    const totalReformAreaBudget = ref(0);
    const outputTargets = ref({}); // Define outputTargets
    const errorMessage = ref('');
    const successMessage = ref('');
    const activitySources = ref({});



    // Define ref variables for storing estimated budgets for activities
    const activityBudgets = ref({});

    const output = ref({
      output_id: '', // Initialize with appropriate values
      MoV: '',
      dataCollectionInstrument: '',
      criticalSuccessFactor: '',
      dataCollectionResponsibility: '',
      totalEstimatedBudget: 0, // Add this property
    });

    const outputIndicators = ref([]); // Initialize with appropriate values

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

    const fetchOutputs = async (reformAreaId) => {
      try {
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        const response = await api.get(`/notargeted/outputs/reform_area/${reformAreaId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        selectedReformAreaOutputs.value = response.data.map(output => ({
          ...output,
          activities: output.activities.map(activity => ({
            ...activity,
            estimated_budget: activityBudgets.value[output.id]?.[activity.id] || '', // Retrieve stored budget or leave empty
            source_of_fund: activitySources.value[output.id]?.[activity.id] || '', // Retrieve stored source of fund or leave empty
          })),
        }));
        selectedReformAreaId.value = reformAreaId;
        // Initialize output targets for each output indicator
        outputTargets.value[output.id] = {};
        output.output_indicators.forEach(indicator => {
          outputTargets.value[output.id][indicator.id] = {
            baseline: '',
            q1: '',
            q2: '',
            q3: '',
            q4: '',
            total: '',
            baselineYear2: '',
            q1Year2: '',
            q2Year2: '',
            q3Year2: '',
            q4Year2: '',
            totalYear2: ''
          };
        });
      } catch (error) {

      }
    };
    const indicatorFields = ref({
    MoV: '',
    dataCollectionInstrument: '',
    criticalSuccessFactor: '',
    dataCollectionResponsibility: ''



  });



    const toggleOutputs = async (reformAreaId) => {
      // If the clicked reform area is already selected, hide its outputs
      if (reformAreaId === selectedReformAreaId.value) {
        selectedReformAreaId.value = null;
        selectedOutputId.value = null;
        selectedIndicatorId.value = null;
        selectedReformAreaOutputs.value = [];
      } else {
        await fetchOutputs(reformAreaId);
      }
    };

    const toggleIndicators = (outputId) => {
      if (selectedOutputId === outputId) {
        selectedOutputId.value = (selectedOutputId.value === outputId) ? null : outputId;
      } else {
        selectedOutputId.value = outputId;
      }
    };

    const showQuestion = (outputId, indicatorId) => {
      selectedOutputId.value = outputId;
      selectedIndicatorId.value = indicatorId;
      const outputIndex = selectedReformAreaOutputs.value.findIndex(output => output.id === outputId);
      if (outputIndex !== -1) {
        // Reset the selectedAnswer to null when showing the question for a new output indicator
        selectedAnswer.value = null;
        selectedReformAreaOutputs.value.forEach((output, index) => {
          if (index !== outputIndex) {
            output.showQuestion = false;
          }
        });
        selectedReformAreaOutputs.value[outputIndex].showQuestion = true;
      }
      showQuestionDialog.value = true;
    };

    const addInput = (field, outputId, indicatorId) => {
  const fieldValue = getOutputTarget(outputId, indicatorId)[field];
  if (!fieldValue) {
    // If the field value is undefined, initialize it as an empty array
    getOutputTarget(outputId, indicatorId)[field] = [];
  }
  getOutputTarget(outputId, indicatorId)[field].push({ value: '' });
};


    // Function to remove input field
    const removeInput = (field, outputId, indicatorId) => {
      const fieldValue = getOutputTarget(outputId, indicatorId)[field];
      if (fieldValue.length > 0) {
        fieldValue.pop();
      }
    };


    const validateTargets = (outputId, indicatorId) => {
  const targets = getOutputTarget(outputId, indicatorId);
  showErrorMessage.value = false; // Reset error message

  // Define a function to check if a value is empty or not
  const isEmpty = (value) => {
    return value === '' || value === null || value === undefined;
  };

  // Define a function to get the last filled target before the blank one
  const getLastFilledTarget = (target, previousTarget) => {
    return isEmpty(target) ? previousTarget : target;
  };

  // Function to get the last filled target considering all quarters
  const getNextFilledTarget = (current, ...nextTargets) => {
    if (!isEmpty(current)) return current;
    for (let target of nextTargets) {
      if (!isEmpty(target)) return target;
    }
    return null; // If all targets are empty
  };

  // Validate Year 1 for Increasing Values
  const lastBaselineYear1 = getLastFilledTarget(targets.baseline, null);
  const lastQ1Year1 = getLastFilledTarget(targets.q1, lastBaselineYear1);
  const lastQ2Year1 = getLastFilledTarget(targets.q2, lastQ1Year1);
  const lastQ3Year1 = getLastFilledTarget(targets.q3, lastQ2Year1);
  const lastQ4Year1 = getLastFilledTarget(targets.q4, lastQ3Year1);
  const nextFilledQYear1 = getNextFilledTarget(targets.q1, targets.q2, targets.q3, targets.q4);

  if (parseFloat(lastBaselineYear1) <= parseFloat(nextFilledQYear1)) {
    // Check for increasing values
    if (!isEmpty(targets.q1) && parseFloat(lastBaselineYear1) >= parseFloat(targets.q1)) {
      console.error("Q1 for the first year should be greater than Baseline");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q2) && parseFloat(lastQ1Year1) >= parseFloat(targets.q2)) {
      console.error("Q2 for the first year should be greater than Q1");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q3) && parseFloat(lastQ2Year1) >= parseFloat(targets.q3)) {
      console.error("Q3 for the first year should be greater than Q2");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q4) && parseFloat(lastQ3Year1) >= parseFloat(targets.q4)) {
      console.error("Q4 for the first year should be greater than Q3");
      showErrorMessage.value = true;
    }

    // Calculate maximum value for Year 1 for increasing case
    const maxYear1 = Math.max(
      parseFloat(targets.baseline || 0),
      parseFloat(targets.q1 || 0),
      parseFloat(targets.q2 || 0),
      parseFloat(targets.q3 || 0),
      parseFloat(targets.q4 || 0)
    );

    // Set targets.total to maxYear1
    targets.total = maxYear1;
    targets.baselineYear2 = maxYear1; // Set baselineYear2 to maxYear1 for Year 2 calculations

    // Validate Year 2 for Increasing Values
    const lastBaselineYear2 = getLastFilledTarget(targets.baselineYear2, maxYear1);
    const lastQ1Year2 = getLastFilledTarget(targets.q1Year2, lastBaselineYear2);
    const lastQ2Year2 = getLastFilledTarget(targets.q2Year2, lastQ1Year2);
    const lastQ3Year2 = getLastFilledTarget(targets.q3Year2, lastQ2Year2);
    const lastQ4Year2 = getLastFilledTarget(targets.q4Year2, lastQ3Year2);

    if (!isEmpty(targets.q1Year2) && parseFloat(lastBaselineYear2) >= parseFloat(targets.q1Year2)) {
      console.error("Q1 for the second year should be greater than Baseline for the second year");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q2Year2) && parseFloat(lastQ1Year2) >= parseFloat(targets.q2Year2)) {
      console.error("Q2 for the second year should be greater than Q1 for the second year");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q3Year2) && parseFloat(lastQ2Year2) >= parseFloat(targets.q3Year2)) {
      console.error("Q3 for the second year should be greater than Q2 for the second year");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q4Year2) && parseFloat(lastQ3Year2) >= parseFloat(targets.q4Year2)) {
      console.error("Q4 for the second year should be greater than Q3 for the second year");
      showErrorMessage.value = true;
    }

    // Calculate maximum value for Year 2 for increasing case
    const maxYear2 = Math.max(
      parseFloat(targets.baselineYear2 || 0),
      parseFloat(targets.q1Year2 || 0),
      parseFloat(targets.q2Year2 || 0),
      parseFloat(targets.q3Year2 || 0),
      parseFloat(targets.q4Year2 || 0)
    );

    // Set targets.totalYear2 to maxYear2
    targets.totalYear2 = maxYear2;
  }

  // Validate Year 1 for Decreasing Values
  if (parseFloat(lastBaselineYear1) >= parseFloat(nextFilledQYear1)) {
    // Check for decreasing values
    if (!isEmpty(targets.q1) && parseFloat(lastBaselineYear1) <= parseFloat(targets.q1)) {
      console.error("Q1 for the first year should be less than Baseline");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q2) && parseFloat(lastQ1Year1) <= parseFloat(targets.q2)) {
      console.error("Q2 for the first year should be less than Q1");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q3) && parseFloat(lastQ2Year1) <= parseFloat(targets.q3)) {
      console.error("Q3 for the first year should be less than Q2");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q4) && parseFloat(lastQ3Year1) <= parseFloat(targets.q4)) {
      console.error("Q4 for the first year should be less than Q3");
      showErrorMessage.value = true;
    }

    // Calculate minimum value for Year 1 for decreasing case
    const minYear1 = Math.min(
      parseFloat(targets.baseline || Number.POSITIVE_INFINITY),
      parseFloat(targets.q1 || Number.POSITIVE_INFINITY),
      parseFloat(targets.q2 || Number.POSITIVE_INFINITY),
      parseFloat(targets.q3 || Number.POSITIVE_INFINITY),
      parseFloat(targets.q4 || Number.POSITIVE_INFINITY)
    );

    // Set targets.total to minYear1
    targets.total = isFinite(minYear1) ? minYear1 : 0;
    targets.baselineYear2 = isFinite(minYear1) ? minYear1 : 0; // Set baselineYear2 to minYear1 for Year 2 calculations

    // Validate Year 2 for Decreasing Values
    const lastBaselineYear2 = getLastFilledTarget(targets.baselineYear2, minYear1);
    const lastQ1Year2 = getLastFilledTarget(targets.q1Year2, lastBaselineYear2);
    const lastQ2Year2 = getLastFilledTarget(targets.q2Year2, lastQ1Year2);
    const lastQ3Year2 = getLastFilledTarget(targets.q3Year2, lastQ2Year2);
    const lastQ4Year2 = getLastFilledTarget(targets.q4Year2, lastQ3Year2);

    if (!isEmpty(targets.q1Year2) && parseFloat(lastBaselineYear2) <= parseFloat(targets.q1Year2)) {
      console.error("Q1 for the second year should be less than Baseline for the second year");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q2Year2) && parseFloat(lastQ1Year2) <= parseFloat(targets.q2Year2)) {
      console.error("Q2 for the second year should be less than Q1 for the second year");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q3Year2) && parseFloat(lastQ2Year2) <= parseFloat(targets.q3Year2)) {
      console.error("Q3 for the second year should be less than Q2 for the second year");
      showErrorMessage.value = true;
    }
    if (!isEmpty(targets.q4Year2) && parseFloat(lastQ3Year2) <= parseFloat(targets.q4Year2)) {
      console.error("Q4 for the second year should be less than Q3 for the second year");
      showErrorMessage.value = true;
    }

    // Calculate minimum value for Year 2 for decreasing case
    const minYear2 = Math.min(
      parseFloat(targets.baselineYear2 || Number.POSITIVE_INFINITY),
      parseFloat(targets.q1Year2 || Number.POSITIVE_INFINITY),
      parseFloat(targets.q2Year2 || Number.POSITIVE_INFINITY),
      parseFloat(targets.q3Year2 || Number.POSITIVE_INFINITY),
      parseFloat(targets.q4Year2 || Number.POSITIVE_INFINITY)
    );

    // Set targets.totalYear2 to minYear2
    targets.totalYear2 = isEmpty(targets.q1Year2) && isEmpty(targets.q2Year2) && isEmpty(targets.q3Year2) && isEmpty(targets.q4Year2)
      ? minYear1
      : minYear2;
  }

  // Optional: Display error message if any validation fails
  if (showErrorMessage.value) {
    console.error("Validation failed. Please correct the errors and try again.");
  }
};


const generateUniqueId = (outputId, indicatorId) => {
      return `output_${outputId}_indicator_${indicatorId}`;
    };

    const getOutputTarget = (outputId, indicatorId) => {
  if (!outputTargets.value[outputId]) {
    outputTargets.value[outputId] = {};
  }
  if (!outputTargets.value[outputId][indicatorId]) {
    outputTargets.value[outputId][indicatorId] = {
      baseline: '',
      q1: '',
      q2: '',
      q3: '',
      q4: '',
      total: 0,
      baselineYear2: '',
      q1Year2: '',
      q2Year2: '',
      q3Year2: '',
      q4Year2: '',
      totalYear2: 0
    };
  }
  return outputTargets.value[outputId][indicatorId];
};


     // Function to save activity budget when input changes
     const saveActivityBudget = (outputId, activityId, budget) => {
      if (!activityBudgets.value[outputId]) {
        activityBudgets.value[outputId] = {};
      }
      activityBudgets.value[outputId][activityId] = budget;
    };

   // Function to save source of funds when input changes
const saveActivitySource = (outputId, activityId, source) => {
  if (!activitySources.value[outputId]) {
    activitySources.value[outputId] = {};
  }
  activitySources.value[outputId][activityId] = source;
};



    // Function to calculate total estimated budget for an output
    const getTotalOutputBudget = (activities) => {
  if (activities && Array.isArray(activities)) {
    return activities.reduce((total, activity) => total + parseFloat(activity.estimated_budget || 0), 0);
  } else {
    return 0;
  }
};



    // Function to calculate total estimated budget for the reform area
    const getTotalReformAreaBudget = () => {
      let totalBudget = 0;
      // Loop through selectedReformAreaOutputs to calculate total budget
      selectedReformAreaOutputs.value.forEach(output => {
        output.activities.forEach(activity => {
          totalBudget += parseFloat(activity.estimated_budget || 0);
        });
      });
      return totalBudget.toFixed(2); // Return total budget with 2 decimal places
    };


// Computed property to calculate the implementation period
const implementationPeriod = computed(() => {
  let currentYearFilledQuarters = [];
  let nextYearFilledQuarters = [];

  // Loop through output targets to find filled quarters for the current and next year
  Object.values(outputTargets.value).forEach(output => {
    Object.values(output).forEach(target => {
      if (target.q1 || target.q2 || target.q3 || target.q4) {
        // Find the lowest filled quarter for the current year
        const lowestQuarter = ['Q1', 'Q2', 'Q3', 'Q4'].find(quarter => target[quarter.toLowerCase()]);
        currentYearFilledQuarters.push(lowestQuarter);

        // Find the highest filled quarter for the current year
        const highestQuarter = ['Q4', 'Q3', 'Q2', 'Q1'].find(quarter => target[quarter.toLowerCase()]);
        currentYearFilledQuarters.push(highestQuarter);
      }

      if (target.q1Year2 || target.q2Year2 || target.q3Year2 || target.q4Year2) {
        // Find the lowest filled quarter for the next year
        const lowestQuarter = ['Q1', 'Q2', 'Q3', 'Q4'].find(quarter => target[quarter.toLowerCase() + 'Year2']);
        nextYearFilledQuarters.push(lowestQuarter);

        // Find the highest filled quarter for the next year
        const highestQuarter = ['Q4', 'Q3', 'Q2', 'Q1'].find(quarter => target[quarter.toLowerCase() + 'Year2']);
        nextYearFilledQuarters.push(highestQuarter);
      }
    });
  });

  // Deduplicate and sort the arrays of filled quarters
  currentYearFilledQuarters = Array.from(new Set(currentYearFilledQuarters)).sort();
  nextYearFilledQuarters = Array.from(new Set(nextYearFilledQuarters)).sort();

  // Construct the implementation period string based on the filled quarters
  let period = '';
  const currentYear = new Date().getFullYear();
  if (currentYearFilledQuarters.length > 0) {
    period += `${currentYear}/${currentYear + 1} FROM ${currentYearFilledQuarters[0]}`;
  }
  if (nextYearFilledQuarters.length > 0) {
    period += period ? ` TO ${currentYear + 1}/${currentYear + 2}  ${nextYearFilledQuarters[nextYearFilledQuarters.length - 1]}` : `${currentYear + 1}/${currentYear + 2} (Lowest: ${nextYearFilledQuarters[0]}, Highest: ${nextYearFilledQuarters[nextYearFilledQuarters.length - 1]})`;
  }
  return period;
});

const outputIndicatorImplementationPeriod = () => {
  const currentYearFilledQuarters = [];
  const nextYearFilledQuarters = [];

  // Check if there is a selected output indicator
  if (selectedOutputId.value && selectedIndicatorId.value) {
    // Retrieve the target for the selected output indicator
    const target = getOutputTarget(selectedOutputId.value, selectedIndicatorId.value);

    // Check if the target for the current year is filled
    if (target.q1 || target.q2 || target.q3 || target.q4) {
      if (target.q1) currentYearFilledQuarters.push('Q1');
      if (target.q2) currentYearFilledQuarters.push('Q2');
      if (target.q3) currentYearFilledQuarters.push('Q3');
      if (target.q4) currentYearFilledQuarters.push('Q4');
    }

    // Check if the target for the next year is filled
    if (target.q1Year2 || target.q2Year2 || target.q3Year2 || target.q4Year2) {
      if (target.q1Year2) nextYearFilledQuarters.push('Q1');
      if (target.q2Year2) nextYearFilledQuarters.push('Q2');
      if (target.q3Year2) nextYearFilledQuarters.push('Q3');
      if (target.q4Year2) nextYearFilledQuarters.push('Q4');
    }
  }

  // Deduplicate and sort the arrays of filled quarters
  const sortedCurrentYearFilledQuarters = Array.from(new Set(currentYearFilledQuarters)).sort();
  const sortedNextYearFilledQuarters = Array.from(new Set(nextYearFilledQuarters)).sort();

  // Construct the implementation period string based on the filled quarters
  let period = '';
  const currentYear = new Date().getFullYear();
  if (sortedCurrentYearFilledQuarters.length > 0) {
    period += `${currentYear}/${currentYear + 1} FROM ${sortedCurrentYearFilledQuarters[0]}`;

  }
  if (sortedNextYearFilledQuarters.length > 0) {
    period += period ? ` TO ${currentYear + 1}/${currentYear + 2} ${sortedNextYearFilledQuarters[sortedNextYearFilledQuarters.length - 1]}` : `${currentYear + 1}/${currentYear + 2} FROM ${sortedNextYearFilledQuarters[0]}`;
  }
  return period;
};


 // Inside your setup() function
const reformAreaImplementationPeriod = computed(() => {
  let hasFirstSectionFilled = false;
  let hasSecondSectionFilled = false;

  // Loop through all reform areas
  for (const reformArea of reformAreas.value) {
    // Loop through selected reform area outputs
    for (const output of selectedReformAreaOutputs.value) {
      for (const indicator of output.output_indicators) {
        // Check if the first section is filled
        if (
          getOutputTarget(output.id, indicator.id).baseline !== '' ||
          getOutputTarget(output.id, indicator.id).q1 !== '' ||
          getOutputTarget(output.id, indicator.id).q2 !== '' ||
          getOutputTarget(output.id, indicator.id).q3 !== '' ||
          getOutputTarget(output.id, indicator.id).q4 !== ''
        ) {
          hasFirstSectionFilled = true;
        }

        // Check if the second section is filled
        if (

          getOutputTarget(output.id, indicator.id).q1Year2 !== '' ||
          getOutputTarget(output.id, indicator.id).q2Year2 !== '' ||
          getOutputTarget(output.id, indicator.id).q3Year2 !== '' ||
          getOutputTarget(output.id, indicator.id).q4Year2 !== ''
        ) {
          hasSecondSectionFilled = true;
        }
      }
    }
  }

  // Update the implementation period based on filled sections
  if (hasFirstSectionFilled && hasSecondSectionFilled) {
    return `${currentYear}/${currentYear + 1} to ${currentYear + 1}/${currentYear + 2}`;
  } else if (hasFirstSectionFilled) {
    return `${currentYear}/${currentYear + 1}`;
  } else {
    return '';
  }
});


   // Watch for changes in selectedReformAreaOutputs and update total budget accordingly
    watch(selectedReformAreaOutputs, () => {
      // Recalculate total budget whenever selectedReformAreaOutputs changes
      totalReformAreaBudget.value = getTotalReformAreaBudget();

    });


    const saveOutputTargets = async () => {
  try {
    const institutionId = await getInstitutionId(); // Assuming getInstitutionId is defined somewhere

    // Save Implementation Period
    const implementationPeriodResponse = await api.post('/periods/', {
      institution: institutionId,
      year: currentYear,
      period: implementationPeriod.value,
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    // Loop through all reform areas
    for (const reformArea of reformAreas.value) {
      // Fetch outputs for the current reform area
      await fetchOutputs(reformArea.id);

      // Loop through selected reform area outputs and save their data
      for (const output of selectedReformAreaOutputs.value) {
        for (const indicator of output.output_indicators) {
          // Get output target data
          const outputTargetData = getOutputTarget(output.id, indicator.id);

          // Set default values if all fields are empty or undefined
          if (!outputTargetData.q1 && !outputTargetData.q2 && !outputTargetData.q3 && !outputTargetData.q4) {
            outputTargetData.q1 = 0;
            outputTargetData.q2 = 0;
            outputTargetData.q3 = 0;
            outputTargetData.q4 = 0;
            outputTargetData.total = 0;
            outputTargetData.dataCollectionResponsibility = 'N/A';
            outputTargetData.MoV = [];
            outputTargetData.criticalSuccessFactor = [];
            outputTargetData.dataCollectionInstrument = [];
          }

          // Save output targets for the current year
          const response1 = await api.post('/output-targets/', {
            output_indicator: indicator.id,
            year: currentYear,
            baseline: outputTargetData.baseline || 0,
            Q1_target: outputTargetData.q1 || 0,
            Q2_target: outputTargetData.q2 || 0,
            Q3_target: outputTargetData.q3 || 0,
            Q4_target: outputTargetData.q4 || 0,
            total_target: outputTargetData.total || 0,
            responsibility: outputTargetData.dataCollectionResponsibility || 'N/A'
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          // Save output targets for the next year
          const response2 = await api.post('/output-targets/', {
            output_indicator: indicator.id,
            year: currentYear + 1,
            baseline: outputTargetData.baselineYear2 || 0,
            Q1_target: outputTargetData.q1Year2 || 0,
            Q2_target: outputTargetData.q2Year2 || 0,
            Q3_target: outputTargetData.q3Year2 || 0,
            Q4_target: outputTargetData.q4Year2 || 0,
            total_target: outputTargetData.totalYear2 || 0,
            responsibility: outputTargetData.dataCollectionResponsibility || 'N/A'
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          // Save Means of Verification (MoVs)
          const movResponse = await api.post('/output-movs/', {
            output_indicator_id: indicator.id,
            movs: outputTargetData.MoV.map(mov => mov.value)
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          // Save Critical Success Factors (CSFs)
          const csfResponse = await api.post('/output-csfs/', {
            output_indicator_id: indicator.id,
            output_csfs: outputTargetData.criticalSuccessFactor.map(csf => csf.value)
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          // Save Data Collection Instruments
          const instrumentResponse = await api.post('/output-instruments/', {
            output_indicator_id: indicator.id,
            output_instruments: outputTargetData.dataCollectionInstrument.map(instrument => instrument.value)
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

         // Save Total Output Budget if not 0
         const totalOutputBudget = getTotalOutputBudget(output.activities).toFixed(2);
          if (totalOutputBudget !== '0.00') {
            await api.post('/output-budgets/', {
              output: output.id,
              budget: totalOutputBudget
            }, {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            });
          }

          // **Save Output Weights**
          const weightResponse = await api.post(`/calculate-weights/${output.id}/${currentYear}/`, null, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          console.log('Output weights saved successfully:', weightResponse.data);
        }
      }

      // Save Total Reform Area Budget
      const totalReformAreaBudget = getTotalReformAreaBudget(selectedReformAreaId);
      await api.post('/reform-budgets/', {
        reform_area: selectedReformAreaId.value,
        budget: totalReformAreaBudget
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      // Save Activity Budgets
      const activityBudgetPromises = [];
      selectedReformAreaOutputs.value.forEach(output => {
        output.activities.forEach(activity => {
          // Only save Activity Budget if it's not all 0 or ''
          if (activity.estimated_budget !== '' && activity.estimated_budget !== 0) {
            activityBudgetPromises.push(api.post('/budgets/', {
              activity: activity.id,
              budget: activity.estimated_budget,
              fund_source: activity.source_of_fund // Include fund_source
            }, {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            }));
          }
        });
      });
      await Promise.all(activityBudgetPromises);

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

    fetchReformAreas();

    return {
      reformAreas,
      selectedReformAreaOutputs,
      selectedReformAreaId,
      selectedOutputId,
      toggleOutputs,
      toggleIndicators,
      showQuestion,
      output,
      outputIndicators,
      selectedIndicatorId,
      selectedAnswer,
      showQuestionDialog,
      currentYear,
      saveActivityBudget,
      getTotalOutputBudget,
      getTotalReformAreaBudget,
      // Additional variable to store total estimated budget for the reform area
      totalReformAreaBudget: ref(0),
      // Save activity budget when input changes
      activityBudgets,
      // Include generateUniqueId in the returned object
      generateUniqueId,
      outputTargets,
      validateTargets,
      getOutputTarget,
      outputFields,
      indicatorFields,
      addInput,
      removeInput,
      errorMessage,
      showErrorMessage,
      getTotalOutputBudget,
      getTotalReformAreaBudget,
      saveOutputTargets,
      saveActivitySource,
      // Additional variable to store total estimated budget for the reform area
      totalReformAreaBudget: ref(0),
      successMessage,
      implementationPeriod,
      outputIndicatorImplementationPeriod,
      reformAreaImplementationPeriod

    };
  },
  // ...
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

form {
			margin: auto;
			width: 100%;
			max-width: 1000px;
			padding: 20px;
			background-color: #f2f2f2;
			border-radius: 10px;
			box-shadow: 0px 0px 10px 2px #888;
			font-family: Arial, sans-serif;
			font-size: 16px;
			line-height: 1.5;
		}

.selected-reform-area h6 {
  margin-top: 0;
  color: #333;
}
.reform-area-item {
  cursor: pointer; /* Pointer cursor */
  transition: color 0.3s ease; /* Smooth color transition */
}

.reform-area-item:hover h5 {
  color: green; /* Text color on hover */
}

/* Optional: To ensure the cursor is always a pointer on the whole section */
.reform-area-item:hover {
  cursor: pointer;
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
