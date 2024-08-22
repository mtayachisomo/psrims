// src/services/institutionApi.js

import { api } from '/src/boot/axios';
import { fetchUserData } from '/src/services/userApi'; // Import fetchUserData function
import { useAuthStore } from 'src/stores/auth'; // Import useAuthStore

export async function fetchInstitutionData() {
  const authStore = useAuthStore();

  try {
    // Get user data to obtain userId
    const userData = await fetchUserData();
    const userId = userData.id; // Extract userId from user data

    const accessToken = authStore.accessToken; // Get access token from store

    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    const response = await api.get(`/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.data && Array.isArray(response.data.institutions) && response.data.institutions.length > 0) {
      return response.data.institutions[0];
    } else {
      throw new Error('Error fetching institution data: Response data is not in the expected format');
    }
  } catch (error) {
    throw new Error(`Error fetching institution data: ${error}`);
  }
}
