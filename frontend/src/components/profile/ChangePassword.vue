<template>
  <v-row justify="center" class="ma-0">
    <v-dialog v-model="showDialog" persistent max-width="320px">
      <v-card class="ma-0">
        <v-card-title class="sandstone calligraphy--text">
          Change Password
        </v-card-title>
        <v-card-text class="desertsand calligraphy--text">
          <v-row wrap dense>
            <v-col cols="12">
              <v-form ref="form" v-model="valid">
                <v-text-field
                  v-model="password1"
                  :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                  :rules="[
                    rules.required,
                    rules.min,
                    rules.upper,
                    rules.number,
                    rules.special
                  ]"
                  :type="show1 ? 'text' : 'password'"
                  name="input-10-1"
                  hint="At least 8 characters"
                  counter
                  label="Password"
                  @click:append="show1 = !show1"
                ></v-text-field>
                <v-text-field
                  v-model="password2"
                  :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                  :rules="[rules.required, rules.passMatch]"
                  :type="show2 ? 'text' : 'password'"
                  name="input-10-2"
                  label="Confirm Password"
                  value=""
                  class="input-group--focused"
                  @click:append="show2 = !show2"
                ></v-text-field>
              </v-form>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="sandstone">
          <v-spacer></v-spacer>
          <v-btn color="garbage desertsand--text" @click="closeDialog"
            >Cancel<v-icon>mdi-cancel</v-icon></v-btn
          >
          <v-btn
            color="primary"
            @click="submitChange"
            :disabled="!valid"
            :loading="submittingChange"
            >Confirm Change</v-btn
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
  name: "ChangePassword",
  props: {
    showDialog: Boolean
  },
  data() {
    return {
      show1: false,
      show2: false,
      rules: {
        required: value => !!value || "Required.",
        min: v => (v || "").length >= 8 || "Min 8 characters",
        upper: v =>
          /(?=.*[A-Z])/.test(v) || "Must have one uppercase character",
        number: v => /(?=.*\d)/.test(v) || "Must have one number",
        special: v =>
          /([!@$%#^~?+])/.test(v) ||
          "Must have one special character [!@$%#^~?+]",
        passMatch: () =>
          this.password1 === this.password2 ||
          "The passwords you entered don't match"
      },
      // oldPassConfirmed: false,
      password1: "",
      password2: "",
      valid: false,
      submittingChange: false,
      changePasswordDialog: false,
      error: null,
      thinking: false,
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
    submitChange() {
      this.submittingChange = true;
      if (this.password1 === this.password2) {
        let endpoint = `/api/rest-auth/password/change/`;
        apiService(endpoint, "POST", {
          new_password1: this.password1,
          new_password2: this.password2
        }).then(data => {
          this.answers.unshift(data);
        });
        if (this.error) {
          this.error = null;
        }
        this.$refs.form.reset();
        this.submittingChange = false;
        this.closeDialog();
      } else {
        this.error = "Passwords must match!";
        this.thinking = false;
        this.submittingChange = false;
        this.valid = false;
      }
    },
    closeDialog() {
      this.$refs.form.reset();
      this.changePasswordDialog = false;
      this.$emit("closeDialog");
    }
  }
};
</script>
<style scoped></style>
