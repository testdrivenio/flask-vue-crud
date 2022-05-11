<template>
<div >
    <br>
    <div style="display: flex">
      <div style="width: 80%; margin: auto; margin-left:1%">
        <vue-good-table style="color: #0032ce;" :selected="enabled" :columns="columns" :rows="usersList"  max-height="300px" :search-options="{enabled: true}" :pagination-options="{enabled: true, perPage: 5,
        nextLabel: 'Següent',
        prevLabel: 'Anterior',
        rowsPerPageLabel: 'elements per pàgina',
        ofLabel: 'de',
        pageLabel: 'pàgina', // for 'pages' mode
        allLabel: 'Tots',}" @on-row-click="onRowClick">
        <template slot="table-row" slot-scope="props">
          <span v-if="props.column.field == 'is_admin'">
          <span v-if="props.row.is_admin === 1">Administrador</span>
          <span v-if="props.row.is_admin === 0">Usuari</span>
          </span>
          <span v-else>
            {{props.formattedRow[props.column.field]}}
          </span>
        </template>
        </vue-good-table>
      </div>
    </div>
    <div style="margin:0 auto;">
      <br>
      <b-button v-if="userIsChoosen" variant="danger" @click="removeAccount">Esborrar l'usuari</b-button>
      <span style="display:inline-block; width:35px;"></span>
      <b-button v-b-modal="modifyUser-modal" v-if="userIsChoosen" variant="outline-primary" @click="updateAccountModal">Modificar l'usuari</b-button>
      <span style="display:inline-block; width:35px;"></span>
      <b-button v-b-modal="addToPlayList-modal" @click="createUser" variant="outline-primary">Crear un usuari nou</b-button>
      <span style="display:inline-block; width:50px;"></span>
      <b-modal id="addUser-modal" hide-footer >
        <label for="inputEmail" style="display: flex; margin-bottom: .5rem;color: #0072ce;">Nom d'usuari:</label>
        <b-form-input id="input-live" v-model="usernameToAdd"  aria-describedby="input-live-help input-live-feedback" trim></b-form-input>
        <label for="inputPassword" style="display: flex; margin-bottom: .5rem;color: #0072ce;">Contrasenya</label>
        <b-form-input type="password" id="input-live-password" v-model="passwordToAdd"  aria-describedby="input-live-help input-live-feedback" trim></b-form-input>
        <br>
        <b-button v-b-modal="addToPlayList-modal" @click="createAccount" variant="outline-primary">Guardar</b-button>
      </b-modal>
      <b-modal id="modifyUser-modal" hide-footer>
        <label for="inputEmail" style="display: flex; margin-bottom: .5rem;color: #0072ce;">Nom d'usuari:(pots deixar-ho en blanc si no el vols canviar)</label>
        <b-form-input id="input-live" v-model="usernameToUpdate"  aria-describedby="input-live-help input-live-feedback" trim></b-form-input>
        <label for="inputPassword" style="display: flex; margin-bottom: .5rem;color: #0072ce;">Contrasenya:(pots deixar-ho en blanc si no el vols canviar)</label>
        <b-form-input type="password" id="input-live-password" v-model="passwordToUpdate"  aria-describedby="input-live-help input-live-feedback" trim></b-form-input>
        <br>
        <b-form-radio-group id="radio-slots" v-model="selected" :options="options" :aria-describedby="ariaDescribedby" name="radio-options-slots"></b-form-radio-group>
        <br>
        <b-button v-b-modal="modifyUser-modal" @click="updateAccount" variant="outline-primary">Guardar</b-button>
      </b-modal>
    </div>
  <br>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignUp',
  /*
      Defines the data used by the component
    */
  data() {
    return {
      previousRow: '',
      timer: '',
      usersList: [],
      userIsChoosen: false,
      selectedUsername: '',
      usernameToAdd: '',
      passwordToAdd: '',
      usernameToUpdate: '',
      passwordToUpdate: '',
      logged: false,
      columns: [
        {
          label: 'Usuari',
          field: 'username',
        },
        {
          label: 'Privilegis',
          field: 'is_admin',
        },
      ],
      selected: '',
      options: [
        { text: 'Usuari', value: 0 },
        { text: 'Administrador', value: 1 },
      ],
    };
  },
  created() {
    this.getAccounts();
    // this.timer = setInterval(this.getAccounts, 5000)
  },
  methods: {
    createUser() {
      this.$root.$emit('bv::show::modal', 'addUser-modal');
    },
    updateAccountModal() {
      this.$root.$emit('bv::show::modal', 'modifyUser-modal');
    },
    createAccount() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:80/account',
        data: {
          username: this.usernameToAdd,
          password: this.passwordToAdd,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        console.log(res);
        this.getAccounts();
        this.$root.$emit('bv::hide::modal', 'addUser-modal');
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    updateAccount() {
      /*
      var data = {}
      if (this.usernameToUpdate !== '') {
        args['username'] = this.usernameToUpdate
      }
      if (this.passwordToUpdate !== '') {
        args['password'] = this.passwordToUpdate
      }
      axios({
        method: 'put',
        url: 'http://127.0.0.1:80/account/' + this.selectedUsername,
        data: {
          // username: this.usernameToUpdate,
          // password: this.passwordToUpdate,
          args,
          is_admin: this.selected
        },
        auth: {username: this.$route.query.token}
      }).then((res) => {
        console.log(res)
        this.getAccounts()
        this.$root.$emit('bv::hide::modal', 'modifyUser-modal')
      })
        .catch(error => {
          alert(error.response.data.message)
        })
      */
      const data2 = {};
      if (this.usernameToUpdate !== '') {
        data2.username = this.usernameToUpdate;
      }
      if (this.passwordToUpdate !== '') {
        data2.password = this.passwordToUpdate;
      }
      data2.is_admin = this.selected;
      axios({
        method: 'put',
        url: `http://127.0.0.1:80/account/${this.selectedUsername}`,
        data: data2,
        auth: { username: this.$route.query.token },
      }).then((res) => {
        console.log(res);
        this.getAccounts();
        if (this.previousRow !== '') {
          this.previousRow.event.target.parentElement.bgColor = '';
          this.userIsChoosen = false;
        }
        this.usernameToUpdate = '';
        this.passwordToUpdate = '';
        if (this.$route.query.username === this.selectedUsername) {
          this.$router.replace({ path: '/', query: { username: this.usernameToUpdate, token: this.$route.query.token } });
        }
        this.$root.$emit('bv::hide::modal', 'modifyUser-modal');
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    removeAccount() {
      if (this.previousRow !== '') {
        this.previousRow.event.target.parentElement.bgColor = '';
        this.userIsChoosen = false;
      }
      if (this.$route.query.username !== this.selectedUsername) {
        axios({
          method: 'delete',
          url: `http://127.0.0.1:80/account/${this.selectedUsername}`,
          auth: { username: this.$route.query.token },
        }).then((res) => {
          console.log(res);
          this.getAccounts();
        })
          .catch((error) => {
            alert(error.response.data.message);
          });
      } else {
        alert('No pots esborrar el teu propi usuari!');
      }
    },
    onRowClick(params) {
      console.log(this.imageSource);
      this.selectedUsername = params.row.username;
      this.userIsChoosen = true;
      params.event.target.parentElement.bgColor = '#f1f5fd';
      if (this.previousRow === '') {
        this.previousRow = params;
      } else {
        this.previousRow.event.target.parentElement.bgColor = '';
        this.previousRow = params;
      }
      this.getAccount();
    },
    getAccounts() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = 'http://127.0.0.1:80/accounts';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          this.usersList = res.data.accounts;
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    getAccount() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = `http://127.0.0.1:80/account/${this.selectedUsername}`;
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          this.selected = res.data.account.is_admin;
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
  },
};
</script>
