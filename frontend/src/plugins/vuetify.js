// import "@mdi/font/css/materialdesignicons.css";
import Vue from "vue";
import Vuetify from "vuetify/lib";
import "vuetify/dist/vuetify.min.css";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    light: true,
    themes: {
      light: {
        // primary: "#E89F1F",
        primary: "#e08903",
        secondary: "#accfd4",
        accent: "#8e2501",
        elements: "#8e2501",
        saves: "#0a2572",

        languages: "#8e2501",
        topics: "#39a9ab",
        tags: "#0a2572",
        error: "#b71c1c",
        warning: "#ffd600",
        success: "#2e7d32",
        info: "#0277bd",
        garbage: "#1b1b1e",

        // Backgrounds
        sandstone: "#dbd4c4",
        desertsand: "#faf5e2",
        // desertsand: "#f9f9f9",
        calligraphy: "#66665e",

        // Titles
        titlebar: "dbd4c4",
        appBar: "#494942",

        // Texts
        textColor: "#66665e",
        text: "#66665e"
        // titlebar: "#FAF5E2",

        // ,
      },
      dark: {
        primary: "#e08903",

        secondary: "#accfd4",
        topics: "#ACCFD4",

        accent: "#8E2501",
        elements: "#8E2501",

        saves: "#0A2572",

        languages: "#C2DEF4",
        tags: "#0A2572",

        error: "#B71C1C",
        warning: "#FFD600",
        success: "#2E7D32",
        info: "#0277BD",
        garbage: "#1b1b1e",

        // Customs & Overrides

        desertSand: "#FAF5E2",
        calligraphyGrey: "#66665E",
        textColor: "#66665E",
        // titlebar: "#494942",
        // appBar: "#494942",
        // cardback: "#33332c",
        cards: "#33332c",
        background: "#1c1c15"
        // ,
      }
    }
  },
  icons: {
    iconfont: "mdi"
  }
});
