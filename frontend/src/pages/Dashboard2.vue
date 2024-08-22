<template>
  <q-page class="q-pa-sm">
    <!-- Container for side-by-side cards -->
    <q-card class="q-mt-sm no-shadow" bordered>
      <q-card-section class="row q-col-gutter-md">
        <!-- Card 1: Significance Levels -->
        <div class="col-lg-5 col-md-6 col-sm-12 col-xs-12">
          <q-card class="q-px-sm q-py-xs" style="max-width: 450px;">
            <q-card-section class="row">
              <div class="col-12">
                <q-item>
                  <q-item-section avatar>
                    <q-icon color="black" name="fas fa-weight" size="20px"/> <!-- Reduced icon size -->
                  </q-item-section>
                  <q-item-section>
                    <div class="text-h6" style="font-size: 12px;">Significance Levels for The Reform Areas</div> <!-- Reduced font size -->
                  </q-item-section>
                </q-item>
                <div>
                  <ECharts :option="weights_pie_options"
                           class="q-mt-md"
                           :resizable="true"
                           autoresize style="height: 350px; "
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
         <!-- Card 2: Summary Table -->
         <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
          <q-card class="q-px-sm q-py-xs" style="max-width: 400px;">
            <q-card-section class="row">
              <div class="col-12">
                <q-item>
                  <q-item-section avatar>
                    <q-icon color="red" name="fas fa-chart-bar" size="24px"/> <!-- Updated icon name and color -->
                  </q-item-section>
                  <q-item-section>
                    <div class="text-h6" style="font-size: 12px;">Summary Of Institution Perfomance</div> <!-- Reduced font size -->
                  </q-item-section>
                </q-item>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </q-card-section>
    </q-card>

    <!-- Card for Summary Table -->
    <q-card class="q-mt-sm no-shadow" bordered>
      <q-card-section class="row">
        <div class="col-lg-12 col-sm-12 col-xs-12">
          <q-item>
            <q-item-section avatar>
              <q-icon color="green" name="fas fa-table" size="20px"/> <!-- Reduced icon size -->
            </q-item-section>
            <q-item-section>
              <div class="text-h6" style="font-size: 14px;">Summary of Output Performance</div> <!-- Reduced font size -->
            </q-item-section>
          </q-item>

          <!-- Custom Headers -->
          <div class="q-pa-sm"> <!-- Reduced padding -->
            <div class="row q-gutter-sm" style="border-bottom: 2px solid #ddd; background-color: #f5f5f5;"> <!-- Added border and background color -->
              <div class="col text-bold text-left" style="font-size: 12px; padding: 8px;">Output</div> <!-- Reduced font size and added padding -->
              <div class="col text-bold text-right" style="font-size: 12px; padding: 8px;">ACR (%)</div> <!-- Reduced font size and added padding -->
            </div>
          </div>

          <!-- Reform Area Rows with Output Data -->
          <div v-for="(row, index) in summaryData" :key="index" class="q-pa-sm"> <!-- Reduced padding -->
            <div class="row q-gutter-sm" style="border-bottom: 1px solid #ddd; background-color: lightgreen;"> <!-- Added border and background color -->
              <div class="col text-left" style="font-size: 12px; padding: 8px;" :colspan="2">{{ row.reform_area }}</div> <!-- Reform area header -->
            </div>
            <div v-for="(output, outputIndex) in row.outputs" :key="outputIndex" class="row q-gutter-sm">
              <div class="col text-left" style="font-size: 12px; padding: 8px;">{{ output.name[0] }}</div> <!-- Reduced font size and added padding -->
              <div class="col text-right" style="font-size: 12px; padding: 8px;">{{ output.acr_percentage.toFixed(2) }}%</div> <!-- Reduced font size and added padding -->
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>

  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import ECharts from "vue-echarts";
import { api } from '/src/boot/axios';
import { fetchInstitutionData } from '/src/services/institutionAPI';

export default defineComponent({
  name: "Dashboard2",
  components: {
    ECharts
  },
  setup() {
    const reformAreaACRData = ref([]);
    const reformAreas = ref([]);
    const summaryData = ref([]);
    const loadingACRData = ref(true);
    const weights_pie_options = ref({});

    const summaryColumns = [
      { name: 'reform_area', label: 'Reform Area', align: 'left' },
      { name: 'name', label: 'Output', align: 'right' },
      { name: 'acr_percentage', label: 'ACR (%)', align: 'right' }
    ];

    const fetchReformAreas = async (accessToken) => {
      try {
        const institutionId = await getInstitutionId(accessToken);
        const response = await api.get(`/reform-areas/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });

        if (response && response.data && Array.isArray(response.data) && response.data.length > 0) {
          reformAreas.value = response.data.map(reform => ({
            id: reform.id,
            name: reform.reform_area,
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

    const fetchReformAreaWeights = async (reformAreaId, accessToken) => {
      try {
        const response = await api.get(`/weights/reform_area/${reformAreaId}/`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });

        if (response && response.data) {
          return response.data;
        } else {
          throw new Error('Invalid or missing weights data.');
        }
      } catch (error) {
        throw new Error(`Error fetching weights for reform area ${reformAreaId}: ${error.message}`);
      }
    };

    const prepareWeightsPieChartOptions = (weightsData) => {
  if (!Array.isArray(weightsData)) {
    console.error('Invalid weights data format.');
    return;
  }

  const pieData = weightsData.map((item) => {
    const weight = typeof item.weight === 'number' ? item.weight : 0;
    const reformAreaName = reformAreas.value.find(area => area.id === item.reform_area)?.name || `Reform Area ${item.reform_area}`;
    return {
      id: item.reform_area,
      name: reformAreaName,
      value: weight,
    };
  });

  pieData.sort((a, b) => b.value - a.value);

  const labeledPieData = pieData.map((item, index) => ({
    name: `Reform Area ${index + 1}`,
    value: item.value,
    originalName: item.name,
  }));

  weights_pie_options.value = {
    title: {
      text: 'Significance Level',
      left: 'center',
      top: 'center',
    },
    tooltip: {
      trigger: 'item',
      formatter: function (params) {
        const originalName = labeledPieData.find(item => item.name === params.name)?.originalName || params.name;
        return `<div style="text-align: center;">
                  <strong>${originalName}</strong><br>
                  Value: ${params.value}<br>
                  Percentage: ${params.percent}%
                </div>`;
      },
      position: function (point, params, dom, rect, size) {
        // Position the tooltip at the center of the chart
        return [size.viewSize[0] / 2 - dom.offsetWidth / 2, size.viewSize[1] / 2 - dom.offsetHeight / 2];
      },
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: labeledPieData.map(item => item.name),
      formatter: function (name) {
        return `{name|${name}}`;
      },
      textStyle: {
        rich: {
          name: {
            width: 100,
            overflow: 'break',
          },
        },
      },
    },
    series: [
      {
        name: 'Weights',
        type: 'pie',
        radius: '50%',
        data: labeledPieData,
        emphasis: {
          itemStyle: {
            borderColor: 'black',
            borderWidth: 1,
          },
        },
        label: {
          show: false, // Hide labels on the pie chart segments
        },
        labelLine: {
          show: false, // Hide label lines
        },
      },
    ],
  };
};

const fetchReformAreaACRData = async () => {
  try {
    const acrDataPromises = reformAreas.value.map(async (reformArea) => {
      const reformAreaId = reformArea.id;
      const accessToken = localStorage.getItem('accessToken');

      if (!accessToken) {
        throw new Error('Access token not found. User is not authenticated.');
      }

      const reformAreaData = await fetchReformArea(reformAreaId, accessToken);

      return {
        reform_area: reformArea.name,
        outputs: reformAreaData.outputs.map(output => ({
          id: output.id,
          name: output.name,
          acr_percentage: (output.average_acr || 0)*100 + (output.extra_avg_acr || 0) * 100// Calculate ACR
            }))
      };
    });

    const results = await Promise.all(acrDataPromises);

    // Flatten and deduplicate
    const tempSummaryData = results.flatMap(result =>
      result.outputs.map(output => ({
        reform_area: result.reform_area,
        ...output
      }))
    );

    // Prepare summary data in the desired format
    summaryData.value = results.map(result => ({
      reform_area: result.reform_area,
      outputs: result.outputs
    }));

    const allWeightsData = await Promise.all(reformAreas.value.map(async (reformArea) => fetchReformAreaWeights(reformArea.id, localStorage.getItem('accessToken'))));
    prepareWeightsPieChartOptions(allWeightsData.flat());

    loadingACRData.value = false;
  } catch (error) {
    console.error('Error fetching Reform Area ACR data:', error);
    loadingACRData.value = false;
  }
};

const fetchReformArea = async (reformAreaId) => {
  try {
    console.log('Fetching reform area with ID:', reformAreaId);

    const accessToken = localStorage.getItem('accessToken');
    console.log('Access token retrieved:', accessToken);

    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    const response = await api.get(`/reform_area/${reformAreaId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    console.log('API response received:', response);

    const reformArea = response.data;
    console.log('Reform area data:', reformArea);

    if (!reformArea || !Array.isArray(reformArea.outcomes)) {
      throw new Error('Invalid or missing reform area data.');
    }

    const outputDetails = reformArea.outcomes.flatMap(outcome =>
          (outcome.outputs || []).map(output => {
            const outputAcrs = output.output_acrs || [];
            console.log(`Processing ACR data for output ID ${output.id}:`, outputAcrs);
            const average_acr = outputAcrs.length > 0 ? outputAcrs.reduce((sum, acr) => sum + acr.average_acr, 0) / outputAcrs.length : 0;
            const extra_avg_acr = outputAcrs.length > 0 ? outputAcrs.reduce((sum, acr) => sum + acr.extra_avg_acr, 0) / outputAcrs.length : 0;

            return {
              id: output.id,
              name: output.output, // Adjust based on how output names are structured
              average_acr: average_acr || 0,
              extra_avg_acr: extra_avg_acr || 0,
              acr_percentage: (average_acr || 0) + (extra_avg_acr || 0) // Add this field for ACR percentage
            };
          })
        );

        return {
          outputs: outputDetails,
        };
      } catch (error) {
        console.error('Error fetching reform area:', error);
        throw new Error(`Error fetching reform area with ID ${reformAreaId}: ${error.message}`);
      }
    };

    onMounted(async () => {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        console.error('Access token not found. User is not authenticated.');
        return;
      }

      await fetchReformAreas(accessToken);
      await fetchReformAreaACRData();
    });

    return {
      reformAreaACRData,
      reformAreas,
      summaryData,
      loadingACRData,
      weights_pie_options,
      summaryColumns,
    };
  }
});
</script>

<style scoped>
/* Add custom CSS for tooltips */
.echarts-tooltip {
  text-align: center
}

</style>
