<template>
  <div class="output-chart-page">
    <!-- Controls section -->
    <div v-if="!isOptionSelected" class="controls">
      <h5>LEVELS OF ANALYSIS</h5>
      <div class="control-group">
        <label style="color: green;" for="analysisSelect"><strong>ANALYSIS LEVELS:</strong></label>

        <q-select
          ref="analysisSelect"
          id="analysisSelect"
          v-model="selectedOption"
          :options="filteredOptions"
          option-value="value"
          option-label="label"
          label="Select Analysis Type"
          emit-value
          map-options
          :use-input="true"
          :input-debounce="300"
          @input="filterOptions"
        ></q-select>

        <q-btn color="positive" @click="toggleSearchBox">Search</q-btn>

        <q-input
          v-if="showSearchBox"
          v-model="searchQuery"
          placeholder="Type here..."
          dense
          debounce="300"
          @input="onSearchInput"
          @keyup.enter="showDropdown"
        ></q-input>
      </div>
    </div>

    <!-- Selected section -->
    <div v-if="isOptionSelected" class="selected-section">
      <q-btn color="negative" @click="resetSelection">Back to Selection</q-btn>

      <div v-if="selectedOption === 'quarterAnalysis'">
        <output-chart></output-chart>
      </div>

      <div v-if="selectedOption === 'analysisBysector'">
        <output-chart></output-chart>
      </div>

      <div v-if="selectedOption === 'quarterlyAnnual'">
        <quarterly-annual></quarterly-annual>
      </div>

      <div v-if="selectedOption === 'OutputEndofContract'">
        <Output-End-of-Contract></Output-End-of-Contract>
      </div>

      <div v-if="selectedOption === 'analysisByThematicArea'">
        <analysis-by-thematic-area></analysis-by-thematic-area>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, nextTick } from 'vue';
import OutputChart from '/src/components/charts/OutputChart.vue'; // Adjust the path as per your project structure
import AnalysisByThematicArea from '/src/components/charts/AnalysisByThematicArea.vue';
import QuarterlyAnnual from '/src/components/charts/QuarterlyAnnual.vue';
import OutputEndOfContract from '/src/components/charts/OutputEndOfContract.vue';

export default {
  components: {
    OutputChart,
    AnalysisByThematicArea,
    QuarterlyAnnual,
    OutputEndOfContract,
  },
  setup() {
    const selectedOption = ref(null);
    const searchQuery = ref('');
    const showSearchBox = ref(false);
    const analysisSelect = ref(null); // Reference to q-select component

    const options = [
      { id: 1, value: 'quarterAnalysis', label: 'Quarter Against Quarter Level' },
      { id: 2, value: 'quarterlyAnnual', label: 'Quarter Against Annual' },
      { id: 3, value: 'OutputEndofContract', label: 'Quarter Against End of the Contract' },
      { id: 4, value: 'analysisByThematicArea', label: 'By Thematic Area' },
      { id: 5, value: 'quarterAnalysis', label: 'By Sector' },
      { id: 6, value: 'analysisType2', label: 'By Reform Area Category' },
    ];

    const filteredOptions = computed(() => {
      const query = searchQuery.value.toLowerCase();
      return options.filter(option =>
        option.label.toLowerCase().includes(query)
      );
    });

    const isOptionSelected = computed(() => {
      return selectedOption.value !== null;
    });

    const toggleSearchBox = () => {
      showSearchBox.value = !showSearchBox.value;
      if (showSearchBox.value) {
        nextTick(() => {
          analysisSelect.value.focus();
        });
      }
    };

    const filterOptions = (value) => {
      searchQuery.value = value;
    };

    const onSearchInput = (value) => {
      filterOptions(value);
    };

    const showDropdown = () => {
      nextTick(() => {
        if (analysisSelect.value) {
          analysisSelect.value.focus();
          analysisSelect.value.showPopup();
        }
      });
    };

    const resetSelection = () => {
      selectedOption.value = null;
    };

    return {
      selectedOption,
      searchQuery,
      showSearchBox,
      analysisSelect,
      filteredOptions,
      toggleSearchBox,
      filterOptions,
      onSearchInput,
      showDropdown,
      isOptionSelected,
      resetSelection,
    };
  },
};
</script>

<style scoped>
.output-chart-page {
  max-width: 800px;
  margin: 20px auto;
  text-align: center;
}

.controls {
  margin-bottom: 20px;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
  font-size: 14px;
  border-left: 6px solid #ff0000; /* Change color as needed */
  padding: 10px;
  margin-bottom: 3px; /* Reduce margin-bottom to 3px */
}

select, input, button {
  font-size: 14px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.selected-section {
  margin-top: 20px;
}
</style>
