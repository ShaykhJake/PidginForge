<template>
  <v-dialog v-model="flaggerDialog" scrollable persistent max-width="300">
    <v-card class="ma-0 desertsand">
      <v-card-title class="pb-1 calligraphy desertsand--text" align="center">
        Flag Inappropriate Content
      </v-card-title>
      <v-card-text class="pa-1 desertsand">
        <p class="body-2 mx-2 black--text text-justify text-wrap">
          Please only flag content if it meets one of three categories:
          <span class="font-weight-black"
            >Copyright Infringement, Obscene, or Offensive.</span
          >
        </p>
        <p class="body-2 mx-2 black--text text-justify text-wrap">
          Your username will be associated with the flag, but only known to PF
          administrators.
        </p>
        <p class="body-2 mx-2 black--text text-justify text-wrap">
          Material that has been flagged more than three times will be
          automatically hidden.
        </p>

        <v-form ref="flagdetails" v-model="valid">
          <v-select
            block
            v-model="flagObject.category"
            :items="flagCategories"
            label="Flag Category*"
            placeholder="choose a flag category"
            :rules="[rules.requiredCategory]"
            required
            outlined
          ></v-select>

          <v-textarea
            outlined
            label="Flag Justification*"
            v-model="flagObject.justification"
            :rules="[rules.requiredJustification]"
            counter
            rows="3"
            maxlength="300"
          ></v-textarea>
        </v-form>
      </v-card-text>

      <v-card-actions class="calligraphy">
        <v-spacer></v-spacer>
        <v-btn color="garbage desertsand--text" @click="closeDialog"
          >Cancel<v-icon right>mdi-close</v-icon></v-btn
        >
        <v-btn
          color="success"
          @click="submitFlag"
          :disabled="!valid"
          :loading="submitting"
          >Submit<v-icon right>mdi-thumb-up</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <!-- TODO: need to ensure that the user information is reloaded after saving -->
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "ContentFlagger",
  components: {},
  props: {
    flaggerDialog: Boolean,
    contentType: String,
    // HERE I NEED TO DECIDE IF IT SHOULD BE A SLUG OR OBJECT ID
    contentid: Number
  },
  data: () => ({
    // userData: Object,
    submitting: false,
    valid: true,
    flagObject: {
      category: "",
      justification: ""
    },
    flagCategories: ["Copyright", "Obscene", "Offensive"],
    rules: {
      requiredCategory: value => !!value || "You must choose a flag category.",
      requiredJustification: value =>
        !!value || "You must provied a justification."
    }
  }),
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    submitFlag() {
      let endpoint = `api/malapropos/flag/`;
      this.flagObject.contenttype = this.contentType;
      this.flagObject.id = this.contentid;
      apiService(endpoint, "POST", this.flagObject).then(data => {
        if (data != null) {
          // Success
          this.$emit("closeDialog");
          this.$emit("flagSuccess");
        } else {
          // No success
        }
      });
    }
  }
};
</script>
