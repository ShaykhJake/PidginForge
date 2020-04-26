import Vue from "vue";
import vuetify from '@/plugins/vuetify'
import VueYouTube from "vue-youtube";
import router from "./router";
import App from "./App.vue";
import VueGoogleApi from "vue-google-api";
// Vuetify's CSS styles
// import "vuetify/dist/vuetify.min.css";
// import store from "./store";

Vue.config.productionTip = false;
Vue.use(vuetify);
Vue.use(VueYouTube);

const config = {
  apiKey: "AIzaSyCvx0EIEVg3PdfgZKJaZbvWTpJ82MIFiTM",
  clientId: "pidginforge-youtube.apps.googleusercontent.com"
  // scope: 'space_separated_scopes',
  // discoveryDocs: [ list_of_discoverydocs_urls ]
};

Vue.use(VueGoogleApi, config);

new Vue({
  router,
  // store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
