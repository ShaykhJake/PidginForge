<template>
  <div class="text-center">
    <v-dialog
      v-model="showDialog"
      width="300"
      slot="activator"
      :fullscreen="$vuetify.breakpoint.xsOnly"
    >
      <v-card>
        <v-card-title class="desertsand calligraphy--text" primary-title>
          Confirm Logout?
        </v-card-title>
        <v-card-actions class="sandstone">
          <div align="center">
            <v-btn
              class="garbage desertsand--text mr-2"
              @click="$emit('closeDialog')"
            >
              Cancel<v-icon right>mdi-cancel</v-icon>
            </v-btn>
            <v-btn class="primary desertsand--text" @click="finishLogout">
              Logout<v-icon right>mdi-exit-run</v-icon>
            </v-btn>
          </div>
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
  props: {
    showDialog: Boolean
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
