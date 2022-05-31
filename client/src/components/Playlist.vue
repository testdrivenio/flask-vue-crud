<template>
  <div>
    <div id="contentView" v-if="seenContent">
      <br>
      <div class="col-3">
        Mode de reproducció
        <div style="">
                <b-form-select :options="options" style="margin-left:1%; width: 150px;"
                               v-model="selected"
                               v-on:change="changeMode"></b-form-select>
                <span style="display:inline-block; width:560px;" v-if="!fileIsChoosen"></span>
                <span style="display:inline-block; width:460px;" v-if="fileIsChoosen"></span>
                <div class="mt-3" v-if="selected === 'inter' || selected === 'rndm-inter' ">
                  Fitxer intercalat:
                  {{ intercalatedFile }}
                </div>
                <br>
                <br>
              </div>
      </div>
      <div class="row">
        <div class="col-3">
          <b>Playlists disponibles:</b>
          <b-list-group class="list-group">
            <b-list-group-item v-for="item in playlists" :key="item"
              class="list-group-item"
              @click="updatePlaylist(item)">
              {{ item.name }}
            </b-list-group-item>
          </b-list-group>
          <!--<div style="cursor: pointer" v-for="item in playlists"
               v-bind:key="item" @click="updatePlaylist(item)">
            - {{ item.name }}
          </div>-->
        </div>
        <div class="col-9">
          <div style="">
            <div style="max-width: 90%;"
                 v-if="selected !== 'rndm' && selected !== 'rndm-inter'">
              <vue-good-table :columns="columns" :pagination-options="{enabled: true, perPage: 25,
        nextLabel: 'Següent',
        prevLabel: 'Anterior',
        rowsPerPageLabel: 'elements per pàgina',
        ofLabel: 'de',
        pageLabel: 'pàgina', // for 'pages' mode
        allLabel: 'Tots',}" :rows="files" :search-options="{enabled: true}"
                              :selected="enabled"
                              @on-row-click="onRowClick" max-height="300px" style="color: #0032ce;">
                <template slot="table-row" slot-scope="props">
          <span v-if="props.column.field === 'duration'">
          <span v-if="props.row.duration !== null">{{props.row.duration/1000}}</span>
          </span>
                  <span v-else>
            {{props.formattedRow[props.column.field]}}
          </span>
                </template>
              </vue-good-table>
            </div>
            <div style="width: 90%; margin: auto auto auto 1%;"
                 v-if="selected === 'rndm' || selected === 'rndm-inter'">
              <vue-good-table :columns="columnsRandom"
                              :pagination-options="{enabled: true, perPage: 25,
                              nextLabel: 'Següent',
                              prevLabel: 'Anterior',
                              rowsPerPageLabel: 'elements per pàgina',
                              ofLabel: 'de',
                              pageLabel: 'pàgina', // for 'pages' mode
                              allLabel: 'Tots',}" :rows="files" :search-options="{enabled: true}"
                              :selected="enabled" @on-row-click="onRowClick"
                              max-height="300px" style="color: #0032ce;">
                <template slot="table-row" slot-scope="props">
          <span v-if="props.column.field === 'duration'">
          <span v-if="props.row.duration !== null">{{props.row.duration/1000}}</span>
          </span>
                  <span v-if="props.column.field === 'played'">
          <span v-if="props.row.played === 1">{{"Si"}}</span>
          <span v-if="props.row.played === 0">{{"En Cua"}}</span>
          </span>
                  <span v-if="props.column.field !== 'duration'
                  && props.column.field !== 'played' ">
            {{ props.formattedRow[props.column.field] }}
          </span>
                </template>
              </vue-good-table>
            </div>
            <div>
              <span style="display:inline-block; width:50px;"></span>
              <b-img alt="Image 1" fluid height="200" thumbnail
                     v-bind:src=imageSource v-if="fileIsChoosen"
                     width="300"></b-img>
            </div>
          </div>
          <div class="row">
        <div class="col">
           <b-button @click="removeAllFiles" v-if="files.length" variant="danger">
             Buidar la llista</b-button>
        </div>
        <div class="col">
          <b-button v-b-modal.modal-center>Guardar Playlist</b-button>
        </div>
      </div>
        </div>
      </div>
        <br>
        <div>
          <b-modal @hidden="resetModal" @ok="handleOk"
                   @show="resetModal"
                   centered
                   id="modal-center"
                   title="Guardar Playlist">
            <b-form-group
              class="my-4"
              id="fieldset-1"
              label="Com vols anomenar aquesta playlist?"
              label-for="input-1"
            >
              <b-form-input id="input-1" v-model="playlist_name"></b-form-input>
            </b-form-group>
            <b-form-group
              class="my-4"
              id="fieldset-2"
              label="Introdueix els tags de la playlist"
              label-for="input-2"
            >
                <vue-taggable-select
                v-model="tags"
                placeholder="Introdueix tags"
                :taggable="true"
                :options="tags"
                ></vue-taggable-select>
            </b-form-group>
            <!--<p class="my-4">Com vols anomenar aquesta playlist?</p>
            <b-form-input v-model="playlist_name" placeholder=""></b-form-input>-->
          </b-modal>
        <span style="display:inline-block; width:950px;" v-if="!fileIsChoosen"></span>
        <span style="display:inline-block; width:450px;"
              v-if="fileIsChoosen && (selected !== 'inter' && selected !== 'rndm-inter')"></span>
        <span style="display:inline-block; width:150px;"
              v-if="fileIsChoosen && (selected === 'inter' || selected !== 'rndm-inter')"></span>
        <b-button @click="removeFile" v-if="fileIsChoosen" variant="danger">
          Esborrar de la llista</b-button>
        <span style="display:inline-block; width:35px;"></span>
        <b-button @click="playNext" v-b-modal="addToPlayList-modal"
                  v-if="fileIsChoosen" variant="outline-primary">
          Reproduir després
        </b-button>
        <span style="display:inline-block; width:50px;"></span>
        <b-button @click="setIntercalated"
                  v-b-modal="addToPlayList-modal"
                  v-if="fileIsChoosen && (selected === 'inter' || selected === 'rndm-inter')"
                  variant="outline-primary">
          Seleccionar com a
          fitxer intercalat
        </b-button>
        <span style="display:inline-block; width:50px;"></span>
      </div>
    </div>
    <br>
  </div>
</template>

<script>
/* eslint-disable no-alert, no-console */
import axios from 'axios';

export default {
  name: 'Playlist',
  created() {
    this.getFiles();
    this.getTags();
    this.timer = setInterval(this.getFiles, 1000);
    this.mode = this.getMode();
    this.intercalatedFile = this.getIntercalatedFile();
    this.getPlaylists();
  },
  destroy() {
    clearInterval(this.timer);
  },
  data() {
    return {
      enabled: false,
      videosType: ['.mp4', '.mkv', '.m4v', '.flv', '.webm', '.ogg'],
      previousRow: '',
      timer: '',
      files: [],
      seenContent: true,
      fileIsChoosen: false,
      intercalatedFile: '',
      imageSource: null,
      urlRPI: 'http://127.0.0.1:80/content',
      selectedFileName: 0,
      duration: 0,
      columns: [
        {
          label: 'Nom',
          field: 'name',
        },
        {
          label: 'Tipus',
          field: 'type',
        },
        {
          label: 'Durada en segons (només Imatges)',
          field: 'duration',
          type: 'number',
        },
      ],
      columnsRandom: [
        {
          label: 'Nom',
          field: 'name',
        },
        {
          label: 'Tipus',
          field: 'type',
        },
        {
          label: 'Durada en segons (només Imatges)',
          field: 'duration',
          type: 'number',
        },
        {
          label: 'Reproduït',
          field: 'played',
        },
      ],
      selected: null,
      options: [
        { value: null, text: 'Seqüencial' },
        { value: 'inter', text: 'Intercalat' },
        { value: 'rndm', text: 'Aleatori' },
        { value: 'rndm-inter', text: 'Aleatori-Intercalat' },
      ],
      playlist_name: '',
      tags: [],
      playlists: [],
    };
  },
  methods: {
    previewFile(path) {
      console.log('path:');
      console.log(path);
      this.imageSource = `/thumbnail/${path}`;
      // console.log(this.imageSource);
    },
    playNext() {
      const fileName = this.selectedFileName;
      const extension = fileName.substring(fileName.lastIndexOf('.'));
      if (this.videosType.includes(extension)) {
        this.setNext(fileName, this.duration, 'video');
      } else {
        let inputDuration;
        inputDuration = prompt(`${fileName}\n Afegir durada en segons: `);
        if (inputDuration === null) {
          inputDuration = 0;
        }
        // eslint-disable-next-line radix
        this.setNext(fileName, parseInt(inputDuration), 'Image');
      }
    },
    setIntercalated() {
      const fileName = this.selectedFileName;
      const extension = fileName.substring(fileName.lastIndexOf('.'));
      if (this.videosType.includes(extension)) {
        this.setIntercalatedAXIOS(fileName, this.duration, 'video');
      } else {
        let inputDuration;
        inputDuration = prompt(`${fileName}\n Afegir durada en segons: `);
        if (inputDuration === null) {
          inputDuration = 0;
        }
        // eslint-disable-next-line radix
        this.setIntercalatedAXIOS(fileName, parseInt(inputDuration), 'Image');
      }
    },
    setNext(fname, fduration, ftype) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/nextEntry',
        data: {
          name: fname,
          duration: fduration * 1000,
          type: ftype,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert(res.data.message);
      })
        .catch((error) => {
          // eslint-disable-next-line no-alert
          alert(error.response.data.message);
        });
    },
    setIntercalatedAXIOS(fname, fduration, ftype) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/intercalatedEntry',
        data: {
          name: fname,
          duration: fduration * 1000,
          type: ftype,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert(res.data.message);
        this.getIntercalatedFile();
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    handleOk() {
      // Trigger submit handler
      console.log(this.tags);
      this.savePlaylist();
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing');
      });
      this.resetModal();
    },
    resetModal() {
      this.name = '';
    },
    savePlaylist() {
      console.log(this.files);
      axios({
        method: 'post',
        url: 'http://127.0.0.1:80/savePlaylist',
        data: {
          playlist_name: this.playlist_name,
          files: this.files,
          tags: this.tags,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert(res.data.message);
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    removeFile() {
      // var id = key + 1
      this.removeFileREQUEST(this.selectedFileName);
    },
    removeAllFiles() {
      let i = 0;
      this.removeIntercalatedREQUEST();
      this.intercalatedFile = 'default.mp4';
      for (i; i < this.files.length; i += 1) {
        this.removeFileREQUEST(this.files[i].name);
      }
      setTimeout(() => this.getFiles(), 2000);
    },
    removeFileREQUEST(fName) {
      if (this.previousRow !== '') {
        this.previousRow.event.target.parentElement.bgColor = '';
      }
      if (this.intercalatedFile === fName) {
        this.removeIntercalatedREQUEST();
        this.intercalatedFile = 'default.mp4';
      }
      const path = `${'http://127.0.0.1:8000/playlistEntry/'}${fName}`;
      axios.delete(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          console.log(res);
          this.getFiles();
          this.fileIsChoosen = false;
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    removeIntercalatedREQUEST() {
      const path = 'http://127.0.0.1:8000/intercalatedEntry';
      axios.delete(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          console.log(res);
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    onRowClick(params) {
      this.imageSource = `/thumbnail/${params.row.name}`;
      this.selectedFileName = params.row.name;
      this.fileIsChoosen = true;
      // eslint-disable-next-line no-param-reassign
      params.event.target.parentElement.bgColor = '#f1f5fd';
      if (this.previousRow === '') {
        this.previousRow = params;
      } else {
        this.previousRow.event.target.parentElement.bgColor = '';
        this.previousRow = params;
      }
    },
    getFiles() {
      if (Object.keys(this.$route.query.token).length !== 0) {
        const path = 'http://127.0.0.1:80/playlist';
        axios.get(path, { auth: { username: this.$route.query.token } })
          .then((res) => {
            this.files = res.data.Playlist;
          })
          .catch((error) => {
            console.log(error.response.data.message);
            if (error.response.data.message === 'La sessió ha caducat, inicia sessió de nou') {
              alert('La sessió ha caducat. Introdueix les teves credencials un altre cop');
              this.$router.replace({ path: '/' });
              this.$root.$emit('login', false);
              clearInterval(this.timer);
            }
          });
      }
    },
    getTags() {
      const path = 'http://127.0.0.1:80/tags';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          console.log(res.data.tags);
          for (let i = 0; i < res.data.tags.length; i += 1) {
            console.log(res.data.tags[i]);
            this.tags.push(res.data.tags[i].name);
          }
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    getMode() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = 'http://127.0.0.1:8000/mode';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          const mode = res.data.message;
          if (mode === 'seq') {
            this.selected = null;
          } else {
            this.selected = mode;
          }
          // this.changeTable()
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    changeMode() {
      let m = this.selected;
      if (this.selected === null) {
        m = 'seq';
      }
      axios({
        method: 'put',
        url: 'http://127.0.0.1:8000/mode',
        data: {
          mode: m,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        console(res.data.message);
        this.getIntercalatedFile();
        // this.changeTable()
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    changeTable() {
      if (this.selected === 'rndm') {
        this.columns = [
          {
            label: 'Nom',
            field: 'name',
          },
          {
            label: 'Tipus',
            field: 'type',
          },
          {
            label: 'Durada en segons (només Imatges)',
            field: 'duration',
            type: 'number',
          },
          {
            label: 'Reproduït',
            field: 'played',
          },
        ];
      } else {
        this.columns = [
          {
            label: 'Nom',
            field: 'name',
          },
          {
            label: 'Tipus',
            field: 'type',
          },
          {
            label: 'Durada en segons (només Imatges)',
            field: 'duration',
            type: 'number',
          },
        ];
      }
    },
    getIntercalatedFile() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = 'http://127.0.0.1:8000/intercalatedEntry';
      axios.get(path)
        .then((res) => {
          this.intercalatedFile = res.data.metadata.path;
          this.intercalatedFile = this.intercalatedFile.substring(this.intercalatedFile.lastIndexOf('/'));
          this.intercalatedFile = this.intercalatedFile.substring(1);
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    methodUpload() {
      this.seenContent = !this.seenContent;
      this.getFiles();
    },
    updatePlaylist(playlist) {
      console.log(this.items);
      // const obj = arr.find(({ data }) => data === name);
      // console.log(obj);
      /* for (let i = 0; i < this.playlists.length; i += 1) {
        if (this.playlists[i].name === playlist.name) {
          console.log(this.playlists[i]);
        }
      } */
      this.items = playlist.items;
      console.log(this.items);
    },
    getPlaylists() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:80/playlistslist',
        auth: { username: this.$route.query.token },
      }).then((res) => {
        console.log(res.data.playlists);
        for (let i = 0; i < res.data.playlists.length; i += 1) {
          console.log(res.data.playlists[i]);
          this.playlists.push(res.data.playlists[i]);
        }
        console.log(res.data.playlists);
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
  },

};
/* eslint-enable no-alert, no-console */
</script>
<style scoped>
  .list-group{
    max-height: 75%;
    overflow:scroll;
    -webkit-overflow-scrolling: touch;
    cursor: pointer;
  }
</style>
