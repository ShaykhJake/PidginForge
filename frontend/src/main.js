import Vue from "vue";
import vuetify from "@/plugins/vuetify";
import VueYouTube from "vue-youtube";
import router from "./router";
import App from "./App.vue";
import VueGoogleApi from "vue-google-api";
import ProfileSnippet from "@/components/profile/ProfileSnippet.vue";

// import AudioRecorder from 'vue-audio-recorder';
// import lamejs from "@/components/recorder/lame.js";
// import VueHtmlToPaper from "vue-html-to-paper";
// Vuetify's CSS styles
// import "vuetify/dist/vuetify.min.css";
// import store from "./store";

Vue.config.productionTip = false;
Vue.use(vuetify);
Vue.use(VueYouTube);
Vue.component("ProfileSnippet", ProfileSnippet);
// Vue.use(AudioRecorder)

// Vue.use(lamejs, '$lamejs');

// https://www.googleapis.com/youtube/v3/videos?key=AIzaSyCRcV3QD6N6RPlc_fm8LI9ZjWOt4CECj_c&part=snippet&id=T0Jqdjbed40

const config = {
  apiKey: "AIzaSyCRcV3QD6N6RPlc_fm8LI9ZjWOt4CECj_c",
  clientId: "pidginforge2021.apps.googleusercontent.com"
  // scope: 'https://www.googleapis.com/auth/youtube.readonly',
  // discoveryDocs: [ list_of_discoverydocs_urls ]
};
Vue.use(VueGoogleApi, config);

// const htmlToPaperOptions = {
//   name: "_blank",
//   specs: ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"],
//   styles: [
//     "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
//     "https://unpkg.com/kidlat-css/css/kidlat.css"
//   ]
// };
// Vue.use(VueHtmlToPaper, htmlToPaperOptions);

new Vue({
  router,
  // store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
