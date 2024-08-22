<template>
    <div class="form-container">
      <h5>Registration Form</h5>
      <form id="registration-form" @submit.prevent="submitForm">
        <div id="current-date" style="display: none">
          <label>Current date</label>
          <input type="date" id="submission_date" name="submission_date" v-model="currentDate">
        </div>
  
        <div class="form-group">
      <label for="institution-name">Institution Name:</label>
      <institution-registration :accessToken="accessToken" />
    </div>

        
        <div id="mandate-container" class="field-container">
          <label for="mandate">Mandate</label>
          <div id="mandateList">
            <textarea type="text" id="mandate" v-model="mandate" required></textarea>
          </div>
        </div>
  
        <div class="form-group">
          <label for="vision">Vision</label>
          <textarea id="vision" v-model="vision" rows="3" required></textarea>
        </div>
  
        <div class="form-group">
          <label for="mission">Mission</label>
          <textarea id="mission" v-model="mission" rows="3" required></textarea>
        </div>
  
        <div id="strategicobjectives-container" class="field-container">
          <label for="strategic-objectives">Strategic Objectives</label>
          <div id="strategicobjectiveList">
            <div v-for="(objective, index) in strategicObjectives" :key="index">
              <textarea v-model="strategicObjectives[index]" rows="3" required></textarea>
              <button type="button" class="remove-section red-button" @click="removeObjective(index)">
                Remove Strategic Objective
              </button>
            </div>
          </div>
          <button type="button" class="add-field" @click="addObjective">Add Strategic Objectives</button>
        
        </div>
  
        
      </form>
      <div id="registration-message" class="registration-message"></div>
      <button type="submit" class="register-button">Register</button>
    </div>
  </template>   


<script>
import InstitutionRegistration from '../components/registration/institution.vue';

export default {
  components: {
    InstitutionRegistration
  },
  data() {
    return {
      strategicObjectives: [],
      accessToken: localStorage.getItem('accessToken') || ''

    };
  },
  methods: {
      addListItem(listId) {
        // Your JavaScript functions go here
        // ...
      },
      removeSection(button) {
        // Your JavaScript functions go here
        // ...
      },
      addObjective() {
        this.strategicObjectives.push('');
      },
      removeObjective(index) {
        this.strategicObjectives.splice(index, 1);
      },
      submitForm() {
        // Handle form submission logic here
      },
      setCurrentDate() {
        const currentDate = new Date();
        const year = currentDate.getFullYear();
        const month = ('0' + (currentDate.getMonth() + 1)).slice(-2);
        const day = ('0' + currentDate.getDate()).slice(-2);
        this.currentDate = `${year}-${month}-${day}`;
      },
    },
    mounted() {
      this.setCurrentDate(); // Set current date on component mount
      // Additional logic to fetch institution details and set the data accordingly
      // Example: Fetch institution name based on institution ID and set 'institutionName'
    },
  };
  </script>

<style>
/* Add your CSS styles here */

.form-container {
  margin: 30px auto;
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
h5 {
  text-align: center;
  margin-bottom: 20px;
}

form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
input[type="number"],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.register-button {
  position: absolute;
  bottom: 1px;
  right: 20px;
  background-color: #1db522;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.register-button:hover {
  background-color: darkgreen;
}

.registration-message {
  text-align: center;
  font-weight: bold;
  margin-top: 15px;
}

.add-field {
  /* Add your preferred colors */
  background-color: #1db522;
  color: white;
  border: none;

  font-size: 12px; /* Adjust the font size */
  padding: 4px 8px; /* Adjust the padding */
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}

.add-field:hover {
  background-color: darkgreen;
}

.remove-section {
    background-color: #ff0000;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px; /* Adjust the font size */
    padding: 4px 8px; /* Adjust the padding */
    font-weight: bold;
    margin-top: 2px;
}

.remove-section:hover {
    background-color:  #ff0303;
}

.objective-item {
  margin-bottom: 15px;
}

/* Additional styles... */
</style>