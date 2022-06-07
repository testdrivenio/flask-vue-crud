<template>
<div>
  <div class="container" style=" background-color:white; color:#0072ce; border-radius: 6px;  margin-top: 2%; padding-right: 0px; padding-left: 0px;" v-if="logged">
    <b-tabs content-class="mt-3">
      <b-tab title="Contingut">
        <Content></Content>
      </b-tab>
      <b-tab title="Llista de reproducció" active>
        <Playlist></Playlist>
      </b-tab>
      <b-tab title="Gestionar usuaris" v-if="is_admin">
        <SignUp></SignUp>
      </b-tab>
      <b-tab title="Mode de Manteniment">
        <SwitchStatus></SwitchStatus>
      </b-tab>
      <b-tab title="Configuració Raspberry">
        <Raspberry></Raspberry>
      </b-tab>
      <b-tab title="Tancar la sessió">
        <LogOut></LogOut>
      </b-tab>
    </b-tabs>
  </div>
  <div class="container" style="background-color:white; color:#0072ce; border-radius: 6px; padding: 5%" v-if="!logged" >
    <Login></Login>
  </div>
</div>
</template>

<script>
import Content from './Content.vue';
import Playlist from './Playlist.vue';
import Login from './Login.vue';
import LogOut from './LogOut.vue';
import SignUp from './SignUp.vue';
import SwitchStatus from './SwitchStatus.vue';
import Raspberry from "./Raspberry";

export default {
  name: 'Panel',
  components: {
    Raspberry,
    Content,
    Playlist,
    Login,
    LogOut,
    SignUp,
    SwitchStatus,
  },
  created() {
    this.logged = false;
    this.token = this.$route.query.token;
    if (this.logged === undefined) {
      this.logged = false;
    }
    this.$root.$on('login', (loginState) => {
      this.logged = loginState;
    });
    this.$root.$on('is_admin', (adm) => {
      this.is_admin = adm;
    });
    // setInterval(this.methodLogOut, 3600000)
  },
  data() {
    return {
      seenUpload: false,
      seenContentList: false,
      seenRestart: false,
      logged: false,
      is_admin: false,
    };
  },
};
</script>
