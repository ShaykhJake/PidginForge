<template>
  <v-card class="ma-0" v-if="userData">
    <v-card-title class="pb-1 grey darken-4 white--text">
      Update User Profile
    </v-card-title>
    <v-card-text class="pa-1 grey lighten-4">
      <p class="body-2 mx-2 black--text text-justify text-wrap">
        Dear Friend, <br /><br /><span class="font-weight-light">Pidgin</span
        ><span class="font-weight-black">Forge</span> deeply values your
        privacy. We will <b>never</b> share your personal information with third
        parties. Only your username, photo, and biography will be available for
        other PidginForge users to see. Please limit your information if you
        have identity concerns. We want you to feel safe to explore, learn, and
        contribute.<br /><br />Love, Shaykh Jake
      </p>
      <v-container class="pa-1" fluid grid-list-md>
        <v-row wrap dense>
          <v-col cols="12">
            <v-row dense>
              <v-col cols="12" md="6">
                <v-card class="pa-2" outlined>
                  <v-img :src="userData.image">
                    <v-container fill-height pa-1 align-start>
                      <v-row no-gutters>
                        <v-col cols="12">
                          <ChangePhoto
                            @emitUserDataChange="emitUserDataChange"
                            :img-src="userData.image"
                            :img-name="userData.image_name"
                            :key="photoKey"
                          ></ChangePhoto>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-img>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-row wrap dense>
                  <v-col cols="12">
                    <v-card class="pa-2" outlined>
                      <v-row>
                        <v-col cols="2">
                          <ChangeUsername
                            @emitUserDataChange="emitUserDataChange"
                            :current-username="userData.user.username"
                          ></ChangeUsername>
                        </v-col>
                        <v-col cols="10">
                          <div class="overline font-weight-black">
                            Username
                          </div>
                          <div class="subtitle-1">
                            {{ userData.user.username }}
                          </div>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>

                  <v-col cols="12">
                    <v-card class="pa-2" outlined>
                      <v-row>
                        <v-col cols="2">
                          <ChangeEmail
                            @emitUserDataChange="emitUserDataChange"
                            :current-email="userData.user.email"
                          ></ChangeEmail>
                        </v-col>
                        <v-col cols="10">
                          <div class="overline font-weight-black">
                            Email
                          </div>
                          <div class="subtitle-1">
                            {{ userData.user.email }}
                          </div>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>

                  <v-col cols="12">
                    <v-card class="pa-2" outlined>
                      <v-row>
                        <v-col cols="2">
                          <ChangePassword></ChangePassword>
                        </v-col>
                        <v-col cols="10">
                          <div class="overline font-weight-black">
                            Password
                          </div>
                          <div class="subtitle-1">* * * * * * * *</div>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-form ref="form" v-model="valid" :hidden="success || thinking">
          <v-row dense>
            <v-col cols="12">
              <v-card outlined class="px-2">
                <v-row wrap dense class="pt-2">
                  <v-col cols="12">
                    <v-select
                      v-model="userData.nativelanguage"
                      :items="allLanguages"
                      label="Native Language*"
                      placeholder="Placeholder"
                      :rules="[rules.requiredNative]"
                      required
                      outlined
                    ></v-select>
                  </v-col>
                  <v-col cols="12">
                    <v-select
                      v-model="userData.learninglanguage"
                      :items="allLanguages"
                      label="Learning Language(s)*"
                      placeholder="Placeholder"
                      :rules="[rules.requiredLanguage]"
                      multiple
                      required
                      outlined
                    ></v-select>
                  </v-col>
                  <v-col cols="12">
                    <v-autocomplete
                      v-model="userData.learningtopics"
                      :items="allTopics"
                      label="Topic Interests"
                      placeholder="Placeholder"
                      multiple
                      required
                      outlined
                    ></v-autocomplete>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>

          <v-row dense>
            <v-col cols="12">
              <v-card outlined>
                <v-card-text>
                  <div class="font-weight-black black--text">
                    User Biography
                  </div>
                  <div>
                    <v-textarea
                      label="About"
                      v-model="userData.biography"
                      counter
                      maxlength="600"
                      full-width
                      single-line
                    ></v-textarea>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
      <small>*indicates required field</small>
    </v-card-text>
    <v-card-actions class="grey darken-4 white--text">
      <v-spacer></v-spacer>
      <v-btn color="orange lighten-2" @click="closeDialog">Cancel</v-btn>
      <v-btn
        color="blue lighten-2"
        @click="submitData"
        :hidden="!valid"
        :loading="submitting"
        >Save Changes</v-btn
      >
      <v-spacer></v-spacer>
      <!-- TODO: need to ensure that the user information is reloaded after saving -->
    </v-card-actions>
  </v-card>
</template>
<script>
import { apiService } from "@/common/api.service.js";
import ChangePassword from "@/components/profile/ChangePassword.vue";
import ChangeEmail from "@/components/profile/ChangeEmail.vue";
import ChangePhoto from "@/components/profile/ChangePhoto.vue";
import ChangeUsername from "@/components/profile/ChangeUsername.vue";
export default {
  name: "ProfileUpdate",
  components: {
    ChangePassword,
    ChangeEmail,
    ChangePhoto,
    ChangeUsername
  },
  props: {
    userData: {}
  },
  data: () => ({
    // userData: Object,
    photoKey: 0,
    nativeLanguage: String,
    thinking: false,
    submitting: false,
    valid: true,
    success: false,
    learningLanguages: [],
    learningTopics: [],
    topicObject: Object,
    methodObject: Object,
    updatedDataObject: {
      nativelanguage: String,
      learninglanguage: Array,
      learningtopics: Array,
      biography: String
    },
    rules: {
      requiredLanguage: value =>
        value.length > 0 || "You must choose at least 1 language.",
      requiredNative: value =>
        value.length > 0 || "You must choose a native language."
      // pattern: v => /.+@.+\..+/.test(v) || "E-mail must be valid",
      // emailMatch: () =>
      // this.email1 === this.email2 || "The addresses you entered don't match"
    },
    allLanguages: [],
    allTopics: [],
    allMethods: []
  }),
  methods: {

    closeDialog() {
      this.$emit("closeDialog");
    },
    forcePhotoRender() {
      this.photoKey += 1;
    },
    checkLearningLanguagesLength() {
      return this.learningLanguages.length < 1;
    },
    emitUserDataChange() {
      this.$emit("emitUserDataChange");
    },
    getLanguages() {
      let endpoint = `/api/categories/languages/`;
      try {
        apiService(endpoint).then(data => {
          if (data != null) {
            this.allLanguages = data;
            this.error = false;
          } else {
            console.log("Something bad happened...");
            this.error = true;
          }
        });
      } catch (err) {
        console.log(err);
      }
    },

    getTopics() {
      let endpoint = `/api/categories/topics/`;
      try {
        apiService(endpoint).then(data => {
          if (data != null) {
            this.allTopics = data;
            this.error = false;
          } else {
            console.log("Something bad happened...");
            this.error = true;
          }
        });
      } catch (err) {
        console.log(err);
      }
    },

    submitData() {
      this.submitting = true;
      try {
        apiService(
          `/api/users/profile/update/`,
          "PATCH",
          this.userData
        ).then(data => {
          if (data.success === true) {
            console.log(data.message);
            this.$emit("emitUserDataChange");
            this.submitting = false;
            this.closeDialog();
          } else {
            this.changeerror = true;
            this.success = false;
            this.changeErrorMessage = data.message;
            console.log("hello");
            console.log(data.message);
            this.submitting = false;
            this.thinking = false;
          }
        });
      } catch (err) {
        console.log(err);
      }
    }
  },
  mounted() {
    this.getLanguages();
    this.getTopics();
    // this.parsePreferences();
  }
};
</script>
<style scoped></style>
