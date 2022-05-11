<template>
  <div id="login">
    <div id="loginDiv" style="padding:15px; border-radius:6px; display: inline-block; width:400px;">
    <br>
    <h5 style="font-weight: bold;color: #0072ce;">Inicia sessió</h5>
    <br>
    <div class="form-label-group">
      <label  style="display: flex; margin-bottom: .5rem;color: #0072ce;">Nom d'usuari:</label>
      <input type="username" id="inputUsername"
             class="form-control" placeholder="Nom d'usuari" required v-model="username">
    </div>

    <div class="form-label-group">
      <br>
      <br>
      <label for="inputPassword" style="display: flex; margin-bottom: .5rem;color: #0072ce;">
        Contrasenya:</label>
      <input type="password" id="inputPassword"
             class="form-control" placeholder="Contrasenya" required v-model="password">
    </div>
    <br>
    <div style="margin:0 auto;">
      <br>
      <b-button style="width: 40%;" @click="checkLogin"
                variant="outline-primary">Iniciar Sessió</b-button>
    </div>
    <br>
  </div>
    <b-modal ref="addRegisterModal" id="modal-Register-User" title="Create Account" hide-footer>
      <b-form @submit="submitUserRegister" @reset="onResetRegister" v-if="show">

        <b-form-group id="input-register-group-1" label="Username:" label-for="input-register-1">
              <b-form-input id="input-artist-1" v-model="addUserForm.username"
                            type="username" required placeholder="Enter username"></b-form-input>
        </b-form-group>

        <b-form-group id="input-register-group-2" label="Password:" label-for="input-register-1">
              <b-form-input id="input-register-2" v-model="addUserForm.password"
                            type="password" required placeholder="Enter password"></b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      is_admin: -1,
      logged: '',
      token: '',
      show: true,
      addUserForm: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    initForm() {
      this.addUserForm.username = '';
      this.addUserForm.password = '';
    },
    submitUserRegister(evt) {
      evt.preventDefault();
      this.$refs.addRegisterModal.hide();
      const parameters = {
        username: this.addUserForm.username,
        password: this.addUserForm.password,
      };
      const path = 'http://127.0.0.1:80/account';
      axios
        .post(path, parameters)
        .then(() => {
          this.logged = true;
          this.find_match = true;
          this.initForm();
          alert('User registered');
        })
        .catch((error) => {
          // eslint-disable-next-line
          alert(error.response.data.message)
        });
    },
    onResetRegister(evt) {
      evt.preventDefault();
      this.initForm();
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    checkLogin() {
      const parameters = {
        username: this.username,
        password: this.password,
      };
      const path = 'http://127.0.0.1:80/login';
      axios
        .post(path, parameters)
        .then((res) => {
          console.log(res);
          this.logged = true;
          this.token = res.data.token;
          this.find_match = true;
          this.getAccount();
        })
        .catch((error) => {
          // eslint-disable-next-line
          alert(error.response.data.message)
        });
    },
    getAccount() {
      const path = `http://127.0.0.1:80/account/${this.username}`;
      axios.get(path)
        .then((res) => {
          this.username = res.data.account.username;
          this.is_admin = res.data.account.is_admin;
          this.$router.replace({ path: '/', query: { username: this.username, token: this.token } });
          this.$parent.$refs.logged = true;
          this.$root.$emit('login', true);
          this.$root.$emit('is_admin', this.is_admin === 1);
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    registerViewForm() {
      this.$refs.addRegisterModal.show();
    },
  },
};
</script>
