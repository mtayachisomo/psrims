// src/services/userApi.js

import { api } from '/src/boot/axios';
import { useAuthStore } from '/src/stores/auth';

export async function fetchUserData() {
  const authStore = useAuthStore();
  try {
    const accessToken = authStore.accessToken;
    if (!accessToken) {
      throw new Error('Access token not found. User is not authenticated.');
    }

    const response = await api.get('/users/me/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.data && response.data.id) {
      return response.data;
    } else {
      throw new Error('Error fetching user data: Response data is not in the expected format');
    }
  } catch (error) {
    throw new Error(`Error fetching user data: ${error}`);
  }
}
