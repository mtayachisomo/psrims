<template>

  <q-page padding style="margin-top: 20px;">
       <!-- Main Content -->
     <div class="q-mt-md">
       <!-- Form Container -->
       <q-card>
         <q-card-section class="q-pa-none">
           <!-- Form Content -->
           <div class="row q-col-gutter-lg">
             <!-- Form Inputs -->
             <div class="col-12 col-md-6 q-px-lg q-py-lg">
               <!-- First Name Input -->
               <div class="row q-mb-lg">
                 <div class="col">
                   <q-input
                     v-model="formData.first_name"
                     outlined
                     standout
                     label="First Name"
                   />
                 </div>
               </div>

               <!-- Last Name Input -->
               <div class="row q-mb-lg">
                 <div class="col">
                   <q-input
                     v-model="formData.last_name"
                     outlined
                     standout
                     label="Last Name"
                   />
                 </div>
               </div>

               <!-- Email Input -->
               <div class="row q-mb-lg">
                 <div class="col">
                   <q-input
                     v-model="formData.email"
                     outlined
                     standout
                     label="Email"
                   />
                 </div>
               </div>

               <!-- Phone Number Input -->
               <div class="row q-mb-lg">
                 <div class="col">
                   <q-input
                     v-model="formData.phone"
                     outlined
                     standout
                     label="Phone number"
                   />
                 </div>
               </div>

               <!-- Action Buttons -->
               <div class="row q-gutter-x-md q-mt-md">
                 <q-btn unelevated color="positive" label="Create" @click="createUser" />
                 <q-btn unelevated flat color="negative" label="Cancel" />
               </div>

               <!-- Error Message from Backend -->
               <div v-if="backendErrorMessage" class="row q-mb-md">
                 <div class="col">
                   <q-banner color="negative">{{ backendErrorMessage }}</q-banner>
                 </div>
               </div>

               <!-- Success/Error Message -->
               <div class="message-container">
                 <q-banner v-if="successMessage" color="positive" class="success-message">{{ successMessage }}</q-banner>
                 <q-banner v-if="errorMessage" color="negative" class="error-message">{{ errorMessage }}</q-banner>
               </div>
             </div>
           </div>
         </q-card-section>
       </q-card>
     </div>
   </q-page>
 </template>

 <script setup>
 import { ref } from "vue";
 import { api } from "/src/boot/axios";
 import { fetchInstitutionData } from '/src/services/institutionApi';

 const formData = ref({
   first_name: '',
   last_name: '',
   email: '',
   phone: ''
 });

 const successMessage = ref('');
 const errorMessage = ref('');
 const backendErrorMessage = ref('');

 const createUser = async () => {
   try {
     const accessToken = localStorage.getItem("accessToken");
     const response = await api.post("/users/create/", formData.value, {
       headers: {
         Authorization: `Bearer ${accessToken}`
       }
     });
     console.log(response.data);
     const userId = response.data.id;

     const institutionData = await fetchInstitutionData();
     const institutionId = institutionData.id;

     await connectUserToInstitution(userId, institutionId);

     successMessage.value = 'User created and connected to institution successfully!';
     errorMessage.value = '';


     return userId;
   } catch (error) {
     console.error(error);
     if (error.response && error.response.data) {
       errorMessage.value = error.response.data.email ? error.response.data.email[0] : "An error occurred";

     } else {
       errorMessage.value = backendErrorMessage.value = "An error occurred";
     }
     successMessage.value = '';

     throw error;
   }
 };

 const connectUserToInstitution = async (userId, institutionId) => {
   try {
     const accessToken = localStorage.getItem("accessToken");
     const response = await api.post("/institution-users/create/", {
       user: userId,
       institution: institutionId
     }, {
       headers: {
         Authorization: `Bearer ${accessToken}`
       }
     });
     console.log(response.data);
   } catch (error) {
     throw new Error(`Failed to connect user to institution: ${error}`);
   }
 };
 </script>
 <style scoped>
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
