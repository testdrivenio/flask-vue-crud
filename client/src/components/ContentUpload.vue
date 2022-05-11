<template>
  <div class="contentUploadDiv">
    <br>
    <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" class="dropzone dz-clickable" @vdropzone-complete="afterComplete" @vdropzone-complete-multiple="afterCompleteAll"></vue-dropzone>
    <br>
    <b-button v-on:click="sendFiles()" variant="outline-primary">Enviar tots els fitxers</b-button>
    <b-button  @click="removeAllFiles" variant="outline-primary">Esborrar tots els fitxers</b-button>
  </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';
// import axios from 'axios'
export default {
  name: 'ContentUpload',
  components: {
    vueDropzone: vue2Dropzone,
  },
  /*
      Defines the data used by the component
    */
  data() {
    return {
      files: [],
      uploadPercentage: 0,
      dropzoneOptions: {
        dictDefaultMessage: 'Arrosega aquí els fitxers',
        autoProcessQueue: false,
        addRemoveLinks: true,
        paramName: 'file',
        thumbnailWidth: 150,
        chunking: true,
        forceChunking: true,
        url: 'http://127.0.0.1:80/content',
        maxFilesize: 10025, // megabytes
        chunkSize: 1000000, // bytes
      },
    };
  },
  methods: {
    afterComplete(file) {
      if (file.status !== 'success') {
        alert(`Hi ha hagut un problema al enviar el fitxer ${file.name}`);
      }
    },
    afterCompleteAll() {
      alert('Els fitxers s"han enviat correctament');
    },
    removeAllFiles() {
      this.$refs.myVueDropzone.removeAllFiles();
    },
    sendFiles() {
      this.$refs.myVueDropzone.processQueue();
    },
    /*
      Adds a file
    */
    addFiles() {
      this.$refs.files.click();
    },
    /*
      Submits the file to the server
      */
  },
};
</script>
