<template>
  <v-row justify="center" class="ma-0">
    <v-dialog v-model="changeEmailDialog" persistent max-width="320px">
      <template v-slot:activator="{ on: changeEmailDialog }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltip }">
            <v-btn
              small
              fab
              class="orange lighten-4"
              v-on="{ ...tooltip, ...changeEmailDialog }"
            >
              <v-icon>edit</v-icon>
            </v-btn>
          </template>
          <span>Change Email</span>
        </v-tooltip>
      </template>
      <v-card class="ma-0">
        <v-card-title class="pb-1 grey darken-4 white--text">
          Change Email Address
        </v-card-title>
        <v-card-text class="pa-1 grey lighten-4">
          <v-container class="pa-1" fluid grid-list-md>
            <v-row wrap dense>
              <v-col cols="12">
                <p>Current address: {{ currentEmail }}</p>
                <v-form
                  ref="form"
                  v-model="valid"
                  :hidden="success || thinking"
                >
                  <v-text-field
                    v-model="email1"
                    :rules="[rules.required, rules.pattern]"
                    name="input-10-1"
                    hint=""
                    autofocus
                    label="New Email"
                    @focus="
                      available = false;
                      error = false;
                    "
                  ></v-text-field>
                  <v-text-field
                    v-model="email2"
                    :rules="[rules.required, rules.emailMatch]"
                    name="input-10-2"
                    label="Confirm New Email"
                    value=""
                    class="input-group--focused"
                  ></v-text-field>
                </v-form>
                <v-alert :value="error" dense type="error"
                  >That E-Mail address is already in use</v-alert
                >
                <v-alert :value="changeerror" dense type="error">{{
                  changeErrorMessage
                }}</v-alert>
                <v-alert :value="success" dense type="info"
                  ><strong>{{ confirmEmail }}</strong
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
            :disabled="success"
            >Cancel</v-btn
          >

          <v-btn
            color="blue lighten-2"
            @click="onSubmit"
            :disabled="!valid || !available"
            :hidden="success || !valid || !available"
            >Submit Change</v-btn
          >

          <v-btn
            color="blue lighten-2"
            @click="checkAvailable"
            :disabled="!valid || available"
            :hidden="success || !valid || available"
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
  name: "ChangeEmail",
  props: {
    currentEmail: String
  },
  data() {
    return {
      rules: {
        required: value => !!value || "Required.",
        pattern: v => /.+@.+\..+/.test(v) || "E-mail must be valid",
        emailMatch: () =>
          this.email1 === this.email2 || "The addresses you entered don't match"
      },
      // oldPassConfirmed: false,
      email1: "",
      email2: "",
      confirmEmail: "",
      valid: false,
      available: false,
      changeEmailDialog: false,
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
      let endpoint = `/api/users/checkemail/`;
      try {
        apiService(endpoint, "POST", { email: this.email1 }).then(data => {
          // console.log(data);
          if (data.available === true) {
            this.available = true;
            console.log("Email address is available");
            this.error = false;
            return true;
          } else {
            console.log("Email address is already in use");
            this.error = true;
            this.notification.message = "Email Address Already in Use";
            return false;
          }
        });
      } catch (err) {
        console.log(err);
      }
    },

    onSubmit() {
      this.thinking = true;
      if (this.available) {
        let endpoint = `/api/users/changeemail/`;
        this.thinking = true;
        this.confirmEmail = this.email1;
        try {
          apiService(endpoint, "POST", { email: this.email1 }).then(data => {
            // console.log(data);
            if (data.success === true) {
              this.error = false;
              this.success = true;
              this.changeSuccessMessage = data.message;
              console.log(data.message);
              this.$refs.form.reset();
              this.thinking = false;
              this.$emit("emitUserDataChange");
            } else {
              this.changeerror = true;
              this.success = false;
              this.changeErrorMessage = data.message;
              console.log(data.message);
              this.thinking = false;
            }
          });
        } catch (err) {
          console.log(err);
          this.thinking = false;
        }
      }
      // this.changeEmailDialog = false;
    },
    closeDialog() {
      this.changeEmailDialog = false;
    },
    cancelDialog() {
      this.$refs.form.reset();
      this.error = false;
      this.success = false;
      this.available = false;
      this.changeEmailDialog = false;
    }
  }
};
</script>
<style scoped></style>
