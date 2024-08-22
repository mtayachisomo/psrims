<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-custom text-black header-rounded" height-hint="48" bordered style="padding-bottom: 2px">
      <q-toolbar style="margin-top: -5px">
        <q-btn
          flat
          dense
          round
          @click="toggleLeftDrawer"
          icon="menu"
          aria-label="Menu"
          class="text-black"
        />
        <q-toolbar-title class="text-black">
          <strong>{{ activeSection || institutionName }} </strong>
        </q-toolbar-title>
        <q-space />
        <div class="q-gutter-sm row items-center no-wrap">
          <!-- Fullscreen toggle button -->
          <q-btn
            round
            dense
            flat
            color="black"
            :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
            @click="$q.fullscreen.toggle()"
            v-if="$q.screen.gt.sm"
            class="text-black"
          >
            <q-tooltip>{{ $t('$.fullscreen') }}</q-tooltip>
          </q-btn>

          <!-- Refresh button with loader -->
          <q-btn
            round
            dense
            flat
            color="black"
            icon="refresh"
            @click="handleReload"
            v-if="$q.screen.gt.sm && $q.fullscreen.isActive"

          >

          </q-btn>
          <q-btn round dense flat color="black" icon="notifications" class="text-black">
            <q-badge color="red" text-color="white" floating>5</q-badge>
            <q-menu>
              <q-list style="min-width: 100px">
                <messages></messages>
                <q-card class="text-center no-shadow no-border">
                  <q-btn
                    label="View All"
                    style="max-width: 120px !important;"
                    flat
                    dense
                    class="text-primary"
                  />
                </q-card>
              </q-list>
            </q-menu>
          </q-btn>
          <q-btn round flat >
            <q-avatar color="primary" text-color="white">
              {{ firstCharacterOfUserName }}
            </q-avatar>
            <q-menu>
              <q-list dense>
                <q-item>
                  <q-item-section>
                    <div>
                      <strong>{{ userName }}</strong>
                    </div>
                  </q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable @click="userLogout">
                  <q-item-section>Sign out</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
            <q-tooltip>user</q-tooltip>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-custom-drawer text-black">
      <q-list>
        <q-item>
          <q-item-section side>
            <img src="/favicon.ico" alt="Favicon" style="width: 100px; height: 50px;">
          </q-item-section>
        </q-item>

        <q-item to="/dashboard" active-class="active-item" @click="setActiveSection('Dashboard')">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Dashboard</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/institutionprofile" active-class="active-item" @click="setActiveSection('Institution Profile')">
          <q-item-section avatar>
            <q-icon name="checklist">
              <div class="bars"></div>
            </q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Institution Profile</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/SituationAnalysis" active-class="active-item" @click="setActiveSection('Situation Analysis')">
          <q-item-section avatar>
            <q-icon name="search">
              <div class="bars"></div>
            </q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Situation Analysis</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/reformareaconfigurations" active-class="active-item" @click="setActiveSection('Reform Area Configuration')">
          <q-item-section avatar>
            <q-icon name="settings">
              <div class="bars"></div>
            </q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Reform Area Configuration</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/reformareaweight" active-class="active-item" @click="setActiveSection('Reform Area Weights')">
          <q-item-section avatar>
            <q-icon name="scale">
              <div class="bars"></div>
            </q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Reform Area Weights</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item icon="work" label="M & E Framework">
          <q-expansion-item :header-inset-level="0.85" label="Planning Stage">
            <q-item
              to="/m&eframework/outputplan"
              class="q-ml-xl"
              style="margin-left: 55px !important;"
              active-class="active-item"
              @click="setActiveSection('Output Plan')"
            >
              <q-item-section>
                <q-item-label>Output</q-item-label>
              </q-item-section>
            </q-item>
            <q-item
              to="/m&eframework/outcomeplan"
              class="q-ml-xl"
              style="margin-left: 55px !important;"
              active-class="active-item"
              @click="setActiveSection('Outcome Plan')"
            >
              <q-item-section>
                <q-item-label>Outcome</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>
          <q-expansion-item :header-inset-level="0.85" label="Reporting Stage">
            <q-item
              to="/m&eframework/reporting/output"
              class="q-ml-xl"
              style="margin-left: 55px !important;"
              active-class="active-item"
              @click="setActiveSection('Output Report')"
            >
              <q-item-section>
                <q-item-label>Output</q-item-label>
              </q-item-section>
            </q-item>
            <q-item
              to="/BlankPage"
              class="q-ml-xl"
              style="margin-left: 55px !important;"
              active-class="active-item"
              @click="setActiveSection('Output & Outcome Report')"
            >
              <q-item-section>
                <q-item-label>Output & Outcome</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>
        </q-expansion-item>

        <q-item to="/commitments" active-class="active-item" @click="setActiveSection('Commitments')">
          <q-item-section avatar>
            <q-icon name="handshake">
              <div class="bars"></div>
            </q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Commitments</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/contract" active-class="active-item" @click="setActiveSection('Contract')">
          <q-item-section avatar>
            <q-icon name="pages">
              <div class="bars"></div>
            </q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Contract</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item icon="folder" label="Progress">
          <q-item
            to="/M&E-output-graphs"
            class="q-ml-xl"
            style="margin-left: 55px !important;"
            active-class="active-item"
            @click="setActiveSection('Output Progress')"
          >
            <q-item-section avatar>
              <q-icon name="assessment">
                <div class="bars"></div>
              </q-icon>
            </q-item-section>
            <q-item-section>
              <q-item-label>Output</q-item-label>
            </q-item-section>
          </q-item>
          <q-item
            to="/M&E-Outcome-graphs"
            class="q-ml-xl"
            style="margin-left: 55px !important;"
            active-class="active-item"
            @click="setActiveSection('Outcome Progress')"
          >
            <q-item-section avatar>
              <q-icon name="assessment">
                <div class="bars"></div>
              </q-icon>
            </q-item-section>
            <q-item-section>
              <q-item-label>Outcome</q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            to="/report"
            class="q-ml-xl"
            style="margin-left: 55px !important;"
            active-class="active-item"
            @click="setActiveSection('Progress Report')"
          >
            <q-item-section avatar>
              <q-icon name="pages">
                <div class="bars"></div>
              </q-icon>
            </q-item-section>
            <q-item-section>
              <q-item-label>Report</q-item-label>
            </q-item-section>
          </q-item>
        </q-expansion-item>

        <q-item-label header class="text-weight-bolder text-black">SYSTEM MANAGEMENT</q-item-label>
        <q-item to="/BlankPage" active-class="active-item" @click="setActiveSection('User Profile')">
          <q-item-section avatar>
            <q-icon name="person" />
          </q-item-section>
          <q-item-section>
            <q-item-label>User Profile</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/users/create" active-class="active-item" @click="setActiveSection('Create User')">
          <q-item-section avatar>
            <q-icon name="person_add" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Create User</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/BlankPage" active-class="active-item" @click="setActiveSection('Roles')">
          <q-item-section avatar>
            <q-icon name="people" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Roles</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/BlankPage" active-class="active-item" @click="setActiveSection('Configurations')">
          <q-item-section avatar>
            <q-icon name="settings" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Configurations</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/help/secretariat" active-class="active-item" @click="setActiveSection('help')">
          <q-item-section avatar>
            <q-icon name="help" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Help</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container class="bg-grey-2">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import { useUserStore } from 'src/stores/user';
import { useAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router';
import { fetchInstitutionData } from '/src/services/institutionApi';
import { fetchUserData } from '/src/services/userApi';
import axios from 'axios'; // Correct import for Axios

export default defineComponent({
  name: 'MainLayout',
  setup() {
    const userId = ref(null);
    const institutionId = ref(null);
    const institutionName = ref('');
    const authStore = useAuthStore();
    const userStore = useUserStore();
    const quasar = useQuasar();
    const leftDrawerOpen = ref(false);
    const activeSection = ref('');
    const router = useRouter();

    // Ensure userStore is initialized properly
    if (!userStore) {
      console.error('User store is not initialized properly.');
    }

    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value;
    };

    const userLogout = async () => {
      try {
        const accessToken = authStore.accessToken;
        if (!accessToken) {
          throw new Error('Access token not found. User is not authenticated.');
        }

        // Call logout endpoint
        await axios.post('http://127.0.0.1:8000/users/logout/', null, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        authStore.clearToken(); // Clear token from authStore
        router.push('/'); // Redirect to home page after logout
      } catch (error) {
        console.error('Logout failed:', error);
        // Handle error as needed
      }
    };

    const setActiveSection = (section) => {
      activeSection.value = section;
    };

    // Fetch user data and institution data on component mount
    onMounted(async () => {
      try {
        const userData = await fetchUserData();
        userId.value = userData.id;
        const institutionData = await fetchInstitutionData(userData.id);
        institutionId.value = institutionData.id;
        institutionName.value = institutionData.institution_name; // Set institutionName from fetched data
      } catch (error) {
        console.error('Error fetching user or institution data:', error);
        // Handle error as needed
      }
    });

    return {
      institutionName,
      userStore,
      leftDrawerOpen,
      toggleLeftDrawer,
      userLogout,
      quasar,
      activeSection,
      setActiveSection,
    };
  },
  computed: {
    firstCharacterOfUserName() {
      return this.userStore.getFirstCharacterOfUserName();
    },
    userName() {
      return this.userStore.getUserName();
    },
  },
});
</script>

<style scoped>
.bg-custom {
  background-color: rgba(180, 180, 180, 0.689); /* Change to your desired background color */
}

.bg-custom-drawer {
  background-color: #3D405B; /* Change to your desired drawer background color */
}

.text-black {
  color: black;
}

.active-item {
  background-color: rgba(180, 180, 180, 0.689); /* Change to your desired active background color */
}

.header-rounded {
  margin-top: 15px; /* Adds space above the header */
  border-radius: 15px; /* Rounds the corners of the header */
  box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 12px 0px; /* Adjusts shadow */
}
</style>
