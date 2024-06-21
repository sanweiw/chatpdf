<template>
  <div>
    <!-- 假设responses是包含所有响应的数组 -->
    <div v-for="(response, index) in responses" :key="index">
      {{ response }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResponseComponent',
  data() {
    return {
      responses: [], // 这里将存储从后端接收到的响应
    };
  }
}
</script>