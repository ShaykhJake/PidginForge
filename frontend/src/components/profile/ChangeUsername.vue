<template>
  <v-row justify="center" class="ma-0">
    <v-dialog v-model="showDialog" persistent max-width="320px">
      <v-card>
        <v-card-title class="sandstone calligraphy--text">
          Change Username
        </v-card-title>
        <v-card-text class="desertsand calligraphy--text">
          <v-row wrap dense>
            <v-col cols="12">
              <p>
                Current username: <strong>{{ currentUsername }}</strong>
              </p>
              <v-form ref="form" v-model="valid">
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
                >That username is already in use; please try a different
                one.</v-alert
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
        </v-card-text>
        <v-card-actions class="sandstone calligraphy--text">
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
            @click="submitChange"
            v-if="valid && available"
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
  name: "ChangeUsername",
  props: {
    currentUsername: String,
    showDialog: Boolean
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
      checkingAvailability: false,
      submittingChange: false,
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
      this.checkingAvailability = true;
      let endpoint = `/api/users/checkusername/`;
      try {
        apiService(endpoint, "POST", { username: this.username1 }).then(
          data => {
            // console.log(data);
            if (data.success === true) {
              this.available = true;
              console.log(data.message);
              this.error = false;
              this.checkingAvailability = false;
              return true;
            } else {
              console.log(data.message);
              this.error = true;
              this.notification.message = data.message;
              this.checkingAvailability = false;
              this.valid = false;
              return false;
            }
          }
        );
      } catch (err) {
        this.checkingAvailability = false;
        console.log(err);
      }
    },

    submitChange() {
      this.submittingChange = true;
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
            this.submittingChange = false;
            this.$emit("emitUserDataChange");
            this.closeDialog();
          } else {
            this.changeerror = true;
            this.success = false;
            this.changeErrorMessage = data.message;
            // console.log(data.message);
            this.submittingChange = false;
          }
        });
      } catch (err) {
        this.submittingChange = false;
      }
      // this.changeUsernameDialog = false;
    },
    closeDialog() {
      this.$refs.form.reset();
      this.error = false;
      this.success = false;
      this.available = false;
      this.$emit("closeDialog");
    }
  }
};
</script>
<style scoped></style>
