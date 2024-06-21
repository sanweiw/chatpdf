<!-- Vue.js (App.vue) -->
<template>
  <div id="app">
    <pdf-upload-component></pdf-upload-component>
    <chat-component></chat-component>
    <response-component></response-component>
  </div>
</template>

<script>
import PdfUploadComponent from './components/PdfUploadComponent'
import ChatComponent from './components/ChatComponent'
import ResponseComponent from './components/ResponseComponent'

export default {
  name: 'App',
  components: {
    PdfUploadComponent,
    ChatComponent,
    ResponseComponent
  }
}
</script>