<template>
  <q-page class="q-pa-md chat-page">
    <q-card class="chat-container" ref="chatContainer">
      <q-card-section class="chat-section">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', message.sender]"
          :style="{ alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start' }"
        >
          <div class="message-header">
            <span class="message-sender" style="text-align: left">{{ message.senderName }}</span>
          </div>
          <div class="message-content">
            <p>{{ message.text }}</p>
            <span class="timestamp">{{ message.time }}</span>
            <div class="status">
              <q-icon
                :name="message.status === 'delivered' ? 'check_double' : 'check'"
                class="status-icon"
              />
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <div class="input-container">
      <q-input
        v-model="newMessage"
        placeholder="Type a message..."
        dense
        outlined
        class="message-input"
        @keyup.enter="sendMessage"
      />
      <q-btn round color="positive" icon="send" @click="sendMessage" />
    </div>
  </q-page>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useUserStore } from 'src/stores/user'; // Import the user store

const userStore = useUserStore();
const userName = userStore.getUserName();

const newMessage = ref('');
const messages = ref([
{ id: 1, text: 'Hello! How can I help you?', sender: 'secretariat', senderName: 'Secretariat', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), status: 'delivered' },
]);

const sendMessage = () => {
  if (newMessage.value.trim() !== '') {
    messages.value.push({
      id: messages.value.length + 1,
      text: newMessage.value,
      sender: 'user',
      senderName: userName,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'sent'
    });
    newMessage.value = '';
    nextTick(() => {
      const chatContainer = document.querySelector('.chat-container');
      chatContainer.scrollTop = chatContainer.scrollHeight;
    });
  }
};
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-container {
  background-color: #fff;
  width: 100%;
  max-width: 100%;
  flex: 1;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  padding: 10px;
  overflow-y: auto;
  margin: 0 10px; /* Add margin to prevent touching the edges */
}

.chat-section {
  flex: 1;
  overflow-y: auto;
}

.message {
  max-width: 75%; /* Adjust max-width to ensure it doesn't reach the edges */
  margin: 10px 0;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.message-header {
  font-size: 12px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.message-content {
  display: flex;
  flex-direction: column;
}

.message p {
  margin: 0;
  font-size: 14px;
}

.timestamp {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.message-sender {
  font-size: 12px;
  font-weight: bold;
}

.input-container {
  display: flex;
  align-items: center;
  position: sticky;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #f5f5f5;
  padding: 10px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.message-input {
  flex: 1;
  margin-right: 10px;
}

.status {
  display: flex;
  align-items: center;
}

.status-icon {
  color: #4caf50;
}

.secretariat {
  background-color: #ffffff; /* White */
  align-self: flex-start;
  margin-left: 10px; /* Add margin to prevent touching the left edge */
}

.user {
  background-color: #dcf8c6; /* Light blue */
  align-self: flex-end;
  margin-right: 10px; /* Add margin to prevent touching the right edge */
}
</style>
