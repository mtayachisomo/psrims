<template>
  <div class="form-container">
    <br>
    <form @submit.prevent="submitForm">
      <!-- Reform Area -->
      <div class="form-section">
        <label class="form-label" for="reformArea">Reform Area:</label>
        <p>{{ reformArea.reform_area }}</p>
      </div>
      <!-- Thematic Area -->
      <div class="form-section">
        <label class="form-label" for="thematicArea">Thematic Area:</label>
        <p>{{ thematicArea }}</p>
      </div>
      <!-- Focus Area -->
      <div class="form-section">
        <label class="form-label">Focus Area:</label>
        <div class="checkbox-options">
          <div v-for="focusArea in focusAreas" :key="focusArea.id" class="checkbox-option">
            <input type="checkbox" v-model="selectedFocusAreas" :value="focusArea.id" :id="'focusArea_' + focusArea.id" />
            <label :for="'focusArea_' + focusArea.id">{{ focusArea.focus_area }}</label>
          </div>
        </div>
      </div>
      <!-- Additional Fields Container -->
      <div id="additionalFieldsContainer" class="additional-fields-container" :style="{ display: additionalFieldsDisplay }">
        <!-- Justification -->
        <div class="form-section">
          <label class="form-label" for="justification">Justification for undertaking the Reform Area:</label>
          <div id="justification-container" class="textarea-container">
            <textarea v-for="(justification, index) in reformArea.justifications" :key="index" v-model="justification.justification"></textarea>
          </div>
        </div>
        <!-- Problems -->
        <div class="form-section">
          <label class="form-label" for="problems">Problems:</label>
          <div id="problems-container" class="textarea-container">
            <textarea v-for="(problem, index) in reformArea.problems" :key="index" v-model="problem.problem"></textarea>
          </div>
        </div>
      <!-- Reform Status -->
      <div class="form-section reform-status-section">
          <label class="form-label">Reform Status:</label>
          <div class="radio-option">
            <input type="radio" id="newReform" value="0" v-model="selectedReformStatus" />
            <label for="newReform">New Reform</label>
          </div>
          <div class="radio-option">
            <input type="radio" id="continuingReform" value="1" v-model="selectedReformStatus" />
            <label for="continuingReform">Continuing Reform</label>
          </div>
        </div>

      <div class="form-row">
  <!-- Sector -->
  <div class="hint">
    <label class="form-label" for="sector">Sector:</label>
    <select v-model="selectedSector" class="custom-select">
      <option disabled value="">Select any option</option>
      <option v-for="sector in sectors" :key="sector.id" :value="sector.id" @mouseover="hoverOption($event, 'green')">{{ sector.sector }}</option>
    </select>
  </div>

  <!-- Reform Category -->
  <div class="hint">
    <label class="form-label" for="reformCategory">Reform Category:</label>
    <select v-model="selectedReformCategory" class="custom-select">
      <option disabled value="">Select any option</option>
      <option v-for="category in reformCategories" :key="category.id" :value="category.id" @mouseover="hoverOption($event, 'green')">{{ category.category }}</option>
    </select>
  </div>
</div>



        <!-- Outcome -->
        <div class="outcome-container">
          <div class="form-section" v-for="(outcome, index) in reformArea.outcomes" :key="index">
            <label class="form-label" for="outcome">Proposed Outcome {{ index + 1 }}</label>
            <div class="textarea-container">
              <textarea v-model="outcome.outcomes"></textarea>
            </div>
            <label class="form-label" for="outcome">Outcome Indicators:</label>
            <div class="textarea-container">
              <textarea v-for="(indicator, i) in outcome.outcome_indicators" :key="i" v-model="indicator.indicator"></textarea>
            </div>
            <!-- Outputs -->
            <div class="output-container">
              <div class="form-section" v-for="(output, i) in outcome.outputs" :key="i">
                <label class="form-label" for="output">Proposed Output {{ i + 1 }} </label>
                <div class="textarea-container">
                  <textarea v-model="output.output"></textarea>
                </div>
                <label class="form-label" for="output">Output Indicators:</label>
                <div class="textarea-container">
                  <textarea v-for="(indicator, j) in output.output_indicators" :key="j" v-model="indicator.indicator"></textarea>
                </div>
                <label class="form-label" for="output">Activities:</label>
                <div class="textarea-container">
                  <textarea v-for="(activity, k) in output.activities" :key="k" v-model="activity.activity"></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Next/Previous Reform Area Buttons -->
        <div class="form-section" id="navigation-buttons">
  <div>
    <q-btn unelevated color="positive" label="Next Reform Area" @click="goToNextReformArea" style="float: right;"/>
  </div>
  <div style="float: right;">&nbsp;&nbsp;&nbsp;</div> <!-- Non-breaking spaces -->
  <q-btn unelevated color="positive" label="Previous Reform Area" @click="goToPreviousReformArea" style="float: right;"/>
  <q-btn unelevated color="positive" label="Save" @click="submitForm" style="float: left;"/>
</div>


<!-- Success and Error Messages -->
<div id="situation-analysis-message" class="message-container">
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
      </div>
    </form>
  </div>

  <!-- Modal for confirmation -->
  <q-dialog v-model="showConfirmationModal">
    <q-card>
      <q-card-section>
        <h5 class="modal-title">Confirmation</h5>
      </q-card-section>

      <q-card-section>
        <p>HAVE YOU COMPLETED THE REFORM AREA CONFIGURATIONS?</p>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="Yes" color="positive" @click="handleNoConfirmation" />
        <q-btn label="No" color="positive" @click="restartFromFirstReformArea" />


      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { api } from '/src/boot/axios';
import { fetchInstitutionData } from '/src/services/institutionAPI';
import { useRouter } from 'vue-router'; // Import Vue Router

export default {
  setup() {
    const accessToken = ref('');
    const reformArea = ref({ problems: '' });
    const thematicArea = ref('');
    const focusAreas = ref([]);
    const selectedFocusAreas = ref([]);
    const reformAreaId = ref(null);
    const selectedReformStatus = ref('');
    const selectedSector = ref('');
    const successMessage = ref('');
    const sectors = ref([]);
    const reformAreas = ref([]);
    const reformCategories = ref([]);
    const selectedReformCategory = ref('');
    let currentIndex = ref(0);
    const showConfirmationModal = ref(false);
    const errorMessage = ref('');
    const router = useRouter(); // Initialize the router instance here

    const resetReformStatus = () => {
  selectedReformStatus.value = ''; // Reset reform status radio buttons
};

const resetSector = () => {
  selectedSector.value = ''; // Reset sector select dropdown
};

const resetReformCategory = () => {
  selectedReformCategory.value = ''; // Reset reform category select dropdown
};

// Combined reset function for all fields
const resetAllFields = () => {
  resetReformStatus();
  resetSector();
  resetReformCategory();
};

    const fetchReformAreas = async () => {
  try {
    accessToken.value = localStorage.getItem('accessToken');
    if (!accessToken.value) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    const institutionId = await getInstitutionId();
    const response = await api.get(`/reform-areas/institution/${institutionId}`, {
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
      },
    });

    if (response && response.data && Array.isArray(response.data) && response.data.length > 0) {
      reformAreas.value = response.data;
      reformArea.value = response.data[currentIndex.value];

      // Extract the thematic area ID
      const thematicAreaId = reformArea.value.thematic_area;

      // Fetch thematic area details
      thematicArea.value = await fetchThematicArea(thematicAreaId);

      // Fetch focus areas using the thematic area ID
      focusAreas.value = await fetchFocusAreas(thematicAreaId);

      // Set the reform area ID
      reformAreaId.value = response.data[currentIndex.value].id;

      // Fetch reform area details
      await fetchReformAreaDetails(reformAreaId.value);

      // Fetch sectors
      await fetchSectors();
      await fetchReformCategories();
    } else {
      throw new Error('No reform areas found.');
    }
  } catch (error) {
    console.error('Error fetching reform areas:', error);
  }
};

// Watch for changes in selectedFocusAreas and toggle display of additionalFieldsContainer accordingly
watch(selectedFocusAreas, (newValue) => {
  if (newValue.length > 0) {
    additionalFieldsDisplay.value = 'block';
  } else {
    additionalFieldsDisplay.value = 'none';
  }
});

const fetchThematicArea = async (thematicAreaId) => {
  try {
    const response = await api.get(`/thematic-areas/${thematicAreaId}`, {
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
      },
    });

    if (response && response.data) {
      return response.data.thematic_area;
    } else {
      throw new Error('No thematic area found.');
    }
  } catch (error) {
    console.error('Error fetching thematic area:', error);
  }
};

    const fetchFocusAreas = async (thematicAreaId) => {
      try {
        const response = await api.get(`/thematic-areas/${thematicAreaId}/focus-areas/`, {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        });

        if (response && response.data && Array.isArray(response.data)) {
          return response.data;
        } else {
          throw new Error('No focus areas found.');
        }
      } catch (error) {
        console.error('Error fetching focus areas:', error);
      }
    };

    const fetchReformAreaDetails = async (reformAreaId) => {
      try {
        const response = await api.get(`/reform_area/${reformAreaId}`, {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        });

        if (response && response.data) {
          const reformAreaDetails = response.data;
          reformArea.value.problems = reformAreaDetails.problems;
          reformArea.value.outcomes = reformAreaDetails.outcomes;
          reformArea.value.justifications = reformAreaDetails.justifications;
        } else {
          throw new Error('No detailed reform area found.');
        }
      } catch (error) {
        console.error('Error fetching detailed reform area:', error);
      }
    };

   // Fetch sectors
   const fetchSectors = async () => {
      try {
        const response = await api.get(`/reform-area-sector/list/`, {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        });
        sectors.value = response.data;
      } catch (error) {
        console.error('Error fetching sectors:', error);
      }
    };

    // Fetch reform categories
    const fetchReformCategories = async () => {
      try {
        const response = await api.get(`/reform-category/list/`, {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        });
        reformCategories.value = response.data;
      } catch (error) {
        console.error('Error fetching reform categories:', error);
      }
    };

    const getInstitutionId = async () => {
      try {
        const institutionData = await fetchInstitutionData();
        return institutionData.id;
      } catch (error) {
        console.error('Error fetching institution ID:', error);
      }
    };

    // Function to hide message after a delay
    const hideMessageAfterDelay = (type) => {
      setTimeout(() => {
        if (type === 'successMessage') {
          successMessage.value = '';
        } else if (type === 'errorMessage') {
          errorMessage.value = '';
        }
      }, 3000); // 3000 ms = 3   seconds
    };


    const submitForm = async () => {
  // Reset error message
  errorMessage.value = '';

  try {
    const reformAreaIdValue = reformAreaId.value;
    const focusAreaIds = selectedFocusAreas.value;

    if (!reformAreaIdValue || focusAreaIds.length === 0) {
      throw new Error('Reform area ID or focus area IDs not available.');
    }

    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Check if the reform status is selected
    if (!selectedReformStatus.value) {
      throw new Error('Please indicate the status of the Reform Area, whether it is New or Old');
    }
    // Check if the sector is selected
    if (!selectedSector.value) {
      throw new Error('Please select a sector.');
    }

    // Check if the reform category is selected
    if (!selectedReformCategory.value) {
      throw new Error('Please select a reform category.');
    }

    for (const focusAreaId of focusAreaIds) {
      const response = await api.post('/reformfocusarea/', {
        reform_area: reformAreaIdValue,
        focus_area: focusAreaId,
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      console.log('Response from server for focus area', focusAreaId, ':', response.data);
    }

    await updateJustifications();
    await updateProblems();
    await postReformStatus();
    await postReformAreaSector();
    await postReformCategoryMapping();
    await updateOutcomes();

    successMessage.value = `The Reform Area: ${reformArea.value.reform_area} has been configured successfully`;
    hideMessageAfterDelay('successMessage');
  } catch (error) {
    console.error('Error submitting form:', error);

    // Display error message to the user
    errorMessage.value = error.message;
    hideMessageAfterDelay('errorMessage');
  }
};



    const updateJustifications = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        for (let i = 0; i < reformArea.value.justifications.length; i++) {
          const justification = reformArea.value.justifications[i];
          await api.put(`/justifications/${justification.id}/update/`, {
            reform_area_id: reformAreaId.value,
            justifications: justification.justification,
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          console.log(`Justification ${justification.id} updated successfully.`);
        }
      } catch (error) {
        console.error('Error updating justifications:', error);
      }
    };

    const updateProblems = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        for (let i = 0; i < reformArea.value.problems.length; i++) {
          const problem = reformArea.value.problems[i];
          await api.put(`/problems/${problem.id}/update/`, {
            reform_area_id: reformAreaId.value,
            problems: problem.problem,
          }, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          console.log(`Problem ${problem.id} updated successfully.`);
        }
      } catch (error) {
        console.error('Error updating problems:', error);
      }
    };

    const postReformStatus = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        await api.post(`/reform-statuses/`, {
          reform_area_id: reformAreaId.value,
          reform_status: selectedReformStatus.value,
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        console.log(`Reform status updated successfully.`);
      } catch (error) {
        console.error('Error updating reform status:', error);
      }
    };


    const postReformAreaSector = async () => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Make sure selectedSector has a value
    if (!selectedSector.value) {
      throw new Error('Please select a sector.');
    }

    // Post data to /reform-area-sector-mapping/create/ endpoint
    await api.post('/reform-area-sector-mapping/create/', {
      reform_area: reformAreaId.value,
      sector: selectedSector.value,
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    console.log('Reform area and sector mapping created successfully.');
  } catch (error) {
    console.error('Error creating reform area and sector mapping:', error);
  }
};

const postReformCategoryMapping = async () => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    // Make sure selectedReformCategory has a value
    if (!selectedReformCategory.value) {
      throw new Error('Please select a reform category.');
    }

    // Post data to /reform-category-mapping/ endpoint
    await api.post('/reform-category-mapping/', {
      reform_area: reformAreaId.value,
      category: selectedReformCategory.value,
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    console.log('Reform area and reform category mapping created successfully.');
  } catch (error) {
    console.error('Error creating reform area and reform category mapping:', error);
  }
};


    const updateOutcomes = async () => {
      try {
        for (let i = 0; i < reformArea.value.outcomes.length; i++) {
          const outcome = reformArea.value.outcomes[i];
          await updateOutcome(outcome);
          await updateOutcomeIndicators(outcome);
          for (let j = 0; j < outcome.outputs.length; j++) {
            const output = outcome.outputs[j];
            await updateOutput(output, outcome.id);
            await updateOutputIndicators(output);
            await updateActivities(output);
          }
          console.log(`Outcome ${outcome.id} and related entities updated successfully.`);
        }
      } catch (error) {
        console.error('Error updating outcomes and related entities:', error);
      }
    };

    const updateOutcome = async (outcome) => {
      try {
        await api.put(`/outcomes/update/${outcome.id}/`, {
          reform_area: reformAreaId.value,
          outcomes: [outcome.outcomes],
        }, {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        });
        console.log(`Outcome ${outcome.id} updated successfully.`);
      } catch (error) {
        console.error(`Error updating outcome ${outcome.id}:`, error);
      }
    };

    const updateOutcomeIndicators = async (outcome) => {
      try {
        for (let i = 0; i < outcome.outcome_indicators.length; i++) {
          const indicator = outcome.outcome_indicators[i];
          await api.put(`/outcome-indicators/update/${indicator.id}/`, {
            outcome: outcome.id,
            indicators: [indicator.indicator],
          }, {
            headers: {
              Authorization: `Bearer ${accessToken.value}`,
            },
          });
          console.log(`Outcome indicator ${indicator.id} updated successfully.`);
        }
      } catch (error) {
        console.error(`Error updating outcome indicators for outcome ${outcome.id}:`, error);
      }
    };

    const updateOutput = async (output, outcomeId) => {
      try {
        await api.put(`/outputs/update/${output.id}/`, {
          reform_area: reformAreaId.value,
          outcome: outcomeId,
          output: [output.output],
        }, {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        });
        console.log(`Output ${output.id} updated successfully.`);
      } catch (error) {
        console.error(`Error updating output ${output.id}:`, error);
      }
    };

    const updateOutputIndicators = async (output) => {
      try {
        for (let i = 0; i < output.output_indicators.length; i++) {
          const indicator = output.output_indicators[i];
          await api.put(`/output-indicators/update/${indicator.id}/`, {
            output: output.id,
            indicators: [indicator.indicator],
          }, {
            headers: {
              Authorization: `Bearer ${accessToken.value}`,
            },
          });
          console.log(`Output indicator ${indicator.id} updated successfully.`);
        }
      } catch (error) {
        console.error(`Error updating output indicators for output ${output.id}:`, error);
      }
    };

    const updateActivities = async (output) => {
      try {
        for (let i = 0; i < output.activities.length; i++) {
          const activity = output.activities[i];
          await api.put(`/activities/update/${activity.id}/`, {
            output: output.id,
            activities: [activity.activity],
          }, {
            headers: {
              Authorization: `Bearer ${accessToken.value}`,
            },
          });
          console.log(`Activity ${activity.id} updated successfully.`);
        }
      } catch (error) {
        console.error(`Error updating activities for output ${output.id}:`, error);
      }
    };

    const goToNextReformArea = async () => {
      successMessage.value = '';
  if (currentIndex.value < reformAreas.value.length - 1) {
    resetAllFields();
    currentIndex.value++;
    // Reset selected focus areas
    selectedFocusAreas.value = [];
    await fetchReformAreas();
  } else {
    // If it's the last reform area, show the confirmation modal
    showConfirmationModal.value = true;
  }
};



    const goToPreviousReformArea = async () => {


      if (currentIndex.value > 0) {
        resetAllFields();
        currentIndex.value--;
        await fetchReformAreas();
      } else {
        console.log('Already at the first reform area.');
      }
    };

    const restartFromFirstReformArea = () => {
      // Reset index to 0 and fetch the first reform area
      currentIndex.value = 0;
      fetchReformAreas();
      // Close the confirmation modal
      showConfirmationModal.value = false;
    };



// Function to handle the response when the user clicks "No" in the confirmation modal
const handleNoConfirmation = () => {
  // Close the confirmation modal
  showConfirmationModal.value = false;
  // Redirect to a separate page

  router.push({ name: 'ThanksReformAreaConfig' }); // Assuming the route name for the new page is 'ReformConfigThanks'
};




    const additionalFieldsDisplay = ref('none'); // Initialize display style for additional fields container

    onMounted(fetchReformAreas);

    return {
      reformArea,
      thematicArea,
      focusAreas,
      selectedFocusAreas,
      submitForm,
      selectedReformStatus,
      sectors,
      selectedSector,
      reformCategories,
      selectedReformCategory,
      successMessage,
      goToNextReformArea,
      goToPreviousReformArea,
      additionalFieldsDisplay, // Expose additionalFieldsDisplay to template
      showConfirmationModal,
      restartFromFirstReformArea,
      handleNoConfirmation,
      errorMessage, // Expose errorMessage to template
      hideMessageAfterDelay,
    };
  },
};
</script>

<style>
.form-label {
  font-weight: bold;
}

.form-section {
  margin-bottom: 20px;
}

.checkbox-option {
  display: flex;
  align-items: center;
}

.checkbox-option input[type="checkbox"] {
  margin-left: 25px;
  margin-right: 8px;
}

.additional-fields-container {
  margin-top: 20px;
}

.textarea-container textarea {
  width: 100%;
  height: 50px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
}

.form-reformCategory {
  float: right;
  width: 300px; /* Adjust width as needed */
}

.hint {
  color: #666;
  font-size: 14px;
  border-left: 6px solid #ff0000; /* Change color as needed */
  padding: 10px;
  margin-bottom: 3px; /* Reduce margin-bottom to 3px */

}

.form-row {
  display: flex;
  justify-content: space-between;
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

.custom-select option:hover {
  background-color: lightgreen; /* Change to the desired hover color */
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

.form-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s;
}

.form-button:hover {
  background-color: #0056b3;
}

.outcome-container,
.output-container {
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
