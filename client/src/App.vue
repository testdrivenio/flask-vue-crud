<template>
  <div id="app" style="height:983px;">
    <div align="left">
      <b-button style="color:white;" variant="link"
                @click="showAbout" >Sobre aquesta aplicació</b-button>
      <b-modal id="about-modal" hide-footer>
        <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">
          Projecte desenvolupat com a Treball de Final de Grau d'Enginyeria Informàtica
          (Universitat de Barcelona)
        </label>
        <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">Llicència: GPL 3</label>
        <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">
          © Francina Pons Llabrés 2022</label>
        <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">
          Contacte: fponsllabres@gmail.com</label>
        <b-link href="https://github.com/francinaPons" style="display: flex; margin-bottom: .5rem;color: #0072ce;" >Github</b-link>
      </b-modal>
    </div>
    <br>
    <h1>Gestió de la cartellera</h1>
    <router-view/>
    <v-footer>
      <img src="../static/logo_ub(1).png" width="300" height="100">
      <span style="display:inline-block; width:1080px;"></span>
      <img src="../static/crai_logo_unatinta_blanc.png" width="300" height="100">
    </v-footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    showAbout() {
      this.$root.$emit('bv::show::modal', 'about-modal');
    },
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fafafa;
  background-color: #0072ce;
}

</style>
