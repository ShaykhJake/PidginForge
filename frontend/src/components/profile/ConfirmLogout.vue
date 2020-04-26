<template>
  <div class="text-center">
    <v-dialog
      v-model="conflogout"
      width="300"
      slot="activator"
      :fullscreen="$vuetify.breakpoint.xsOnly"
    >
      <template v-slot:activator="{ on: dialog }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltip }">
            <v-btn small fab class="primary" v-on="{ ...tooltip, ...dialog }">
              <v-icon class="desertsand--text">logout</v-icon>
            </v-btn>
          </template>
          <span>Logout</span>
        </v-tooltip>
        <!-- <v-btn class="orange" v-on="on">
            <span class="hidden-xs-and-down">Logout</span>
            <v-icon right>logout</v-icon>
        </v-btn> -->
      </template>

      <v-card>
        <v-card-title class="desertsand calligraphy--text" primary-title>
          Confirm Logout?
        </v-card-title>
        <v-card-actions class="sandstone">
          <v-spacer></v-spacer>
          <v-btn class="garbage desertsand--text" @click="finishLogout">
            Yes
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn class="primary desertsand--text" @click="conflogout = false">
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "ConfirmLogout",
  data() {
    return {
      conflogout: false
    };
  },
  methods: {
    finishLogout() {
      let endpoint = `/api/rest-auth/logout/`;
      apiService(endpoint, "POST").then(data => {
        window.location.replace("/accounts/login/");
        console.log(data);
      });
    }
  }
};
</script>
<style scoped></style>
