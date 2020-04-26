<template>
  <v-row justify="center" class="ma-0">
    <v-dialog v-model="changeUsernameDialog" persistent max-width="320px">
      <template v-slot:activator="{ on: changeUsernameDialog }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltip }">
            <v-btn
              small
              fab
              class="orange lighten-4"
              v-on="{ ...tooltip, ...changeUsernameDialog }"
            >
              <v-icon>edit</v-icon>
            </v-btn>
          </template>
          <span>Change Username</span>
        </v-tooltip>
      </template>
      <v-card class="ma-0">
        <v-card-title class="pb-1 grey darken-4 white--text">
          Change Username
        </v-card-title>
        <v-card-text class="pa-1 grey lighten-4">
          <v-container class="pa-1" fluid grid-list-md>
            <v-row wrap dense>
              <v-col cols="12">
                <p>Current username: {{ currentUsername }}</p>
                <v-form
                  ref="form"
                  v-model="valid"
                  :hidden="success || thinking"
                >
                  <v-text-field
                    v-model="username1"
                    :rules="[rules.required, rules.nospace]"
                    name="input-10-1"
                    hint=""
                    autofocus
                    label="New Username"
                    @focus="
                      available = false;
                      error = false;
                    "
                  ></v-text-field>
                  <v-text-field
                    v-model="username2"
                    :rules="[rules.required, rules.usernameMatch]"
                    name="input-10-2"
                    label="Confirm New Username"
                    value=""
                    class="input-group--focused"
                  ></v-text-field>
                </v-form>
                <v-alert :value="error" dense type="error"
                  >That username is already in use</v-alert
                >
                <v-alert :value="changeerror" dense type="error">{{
                  changeErrorMessage
                }}</v-alert>
                <v-alert :value="available" dense type="info"
                  >Username is available!</v-alert
                >
                <v-alert :value="success" dense type="info"
                  ><strong>{{ confirmUsername }}</strong
                  >: {{ changeSuccessMessage }}</v-alert
                >
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions class="grey darken-4 white--text">
          <v-spacer></v-spacer>
          <v-btn
            color="orange lighten-2"
            @click="cancelDialog"
            :hidden="success"
            >Cancel</v-btn
          >
          <v-btn
            color="blue lighten-2"
            @click="onSubmit"
            :disabled="!valid || !available"
            :hidden="success || !valid || !available"
            :loading="thinking"
            >Submit Change</v-btn
          >
          <v-btn
            color="blue lighten-2"
            @click="checkAvailable"
            :disabled="!valid || available"
            :hidden="success || !valid || available"
            :loading="thinking"
            >Check Availability</v-btn
          >

          <v-btn
            color="orange lighten-2"
            @click="closeDialog"
            :hidden="!success"
            >Close</v-btn
          >

          <v-spacer></v-spacer>
          <!-- TODO: need to ensure that the user information is reloaded after saving -->
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "ChangeUsername",
  props: {
    currentUsername: String
  },
  data() {
    return {
      rules: {
        required: value => !!value || "Required.",
        nospace: v => !/([ ])/.test(v) || "Username Cannot Contain Spaces",
        usernameMatch: () =>
          this.username1 === this.username2 ||
          "The usernames you entered don't match"
      },
      // oldPassConfirmed: false,
      username1: "",
      username2: "",
      confirmUsername: "",
      valid: false,
      available: false,
      changeUsernameDialog: false,
      error: null,
      success: false,
      thinking: false,
      changeSuccessMessage: "",
      changeerror: false,
      changeErrorMessage: "",

      notification: {
        message: "",
        type: ""
      }
    };
  },
  methods: {
    validate() {
      this.$refs.form.validate();
    },
    checkAvailable() {
      this.thinking = true;
      let endpoint = `/api/users/checkusername/`;
      try {
        apiService(endpoint, "POST", { username: this.username1 }).then(
          data => {
            // console.log(data);
            if (data.success === true) {
              this.available = true;
              console.log(data.message);
              this.error = false;
              this.thinking = false;
              return true;
            } else {
              console.log(data.message);
              this.error = true;
              this.notification.message = data.message;
              this.thinking = false;
              return false;
            }
          }
        );
      } catch (err) {
        console.log(err);
      }
    },

    onSubmit() {
      this.thinking = true;
      try {
        let payload = { username: this.username1 };
        let endpoint = `/api/users/changeusername/`;
        apiService(endpoint, "POST", payload).then(data => {
          // console.log(data);
          if (data.success === true) {
            this.available = false;
            this.error = false;
            this.success = true;
            this.confirmUsername = this.username1;
            this.changeSuccessMessage = data.message;
            // console.log(data.message);
            this.$refs.form.reset();
            this.thinking = false;
            this.$emit("emitUserDataChange");
          } else {
            this.changeerror = true;
            this.success = false;
            this.changeErrorMessage = data.message;
            // console.log(data.message);
            this.thinking = false;
          }
        });
      } catch (err) {
        this.thinking = false;
      }
      // this.changeUsernameDialog = false;
    },
    closeDialog() {
      this.$refs.form.reset();
      this.error = false;
      this.success = false;
      this.available = false;
      this.changeUsernameDialog = false;
    },
    cancelDialog() {
      this.$refs.form.reset();
      this.error = false;
      this.success = false;
      this.available = false;
      this.changeUsernameDialog = false;
    }
  }
};
</script>
<style scoped></style>
