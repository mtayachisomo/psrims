<template>
  <div class="page">
    <div class="frame">
      <div class="black-layer">
        <div class="red-layer">
          <div class="green-layer">
            <img src="/src/assets/govt.jpg" alt="Government Logo" class="logo" />
            <h5 class="title">Republic of Malawi</h5>
            <h2 class="subtitle"><strong>PUBLIC SECTOR REFORMS SECRETARIAT</strong></h2>
            <h3 class="council"><strong>{{ institutionName }}</strong></h3>
            <div class="implementation-container">
              <h3 class="implementation-heading">REPORTING PERIOD</h3>
              <p class="implementation-period">{{ implementationPeriod }}</p>
            </div>
            <img :src="institutionLogo" :alt="institutionName" class="logo" />
            <p class="submission-date">DATE OF REPORT: {{ currentDate }}</p>

            <img src="favicon.ico" alt="Logo" style="max-width: 100%; display: block; margin: 0 auto;">
          </div>
        </div>
      </div>
    </div>

    <!-- Section for Mandate, Vision, Mission, and Strategic Objectives -->
    <h5>PART I: MANDATE, VISION, MISSION, AND STRATEGIC OBJECTIVES</h5>
<h5>INTRODUCTION</h5>
    <!-- Display Mandate -->
    <div class="form-section">
      <label class="form-label" for="mandate"><strong>(a) MANDATE:</strong></label>
      <textarea v-model="mandate"></textarea>
    </div>

    <!-- Display Vision -->
    <div class="form-section">
      <label class="form-label" for="vision"><strong>(b) VISION:</strong></label>
      <textarea v-model="vision"></textarea>
    </div>

    <!-- Display Mission -->
    <div class="form-section">
      <label class="form-label" for="mission"><strong>(c) MISSION:</strong></label>
      <textarea v-model="mission"></textarea>
    </div>

    <!-- Display Strategic Objectives -->
    <div class="form-section">
      <label class="form-label" for="objectives"><strong>(d) STRATEGIC OBJECTIVES:</strong></label>
      <div>
        <div v-for="(objective, index) in editedObjectives" :key="index" class="objective-item">
          <span class="objective-index">{{ index + 1 }}</span>
          <textarea v-model="editedObjectives[index]" :placeholder="'Objective ' + (index + 1) + ': ' + editedObjectives[index]"></textarea>
        </div>
      </div>
    </div>

<h5>PROGRESS</h5>
     <!-- Display Thematic Areas -->
    <div v-if="thematicAreas.length > 0">
      <div v-for="(thematicArea, index) in thematicAreas" :key="'thematicArea' + index">
        <h6><label class="form-label" for="thematicArea">THEMATIC AREA:</label>  <br>{{ thematicArea.thematic_area }}</h6>

        <!-- Display information for each thematic area -->
        <div v-for="(reformArea, i) in thematicArea.reformaredetail" :key="reformArea.id">
          <div class="reform-area-container">
            <h6><label class="form-label" for="reformArea">Reform Area:</label> {{ i + 1 }}. <br>{{ reformArea.reform_area }}</h6>


            <!-- Justifications -->
            <div class="form-section">
              <label class="form-label" for="justifications"><strong>JUSTIFICATIONS:</strong></label>
              <div class="textarea-container">
                <template v-for="(justification, j) in reformArea.justifications" :key="j">
                  <div class="justification-item">
                    <span class="objective-index">{{ j + 1 }}</span>
                    <textarea v-model="justification.justification" :placeholder="'Justification ' + (j + 1) + ': ' + justification.justification"></textarea>
                  </div>
                </template>
              </div>
            </div>

            <!-- Problems -->
            <div class="form-section">
              <label class="form-label" for="problems"><strong>PROBLEMS:</strong></label>
              <div class="textarea-container">
                <template v-for="(problem, j) in reformArea.problems" :key="j">
                  <div class="problem-item">
                    <span class="objective-index problem-number">{{ j + 1 }}</span>
                    <textarea v-model="problem.problem" :placeholder="'Problem ' + (j + 1) + ': ' + problem.problem"></textarea>
                  </div>
                </template>
              </div>
            </div>

            <!-- Outcomes -->
            <div v-if="reformArea.outcomes.length === 0">
              No outcomes found for this reform area.
            </div>
            <div v-else>
              <div v-for="(outcome, k) in reformArea.outcomes" :key="k">
                <div class="outcome-container">
                  <div class="form-section">
                    <label class="form-label" for="outcome"><strong> OUTCOME {{ k + 1 }}</strong></label>
                    <div class="textarea-container outcome-textarea-container">
                      <textarea v-model="outcome.outcomes" class="outcome-textarea"></textarea>
                    </div>

                    <!-- Outcome Indicators -->
                    <div class="form-section">
                      <label class="form-label" for="outcomeIndicators"><strong>OUTCOME INDICATORS:</strong></label>
                      <div class="textarea-container">
                        <template v-for="(indicator, l) in outcome.outcome_indicators" :key="l">
                          <div class="outcome-indicator-item">
                            <span class="objective-index indicator-number">{{ l + 1 }}</span>
                            <textarea v-model="indicator.indicator" :placeholder="'Outcome Indicator ' + (l + 1) + ': ' + indicator.indicator"></textarea>
                          </div>
                        </template>
                      </div>
                    </div>

                    <!-- Outputs -->
                    <div v-if="outcome.outputs.length === 0">
                      No outputs found for this outcome.
                    </div>
                    <div v-else>
                      <div v-for="(output, m) in outcome.outputs" :key="m">
                        <div class="output-container">
                          <div class="form-section">
                            <label class="form-label" for="output"><strong>PROPOSED OUTPUT {{ m + 1 }}</strong></label>
                            <div class="textarea-container output-textarea-container">
                              <textarea v-model="output.output" class="output-textarea"></textarea>
                            </div>

                            <!-- Output Indicators -->
                            <div class="form-section">
                              <label class="form-label" for="outputIndicators"><strong>OUTPUT INDICATORS:</strong></label>
                              <div class="textarea-container">
                                <template v-for="(indicator, n) in output.output_indicators" :key="n">
                                  <div class="output-indicator-item">
                                    <span class="objective-index indicator-number">{{ n + 1 }}</span>
                                    <textarea v-model="indicator.indicator" :placeholder="'Output Indicator ' + (n + 1) + ': ' + indicator.indicator"></textarea>
                                  </div>
                                </template>
                              </div>
                            </div>

                            <!-- Activities -->
                            <div class="form-section">
                              <label class="form-label" for="activities"><strong>ACTIVITIES:</strong></label>
                              <div class="textarea-container">
                                <template v-for="(activity, o) in output.activities" :key="o">
                                  <div class="activity-item">
                                    <span class="objective-index activity-number">{{ o + 1 }}</span>
                                    <textarea v-model="activity.activity" :placeholder="'Activity ' + (o + 1) + ': ' + activity.activity"></textarea>
                                  </div>
                                </template>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Display Period from reformareaimplementationperiod -->
            <div class="form-section">
              <label class="form-label" for="period"><strong>Implementation Period for {{ reformArea.reform_area }}:</strong></label>
              <div class="period-container">
                <template v-for="(periodItem, index) in reformArea.reform_area_periods" :key="index">
                  <div class="period-item">
                    <span>{{ periodItem.period }}</span>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
  <!-- Display Thematic Areas -->
  <h5>PART V: M & E FRAMEWORK</h5>
  <div v-if="thematicAreas.length > 0">
    <div v-for="(thematicArea, index) in thematicAreas" :key="'thematicArea' + index">
      <!-- Space between tables -->
      <div style="margin-bottom: 20px;"></div>
      <!-- Planning Matrix Table -->
      <table class="planning-matrix">
        <thead>
          <tr >
    <th colspan="15" style="text-align: center; background-color: green !important;color: black !important; font-weight: bold !important;">THEMATIC AREAS ALIGNED TO MW2063</th>
</tr>


          <tr>
            <th rowspan="0" style="text-align: center; background-color: lightgrey;">{{ thematicArea.thematic_area }}</th>
          </tr>

          <!-- Iterate over reform areas -->
          <template v-for="(reformArea, i) in thematicArea.reformaredetail" :key="reformArea.id">
            <tr>
              <th colspan="14" style="text-align: center; border-top: 2px solid black;background-color: lightblue;">Reform Area{{ i + 1 }}: {{ reformArea.reform_area }}</th>
            </tr>

<!-- Outcome Heading -->
<tr class="outcome-heading bold-text">
  <th>OUTCOME</th>
  <th colspan="3">OUTCOME INDICATOR</th>
  <th>Year</th>
  <th>Baseline</th>
  <th colspan="2">H1 Target</th>
  <th colspan="2">H2 Target</th>
  <th>Means of Verification</th>
  <th>Critical Success Factor</th>
  <th>Data collection Instrument</th>
  <th>Responsible person</th>
</tr>

<!-- Display Outcomes and Indicators -->
<template v-for="(outcome, k) in reformArea.outcomes" :key="'outcome' + k">
  <template v-for="(indicator, l) in outcome.outcome_indicators" :key="'indicator' + l">
    <tr>
      <!-- Display outcome name only for the first indicator -->
      <td :rowspan="outcome.outcome_indicators.length * 2" v-if="l === 0">{{ outcome.outcomes[0] }}</td>
      <td :rowspan="2" colspan="3">{{ indicator.indicator }}</td>
      <!-- Year, Baseline, H1 Target, H2 Target for the first indicator -->
      <td>{{ indicator.outcome_targets[0]?.year || 0 }}</td>
      <td>{{ indicator.outcome_targets[0]?.baseline || 0 }}</td>
      <td colspan="2">{{ indicator.outcome_targets[0]?.H1_target || 0 }}</td>
      <td colspan="2">{{ indicator.outcome_targets[0]?.H2_target || 0 }}</td>

      <!-- Display outcome_movs -->
      <td :rowspan="2" colspan="1">
        <template v-if="indicator.outcome_movs.length">
          <template v-for="(mov, m) in indicator.outcome_movs" :key="'mov' + m">
            {{ m + 1 }}. {{ mov.mov }} <!-- Display numbering based on index (m + 1) -->
            <br v-if="m < indicator.outcome_movs.length - 1"> <!-- Add line break if not the last mov -->
          </template>
        </template>
        <template v-else>
          None
        </template>
      </td>

      <!-- Display outcome_csfs -->
      <td :rowspan="2" colspan="1">
        <template v-if="indicator.outcome_csfs.length">
          <template v-for="(csf, c) in indicator.outcome_csfs" :key="'csf' + c">
            {{ c + 1 }}. {{ csf.csf }} <!-- Display numbering based on index (c + 1) -->
            <br v-if="c < indicator.outcome_csfs.length - 1"> <!-- Add line break if not the last csf -->
          </template>
        </template>
        <template v-else>
          None
        </template>
      </td>

      <!-- Display outcome_instruments -->
      <td :rowspan="2" colspan="1">
        <template v-if="indicator.outcome_instruments.length">
          <template v-for="(instrument, i) in indicator.outcome_instruments" :key="'instrument' + i">
            {{ i + 1 }}. {{ instrument.instrument }} <!-- Display numbering based on index (i + 1) -->
            <br v-if="i < indicator.outcome_instruments.length - 1"> <!-- Add line break if not the last instrument -->
          </template>
        </template>
        <template v-else>
          None
        </template>
      </td>

      <td :rowspan="2" colspan="2">{{ indicator.outcome_targets[0]?.responsibility || 'N/A' }}</td>
    </tr>

    <!-- If there are additional targets, add rows for them -->
    <template v-if="indicator.outcome_targets.length > 1">
      <tr>
        <!-- Year, Baseline, H1 Target, H2 Target for the second indicator -->
        <td>{{ indicator.outcome_targets[1]?.year || 0 }}</td>
        <td>{{ indicator.outcome_targets[1]?.baseline || 0 }}</td>
        <td colspan="2">{{ indicator.outcome_targets[1]?.H1_target || 0 }}</td>
        <td colspan="2">{{ indicator.outcome_targets[1]?.H2_target || 0 }}</td>
      </tr>
    </template>
  </template>

<!-- Outputs Heading -->
<tr class="output-heading bold-text">
  <th>OUTPUT</th>
  <th colspan="2">OUTPUT INDICATORS</th>
  <th>ACTIVITIES</th>
  <th>Year</th>
  <th>Baseline</th>
  <th>Q1 Target</th>
  <th>Q2 Target</th>
  <th>Q3 Target</th>
  <th>Q4 Target</th>
  <th>Means of Verification</th>
  <th>Critical Success Factor</th>
  <th>Data collection Instrument</th>
  <th>Responsible person</th>
</tr>

<!-- Display Outputs and Indicators -->
<template v-for="(output, m) in outcome.outputs" :key="'output' + m">
  <template v-for="(indicator, n) in output.output_indicators" :key="'indicator' + n">
    <tr>
      <!-- Display output name only for the first indicator -->
      <td :rowspan="output.output_indicators.length * 2" v-if="n === 0">{{ output.output[0] }}</td>
      <td :rowspan="2" colspan="2">
        {{ indicator.indicator }}
      </td>
              <!-- Display Activities only for the first indicator -->
        <td :rowspan="output.output_indicators.length * 2" colspan="1" v-if="n === 0">
        <!-- Iterate through activities to display activities -->
        <template v-for="(activity, o) in output.activities" :key="'activity' + o">
          {{ o + 1 }}. {{ activity.activity }} <!-- Display numbering based on index (o + 1) -->
          <br v-if="o < output.activities.length - 1"> <!-- Add line break if not the last activity -->
        </template>
      </td>
      <!-- Year, Baseline, Q1 Target, Q2 Target, Q3 Target, Q4 Target for the first indicator -->
      <td>{{ indicator.output_targets[0]?.year || 0 }}</td>
      <td>{{ indicator.output_targets[0]?.baseline || 0 }}</td>
      <td>{{ indicator.output_targets[0]?.Q1_target || 0 }}</td>
      <td>{{ indicator.output_targets[0]?.Q2_target || 0 }}</td>
      <td>{{ indicator.output_targets[0]?.Q3_target || 0 }}</td>
      <td>{{ indicator.output_targets[0]?.Q4_target || 0 }}</td>

      <!-- Display output_movs -->
      <td :rowspan="2" colspan="1">
        <!-- Iterate through output_movs to display movs -->
        <template v-if="indicator.output_movs.length">
          <template v-for="(mov, p) in indicator.output_movs" :key="'mov' + p">
            {{ p + 1 }}. {{ mov.mov }} <!-- Display numbering based on index (p + 1) -->
            <br v-if="p < indicator.output_movs.length - 1"> <!-- Add line break if not the last mov -->
          </template>
        </template>
        <template v-else>
          None
        </template>
      </td>

      <!-- Display output_csfs -->
      <td :rowspan="2" colspan="1">
        <!-- Iterate through output_csfs to display csfs -->
        <template v-if="indicator.output_csfs.length">
          <template v-for="(csf, q) in indicator.output_csfs" :key="'csf' + q">
            {{ q + 1 }}. {{ csf.output_csf }} <!-- Display numbering based on index (q + 1) -->
            <br v-if="q < indicator.output_csfs.length - 1"> <!-- Add line break if not the last csf -->
          </template>
        </template>
        <template v-else>
          None
        </template>
      </td>

      <!-- Display output_instruments -->
      <td :rowspan="2" colspan="1">
        <!-- Iterate through output_instruments to display instruments -->
        <template v-if="indicator.output_instruments.length">
          <template v-for="(instrument, r) in indicator.output_instruments" :key="'instrument' + r">
            {{ r + 1 }}. {{ instrument.output_instrument }} <!-- Display numbering based on index (r + 1) -->
            <br v-if="r < indicator.output_instruments.length - 1"> <!-- Add line break if not the last instrument -->
          </template>
        </template>
        <template v-else>
          None
        </template>
      </td>

      <td :rowspan="2" colspan="2" v-if="indicator.output_targets && indicator.output_targets[0]">{{ indicator.output_targets[0].responsibility }}</td>
    </tr>

    <!-- If there are additional targets, add rows for them -->
    <template v-if="indicator.output_targets.length > 1">
      <tr>
        <!-- Year, Baseline, Q1 Target, Q2 Target, Q3 Target, Q4 Target for the second indicator -->
        <td>{{ indicator.output_targets[1]?.year || 0 }}</td>
        <td>{{ indicator.output_targets[1]?.baseline || 0 }}</td>
        <td>{{ indicator.output_targets[1]?.Q1_target || 0 }}</td>
        <td>{{ indicator.output_targets[1]?.Q2_target || 0 }}</td>
        <td>{{ indicator.output_targets[1]?.Q3_target || 0 }}</td>
        <td>{{ indicator.output_targets[1]?.Q4_target || 0 }}</td>
      </tr>
    </template>
  </template>
</template>
            </template>
          </template>
        </thead>
      </table>
    </div>
  </div>
</div>

<!-- PART VI: RESOURCE REQUIREMENTS -->
<h5>PART VI: RESOURCE REQUIREMENTS</h5>
<template v-for="(thematicArea, index) in thematicAreas" :key="'thematicArea' + index">
  <h5>{{ thematicArea.name }}</h5> <!-- Display thematic area name -->
  <table class="planning-matrix">
    <thead>
      <tr class="outcome-heading bold-text" >
        <th style="background-color: dodgerblue;">REFORM AREA</th>
        <th style="background-color: dodgerblue;">OUTCOME</th>
        <th style="background-color: dodgerblue;">OUTPUT</th>
        <th style="background-color: dodgerblue;">ACTIVITY</th>
        <th style="background-color: dodgerblue;">FINANCIAL REQUIREMENTS (MK)</th>
        <th style="background-color: dodgerblue;">SOURCE OF FINANCING</th>
      </tr>
    </thead>
    <tbody>
      <!-- Loop through reform areas -->
      <template v-for="(reformArea, i) in thematicArea.reformaredetail" :key="reformArea.id">
        <tr>
          <td :rowspan="reformArea.outcomes.flatMap(outcome => outcome.outputs.flatMap(output => output.activities)).length + 1">
            <h6><label class="form-label" for="reformArea">Reform Area:</label> {{ i + 1 }}. <br>{{ reformArea.reform_area }}</h6>
          </td>
        </tr>
        <!-- Loop through outcomes within the current reform area -->
        <template v-for="(outcome, k) in reformArea.outcomes" :key="k">
          <!-- Loop through outputs within the current outcome -->
          <template v-for="(output, m) in outcome.outputs" :key="'output' + m">
            <!-- Loop through activities within the current output -->
            <template v-for="(activity, p) in output.activities" :key="'output' + m + 'activity' + p">
              <tr>
                <!-- Display Outcome -->
                <td v-if="m === 0 && p === 0" :rowspan="outcome.outputs.reduce((acc, output) => acc + output.activities.length, 0)">
                  <h6><label class="form-label" for="outcome">Outcome:</label> {{ k + 1 }}. <br>{{ outcome.outcomes[0] }}</h6>
                </td>
                <!-- Display Output -->
                <td v-if="p === 0" :rowspan="output.activities.length">
                  {{ output.output[0] }}
                </td>
                <!-- Display Activity -->
                <td  >
                  {{ activity.activity }}
                </td>
                <!-- Display Financial Requirements -->
                <td>
                  <span v-if="!activity.budgets || activity.budgets.length === 0">__</span>
                  <span v-else>{{ activity.budgets[0].budget }}</span>
                </td>
                <!-- Display Source of Financing -->
                <td>
                  <span v-if="!activity.budgets || activity.budgets.length === 0">N/A</span>
                  <span v-else>{{ activity.budgets[0].fund_source }}</span>
                </td>
              </tr>
            </template>
          </template>
        </template>
        <!-- Total row for Reform Area -->
        <tr>
          <td class="total-text">TOTAL</td>


          <!-- Financial Requirements -->
          <td colspan="5" class="total-value" style="text-align: center;">
            {{
              reformArea.outcomes.flatMap(outcome => outcome.outputs.flatMap(output => output.activities)).reduce((acc, activity) => {
                return acc + (activity.budgets && activity.budgets.length > 0 ? activity.budgets[0].budget : 0);
              }, 0)
            }}
          </td>

        </tr>
      </template>
    </tbody>
  </table>
</template>

 <!-- Add download button and submit button -->
 <div class="button-container">
      <button class="download-button" @click="downloadDocument">Download</button>
      <button class="submit-button">Submit</button>
    </div>


</div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { fetchUserData } from '/src/services/userApi';
import { fetchInstitutionData } from '/src/services/institutionApi';
import { api } from '/src/boot/axios';


export default {
  setup() {
    const institutionName = ref('');
    const institutionLogo = ref('');
    const currentDate = ref('');
    const implementationPeriod = ref('');
    const mandate = ref('');
    const vision = ref('');
    const mission = ref('');
    const editedObjectives = ref([]);
    const orgResponsibilities = ref([]);
    const govtObligations = ref([]);
    const reformAreas = ref([]);
    const thematicAreas = ref([]);
    // Function to download the document
    const downloadDocument = () => {
      const format = 'word'; // Default to Word format
      if (format === 'word') {
        exportToWord();
      } else if (format === 'pdf') {
        // Call the function to export to PDF
        // exportToPDF(); // Implement this function if needed
      }
    };

    const exportToWord = async () => {
      try {
        // Fetch base64 encoded images
        const govtLogoBase64 = await getBase64FromImageUrl("/src/assets/govt.jpg");
        const institutionLogoBase64 = await getBase64FromImageUrl(institutionLogo.value, 200);
        const faviconBase64 = await getBase64FromImageUrl("/src/assets/reform.jpg", 200);

        // Start building the Word document
        let content = `
          <!DOCTYPE html>
          <html>
          <head>
            <meta charset="utf-8">
            <title>Document</title>
            <style>
              /* CSS for the layers */
              body {
                background-color: white; /* Set document background to white */
                padding: 20px; /* Add padding to create space between content and frame */
                font-size: 12pt;
              }
              .frame {
                position: relative;
                width: calc(100% - 40px); /* Adjust as needed to account for padding */
                height: calc(100% - 40px); /* Adjust as needed to account for padding */
                border: 10px solid black; /* Outer layer color */
                box-sizing: border-box; /* Include border and padding in total width and height */
                background-color: red; /* Inner layer color (white) */
              }
              .red-layer {
                background-color: red; /* Middle layer color */
                height: calc(100% - 20px); /* Adjust height to account for padding */
                box-sizing: border-box; /* Include padding in total height */
                border: 10px solid red;
              }
              .green-layer {
                background-color: white; /* Inner layer color */
                height: calc(100% - 20px); /* Adjust height to account for padding */
                box-sizing: border-box; /* Include padding in total height */
                border: 10px solid green;
                text-align: center; /* Center align content */
              }
              .logo {
                max-width: 50%; /* Reduce the size of logos */
                display: block;
                margin: 20px auto; /* Center align and adjust margin */
              }
              .council {
                text-align: center;
                margin-top: 20px; /* Adjust margin as needed to position the text */
              }
              .implementation-container {
                background-color: rgb(15, 148, 29);
                width: 50%;
                padding: 10px;
                margin-top: 20px;
                border-radius: 10px;
                margin-bottom: 10px; /* Adjust this margin to move the logo up or down */
              }
              .implementation-heading {
                font-size: 24px;
                color: white;
                text-align: center;
              }
              .implementation-period {
                font-size: 20px;
                color: white;
                text-align: center;
              }
              .title {
                margin-top: 10px; /* Adjust the margin between the title and other content */
              }
              .favicon {
                max-width: 30px; /* Enlarge the size of the favicon */
                display: block;
                margin: 20px auto; /* Center align and adjust margin */
              }
              /* End of layer styles */
            </style>
          </head>
          <body>
            <div class="frame">
              <div class="red-layer">
                <div class="green-layer">
                  <br>
                  <img src="${govtLogoBase64}" alt="Government Logo" class="logo" style="max-width: 200px; height: auto;" />
                  <h1 class="title">Republic of Malawi</h1>
                  <h2 class="subtitle"><strong>PUBLIC SECTOR REFORMS SECRETARIAT</strong></h2>
                  <h3 class="council"><strong>${institutionName.value}</strong></h3>
                  <div class="implementation-container">
                    <h3 class="implementation-heading">Implementation Period</h3>
                    <p class="implementation-period">${implementationPeriod.value}</p>
                  </div>
                  <img src="${institutionLogoBase64}" alt="${institutionName.value}" class="logo" style="width: 50%; height: auto; max-width: 200px;" />
                  <br>
                  <p class="submission-date">DATE OF SUBMISSION: ${currentDate.value}</p>
                  <img src="${faviconBase64}" alt="Logo" class="favicon"> <!-- Include favicon -->
                </div>
              </div>
            </div>

            <div style="page-break-before:always">&nbsp;</div>

        <h5>PART I: MANDATE, VISION, MISSION, AND STRATEGIC OBJECTIVES</h5>
      <div class="form-section">
        <label class="form-label" for="mandate"><strong>(a) MANDATE:</strong></label>
        <p>${mandate.value}</p>
      </div>
      <div class="form-section">
        <label class="form-label" for="vision"><strong>(b) VISION:</strong></label>
        <p>${vision.value}</p>
      </div>
      <div class="form-section">
        <label class="form-label" for="mission"><strong>(c) MISSION:</strong></label>
        <p>${mission.value}</p>
      </div>
      <div class="form-section">
        <label class="form-label" for="objectives"><strong>(d) STRATEGIC OBJECTIVES:</strong></label>
        ${editedObjectives.value.map((objective, index) => `<p>${index + 1}. ${objective}</p>`).join('')}
      </div>
<!-- PART II: COMMITMENTS AND RESPONSIBILITIES OF THE ORGANIZATION -->
            <h5>PART II: COMMITMENTS AND RESPONSIBILITIES OF THE ORGANIZATION</h5>
            <div class="form-section">

              ${Array.isArray(orgResponsibilities.value) && orgResponsibilities.value.length > 0 ?
                orgResponsibilities.value.map((responsibility, index) => `
                  <div class="objective-item" style="margin-bottom: 10px;">
                    <span class="objective-index">${index + 1}.</span>
                    <textarea>${responsibility.responsibility}</textarea>
                  </div>
                `).join('') :
                '<div>No organization responsibilities found.</div>'
              }
            </div>

  <!-- PART III: COMMITMENT AND OBLIGATIONS OF THE GOVERNMENT -->
        <h5>PART III: COMMITMENT AND OBLIGATIONS OF THE GOVERNMENT</h5>
        <div class="form-section">

          ${Array.isArray(govtObligations.value) && govtObligations.value.length > 0 ?
            govtObligations.value.map((obligation, index) => `
              <div class="objective-item" style="margin-bottom: 10px;">
                <span class="objective-index" >${index + 1}.</span>
                <textarea>${obligation.govt_obligation}</textarea>
              </div>
            `).join('') :
      '<div>No government obligations found.</div>'
    }
  </div>

<!-- PART IV: THEMATIC AREAS, REFORMS AND JUSTIFICATIONS -->
<div class="form-section" style="margin-top: 20px;">
  <label class="form-label" style="font-size: 12pt;"><strong>PART IV: THEMATIC AREAS, REFORMS AND JUSTIFICATIONS</strong></label>
</div>
${thematicAreas.value.map((thematicArea, index) => `
  <div key="thematicArea${index}" style="margin-top: 20px;">
    <h6 style="font-size: 12pt;"><label class="form-label" for="thematicArea">THEMATIC AREA:</label> ${String.fromCharCode(65 + index)}. <br>${thematicArea.thematic_area}</h6>
    ${thematicArea.reformaredetail.map((reformArea, i) => `

     <!-- Display Focus Areas -->
            <div class="form-section" style="margin-top: 10px;">
              <label class="form-label" for="focusAreas"><strong>FOCUS AREAS:</strong></label>
              <div class="textarea-container">
                ${thematicArea.focus_areas.map((focusArea, j) => `
                  <div key="focusArea${j}" class="focus-area-item" style="margin-top: 10px;">
                    <span class="objective-index focus-area-number" style="font-size: 12pt;">${j + 1}.</span>
                    <span style="font-size: 12pt;">${focusArea.focus_area}</span>
                  </div>`).join('')}
              </div>
            </div>

      <div key="${reformArea.id}" class="reform-area-container" style="font-size: 12pt; margin-top: 20px;">
        <h6 style="font-size: 12pt;"><label class="form-label" for="reformArea">REFORM AREA:</label> ${i + 1}.${reformArea.reform_area}</h6>



        <!-- Rest of the code for justifications, problems, outcomes, etc. -->
        <!-- JUSTIFICATIONS -->
        <div class="form-section" style="margin-top: 10px;">
          <label class="form-label" for="justifications" style="font-size: 12pt;"><strong>JUSTIFICATIONS:</strong></label>
          <div class="textarea-container">
            ${reformArea.justifications.map((justification, j) => `
              <div key="${j}" class="justification-item" style="margin-top: 10px;">
                <span class="objective-index" style="font-size: 12pt;">${j + 1}.</span>
                <textarea style="font-size: 12pt;">${justification.justification}</textarea>
              </div>`).join('')}
          </div>
        </div>
        <!-- PROBLEMS -->
        <div class="form-section" style="margin-top: 10px;">
          <label class="form-label" for="problems" style="font-size: 12pt;"><strong>PROBLEMS:</strong></label>
          <div class="textarea-container">
            ${reformArea.problems.map((problem, j) => `
              <div key="${j}" class="problem-item" style="margin-top: 10px;">
                <span class="objective-index problem-number" style="font-size: 12pt;">${j + 1}.</span>
                <textarea style="font-size: 12pt;">${problem.problem}</textarea>
              </div>`).join('')}
          </div>
        </div>
        <!-- OUTCOMES -->
        ${reformArea.outcomes.map((outcome, k) => `
          <div key="${k}" class="outcome-container" style="margin-top: 10px;">
            <div class="form-section">
              <label class="form-label" for="outcome" style="font-size: 12pt;"><strong>OUTCOME ${k + 1}</strong></label>
              <div class="textarea-container">
                <textarea style="font-size: 12pt;">${outcome.outcomes}</textarea>
              </div>
            </div>
            <!-- Outcome Indicators -->
            <div class="form-section" style="margin-top: 10px;">
              <label class="form-label" for="outcomeIndicators" style="font-size: 12pt;"><strong>OUTCOME INDICATORS:</strong></label>
              <div class="textarea-container">
                ${outcome.outcome_indicators.map((indicator, l) => `
                  <div key="${l}" class="outcome-indicator-item" style="margin-top: 10px;">
                    <span class="objective-index" style="font-size: 12pt;">${l + 1}.</span>
                    <textarea style="font-size: 12pt;">${indicator.indicator}</textarea>
                  </div>`).join('')}
              </div>
            </div>
            <!-- Outputs -->
            ${outcome.outputs.map((output, m) => `
              <div key="${m}" class="output-container" style="margin-top: 10px;">
                <div class="form-section">
                  <label class="form-label" for="output" style="font-size: 12pt;"><strong>PROPOSED OUTPUT ${m + 1}</strong></label>
                  <div class="textarea-container">
                    <textarea style="font-size: 12pt;">${output.output}</textarea>
                  </div>
                </div>
                <!-- Output Indicators -->
                <div class="form-section" style="margin-top: 10px;">
                  <label class="form-label" for="outputIndicators" style="font-size: 12pt;"><strong>OUTPUT INDICATORS:</strong></label>
                  <div class="textarea-container">
                    ${output.output_indicators.map((indicator, n) => `
                      <div key="${n}" class="output-indicator-item" style="margin-top: 10px;">
                        <span class="objective-index" style="font-size: 12pt;">${n + 1}.</span>
                        <textarea style="font-size: 12pt;">${indicator.indicator}</textarea>
                      </div>`).join('')}
                  </div>
                </div>
                <!-- Activities -->
                          <div class="form-section" style="margin-top: 10px;">
                            <label class="form-label" for="activities" style="font-size: 12pt;"><strong>ACTIVITIES:</strong></label>
                            <div class="textarea-container">
                              ${output.activities.map((activity, o) => `
                                <div key="activity${o}" class="activity-item" style="margin-top: 10px;">
                                  <span class="objective-index" style="font-size: 12pt;">${o + 1}.</span>
                                  <textarea style="font-size: 12pt;">${activity.activity}</textarea>
                                </div>`).join('')}
                            </div>
                          </div>

                          <!-- Implementation Period -->
                          <div class="form-section" style="margin-top: 10px;">
                            <label class="form-label" for="period" style="font-size: 12pt;"><strong>Implementation Period for ${reformArea.reform_area}:</strong></label>
                            <div class="period-container">
                              ${reformArea.reform_area_periods.map((periodItem, index) => `
                                <div key="periodItem${index}" class="period-item" style="margin-top: 10px;">
                                  <span style="font-size: 12pt;">${periodItem.period}</span>
                                </div>`).join('')}
                            </div>
                          </div>
                        </div>
                      </div>`).join('')}
                  </div>`).join('')}
              </div>`).join('')}
          </div>`).join('')}

<div style="page-break-before:always">&nbsp;</div>

<!-- PART V: M & E FRAMEWORK (LANDSCAPE) -->
<div class="landscape-container">
  <div style="page-break-before: always;"></div>
  <div class="rotate-content">
    <div class="form-section" style="margin-top: 20px;">
      <label class="form-label" style="font-size: 12pt;"><strong>PART V: M & E FRAMEWORK</strong></label>
    </div>
    ${thematicAreas.value.map((thematicArea, index) => `
      <div key="thematicArea${index}" style="margin-top: 20px;">
        <table class="planning-matrix" style="border-collapse: collapse; border: 2px solid black;">
          <thead>
            <tr>
              <th colspan="15" style="text-align: center; border: 2px solid black;background-color: green !important;color: black !important; font-weight: bold !important; ">THEMATIC AREAS ALIGNED TO MW2063</th>
            </tr>
            <tr>
              <th rowspan="100" style="text-align: center; border: 2px solid black; background-color: lightgrey;">
                ${thematicArea.thematic_area}
              </th>
            </tr>
            <!-- Iterate over reform areas -->
                ${thematicArea.reformaredetail.map((reformArea, i) => `
                  <tr key="${reformArea.id}">
                    <td colspan="14" style="text-align: center; border: 2px solid black; background-color: lightblue;">REFORM AREA ${i + 1}:
                  ${reformArea.reform_area}
                </td>
                  </tr>
            <tr class="solid-line">
              <th style="border: 2px solid black;">OUTCOME</th>
              <th colspan="3" style="border: 2px solid black;">OUTCOME INDICATOR</th>
              <th style="border: 2px solid black;">Year</th>
              <th style="border: 2px solid black;">Baseline</th>
              <th colspan="2" style="border: 2px solid black;">H1 Target</th>
              <th colspan="2" style="border: 2px solid black;">H2 Target</th>
              <th style="border: 2px solid black;">Means of Verification</th>
              <th style="border: 2px solid black;">Critical Success Factor</th>
              <th style="border: 2px solid black;">Data collection Instrument</th>
              <th style="border: 2px solid black;">Responsible person</th>
            </tr>
          </thead>
          <tbody>

                   <!-- Display Outcomes and Indicators -->
            ${reformArea.outcomes.map((outcome, k) => `
              ${outcome.outcome_indicators.map((indicator, l) => `
                <tr key="indicator${l}">
                  <!-- Display outcome name for the first indicator -->
                  ${l === 0 ? `<td style="border: 2px solid black;" rowspan="${outcome.outcome_indicators.length * 2}">${outcome.outcomes}</td>` : ''}
                  <td style="border: 2px solid black;" rowspan="2" colspan="3">${indicator.indicator}</td>
                  <!-- Year, Baseline, H1 Target, H2 Target for the first year -->
                  <td style="border: 2px solid black;">${indicator.outcome_targets[0]?.year || 0}</td>
                  <td style="border: 2px solid black;">${indicator.outcome_targets[0]?.baseline || 0}</td>
                  <td style="border: 2px solid black;" colspan="2">${indicator.outcome_targets[0]?.H1_target || 0}</td>
                  <td style="border: 2px solid black;" colspan="2">${indicator.outcome_targets[0]?.H2_target || 0}</td>

                  <!-- Display outcome_movs -->
                  <td style="border: 2px solid black;" rowspan="2" colspan="1">
                    ${indicator.outcome_movs.length ? indicator.outcome_movs.map((mov, m) => `${m + 1}. ${mov.mov}`).join('<br>') : 'None'}
                  </td>

                  <!-- Display outcome_csfs -->
                  <td style="border: 2px solid black;" rowspan="2" colspan="1">
                    ${indicator.outcome_csfs.length ? indicator.outcome_csfs.map((csf, c) => `${c + 1}. ${csf.csf}`).join('<br>') : 'None'}
                  </td>

                  <!-- Display outcome_instruments -->
                  <td style="border: 2px solid black;" rowspan="2" colspan="1">
                    ${indicator.outcome_instruments.length ? indicator.outcome_instruments.map((instrument, r) => `${r + 1}. ${instrument.instrument}`).join('<br>') : 'None'}
                  </td>

                  <!-- Responsible person -->
                  <td style="border: 2px solid black;" rowspan="2" colspan="2">${indicator.outcome_targets[0]?.responsibility || 'N/A'}</td>
                </tr>

                <!-- If there are additional targets, add rows for them -->
                ${indicator.outcome_targets.length > 1 ? `
                  <tr>
                    <!-- Year, Baseline, H1 Target, H2 Target for the second year -->
                    <td style="border: 2px solid black;">${indicator.outcome_targets[1]?.year || 0}</td>
                    <td style="border: 2px solid black;">${indicator.outcome_targets[1]?.baseline || 0}</td>
                    <td style="border: 2px solid black;" colspan="2">${indicator.outcome_targets[1]?.H1_target || 0}</td>
                    <td style="border: 2px solid black;" colspan="2">${indicator.outcome_targets[1]?.H2_target || 0}</td>
                  </tr>
                ` : ''}
              `).join('')}

                 <!-- Outputs Heading -->
                        <tr class="output-heading bold-text">
                          <th style="border: 2px solid black;">OUTPUT</th>
                          <th colspan="2" style="border: 2px solid black;">OUTPUT INDICATORS</th>
                          <th style="border: 2px solid black;">ACTIVITIES</th>
                          <th style="border: 2px solid black;">Year</th>
                          <th style="border: 2px solid black;">Baseline</th>
                          <th style="border: 2px solid black;">Q1 Target</th>
                          <th style="border: 2px solid black;">Q2 Target</th>
                          <th style="border: 2px solid black;">Q3 Target</th>
                          <th style="border: 2px solid black;">Q4 Target</th>
                          <th style="border: 2px solid black;">Means of Verification</th>
                          <th style="border: 2px solid black;">Critical Success Factor</th>
                          <th style="border: 2px solid black;">Data collection Instrument</th>
                          <th style="border: 2px solid black;">Responsible person</th>
                        </tr>

              <!-- Display Outputs and Indicators -->
              ${outcome.outputs.map((output, m) => `
                ${output.output_indicators.map((outputIndicator, n) => `
                  <tr key="output${m}-indicator${n}">
                    <!-- Display output name only for the first indicator -->
                    ${n === 0 ? `<td style="border: 2px solid black;" rowspan="${output.output_indicators.length * 2}">${output.output}</td>` : ''}
                    <td style="border: 2px solid black;" rowspan="2" colspan="2">${outputIndicator.indicator}</td>

                    <!-- Display Activities only for the first indicator -->
                    ${n === 0 ? `<td style="border: 2px solid black;" rowspan="${output.output_indicators.length * 2}">
                      ${output.activities.map((activity, o) => `${o + 1}. ${activity.activity}`).join('<br>')}
                    </td>` : ''}

                    <!-- Year, Baseline, Q1 Target, Q2 Target, Q3 Target, Q4 Target for the first indicator -->
                    <td style="border: 2px solid black;">${outputIndicator.output_targets[0]?.year || 0}</td>
                    <td style="border: 2px solid black;">${outputIndicator.output_targets[0]?.baseline || 0}</td>
                    <td style="border: 2px solid black;">${outputIndicator.output_targets[0]?.Q1_target || 0}</td>
                    <td style="border: 2px solid black;">${outputIndicator.output_targets[0]?.Q2_target || 0}</td>
                    <td style="border: 2px solid black;">${outputIndicator.output_targets[0]?.Q3_target || 0}</td>
                    <td style="border: 2px solid black;">${outputIndicator.output_targets[0]?.Q4_target || 0}</td>

                    <!-- Display output_movs -->
                    <td style="border: 2px solid black;" rowspan="2">
                      ${outputIndicator.output_movs.length ? outputIndicator.output_movs.map((mov, p) => `${p + 1}. ${mov.mov}`).join('<br>') : 'None'}
                    </td>

                    <!-- Display output_csfs -->
                    <td style="border: 2px solid black;" rowspan="2">
                      ${outputIndicator.output_csfs.length ? outputIndicator.output_csfs.map((csf, q) => `${q + 1}. ${csf.output_csf}`).join('<br>') : 'None'}
                    </td>

                    <!-- Display output_instruments -->
                    <td style="border: 2px solid black;" rowspan="2">
                      ${outputIndicator.output_instruments.length ? outputIndicator.output_instruments.map((instrument, r) => `${r + 1}. ${instrument.output_instrument}`).join('<br>') : 'None'}
                    </td>

                    <!-- Responsible person -->
                    <td style="border: 2px solid black;" rowspan="2" colspan="2">${outputIndicator.output_targets[0]?.responsibility || 'N/A'}</td>
                  </tr>

                  <!-- If there are additional targets, add rows for them -->
                  ${outputIndicator.output_targets.length > 1 ? `
                    <tr>
                      <!-- Year, Baseline, Q1 Target, Q2 Target, Q3 Target, Q4 Target for the second indicator -->
                      <td style="border: 2px solid black;">${outputIndicator.output_targets[1]?.year || 0}</td>
                      <td style="border: 2px solid black;">${outputIndicator.output_targets[1]?.baseline || 0}</td>
                      <td style="border: 2px solid black;">${outputIndicator.output_targets[1]?.Q1_target || 0}</td>
                      <td style="border: 2px solid black;">${outputIndicator.output_targets[1]?.Q2_target || 0}</td>
                      <td style="border: 2px solid black;">${outputIndicator.output_targets[1]?.Q3_target || 0}</td>
                      <td style="border: 2px solid black;">${outputIndicator.output_targets[1]?.Q4_target || 0}</td>
                    </tr>
                  ` : ''}
                `).join('')}
              `).join('')}
            `).join('')}
          `).join('')}

          </tbody>
        </table>
      </div>
    `).join('')}
  </div>
</div>



<h5 style="margin-top: 20px; font-size: 1.2em;">PART VI: RESOURCE REQUIREMENTS</h5>

${thematicAreas.value.map((thematicArea, index) => `
  <div key="thematicArea${index}" style="margin-top: 20px;">

    <table class="planning-matrix" style="border-collapse: collapse; width: 100%; margin-top: 10px; border: 2px solid black;">
      <thead>
        <tr class="outcome-heading bold-text">
          <th style="border: 2px solid black; padding: 8px; text-align: center; width: 15%; background-color: dodgerblue;">REFORM AREA</th>
          <th style="border: 2px solid black; padding: 8px; text-align: center; width: 15%; background-color: dodgerblue;">OUTCOME</th>
          <th style="border: 2px solid black; padding: 8px; text-align: center; width: 15%; background-color: dodgerblue;">OUTPUT</th>
          <th style="border: 2px solid black; padding: 8px; text-align: center; width: 25%; background-color: dodgerblue;">ACTIVITY</th>
          <th style="border: 2px solid black; padding: 8px; text-align: center; width: 15%; background-color: dodgerblue;">FINANCIAL REQUIREMENTS (MK)</th>
          <th style="border: 2px solid black; padding: 8px; text-align: center; width: 15%; background-color: dodgerblue;">SOURCE OF FINANCING</th>
        </tr>
      </thead>
      <tbody>
        ${thematicArea.reformaredetail.map((reformArea, i) => `
          <tr>
            <td style="border: 2px solid black; padding: 8px; text-align: left;" rowspan="${reformArea.outcomes.reduce((acc, outcome) => acc + outcome.outputs.reduce((accOut, output) => accOut + output.activities.length, 0), 0) + 1}">
              <h6 style="font-size: 1.1em;"><label class="form-label" for="reformArea">Reform Area ${i + 1}:</label><br>${reformArea.reform_area}</h6>
            </td>
          </tr>
          ${reformArea.outcomes.map((outcome, k) => `
            ${outcome.outputs.map((output, m) => `
              ${output.activities.map((activity, p) => `
                <tr key="output${m}-activity${p}">
                  ${m === 0 && p === 0 ? `<td style="border: 2px solid black; padding: 8px; text-align: left;" rowspan="${outcome.outputs.reduce((accOut, out) => accOut + out.activities.length, 0)}">
                    <h6 style="font-size: 1em;"><label class="form-label" for="outcome">Outcome ${k + 1}:</label><br>${outcome.outcomes}</h6>
                  </td>` : ''}
                  ${p === 0 ? `<td style="border: 2px solid black; padding: 8px; text-align: left;" rowspan="${output.activities.length}">${output.output}</td>` : ''}
                  <td style="border: 2px solid black; padding: 8px; text-align: left;">${activity.activity}</td>
                  <td style="border: 2px solid black; padding: 8px; text-align: center;">${activity.budgets && activity.budgets.length > 0 ? activity.budgets[0].budget : '__'}</td>
                  <td style="border: 2px solid black; padding: 8px; text-align: center;">${activity.budgets && activity.budgets.length > 0 ? activity.budgets[0].fund_source : 'N/A'}</td>
                </tr>
              `).join('')}
            `).join('')}
          `).join('')}
          <!-- Total row for Reform Area -->
          <tr>
            <td class="total-text" style="border: 2px solid black; padding: 8px; text-align: center;">TOTAL</td>
            <!-- Total for Outcome -->
            <td class="total-value" style="border: 2px solid black; padding: 8px; text-align: center;" colspan="5">
              ${reformArea.outcomes.reduce((total, outcome) =>
                total + outcome.outputs.reduce((totalOut, output) =>
                  totalOut + output.activities.reduce((acc, activity) =>
                    acc + (activity.budgets && activity.budgets.length > 0 ? activity.budgets[0].budget : 0), 0), 0), 0)}
            </td>

          </tr>
        `).join('')}
      </tbody>
    </table>
  </div>
`).join('')}


          </body>
          </html>
        `;


        // Create a Blob object representing the data as a file
        const blob = new Blob([content], { type: 'application/msword' });

        // Create a link element to trigger the download
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'document.doc';
        link.click();
      } catch (error) {
        console.error('Error exporting to Word:', error);
      }
    };

    const getBase64FromImageUrl = async (url, maxWidth = 200, maxHeight = 200) => {
      try {
        const response = await fetch(url);
        const blob = await response.blob();

        return new Promise((resolve, reject) => {
          const image = new Image();
          image.src = URL.createObjectURL(blob);
          image.onload = () => {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            let width = image.width;
            let height = image.height;

            if (width > maxWidth || height > maxHeight) {
              const aspectRatio = width / height;
              if (width > height) {
                width = maxWidth;
                height = width / aspectRatio;
              } else {
                height = maxHeight;
                width = height * aspectRatio;
              }
            }

            canvas.width = width;
            canvas.height = height;
            context.drawImage(image, 0, 0, width, height);

            resolve(canvas.toDataURL());
          };
          image.onerror = reject;
        });
      } catch (error) {
        console.error('Error fetching image:', error);
        return null;
      }
    };

const fetchInstitution = async () => {
      try {
        const userData = await fetchUserData();
        const institutionData = await fetchInstitutionData(userData.id);
        institutionName.value = institutionData.institution_name;

        // Fetch the institution's logo based on its name
        institutionLogo.value = `/src/assets/${institutionName.value}.png`; // Assuming logo files are in png format

        // Set current date
        currentDate.value = getCurrentDate();

        // Fetch implementation period from the endpoint
        const institutionId = institutionData.id; // Get institution ID directly
        const accessToken = localStorage.getItem('accessToken'); // Ensure accessToken is retrieved

        const response = await api.get(`/periods/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });

        // Check if response.data exists and has elements
        if (response.data && response.data.length > 0) {
          const periodData = response.data[0];
          implementationPeriod.value = periodData.period;
        } else {
          throw new Error('No period data found.');
        }

        // Fetch mandate, vision, mission, and strategic objectives
        await fetchMandate(accessToken, institutionId);
        await fetchVision(accessToken, institutionId);
        await fetchMission(accessToken, institutionId);
        await fetchObjectives(accessToken, institutionId);
        await fetchOrgResponsibilities(accessToken, institutionId);
        await fetchGovtObligations(accessToken, institutionId);
        await fetchReformAreas(accessToken, institutionId);

      } catch (error) {
        console.error('Error fetching institution data:', error);
      }
    };

    const getCurrentDate = () => {
      const now = new Date();
      const day = now.getDate();
      const month = now.toLocaleString('default', { month: 'long' });
      const year = now.getFullYear();
      return `${day}th ${month}, ${year}`;
    };

    const fetchMandate = async (accessToken, institutionId) => {
      try {
        const response = await api.get(`/mandates/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        mandate.value = response.data.mandate;
      } catch (error) {
        console.error('Error fetching mandate:', error);
      }
    };

    const fetchVision = async (accessToken, institutionId) => {
      try {
        const response = await api.get(`/visions/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        vision.value = response.data.vision;
      } catch (error) {
        console.error('Error fetching vision:', error);
      }
    };

    const fetchMission = async (accessToken, institutionId) => {
      try {
        const response = await api.get(`/missions/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        mission.value = response.data.mission || '';
      } catch (error) {
        console.error('Error fetching mission:', error);
      }
    };

    const fetchObjectives = async (accessToken, institutionId) => {
      try {
        const response = await api.get(`/strategic-objectives/current/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        editedObjectives.value = response.data.map(obj => obj.objective) || [];
      } catch (error) {
        console.error('Error fetching objectives:', error);
      }
    };

    const fetchOrgResponsibilities = async (accessToken, institutionId) => {
      try {
        const response = await api.get(`/org-responsibilities/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        orgResponsibilities.value = response.data.map(item => ({
          id: item.id,
          responsibility: item.responsibility,
          year: item.year,
          updated_at: item.updated_at,
          created_at: item.created_at,
          deleted: item.deleted
        })) || [];
      } catch (error) {
        console.error('Error fetching organization responsibilities:', error);
      }
    };

    const fetchGovtObligations = async (accessToken, institutionId) => {
      try {
        const response = await api.get(`/govt-obligations/institution/${institutionId}`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        govtObligations.value = response.data.map(item => ({
          id: item.id,
          govt_obligation: item.govt_obligation,
          year: item.year,
          updated_at: item.updated_at,
          created_at: item.created_at,
          deleted: item.deleted
        })) || [];
      } catch (error) {
        console.error('Error fetching government obligations:', error);
      }
    };

    const fetchReformAreas = async (accessToken, institutionId) => {
  try {
    const response = await api.get(`/reform-areas/institution/${institutionId}`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    if (response && response.data && Array.isArray(response.data)) {
      const fetchedThematicAreas = new Set();
      const thematicAreaPromises = response.data.map(async reformArea => {
        if (!fetchedThematicAreas.has(reformArea.thematic_area)) {
          fetchedThematicAreas.add(reformArea.thematic_area);
          const thematicAreaData = await fetchThematicArea(reformArea.thematic_area, institutionId, accessToken);          return thematicAreaData;
        }
        return null;
      });

      const thematicAreasData = await Promise.all(thematicAreaPromises);
      thematicAreas.value = thematicAreasData.filter(thematicArea => thematicArea !== null);
    } else {
      throw new Error('Error fetching reform areas or response structure is incorrect.');
    }
  } catch (error) {
    console.error('Error fetching reform areas:', error);
    // Handle error as needed
  }
};

const fetchThematicArea = async (thematicAreaId, institutionId, accessToken) => {
  try {
    const response = await api.get(`/thematic-areas/${thematicAreaId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`, // Include the access token in the headers
      },
      params: {
        institution_id: institutionId // Include the institution_id as a query parameter
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching thematic area:', error);
    return null;
  }
};




    onMounted(() => {
      fetchInstitution();
    });
    return {
      institutionName,
      institutionLogo,
      currentDate,
      implementationPeriod,
      mandate,
      vision,
      mission,
      editedObjectives,
      orgResponsibilities,
      govtObligations,
      reformAreas,
      thematicAreas,
      downloadDocument
    };
  },
};
</script>

<style scoped>
.page {
  width: 21cm;
  height: 29.7cm;
  margin: 0 auto;
}

.frame {
  width: 100%;
  height: 100%;
  background-color: rgb(0, 0, 0);
  display: flex;
  justify-content: center;
  align-items: center;
}

.black-layer {
  background-color: rgb(15, 148, 29);
  width: 99%;
  height: 99%;
  border: 4px solid red;
  display: flex;
  justify-content: center;
  align-items: center;
}

.red-layer {
  background-color: rgb(255, 255, 255);
  width: 99%;
  height: 99%;
  border: 20px solid rgb(255, 255, 255);
  display: flex;
  justify-content: center;
  align-items: center;
}

.green-layer {
  background-color: rgb(255, 255, 255);
  width: 99%;
  height: 99%;
  padding: 20px;
  border: 20px solid rgb(255, 255, 255);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.logo {
  width: 150px;
  height: auto;
}

.title {
  font-size: 32px;
  margin: 10px 0;
  text-align: center;
}

.subtitle {
  font-size: 24px;
  margin: 10px 0;
  text-align: center;
}

.council {
  font-size: 20px;
  margin: 10px 0;
  text-align: center;
}

.implementation-container {
  background-color: rgb(15, 148, 29);
  width: 100%;
  padding: 20px;
  margin-top: 20px;
  border-radius: 10px;
  margin-bottom: 10px; /* Adjust this margin to move the logo up or down */
}

.implementation-heading {
  font-size: 24px;
  color: white;
  text-align: center;
}

.implementation-period {
  font-size: 20px;
  color: white;
  text-align: center;
}

.submission-date {
  font-size: 18px;
  margin: 20px 0;
  text-align: center;
}

.title {
  margin-top: 5px; /* Adjust the margin between the title and other content */
}

.reform-logo {
  width: 200px;
  height: auto;
  margin-top: 50px;
}

.objectives-list {
  list-style-type: disc;
  margin-left: 20px;
  color: #666;
}

.objectives-list li {
  margin-bottom: 5px;
}

textarea {
  display: block;
  width: 95%;
  padding: 10px;
  margin-top: 5px;
  margin-left: 20px; /* Adjust this value to move the text areas to the right */
  resize: vertical;
}

.objective-item {
  display: flex;
  align-items: center;
}


.objective-index,
.justification-number {
  margin-right: 10px; /* Adjust as needed */
  font-weight: bold;
  text-align: center; /* Center the numbering */
}

.justification-item {
  display: flex;
  align-items: center;
  justify-content: flex-end; /* Right-align the justification items */
}

.problem-item {
  display: flex;
  align-items: center;
  justify-content: flex-end; /* Right-align the problem items */
}

.problem-number {
  margin-right: 10px; /* Adjust as needed */
  font-weight: bold;
  text-align: center; /* Center the numbering */
}

.outcome-textarea {
  display: block;
  width: 100%; /* Adjust the width as needed */
  padding: 10px;
  margin-top: 5px;
  margin-left: 40px; /* Move the textarea to the right */

  resize: vertical;
}

.outcome-textarea-container {
  display: flex;
  align-items: center;
}

.outcome-indicator-item {
  display: flex;
  align-items: center;
  justify-content: flex-end; /* Right-align the outcome indicator items */
}

.indicator-number {
  margin-right: 10px; /* Adjust as needed */
  font-weight: bold;
  text-align: center; /* Center the numbering */
}

.output-textarea {
  display: block;
  width: 100%; /* Adjust the width as needed */
  padding: 10px;
  margin-top: 5px;
  margin-left: 40px; /* Move the textarea to the right */

  resize: vertical;
}

.output-textarea-container {
  display: flex;
  align-items: center;
}


.output-indicator-item {
  display: flex;
  align-items: center;
  justify-content: flex-end; /* Right-align the output indicator items */
}

.indicator-number {
  margin-right: 10px; /* Adjust as needed */
  font-weight: bold;
  text-align: center; /* Center the numbering */
}

.activity-item {
  display: flex;
  align-items: center;
  justify-content: flex-end; /* Right-align the activity items */
}

.activity-number {
  margin-right: 10px; /* Adjust as needed */
  font-weight: bold;
  text-align: center; /* Center the numbering */
}

.planning-matrix {
  border-collapse: collapse;
  width: 100%;
}

.planning-matrix th,
.planning-matrix td {
  border: 1px solid #000;
  padding: 8px;
  text-align: left;
}

.planning-matrix th {
  background-color: #f2f2f2;
}

.planning-matrix tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

.planning-matrix tbody tr:hover {
  background-color: #ddd;
}


.message-container {
  position: fixed;
  bottom: 20px; /* Adjust the bottom position */
  left:50%;

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
  color: green;
  margin-top: 20px; /* Increase top margin */
  background-color: #e6ffe6; /* Light green background */
  border: 2px solid #4CAF50; /* Green border */
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
