<template>
  <div>
    <div id="contentView">
      <b-row class="justify-content-md-center">
        <b-col cols="3">
          <b-button class="btn-danger btn-block" v-on:click="executeScript(1)">
            Reiniciar Raspberry
          </b-button>
        </b-col>
        <b-col style="text-align: left">
          Descripció reiniciar
        </b-col>
      </b-row>
      <b-row class="justify-content-md-center">
        <b-col cols="3">
          <b-button class="btn-danger btn-block" v-on:click="executeScript(2)">
            Apagar Raspberry
          </b-button>
        </b-col>
        <b-col style="text-align: left">
          Descripció apagar
        </b-col>
      </b-row>
      <b-row class="justify-content-md-center">
        <b-col cols="3">
          <b-button class="btn-danger btn-block" v-on:click="executeScript(3)">
            Iniciar Billboard
          </b-button>
        </b-col>
        <b-col style="text-align: left">
          <span class="">Descripció iniciar</span>
        </b-col>
      </b-row>
      <b-row class="justify-content-md-center">
        <b-col cols="3">
          <b-button class="btn-danger btn-block" v-on:click="executeScript(4)">
            Reiniciar Docker
          </b-button>
        </b-col>
        <b-col style="text-align: left">
          Descripció reiniciar docker
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
    import axios from "axios";

    export default {
      name: "Raspberry",
      data() {
        return {

        }
      },
      methods: {
        executeScript(script_mode) {
          let script = ""
          switch (script_mode) {
            case 1:
              script = 'sudo shutdown -r now'
              break
            case 2:
              script = 'sudo shutdown -h'
              break
            case 3:
              script = 'sudo shutdown -h 19:57; cd TFG_Cartellera/; ' +
                'docker-compose up -d ;chromium-browser --kiosk --app=localhost:8000\n'
              break
            case 4:
              script = 'docker-compose stop; docker-compose down; docker-compose up \n'
              break
          }
          axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/script',
            data: {
              script: script,
            },
            auth: { username: this.$route.query.token },
          }).then((res) => {
            alert(res.data.message);
          })
            .catch((error) => {
              alert(error.response.data.message);
            });
          },
      }
    }
</script>

<style scoped>
</style>
