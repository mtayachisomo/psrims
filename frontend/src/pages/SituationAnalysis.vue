<template>
  <div class="form-container">
    <br>
    <form @submit.prevent="submitForm">
      <!-- Problem Identification -->
      <div id="problem-container">
        <label for="problem">1. Problem identification</label>
        <div class="hint" style="color: green;" ><strong>Hint:</strong> What are the challenges, issues, or problems deterring the efficient and effective delivery of the mandate?</div>
        <ul id="problemList">
          <li v-for="(problem, index) in problems" :key="index">
            <div>
              <textarea v-model="problems[index]" @input="updateIssues(index)" required></textarea>
              <q-btn unelevated flat label="Remove Problem" @click="removeProblem(index)" style="float: right; color: #ff0000;" />
            </div>
          </li>
        </ul>
        <q-btn unelevated color="positive" label="Add Problem" @click="addProblem" />
      </div>

      <!-- Reform Area -->
      <div id="reformArea-container">
        <label for="reformArea">2. Strategic interventions (Reform Area)</label>
        <div class="hint" style="color: green;"><strong>Hint:</strong> What are strategic interventions intended to be used to address the identified problems</div>
        <ul id="reformList">
          <li><textarea id="reformArea" v-model="reformArea" required style="width: calc(100% - 20px); padding: 8px;"></textarea></li>
        </ul>
      </div>

      <!-- Strategic Objectives selection -->
      <div id="strategic-objective-container">
        <label for="strategicObjective">3. Strategic Objective linked to the strategic intervention</label>
        <div class="hint" style="color: green;"><strong>Hint:</strong> Select the Strategic Objective to the strategic intervention (Reform Area)</div>
        <q-select
          v-model="selectedStrategicObjective"
          :options="formattedStrategicObjectives"
          label="Select Strategic Objective"
          emit-value
          map-options
          @input="onStrategicObjectiveSelected"
        />
      </div>

      <!-- Justification Section -->
      <div id="justification-container">
        <label for="justification">4. Justification</label>
        <div class="hint" style="color: green;"><strong>Hint:</strong> Provide justifications for the identified problems</div>
        <div v-for="(justification, index) in justifications" :key="index">
          <textarea class="justification-textarea" v-model="justifications[index]" required></textarea>
          <q-btn unelevated flat  label="Remove Justification" @click="removeJustification(index)" style="float: right; color: #ff0000;"/>
        </div>
        <q-btn unelevated color="positive" label="Add Justification" @click="addJustification" />
      </div>

      <!-- Thematic Area selection -->
      <div id="thematic-area-container">
        <label for="thematicArea">5. Thematic Area linked to MW2063</label>
        <div class="hint" style="color: green;"><strong>Hint:</strong> Under what Thematic Area (Pillar or Enabler) of MW2063, is the above Reform Area linked to</div>
        <q-select
          v-model="selectedThematicArea"
          :options="formattedThematicAreas"
          label="Select Thematic Area"
          emit-value
          map-options
          @input="onThematicAreaSelected"
        />
      </div>

      <!-- Issues Container -->
      <div>
        <label for="issues">6. Issues to be addressed by the reform area</label>
        <div class="hint" style="color: green;"><strong>Hint:</strong> What are the challenges, issues, or problems that the Reform Area is trying to resolve</div>
        <ul id="issues">
          <li v-for="(problem, index) in selectedProblems" :key="index">
            <label>
              <input type="checkbox" :value="problem" @change="updateSelectedIssues($event.target.value, $event.target.checked)">
              {{ problem }}
            </label>
          </li>
        </ul>
      </div>

      <!-- Outcome and Outcome Indicator Sections -->
      <div id="outcomes-container" v-if="showOutcomes">
        <div v-for="(outcome, outcomeIndex) in outcomes" :key="outcomeIndex" class="outcome-item">
          <label for="outcomes">Outcome {{ outcomeIndex + 1 }}</label>
          <div class="hint" style="color: green;"><strong>Hint:</strong> What are the ultimate benefits/results of the Reform Area</div>
          <ul class="outcomes-list">
            <li><textarea v-model="outcome.name" required></textarea></li>
          </ul>
          <div class="outcome-indicator-container">
            <label for="outcome_indicators">Outcome indicators</label>
            <div class="hint" style="color: green;"><strong>Hint:</strong> What are the measures to demonstrate that an outcome has been achieved</div>
            <ul class="outcome-indicators-list">
              <li v-for="(indicator, indicatorIndex) in outcome.indicators" :key="indicatorIndex">
                <textarea v-model="outcome.indicators[indicatorIndex]" required></textarea>
                <q-btn unelevated flat  label="Remove Outcome Indicator" @click="removeOutcomeIndicator(outcomeIndex, indicatorIndex)" style="float: right; color: #ff0000;" />
              </li>
            </ul>
            <q-btn unelevated color="positive" label="Add Outcome Indicator" @click="addOutcomeIndicator(outcomeIndex)" />
          </div><br>

          <!-- Output Section -->
          <div id="output-activity-container" v-for="(output, outputIndex) in outcome.outputs" :key="outputIndex">
            <label for="output">Output {{ outcomeIndex + 1 }}.{{ outputIndex + 1 }}</label>
            <textarea v-model="output.value" required></textarea>
            <div class="output-indicator-container">
              <label for="output_indicators">Output Indicators</label>
              <div class="hint" style="color: green;"><strong>Hint:</strong> What are intermediate deliverables, which should be in place to achieve the outcome.</div>
              <ul class="output-indicators-list">
                <li v-for="(indicator, indicatorIndex) in output.indicators" :key="indicatorIndex">
                  <textarea v-model="indicator.value" required></textarea>
                  <q-btn unelevated flat  label="Remove Output Indicator" @click="removeOutputIndicator(outcomeIndex, outputIndex, indicatorIndex)" style="float: right; color: #ff0000;" />
                </li>
              </ul>
              <q-btn unelevated color="positive" label="Add Output Indicator" @click="addOutputIndicator(outcomeIndex, outputIndex)" />
            </div>

            <!-- Activities Section -->
            <div class="activities-section">
              <label for="activities">Activities</label>
              <div class="hint" style="color: green;"><strong>Hint:</strong> What activities must be carried out in order to achieve the output</div>
              <ul class="activities-list">
                <li v-for="(activity, activityIndex) in output.activities" :key="activityIndex">
                  <textarea v-model="activity.value" required></textarea>
                  <q-btn unelevated flat  label="Remove Activity" @click="removeActivity(outcomeIndex, outputIndex, activityIndex)" style="float: right; color: #ff0000;" />
                </li>
              </ul>
              <q-btn unelevated color="positive" label="Add Activity" @click="addActivity(outcomeIndex, outputIndex)" />
            </div>
            <q-btn unelevated flat  label="Remove Output" @click="removeOutput(outcomeIndex, outputIndex)" style="float: right; color: #ff0000;" />
          </div><br>

          <q-btn unelevated color="positive" label="Add Output" @click="addOutput(outcomeIndex)" />
          <q-btn unelevated flat  label="Remove Outcome" @click="removeOutcome(outcomeIndex)" style="float: right; color: #ff0000;" />
        </div>
      </div>
      <div id="add-outcome-button-container">
        <q-btn unelevated color="positive" label="Add Outcome" @click="addOutcome" />
      </div>

      <div id="situation-analysis-message" class="message-container">
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </div>

      <div class="form-buttons">
          <!-- Submit and Additional Buttons -->
      <br>

      <q-btn unelevated color="positive" class="submit-button" label="Save" @click="validateAndShowConfirmationDialog" style="float: right; color: #ff0000;" />
      <br><br>
<q-btn unelevated color="positive" label="Add Reform Area" @click="addReformArea" style="float: right; color: #ff0000;"/><br><br>
<q-btn unelevated color="positive" label="Complete" @click="addComplete" style="float: right; color: #ff0000;"/><br><br>

      </div>
    </form>

<!-- Confirmation Modal -->
<q-dialog v-model="showDialog" persistent>
      <q-card class="custom-dialog">
        <q-card-section>
          <div class="text-h6">Reform Area Criteria</div>
          <div style="margin: auto; width: 80%;">{{ reformArea }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit.prevent="submitForm">
            <div class="criteria-input">
              <label>Efficiency</label>
              <div class="hint" style="color: green;"><strong>Hint:</strong> The ability of the reform area to deliver more output (service or products) with the least cost.</div>
              <q-input v-model="criteria.efficiency" type="textarea" autogrow required  />
            </div>
            <div class="criteria-input">
              <label>Effectiveness</label>
              <div class="hint" style="color: green;"><strong>Hint:</strong> The extent to which the reform area will produce the targeted or desired level of output (service or product).</div>
              <q-input v-model="criteria.effectiveness" type="textarea" autogrow required />
            </div>
            <div class="criteria-input">
              <label>Innovativeness</label>
              <div class="hint" style="color: green;"><strong>Hint:</strong> Originality in the reform area by virtue of introducing new ideas in the way of delivering the public services to achieve efficiency and effectiveness.</div>
              <q-input v-model="criteria.innovativeness" type="textarea" autogrow required />
            </div>
            <div class="criteria-input">
              <label>Creativity</label>
              <div class="hint" style="color: green;"><strong>Hint:</strong> The ability to use the idea created through innovation or innovativeness to enhance efficiency and effectiveness in the delivery of public services.</div>
              <q-input v-model="criteria.creativity" type="textarea" autogrow required />
            </div>
            <div class="criteria-input">
              <label>Sustainability</label>
              <div class="hint" style="color: green;"><strong>Hint:</strong> The extent to which the broad strategic initiative will sustain itself over time in terms of its existence and its impact.</div>
              <q-input v-model="criteria.sustainability" type="textarea" autogrow required />
            </div>
            <div class="criteria-input">
          <label>Transformativeness</label>
          <div class="hint" style="color: green;">
            <strong>Hint:</strong> The potential of the reform area to significantly change or revolutionize the way public services are delivered, leading to substantial improvements.
          </div>
          <q-input v-model="criteria.transformativeness" type="textarea" autogrow required />
        </div>
          </q-form>
        </q-card-section>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <q-card-actions align="right">
          <q-btn flat label="Cancel" style="color: #ff0000;"  v-close-popup />
          <q-btn flat label="Save" color="positive" @click="submitForm" />
        </q-card-actions>


      </q-card>
    </q-dialog>

  </div>
</template>
<script>
import { ref, onMounted } from 'vue';
import { api } from '/src/boot/axios';
import { fetchInstitutionData } from '/src/services/institutionAPI';
import { useRouter } from 'vue-router'; // Import Vue Router


export default {

  setup() {

    const problems = ref(['']);
    const justifications = ref(['']);
    const reformArea = ref('');
    const thematicAreaSelected = ref(false);
    const selectedProblems = ref([]);
    const successMessage = ref('');
    const errorMessage = ref('');
    const selectedStrategicObjective = ref(null);
    const selectedThematicArea = ref(null);
    const formattedThematicAreas = ref([]);
    const formattedStrategicObjectives = ref([]);
    const showOutcomes = ref(false);
    const objective_id = ref(null);
    const selectedIssues = ref([]); // Store selected issues as strings
    const outcomes = ref([]);
    const formSubmitted = ref(false);
    const showDialog = ref(false); // State for showing the confirmation dialog

    const criteria = ref({
      efficiency: '',
      effectiveness: '',
      innovativeness: '',
      creativity: '',
      sustainability: '',
      transformativeness: '',
    });

    const resetCriteria = () => {
      criteria.value = {
        efficiency: '',
        effectiveness: '',
        innovativeness: '',
        creativity: '',
        sustainability: '',
        transformativeness: '',
      };
    };
    const resetCheckboxes = () => {
      selectedIssues.value = []; // Reset the selectedIssues array
    };

    const resetSituationAnalysisMessage = () => {
      successMessage.value = ''; // Reset success message
      errorMessage.value = ''; // Reset error message
    };
    const resetJustifications = () => {
      justifications.value = [''];
    };

    const resetReformArea = () => {
      reformArea.value = '';
    };


    const resetThematicArea = () => {
      selectedThematicArea.value = null;
    };

    const resetStrategicObjective = () => {
      selectedStrategicObjective.value = null;
    };

    const resetOutcomes = () => {
      outcomes.value = [];
      showOutcomes.value = false;
    };


    const addProblem = () => {
      problems.value.push('');
      // Check if both problems are added and a thematic area is selected
      if (problems.value.length > 0 && selectedThematicArea.value !== null) {
        thematicAreaSelected.value = true;
        errorMessage.value = ''; // Reset error message
      }
    };

    const removeProblem = index => problems.value.splice(index, 1);

    const addJustification = () => {
  justifications.value.push('');
  errorMessage.value = ''; // Reset error message
};

    const removeJustification = index => justifications.value.splice(index, 1);

    const onStrategicObjectiveSelected = selectedObjective => {
      selectedStrategicObjective.value = selectedObjective;
    };


    const updateSelectedIssues = (value, checked) => {
  if (checked) {
    selectedIssues.value.push(value);
  } else {
    const index = selectedIssues.value.indexOf(value);
    if (index !== -1) {
      selectedIssues.value.splice(index, 1);
    }
  }
};



    const onThematicAreaSelected = selectedArea => {
      console.log('Selected Thematic Area:', selectedArea);
      selectedThematicArea.value = selectedArea;
      thematicAreaSelected.value = true;
      errorMessage.value = ''; // Reset error message
    };

    const updateIssues = index => {
      selectedProblems.value[index] = problems.value[index];
      errorMessage.value = ''; // Reset error message
    };

    const fetchThematicAreas = async () => {
  try {
    const institutionId = await getInstitutionId();
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Fetch thematic areas
    const thematicAreasResponse = await api.get('/thematic-areas/all/', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    if (thematicAreasResponse && thematicAreasResponse.data && Array.isArray(thematicAreasResponse.data)) {
      formattedThematicAreas.value = thematicAreasResponse.data.map(area => ({
        label: area.thematic_area,
        value: area.id
      }));
    } else {
      throw new Error('Invalid response format for thematic areas');
    }

  } catch (error) {
    console.error('Error fetching thematic areas and strategic objectives:', error);
    throw new Error('Failed to fetch thematic areas and strategic objectives');
  }
};

    const fetchStrategicObjectives = async () => {
      try {
        const institutionId = await getInstitutionId();
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        // Fetch strategic objectives based on institution ID
        const strategicObjectivesResponse = await api.get(`/strategic-objectives/institution/${institutionId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        if (strategicObjectivesResponse && strategicObjectivesResponse.data) {
          // Format strategic objectives with both label and ID
          formattedStrategicObjectives.value = strategicObjectivesResponse.data.map(objective => ({
            label: objective.objective, // Use the name of the objective as the label
            value: objective.id // Use the ID of the objective as the value
          }));
        } else {
          throw new Error('Invalid response format for strategic objectives');
        }
      } catch (error) {
        console.error('Error fetching strategic objectives:', error);
        throw new Error('Failed to fetch strategic objectives');
      }
    };

    const getInstitutionId = async () => {
      try {
        const institutionData = await fetchInstitutionData();
        return institutionData.id;
      } catch (error) {
        throw new Error('Failed to fetch institution ID');
      }
    };

    const addOutcome = () => {
      outcomes.value.push({ name: '', indicators: [''] });
      showOutcomes.value = true;
      errorMessage.value = ''; // Reset error message
    };

    const removeOutcome = index => {
      outcomes.value.splice(index, 1);
      if (outcomes.value.length === 0) {
        showOutcomes.value = false;
      }
    };



    const addOutcomeIndicator = (outcomeIndex) => {
  outcomes.value[outcomeIndex].indicators.push('');
  errorMessage.value = ''; // Reset error message
};



    const removeOutcomeIndicator = (outcomeIndex, indicatorIndex) => {
      outcomes.value[outcomeIndex].indicators.splice(indicatorIndex, 1);
    };

    const updateOutcomeIndicator = (outcomeIndex, indicatorIndex, value) => {
      outcomes.value[outcomeIndex].indicators[indicatorIndex] = value;
    };

    const addOutput = outcomeIndex => {
      if (!outcomes.value[outcomeIndex].outputs) {
        outcomes.value[outcomeIndex].outputs = []; // Initialize outputs array if it's undefined
      }
      outcomes.value[outcomeIndex].outputs.push({ value: '', indicators: [] });
      errorMessage.value = ''; // Reset error message
    };

    const removeOutput = (outcomeIndex, outputIndex) => {
      outcomes.value[outcomeIndex].outputs.splice(outputIndex, 1);
    };

    const addOutputIndicator = (outcomeIndex, outputIndex) => {
      const output = outcomes.value[outcomeIndex].outputs[outputIndex];
      if (!output.indicators) {
        // Initialize indicators array if it's undefined
        output.indicators = [];
      }
      output.indicators.push({ value: '' });
      errorMessage.value = ''; // Reset error message
    };

    const removeOutputIndicator = (outcomeIndex, outputIndex, indicatorIndex) => {
      outcomes.value[outcomeIndex].outputs[outputIndex].indicators.splice(indicatorIndex, 1);
    };

    const addActivity = (outcomeIndex, outputIndex) => {
      const output = outcomes.value[outcomeIndex].outputs[outputIndex];
      if (!output.activities) {
        // Initialize activities array if it's undefined
        output.activities = [];
      }
      output.activities.push({ value: '' });
      errorMessage.value = ''; // Reset error message
    };

    const removeActivity = (outcomeIndex, outputIndex, activityIndex) => {
      outcomes.value[outcomeIndex].outputs[outputIndex].activities.splice(activityIndex, 1);
    };

// Function to show the confirmation dialog
const showConfirmationDialog = () => {
      showDialog.value = true;
    };



    // Validation functions
    const validateForm = () => {

      if (!reformArea.value) {
        errorMessage.value = 'Reform Area is required.';
        return false;
      }
      if (!selectedStrategicObjective.value) {
        errorMessage.value = 'Strategic Objective is required.';
        return false;
      }
      if (!selectedThematicArea.value) {
        errorMessage.value = 'Thematic Area is required.';
        return false;
      }
      if (selectedIssues.value.length === 0) {
        errorMessage.value = 'At least one Problem must be selected.';
        return false;
      }
      if (outcomes.value.length === 0) {
        errorMessage.value = 'At least one Outcome is required.';
        return false;
      }

      for (const outcome of outcomes.value) {
        if (outcome.indicators.length === 0 || !outcome.indicators[0]) {
          errorMessage.value = 'Each Outcome must have at least one Indicator.';
          return false;
        }
          if (!outcome.outputs || outcome.outputs.length === 0) {
          errorMessage.value = 'Each Outcome must have at least one Output.';
          return false;
        }

        for (const output of outcome.outputs) {
          if (output.indicators.length === 0 || !output.indicators[0]) {
            errorMessage.value = 'Each Output must have at least one Indicator.';
            return false;
          }
          if (!output.activities || output.activities.length === 0 || !output.activities[0]) {
          errorMessage.value = 'Each Output must have at least one Activity.';
          return false;
        }

        }
      }

      errorMessage.value = '';
      return true;
    };

    // Criteria validation function
    const validateCriteria = () => {
  // Clear previous error messages
  errorMessage.value = '';

  // Check if mandatory fields are filled
  if (!criteria.value.efficiency) {
    errorMessage.value = 'Efficiency is required.';
    return false;
  }
  if (!criteria.value.effectiveness) {
    errorMessage.value = 'Effectiveness is required.';
    return false;
  }
  if (!criteria.value.sustainability) {
    errorMessage.value = 'Sustainability is required.';
    return false;
  }
  if (!criteria.value.transformativeness) {
    errorMessage.value = 'Transformativeness is required.';
    return false;
  }

  // Set default values for optional fields if they are not provided
  if (!criteria.value.innovativeness) {
    criteria.value.innovativeness = 'N/A';
  }
  if (!criteria.value.creativity) {
    criteria.value.creativity = 'N/A';
  }

  // Validation passed
  return true;
};

     // Function to validate form and show confirmation dialog
const validateAndShowConfirmationDialog = async () => {
  if (!validateForm()) {
    console.error('Form validation failed.');
    return;
  }

  // If form and criteria are valid, proceed to show the confirmation dialog
  showConfirmationDialog();
};

    // Submission function
    const submitForm = async () => {
      if (!validateForm()) return;

      // Validate criteria fields
  if (!validateCriteria()) {
    console.error('Criteria validation failed.');
    return;
  }


  try {
    const reformAreaId = await postReformArea();
    await postJustifications(reformAreaId);
    await postReformAreaCriteria(reformAreaId, criteria.value);


    // Post the selected issues as problems
    await postProblems(reformAreaId, selectedIssues.value);

    // Iterate over outcomes and post each one with the reform area ID
    await Promise.all(outcomes.value.map(async outcome => {
      const outcomeId = await postOutcome(outcome, reformAreaId); // Get the outcomeId from the postOutcome function
      await postOutcomeIndicators(outcomeId, outcome.indicators); // Pass outcomeId and indicators to postOutcomeIndicators

      // Iterate over outputs and post each one with the outcome ID
      await Promise.all(outcome.outputs.map(async output => {
        const outputId = await postOutputs(reformAreaId, outcomeId, [output]); // Assuming each output is an object
        await postOutputIndicator(outputId, output.indicators); // Pass outputId and indicators to postOutputIndicator
        await postActivity(outputId, output.activities); // Pass outputId and activities to postActivity
      }));

      console.log('Outcome ID:', outcomeId); // Log the outcome ID
    }));
    // Set formSubmitted to true after successful form submission
    formSubmitted.value = true;
 // Set success message if form submission is successful
 successMessage.value = 'Form saved successfully.';
        // Clear error message if there was any
        errorMessage.value = '';
      } catch (error) {
        console.error('Error submitting form:', error);
        // Set error message if form submission fails
        errorMessage.value = 'Failed to submit form. Please try again later.';
        // Clear success message if there was any
        successMessage.value = '';
      }
    };

    const postReformArea = async () => {
  try {
    const institutionId = await getInstitutionId();
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Post reform area
    const response = await api.post('/reform-areas/', {
      objective: selectedStrategicObjective.value,
      institution: institutionId,
      thematic_area: selectedThematicArea.value, // Include thematic area ID
      reform_area: reformArea.value,
      year: new Date().getFullYear()
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    // Extract the id from the response
    const reformAreaId = response.data.id;

    console.log('Reform area posted successfully with id:', reformAreaId);

    // Return the reform area id
    return reformAreaId;
  } catch (error) {
    console.error('Failed to post reform area:', error);
    throw new Error('Failed to post reform area');
  }
};



    const postProblems = async (reformAreaId, selectedIssues) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Construct the request body with reform area id and selected issues
    const requestBody = {
      reform_area_id: reformAreaId,
      problems: selectedIssues
    };

    // Post problems
    const response = await api.post('/problems/', requestBody, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    console.log('Problems posted successfully');
    return response.data; // Optionally, you can return data from the response
  } catch (error) {
    console.error('Failed to post problems:', error);
    throw new Error('Failed to post problems');
  }
};

const postReformAreaCriteria = async (reformAreaId, criteriaData) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Construct the request body with reform area id and criteria data
    const requestBody = {
      reform_area: reformAreaId,
      effectiveness: criteriaData.effectiveness,
      efficiency: criteriaData.efficiency,
      innovativeness: criteriaData.innovativeness,
      creativity: criteriaData.creativity,
      sustainability: criteriaData.sustainability,
      transformativeness:criteriaData.transformativeness,
    };

    // Post criteria
    const response = await api.post('/reform-area-criteria/', requestBody, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    console.log('Criteria posted successfully');
    showDialog.value = false; // Close dialog on successful save

    return response.data; // Optionally, you can return data from the response

  } catch (error) {
    console.error('Failed to post criteria:', error);
    throw new Error('Failed to post criteria');
  }
};


    const postJustifications = async (reformAreaId) => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        // Construct the request body with the reform area id
        const requestBody = {
          reform_area_id: reformAreaId,
          justifications: justifications.value
        };

        await api.post('/justifications/', requestBody, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        console.log('Justifications posted successfully');
      } catch (error) {
        throw new Error('Failed to post justifications');
      }
    };

    const postOutcome = async (outcome, reformAreaId) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Post outcome
    const outcomeResponse = await api.post('/outcomes/', {
      reform_area: reformAreaId, // Include reform area ID in the payload
      outcomes: [outcome.name]
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    // Log the response data for debugging
    console.log('Outcome Response Data:', outcomeResponse.data);

    // Extract the outcome ID from the first object in the data array
    const outcomeId = outcomeResponse.data.data[0]?.id;

    if (!outcomeId) {
      console.error('Invalid response format for outcome. Response data:', outcomeResponse.data);
      throw new Error('Failed to extract outcome ID from response');
    }

    console.log('Outcome posted successfully with id:', outcomeId);

    // Return the outcome ID
    return outcomeId;
  } catch (error) {
    console.error('Failed to post outcome:', error);
    throw new Error('Failed to post outcome');
  }
};



const postOutcomeIndicators = async (outcomeId, indicators) => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        // Prepare the request body with outcome ID and indicators
        const requestBody = {
          outcome: outcomeId,
          indicators: indicators
        };

        // Post the outcome indicators
        const response = await api.post('/outcome-indicators/', requestBody, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        console.log('Outcome indicators posted successfully');
        return response.data; // Optionally, you can return data from the response
      } catch (error) {
        console.error('Failed to post outcome indicators:', error);
        throw new Error('Failed to post outcome indicators');
      }
    };

    const postOutputs = async (reformAreaId, outcomeId, outputs) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Post outputs
    const response = await api.post('/outputs/', {
      reform_area: reformAreaId,
      outcome: outcomeId,
      outputs: outputs.map(output => output.value) // Assuming each output has a 'value' property
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    console.log('Outputs posted successfully');
    console.log('Response Data:', response.data); // Log the entire response data

    // Extract and log the output ID
    const outputData = response.data.data; // Access the 'data' array
    const outputId = outputData[0].id; // Access the 'id' property from the first object in the 'data' array
    console.log('Output ID:', outputId);

    return outputId;
  } catch (error) {
    console.error('Failed to post outputs:', error);
    throw new Error('Failed to post outputs');
  }
};


const postOutputIndicator = async (outputId, indicators) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Construct the request body with the outputId and indicators
    const requestBody = {
      output: outputId, // Use the obtained outputId here
      indicators: indicators.map(indicator => indicator.value) // Assuming each indicator has a 'value' property
    };

    // Post output indicators
    const response = await api.post('/output-indicators/', requestBody, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    console.log('Output indicators posted successfully');
    return response.data; // Optionally, you can return data from the response
  } catch (error) {
    console.error('Failed to post output indicators:', error);
    throw new Error('Failed to post output indicators');
  }
};



const postActivity = async (outputId, activities) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Post activities
    const response = await api.post('/activities/', {
      output: outputId,
      activities: activities.map(activity => activity.value) // Assuming each activity has a 'value' property
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    console.log('Activities posted successfully');
    hideMessageAfterDelay('successMessage');
    return response.data; // Optionally, you can return data from the response
  } catch (error) {
    console.error('Failed to post activities:', error);
    throw new Error('Failed to post activities');
  }
};

const hideMessageAfterDelay = (messageType) => {
      setTimeout(() => {
        if (messageType === 'successMessage') {
          successMessage.value = '';
        } else if (messageType === 'errorMessage') {
          errorMessage.value = '';
        }
      }, 2000); // 3 seconds
    };

const addReformArea = () => {

// Untick all checkboxes
const checkboxes = document.querySelectorAll('input[type="checkbox"]');
checkboxes.forEach((checkbox) => {
checkbox.checked = false;
});
// Reset sections
resetSituationAnalysisMessage();
resetJustifications();
resetReformArea();
resetThematicArea();
resetStrategicObjective();
resetOutcomes();
resetCheckboxes();
resetCriteria();


// Scroll to the Reform Area section after resetting
const reformAreaContainer = document.getElementById('problem-container');
reformAreaContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
};



const router = useRouter(); // Initialize router

const addComplete = () => {
  if (formSubmitted.value) {
    // Clear all form fields
    problems.value = [''];
    justifications.value = [''];
    reformArea.value = '';
    resetThematicArea();
    resetStrategicObjective();
    resetOutcomes();
    resetCheckboxes();

    // Redirect to the 'ThanksSituationAnalysis' page
    router.push({ name: 'ThanksSituationAnalysis' });
  } else {
    // Handle the case where form is not yet submitted
    // You can display an error message or perform other actions here
    errorMessage.value = 'Please add at Least ONE REFORM AREA😊';
  }
};

    const formatOptions = options => options.map(option => ({ label: option.thematic_area || option.objective, value: option.id }));


    // Fetch thematic areas and strategic objectives on component mount
    fetchThematicAreas();
    fetchStrategicObjectives();

    return {
      problems,
      justifications,
      reformArea,
      thematicAreaSelected,
      selectedProblems,
      selectedIssues,
      selectedStrategicObjective,
      selectedThematicArea,
      formattedThematicAreas,
      formattedStrategicObjectives,
      postOutcomeIndicators,
      postReformAreaCriteria,
      addProblem,
      removeProblem,
      addJustification,
      removeJustification,
      onStrategicObjectiveSelected,
      onThematicAreaSelected,
      updateIssues,
      submitForm,
      showOutcomes,
      outcomes,
      addOutcome,
      removeOutcome,
      addOutcomeIndicator,
      updateSelectedIssues,
      updateOutcomeIndicator,
      removeOutcomeIndicator,
      removeOutputIndicator,
      addOutputIndicator,
      removeOutput,
      addActivity,
      removeActivity,
      addOutput,
      addReformArea,
      addComplete,
      objective_id,
      successMessage,
      errorMessage,
      showDialog,
      criteria,
      showConfirmationDialog,
      validateAndShowConfirmationDialog,




    };
  }
};
</script>

<style scoped>



.hint {
  color: #666;
  font-size: 14px;
  border-left: 6px solid #ff0000; /* Change color as needed */
  padding: 10px;
  margin-bottom: 3px; /* Reduce margin-bottom to 3px */

}

ul {
  list-style-type: none;

}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

textarea {
  width: calc(100% - 20px);
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  margin-bottom: 10px; /* Maintain the same margin-bottom for text areas */
  margin-top: 5px; /* Reduce margin-top for text areas */
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

#outcomes-container {
    width: 100%;
    max-width: 1000px;
    margin-bottom: 20px;
    padding: 20px;
    background-color: #f2f2f2;
    border-radius: 10px;
    box-shadow: 0px 0px 10px 2px #888;
    font-family: Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5;
}
.custom-dialog {
  width: 600px;
  max-width: 90vw;
  height: auto;
  max-height: 90vh;
}
.criteria-input {
  margin-bottom: 5px;
}

#output-activity-container {
  margin: auto;
  width: 80%;
  max-width: 1000px;
  padding: 20px;
  background-color: #f2f2f2;
  border-radius: 10px;
  box-shadow: 0px 0px 10px 2px #888;
  font-family: Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px; /* Added margin-bottom for spacing between output/activity sections */
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
