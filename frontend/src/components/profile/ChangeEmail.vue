<template>
  <v-row justify="center" class="ma-0">
    <v-dialog v-model="showDialog" persistent max-width="320px">
      <v-card class="ma-0">
        <v-card-title class="pb-1 sandstone calligraphy--text">
          Change Email Address
        </v-card-title>
        <v-card-text class="pa-1 desertsand">
          <v-row wrap dense>
            <v-col cols="12">
              <p>Current address: {{ currentEmail }}</p>
              <v-form ref="form" v-model="valid">
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
        </v-card-text>
        <v-card-actions class="sandstone">
          <v-spacer></v-spacer>
          <v-btn
            color="garbage desertsand--text"
            @click="closeDialog"
            v-if="!success"
            >Cancel<v-icon>mdi-cancel</v-icon></v-btn
          >
          <v-btn
            color="primary"
            @click="checkAvailable"
            v-if="!available && valid"
            :loading="checkingAvailability"
            >Check Availability</v-btn
          >
          <v-btn
            color="primary"
            @click="onSubmit"
            v-if="valid & available"
            :loading="submittingChange"
            >Submit Change</v-btn
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
    showDialog: Boolean,
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
      changeSuccessMessage: "",
      changeerror: false,
      changeErrorMessage: "",
      checkingAvailability: false,
      submittingChange: false,
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
      this.checkingAvailability = true;
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
        this.checkingAvailability = false;
      } catch (err) {
        console.log(err);
        this.checkingAvailability = false;
      }
    },

    onSubmit() {
      this.submittingChange = true;
      if (this.available) {
        let endpoint = `/api/users/changeemail/`;
        this.confirmEmail = this.email1;
        try {
          apiService(endpoint, "POST", { email: this.email1 }).then(data => {
            // console.log(data);
            if (data.success === true) {
              this.error = false;
              this.success = true;
              this.changeSuccessMessage = data.message;
              this.$refs.form.reset();
              this.$emit("emitUserDataChange");
              this.closeDialog();
            } else {
              this.changeerror = true;
              this.success = false;
              this.changeErrorMessage = data.message;
            }
            this.submittingChange = false;
          });
        } catch (err) {
          console.log(err);
          this.submittingChange = false;
        }
      }
      this.submittingChange = false;
      // this.changeEmailDialog = false;
    },
    closeDialog() {
      this.error = false;
      this.success = false;
      this.available = false;
      this.$emit("closeDialog");
    }
  }
};
</script>
<style scoped></style>
