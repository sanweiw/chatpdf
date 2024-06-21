<template>
  <div>
    <input type="file" @change="uploadPDF" />
  </div>
</template>

<script>
export default {
  name: 'PdfUploadComponent',
  methods: {
    uploadPDF(event) {
      const file = event.target.files[0];
      if (!file) {
        console.error('No file selected.');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      fetch('http://localhost:5000/upload', { // 确保这个URL匹配你的后端接口
        method: 'POST',
        body: formData,
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    }
  }
}
</script>