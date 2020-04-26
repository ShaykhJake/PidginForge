import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
import { apiService } from "@/common/api.service.js";
export default new Vuex.Store({
  state: {
    // userdata: apiService("/api/users/profile/"),
    userdata: {
      user: {
        username: "shaykhjake2",
        userProfile: 1
      },
      biography: "The Shaykh of West Howard rides again!",
      country: "",
      image:
        "https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/2020/02/28/IMG_2469.jpg",
      nativelanguage: {
        name: "English",
        trigraph: "ENG",
        direction: "LTR"
      },
      learninglanguage: [
        {
          name: "English",
          trigraph: "ENG",
          direction: "LTR"
        },
        {
          name: "Arabic-Modern Standard",
          trigraph: "ARB",
          direction: "LTR"
        }
      ],
      learningtopics: [
        {
          name: "health"
        },
        {
          name: "food"
        }
      ],
      points: 0
    },
    bob: "bob"
  },
  getters: {
    getUserStuff: state => state.userdata
    // setUserData: state => {
    //   return state.userdata;
    // }
  },
  mutations: {
    // setUserStuff: state => { state.userdata = apiService("/api/users/profile/");},
    SET_LOADING_STATUS(state, status) {
      state.loadingStatus = status;
    },
    SET_USERDATA(state, userdata) {
      state.userdata = userdata;
    },
    setAge: (state, payload) => {
      const { age, name } = payload;
      const person = state.people.find(p => p.Name === name);
      person.age = age;
    }
  },
  actions: {
    fetchUserData(context) {
      context.commit("SET_LOADING_STATUS", "loading");
      let endpoint = `/api/users/profile/`;
      apiService(endpoint).then(response => {
        context.commit("SET_LOADING_STATUS", "notLoading");
        context.commit("SET_USERDATA", response.data);
      });
    }
  },
  modules: {}
});

// setUserData() {
//   let endpoint = `/api/users/profile/`;
//   this.userdata = apiService(endpoint, "GET");
//   // to.params.previousAnswer = data.body;
//   // to.params.questionSlug = data.question_slug;
// }
