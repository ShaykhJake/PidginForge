<template>
  <v-dialog v-model="showDialog" scrollable persistent max-width="650px">
    <v-card class="ma-0" v-if="userData">
      <v-card-title class="pb-1 sandstone calligraphy--text">
        Update User Profile
      </v-card-title>
      <v-card-text class="pa-1 desertsand black--text">
        <p class="body-2 mx-2 black--text text-justify text-wrap">
          Dear Friend, <br /><br /><span class="font-weight-light">Pidgin</span
          ><span class="font-weight-black">Forge</span> deeply values your
          privacy. We will <b>never</b> share your personal information with
          third parties. Only your username, photo, and biography will be
          available for other PidginForge users to see. Please limit your
          information if you have identity concerns. We want you to feel safe to
          explore, learn, and contribute.<br /><br />Love, Shaykh Jake
        </p>
        <v-row wrap dense>
          <v-col cols="12" sm="6">
            <v-card class="ma-2">
              <v-img :src="userData.image">
                <v-container fill-height pa-1 align-start>
                  <v-row no-gutters>
                    <v-col cols="12">
                      <v-btn
                        small
                        class="primary"
                        @click="changePhotoDialog = true"
                        >Change<v-icon>mdi-pencil</v-icon></v-btn
                      >
                      <ChangePhoto
                        v-if="changePhotoDialog"
                        :show-dialog="changePhotoDialog"
                        @closeDialog="changePhotoDialog = false"
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

          <v-col cols="12" sm="6">
            <v-card class="ma-2 pl-2 sandstone">
              <v-row>
                <v-col>
                  <div class="overline font-weight-black">
                    Username
                  </div>
                  <div class="subtitle-1">
                    {{ userData.user.username }}
                  </div>
                  <v-btn
                    small
                    class="primary"
                    @click="changeUsernameDialog = true"
                    >Change<v-icon>mdi-pencil</v-icon></v-btn
                  >
                </v-col>
                <ChangeUsername
                  v-if="changeUsernameDialog"
                  :show-dialog="changeUsernameDialog"
                  @closeDialog="changeUsernameDialog = false"
                  @emitUserDataChange="emitUserDataChange"
                  :current-username="userData.user.username"
                ></ChangeUsername>
              </v-row>
            </v-card>

            <v-card class="ma-2 pl-2 sandstone">
              <v-row>
                <v-col>
                  <div class="overline font-weight-black">
                    Email
                  </div>
                  <div class="subtitle-1">
                    {{ userData.user.email }}
                  </div>
                  <v-btn small class="primary" @click="changeEmailDialog = true"
                    >Change<v-icon>mdi-pencil</v-icon></v-btn
                  >
                </v-col>
                <ChangeEmail
                  v-if="changeEmailDialog"
                  :show-dialog="changeEmailDialog"
                  @closeDialog="changeEmailDialog = false"
                  @emitUserDataChange="emitUserDataChange"
                  :current-email="userData.user.email"
                ></ChangeEmail>
              </v-row>
            </v-card>

            <v-card class="ma-2 pl-2 sandstone">
              <v-row>
                <v-col>
                  <div class="overline font-weight-black">
                    Password
                  </div>
                  <div class="subtitle-1">* * * * * * * *</div>
                  <v-btn
                    small
                    class="primary"
                    @click="changePasswordDialog = true"
                    >Change<v-icon>mdi-pencil</v-icon></v-btn
                  >
                </v-col>
                <ChangePassword
                  @closeDialog="changePasswordDialog = false"
                  v-if="changePasswordDialog"
                  :show-dialog="changePasswordDialog"
                >
                </ChangePassword>
              </v-row>
            </v-card>
          </v-col>
          <v-col cols="12">
            <v-card outlined class="px-2 desertsand">
              <v-form
                ref="form"
                v-model="valid"
                :hidden="success || thinking"
                class="pt-5"
              >
                <v-select
                  v-model="userData.nativelanguage"
                  :items="allLanguages"
                  label="Native Language*"
                  placeholder="Placeholder"
                  :rules="[rules.requiredNative]"
                  required
                  outlined
                  v-on:change="unsavedChanges = true"
                ></v-select>

                <v-select
                  v-model="userData.learninglanguage"
                  :items="allLanguages"
                  label="Learning Language(s)*"
                  placeholder="Placeholder"
                  :rules="[rules.requiredLanguage]"
                  multiple
                  required
                  outlined
                  v-on:change="unsavedChanges = true"
                ></v-select>

                <v-autocomplete
                  v-model="userData.learningtopics"
                  :items="allTopics"
                  label="Topic Interests"
                  placeholder="Placeholder"
                  multiple
                  required
                  outlined
                  v-on:change="unsavedChanges = true"
                ></v-autocomplete>

                <v-textarea
                  outlined
                  name="userbio"
                  label="User Biography"
                  :value="userData.biography"
                  counter
                  maxlength="300"
                  v-on:change="unsavedChanges = true"
                ></v-textarea>
              </v-form>
              <small>*indicates required field</small>
            </v-card>
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
          @click="submitData"
          :disabled="!valid || !unsavedChanges"
          :loading="submitting"
          >Save Changes<v-icon>mdi-content-save</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <!-- TODO: need to ensure that the user information is reloaded after saving -->
      </v-card-actions>
    </v-card>
  </v-dialog>
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
    userData: {},
    showDialog: Boolean
  },
  data: () => ({
    // userData: Object,
    changePhotoDialog: false,
    changeUsernameDialog: false,
    changePasswordDialog: false,
    changeEmailDialog: false,
    photoKey: 0,
    unsavedChanges: false,
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
      var localLanguages = localStorage.getItem("languages");
      if (localLanguages.length > 1) {
        console.log("Shop local!");
        this.allLanguages = JSON.parse(localLanguages);
      } else {
        this.loadingLanguages = true;
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
            this.loadingLanguages = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },

    getTopics() {
      var localTopics = localStorage.getItem("topics");
      if (localTopics.length > 1) {
        console.log("Shop local!");
        this.allTopics = JSON.parse(localTopics);
      } else {
        this.loadingTopics = true;
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
            this.loadingTopics = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },

    submitData() {
      this.submitting = true;
      try {
        apiService(`/api/users/profile/update/`, "PATCH", this.userData).then(
          data => {
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
          }
        );
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
