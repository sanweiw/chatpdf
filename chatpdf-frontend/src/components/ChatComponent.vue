<template>
  <div class="chat-component">
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" :class="{'user': message.sender === 'user', 'bot': message.sender === 'bot'}">
        {{ message.text }}
      </div>
    </div>
    <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message...">
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newMessage: '',
      messages: [],
    };
  },
  methods: {
    sendMessage() {
      const messageText = this.newMessage.trim();
      if (messageText) {
        // Add user message to messages array
        this.messages.push({ sender: 'input_text', text: messageText });
        // Send message to bot API
        fetch('http://localhost:5000/process-input', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ input_text: messageText }),
        })
        .then(response => response.json())
        .then(data => {
          // Assuming the bot's reply is in data.reply
          this.messages.push({ sender: 'response', text: data.message });
        })
        .catch(error => {
          console.error('Error:', error);
          // Handle error or show a default bot error message
          this.messages.push({ sender: 'response', text: 'Sorry, I am having trouble responding right now.' });
        });
      }
      // Clear the input field
      this.newMessage = '';
    }
  },
  mounted() {
    console.log('Component mounted');
  }  
}
</script>

<style>
.messages {
  max-height: 300px;
  overflow-y: auto;
}

.user {
  text-align: right;
  color: blue;
}

.bot {
  text-align: left;
  color: green;
}
</style>
