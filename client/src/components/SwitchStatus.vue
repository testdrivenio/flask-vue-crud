<template>
<div >
    <div>
      <h1>Mode manteniment:</h1>
      <br>
      <b-button  v-if="activated" variant="outline-primary" @click="switchStatus">Desactivar</b-button>
      <b-button  v-if="!activated" variant="danger" @click="switchStatus">Activar</b-button>
    </div>
    <br>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SwitchStatus',
  /*
      Defines the data used by the component
    */
  created() {
    this.getStatus();
  },
  methods: {
    switchStatus() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/status',
        data: {
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        this.activated = !this.activated;
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    getStatus() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = 'http://127.0.0.1:8000/status';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          const mode = res.data.message;
          if (mode === 'stop') {
            this.activated = true;
          } else {
            this.selected = false;
          }
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
  },
  data() {
    return {
      activated: false,
    };
  },
};
</script>
