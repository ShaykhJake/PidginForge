<template>
  <v-row justify="center" class="ma-0">
    <v-dialog v-model="changePasswordDialog" persistent max-width="320px">
      <template v-slot:activator="{ on: changePasswordDialog }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltip }">
            <v-btn
              small
              fab
              class="orange lighten-4"
              v-on="{ ...tooltip, ...changePasswordDialog }"
            >
              <v-icon>edit</v-icon>
            </v-btn>
          </template>
          <span>Change Password</span>
        </v-tooltip>
      </template>
      <v-card class="ma-0">
        <v-card-title class="pb-1 grey darken-4 white--text">
          Change Password
        </v-card-title>
        <v-card-text class="pa-1 grey lighten-4">
          <v-container class="pa-1" fluid grid-list-md>
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
          </v-container>
        </v-card-text>
        <v-card-actions class="grey darken-4 white--text">
          <v-spacer></v-spacer>
          <v-btn color="orange lighten-2" @click="closeDialog">Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="orange lighten-2"
            @click="onSubmit"
            :disabled="!valid"
            :loading="thinking"
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
  data() {
    return {
      show1: false,
      show2: false,
      rules: {
        required: value => !!value || "Required.",
        min: v => v.length >= 8 || "Min 8 characters",
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
    onSubmit() {
      this.thinking = true;
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
        this.changePasswordDialog = false;
        this.thinking = false;
      } else {
        this.error = "Passwords must match!";
        this.thinking = false;
      }
    },
    closeDialog() {
      this.$refs.form.reset();
      this.changePasswordDialog = false;
    }
  }
};
</script>
<style scoped></style>
