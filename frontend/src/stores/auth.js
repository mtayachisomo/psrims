// src/stores/auth.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
  }),
  actions: {
    storeToken(token) {
      this.accessToken = token;
      localStorage.setItem('accessToken', token);
    },
    clearToken() {
      this.accessToken = null;
      localStorage.removeItem('accessToken');
    },
  },
});
