import Vue from "vue";
import VueRouter from "vue-router";
import AnswerEditor from "../views/AnswerEditor.vue";
import Home from "../views/Home.vue";
import NotFound from "../views/NotFound.vue";
import QuestionViewer from "../views/QuestionViewer.vue";
// import YouTubeViewer from "../views/YouTubeViewer.vue";
// import AudioViewer from "../views/AudioViewer.vue";
import MediaElementViewer from "../views/MediaElementViewer.vue";
import TextElementViewer from "../views/TextElementViewer.vue";
import Curate from "../views/Curate.vue";
import Learn from "../views/Learn.vue";

Vue.use(VueRouter);

export default new VueRouter({
  // TODO Enable history mode later when going to production
  // mode: "history",
  // base: process.env.BASE_URL,
  routes: [
    {
      path: "/curate",
      name: "Curate",
      component: Curate
    },
    {
      // TODO - Should figure out how to show different content based on authenticated or anonymous
      path: "/learn",
      name: "Learn",
      component: Learn
    },
    {
      // TODO - Should figure out how to show different content based on authenticated or anonymous
      path: "/collaborate",
      name: "Collaborate",
      // Change 'Home' to collaborate once that component/view has actually been built
      component: Home
    },
    {
      path: "/questions/:slug",
      name: "Question-Viewer",
      component: QuestionViewer,
      props: true
    },
    {
      path: "/answer/:id",
      name: "Answer-Editor",
      component: AnswerEditor,
      props: true
    },
    {
      path: "/media/:elementtype/:elementslug",
      name: "Media-Viewer",
      component: MediaElementViewer,
      props: true
    },
    {
      path: "/text/:elementslug",
      name: "Text-Viewer",
      component: TextElementViewer,
      props: true
    },
    {
      path: "/",
      name: "Home",
      component: Home
    },

    {
      path: "*",
      name: "page-not-found",
      component: NotFound
    }
  ]
});

// const routes = [
//   {
//     path: "/",
//     name: "Home",
//     component: Home
//   },
//   {
//     path: "/about",
//     name: "About",
//     // route level code-splitting
//     // this generates a separate chunk (about.[hash].js) for this route
//     // which is lazy-loaded when the route is visited.
//     component: () =>
//       import(/* webpackChunkName: "about" */ "../views/About.vue")
//   }
// ];
