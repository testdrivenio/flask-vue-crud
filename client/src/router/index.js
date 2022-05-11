import Vue from 'vue';
import Router from 'vue-router';
import Panel from '../components/Panel.vue';
import ContentUpload from '../components/ContentUpload.vue';
import Content from '../components/Content.vue';
import Playlist from '../components/Playlist.vue';
import Login from '../components/Login.vue';
import LogOut from '../components/LogOut.vue';
import SignUp from '../components/SignUp.vue';
import SwitchStatus from '../components/SwitchStatus.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Panel',
      component: Panel,
    }, {
      path: '/',
      name: 'Content',
      component: Content,
    }, {
      path: '/',
      name: 'ContentUpload',
      component: ContentUpload,
    }, {
      path: '/',
      name: 'Playlist',
      component: Playlist,
    }, {
      path: '/',
      name: 'Login',
      component: Login,
    }, {
      path: '/',
      name: 'LogOut',
      component: LogOut,
    }, {
      path: '/',
      name: 'SignUp',
      component: SignUp,
    }, {
      path: '/',
      name: 'SwitchStatus',
      component: SwitchStatus,
    },
  ],
});
