<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center bg-gradient">
        <q-card v-bind:style="$q.screen.lt.sm ? { width: '80%' } : { width: '30%' }">

          <q-card-section>
            <img src="favicon.ico" alt="Logo" style="max-width: 50%; display: block; margin: 0 auto;">
            <div class="text-center q-pt-lg">
              <div class="text-h6 ellipsis">
                Log in
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <q-form class="q-gutter-md" @submit.prevent="login">
              <q-input
                filled
                v-model="email"
                label="Email"
                lazy-rules
                :rules="[(val) => !!val || 'Please enter an email']" />

              <q-input
                filled
                v-model="password"
                label="Password"
                :type="isPwd ? 'text' : 'password'"
                :rules="[(val) => !!val || 'Please enter the password']">
                <template v-slot:append>
                  <q-icon :name="isPwd ? 'visibility' : 'visibility_off'" class="cursor-pointer" @click="togglePwdVisibility" />
                </template>
              </q-input>

              <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
              <div class="checkbox">
                <label>
                  <input type="checkbox"> Remember Me
                </label><br>
                <label class="forgot-password">
                  <a href="">Forgotten Password?</a>
                </label>
                <br>
              </div>
              <div class="text-center button-container">
                <q-btn label="Login" type="submit" color="positive"/>
              </div>

            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { useUserStore } from 'src/stores/user';
import { ref, onMounted } from 'vue';
import { api } from '/src/boot/axios';
import { useRouter } from 'vue-router';
import { fetchUserData } from 'src/services/userAPI';

export default {
  name: 'Login',
  setup() {
    const email = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const isPwd = ref(false);
    const router = useRouter();
    const userStore = useUserStore();

    const login = async () => {
      try {
        const response = await api.post('/users/login/', {
          email: email.value,
          password: password.value
        }, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        });

        const accessToken = response.data.tokens.access;
        userStore.storeToken(accessToken);

        const userResponse = await fetchUserData();
        userStore.setUserInfo(userResponse);

        errorMessage.value = '';

        router.push('/dashboard');
      } catch (error) {
        errorMessage.value = 'Invalid credentials. Please try again.';
        console.error(error);
      }
    };

    const togglePwdVisibility = () => {
      isPwd.value = !isPwd.value;
    };

    onMounted(() => {
      errorMessage.value = '';
    });

    return {
      email,
      password,
      errorMessage,
      isPwd,
      login,
      togglePwdVisibility
    };
  }
};
</script>

<style>
.error-message {
  color: red;
  margin-top: 1px;
  margin-bottom: 1px;
  text-align: center;
}
.bg-gradient {
  background-color: #f1f1f1;
}

.logo {
  display: block;
  margin: auto;
  margin-bottom: 20px;
  max-width: 150px;
  height: auto;
}

.forgot-password {
  float: right;
}
.button-container {
  display: flex;
  justify-content: center;
}
</style>
