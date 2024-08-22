// src/stores/user.ts

import { reactive } from 'vue';
import { useAuthStore } from './auth'; // Import useAuthStore from auth.js

const state = reactive({
  user: null
});

export const useUserStore = () => {
  const authStore = useAuthStore(); // Initialize authStore

  const setUserInfo = (userInfo) => {
    state.user = userInfo;
  };

  const getUserName = () => {
    return state.user ? `${state.user.first_name} ${state.user.last_name}` : '';
  };
  const getFirstCharacterOfUserName = () => {
    if (state.user) {
      const firstNameInitial = state.user.first_name.charAt(0).toUpperCase();
      const lastNameInitial = state.user.last_name.charAt(0).toUpperCase();
      return `${firstNameInitial}${lastNameInitial}`;
    }
    return '';
  };

  const storeToken = (token: string) => {
    authStore.storeToken(token); // Delegate token storage to authStore
  };

  return {
    setUserInfo,
    getUserName,
    getFirstCharacterOfUserName,
    storeToken // Expose storeToken method
  };
};
