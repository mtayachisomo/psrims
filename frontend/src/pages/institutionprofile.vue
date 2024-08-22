<template>
  <div class="container">
    <div class="section-container">
      <!-- Mandate Section -->
      <div class="section-box" @click="toggleEdit('mandate')">
        <h6 class="section-header">MANDATE</h6>
        <div v-if="!editingMandate">
          <p>{{ mandate }}</p>
        </div>
        <textarea v-model="editedMandate" v-show="editingMandate"></textarea>
      </div>

      <!-- Vision Section -->
      <div class="section-box" @click="toggleEdit('vision')">
        <h6 class="section-header">VISION</h6>
        <div v-if="!editingVision">
          <p>{{ vision }}</p>
        </div>
        <textarea v-model="editedVision" v-show="editingVision"></textarea>
      </div>

      <!-- Mission Section -->
      <div class="section-box" @click="toggleEdit('mission')">
        <h6 class="section-header">MISSION</h6>
        <div v-if="!editingMission">
          <p>{{ mission }}</p>
        </div>
        <textarea v-model="editedMission" v-show="editingMission"></textarea>
      </div>

      <!-- Strategic Objectives Section -->
      <div class="section-box" @click="toggleEdit('objectives')">
        <h6 class="section-header">STRATEGIC OBJECTIVES</h6>
        <div v-if="!editingObjectives">
          <ul>
            <li v-for="(objective, index) in editedObjectives" :key="index">{{ objective.objective }}</li>
          </ul>
        </div>
        <div v-show="editingObjectives">
          <div v-for="(objective, index) in editedObjectives" :key="index">
            <textarea v-model="editedObjectives[index].objective"></textarea>
            <q-btn
              class="remove-btn"
              unelevated
              flat
              label="Remove"
              @click="removeObjective(index)"
            />
          </div>
          <q-btn
            class="add-btn"
            unelevated
            color="positive"
            label="Add"
            @click="addObjective"
          />
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <q-btn class="edit-btn" unelevated color="positive" label="Edit" @click="editData" />
      <q-btn
        class="save-btn"
        unelevated
        color="positive"
        label="Save"
        v-if="editingMandate || editingVision || editingMission || editingObjectives"
        @click="saveData"
      />
    </div>

    <!-- Success/Error Messages -->
    <div class="message-container">
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { fetchUserData } from '/src/services/userApi';
import { fetchInstitutionData } from '/src/services/institutionApi';
import { api } from '/src/boot/axios';
import { useAuthStore } from '/src/stores/auth'; // Import useAuthStore

export default {
  name: 'InstitutionProfile',
  setup() {
    const userId = ref(null);
    const institutionId = ref(null);
    const institutionName = ref('');
    const mandate = ref('');
    const vision = ref('');
    const mission = ref('');
    const editingMandate = ref(false);
    const editingVision = ref(false);
    const editingMission = ref(false);
    const editingObjectives = ref(false);
    const editedMandate = ref('');
    const editedVision = ref('');
    const editedMission = ref('');
    const editedObjectives = ref([]);
    const successMessage = ref('');
    const errorMessage = ref('');

    const authStore = useAuthStore(); // Get access to the auth store

    const handleFetchError = (error, errorType) => {
      if (error.response && error.response.status === 404 && error.response.data.error.includes('not found')) {
        // Automatically activate edit mode if data is not found
        if (errorType === 'mandate') {
          editingMandate.value = true;
        } else if (errorType === 'vision') {
          editingVision.value = true;
        } else if (errorType === 'mission') {
          editingMission.value = true;
        }
      } else {
        errorMessage.value = `Error fetching ${errorType}: ${error}`;
      }
    };

    const fetchMandate = async () => {
      const accessToken = authStore.accessToken; // Retrieve access token
      try {
        const response = await api.get(`/mandates/institution/${institutionId.value}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        if (response.data) {
          mandate.value = response.data.mandate;
        } else {
          // Automatically activate edit mode if mandate is empty
          editingMandate.value = true;
        }
      } catch (error) {
        handleFetchError(error, 'mandate');
      }
    };

    const fetchVision = async () => {
      const accessToken = authStore.accessToken; // Retrieve access token
      try {
        const response = await api.get(`/visions/institution/${institutionId.value}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        if (response.data) {
          vision.value = response.data.vision;
        } else {
          // Automatically activate edit mode if vision is empty
          editingVision.value = true;
        }
      } catch (error) {
        handleFetchError(error, 'vision');
      }
    };

    const fetchMission = async () => {
      const accessToken = authStore.accessToken; // Retrieve access token
      try {
        const response = await api.get(`/missions/institution/${institutionId.value}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        if (response.data) {
          mission.value = response.data.mission;
        } else {
          // Automatically activate edit mode if mission is empty
          editingMission.value = true;
        }
      } catch (error) {
        handleFetchError(error, 'mission');
      }
    };


    const fetchObjectives = async () => {
      const accessToken = authStore.accessToken; // Retrieve access token
  try {
    const response = await api.get(`/strategic-objectives/current/institution/${institutionId.value}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    if (response.data && response.data.length > 0) {
      // Map the response data to include both objective data and their IDs
      editedObjectives.value = response.data.map(obj => ({
        id: obj.id, // assuming `id` is the property name for the objective ID
        objective: obj.objective,
        editing: false
      }));
    } else {
      // Automatically activate edit mode if objectives are empty
      editingObjectives.value = true;
    }
  } catch (error) {
    errorMessage.value = `Error fetching strategic objectives: ${error}`;
  }
};


    const editData = () => {
      editingMandate.value = true;
      editingVision.value = true;
      editingMission.value = true;
      editingObjectives.value = true;
      editedMandate.value = mandate.value;
      editedVision.value = vision.value;
      editedMission.value = mission.value;
    };

    const saveData = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          errorMessage.value = 'Access token not found. User is not authenticated.';
          return;
        }

       // Save mandate
       await api.post('/mandates/', { mandate: editedMandate.value, institution: institutionId.value }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        mandate.value = editedMandate.value; // Update mandate value


        // Save vision
        await api.post('/visions/', { vision: editedVision.value, institution: institutionId.value }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        vision.value = editedVision.value; // Update vision value

        // Save mission
        await api.post('/missions/', { mission: editedMission.value, institution: institutionId.value }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        mission.value = editedMission.value; // Update mission value

        // Save strategic objectives
        const objectivesData = {
          institution_id: institutionId.value,
          objectives: editedObjectives.value.map(obj => obj.objective)
        };

        await api.post('/strategic-objectives/', objectivesData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });


        successMessage.value = 'Form saved successfully';
        hideMessageAfterDelay('successMessage');
      } catch (error) {
        errorMessage.value = `Error saving form: ${error}`;
      } finally {
        // Reset editing flags
        editingMandate.value = false;
        editingVision.value = false;
        editingMission.value = false;
        editingObjectives.value = false;
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

    const addObjective = () => {
      editedObjectives.value.push({ objective: '' });
    };

    const removeObjective = index => {
      editedObjectives.value.splice(index, 1);
    };

    const { institutionName: fetchedInstitutionName } = fetchInstitutionData(userId.value);
    institutionName.value = fetchedInstitutionName;

    onMounted(async () => {
      const userData = await fetchUserData();
      userId.value = userData.id;
      const institutionData = await fetchInstitutionData(userData.id);
      institutionId.value = institutionData.id;
      institutionName.value = institutionData.institution_name; // Set institutionName from fetched data

      // Fetch data using access token stored in Vuex
      const accessToken = authStore.accessToken;
      fetchMandate(accessToken);
      fetchVision(accessToken);
      fetchMission(accessToken);
      fetchObjectives(accessToken);


    });

    return {
      institutionName,
      mandate,
      vision,
      mission,
      editedMandate,
      editedVision,
      editedMission,
      editedObjectives,
      editingMandate,
      editingVision,
      editingMission,
      editingObjectives,
      editData,
      saveData,
      addObjective,
      removeObjective,
      successMessage,
      errorMessage,
      handleFetchError,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.section-container {
  display: grid;
  grid-template-areas:
    "mandate vision"
    "mission objectives";
  grid-gap: 10px;
}

.section-box {
  background-color: rgb(24, 141, 24);
  color: white;
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
}

.section-header {
  margin: 0;
  font-size: 1.2rem;
}

.section-box textarea {
  width: calc(100% - 20px);
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  display: block;
  resize: vertical;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.message-container {
  margin-top: 20px;
}

.success-message, .error-message {
  padding: 12px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 14px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
