<template>
  <div>
    <br>
    <form @submit.prevent="submitWeights">
      <div class="hint" style="color: green;">
        <strong>NOTE:</strong> The summation of the weights for all Reform Areas should equal 100 percent.
      </div>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Reform Area</th>
            <th>Weights (%)</th>
            <th>Justification</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(reform, index) in reformAreas" :key="reform.id">
            <td>{{ index + 1 }}</td>
            <td>{{ reform.reform_area }}</td>
            <td>
              <input type="number" step="0.01" min="0" max="100" v-model="weights[index]" @input="calculateTotalSum" placeholder="%" required>
              <input type="hidden" :value="reform.id" name="reform_ids[]">
            </td>
            <td>
              <textarea v-model="justifications[index]" cols="50" placeholder="Enter justification here..."></textarea>
            </td>
          </tr>
        </tbody>
      </table>
      <p id="totalSum" style="color: green;">{{ totalSumMessage }}</p>
      <p id="errorMessage" style="color: red;">{{ errorMessage }}</p>
      <q-btn unelevated color="positive" label="Save" @click="submitWeights" style="float: left;"/>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { api } from '/src/boot/axios';
import { fetchInstitutionData } from '/src/services/institutionAPI';
import { useRouter } from 'vue-router'; // Import Vue Router

export default {
  setup() {
    const reformAreas = ref([]);
    const weights = ref([]);
    const justifications = ref([]);
    const totalSumMessage = ref('');
    const errorMessage = ref('');
    const router = useRouter(); // Initialize router

    const fetchReformAreas = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
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
          weights.value = Array(response.data.length).fill(''); // Initialize weights array with blanks
          justifications.value = Array(response.data.length).fill(''); // Initialize justifications array with blanks
        } else {
          throw new Error('No reform areas found.');
        }
      } catch (error) {
        console.error('Error fetching reform areas:', error);
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

    const calculateTotalSum = () => {
      const sum = weights.value.reduce((acc, curr) => acc + parseFloat(curr || 0), 0); // Ensure 0 is added if the weight is empty
      totalSumMessage.value = `Total Weight: ${sum}`;
      if (sum !== 100) {
        errorMessage.value = 'Total weight must be 100 percent';
      } else {
        errorMessage.value = '';
      }
    };

    const submitWeights = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        calculateTotalSum(); // Calculate total sum before submission

        if (errorMessage.value) {
          throw new Error('Total weight is not 100');
        }

        // Divide each weight by 100 before submitting
        const reformWeightData = reformAreas.value.map((reform, index) => ({
          reform_area: reform.id,
          weight: parseFloat(weights.value[index]) / 100, // Divide by 100
          justification: justifications.value[index], // Include justification
        }));

        // Log data to be sent for debugging
        console.log('Data to be sent:', reformWeightData);

        await Promise.all(reformWeightData.map(async data => {
          const response = await api.post('/weights/create/', data, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          // Log response for debugging
          console.log('API Response:', response.data);
          return response;
        }));

        router.push({ name: 'ThanksReformWeights' }); // Assuming you have access to router instance

      } catch (error) {
        console.error('Error submitting weights:', error);
        errorMessage.value = 'Failed to submit weights. Please try again later.';
      }
    };

    onMounted(fetchReformAreas);

    return {
      reformAreas,
      weights,
      justifications,
      totalSumMessage,
      errorMessage,
      submitWeights,
      calculateTotalSum
    };
  },
};
</script>
<style scoped>
  /* Table styles */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
  /* Form styles */
  form {
    margin-bottom: 20px;
  }
  /* Message styles */
  #totalSum, #errorMessage {
    margin-top: 10px;
  }
  /* Button styles */
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    border-radius: 4px;
  }
  button:hover {
    background-color: #45a049;
  }
  /* Hint styles */
  .hint {
    background-color: #f9f9f9;
    border-left: 6px solid #ff0000; /* Change color as needed */
    padding: 10px;
    margin-bottom: 20px;
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

  .message-container {
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

.success-message {
  color: rgb(0, 64, 128);
  margin-top: 20px; /* Increase top margin */
  background-color: #e6ffe6; /* Light green background */
  border: 2px solid #162b4d; /* Green border */
}

.error-message {
  color: red;
  margin-top: 20px;
  background-color: #ffe6e6;
  border: 2px solid #f44336;
  animation-name: slideInFromRight; /* Name of the animation */
}

/* Keyframes for the slide-in animation */
@keyframes slideInFromRight {
  from {
    opacity: 0; /* Start with opacity 0 */
    right: -100%; /* Move 100% to the right */
  }
  to {
    opacity: 1; /* End with opacity 1 */
    right: 0; /* Move to the original position */
  }
}
</style>
