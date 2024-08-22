<template>
  <div>
    <!-- Commitments and Responsibilities of the Organization -->
    <div>
      <h5>Commitments and Responsibilities of the Organization</h5>
      <div v-for="(item, index) in organizationCommitments" :key="index">
        <q-input v-model="organizationCommitments[index]" label="Commitment" />
        <q-btn  @click="removeOrganizationCommitment(index)" label="Remove" style=" float: right; color: #ff0000;"/>
      </div>
      <q-btn color="positive" @click="addOrganizationCommitment" label="Add Commitment" />
    </div>

    <!-- Commitment and Obligations of the Government -->
    <div>
      <h5>Commitment and Obligations of the Government</h5>
      <div v-for="(item, index) in governmentCommitments" :key="index">
        <q-input v-model="governmentCommitments[index]" label="Commitment" />
        <q-btn @click="removeGovernmentCommitment(index)" label="Remove" style="float: right; color: #ff0000;"/>
      </div>
      <q-btn color="positive" @click="addGovernmentCommitment" label="Add Commitment" />
    </div>
    <br>

    <!-- Save Button -->
    <div>
      <q-btn
        class="save-btn"
        unelevated
        color="positive"
        label="Save"
        @click="saveData"
        style="margin-right: auto;"
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
import { ref } from 'vue';
import { api } from '/src/boot/axios';
import { fetchUserData } from '/src/services/userAPI';
import { fetchInstitutionData } from '/src/services/institutionApi';

export default {
  setup() {
    const organizationCommitments = ref([]);
    const governmentCommitments = ref([]);
    const successMessage = ref('');
    const errorMessage = ref('');

    const addOrganizationCommitment = () => {
      organizationCommitments.value.push('');
    };

    const removeOrganizationCommitment = (index) => {
      organizationCommitments.value.splice(index, 1);
    };

    const addGovernmentCommitment = () => {
      governmentCommitments.value.push('');
    };

    const removeGovernmentCommitment = (index) => {
      governmentCommitments.value.splice(index, 1);
    };

    const saveData = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          errorMessage.value = 'Access token not found. User is not authenticated.';
          return;
        }

        // Fetch institution data to get the institution ID
        const institutionData = await fetchInstitutionData();
        const institutionId = institutionData.id;

        // Save commitments and responsibilities of the organization
        await api.post('/org-responsibilities/', {
          institution_id: institutionId,
          responsibilities: organizationCommitments.value,
          year: new Date().getFullYear() // Assuming the current year
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        // Save commitments and obligations of the government
        await api.post('/govt-obligations/', {
          institution_id: institutionId,
          govt_obligations: governmentCommitments.value,
          year: new Date().getFullYear() // Assuming the current year
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        successMessage.value = 'Commitments and responsibilities saved successfully.';
        hideMessageAfterDelay('successMessage');
      } catch (error) {
        errorMessage.value = `Error saving commitments and responsibilities: ${error}`;
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

    return {
      organizationCommitments,
      governmentCommitments,
      addOrganizationCommitment,
      removeOrganizationCommitment,
      addGovernmentCommitment,
      removeGovernmentCommitment,
      saveData,
      successMessage,
      errorMessage
    };
  }
};
</script>

<style scoped>

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
