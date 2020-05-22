<template>
  <v-dialog v-model="showDialog" width="275" persistent scrollable>
    <v-card class="sandstone calligraphy--text">
      <v-card-title>
        Event RSVP
      </v-card-title>
      <v-card-text class="desertsand calligraphy--text px-2">
        <v-form v-model="valid">
          <v-select
            v-model="RSVP.attending"
            :items="['Yes', 'Maybe', 'No']"
            label="Will you attend?"
            placeholder="Will you attend?"
            outlined
            class="pt-5"
            :rules="[rules.requiredStatus]"
            required
          ></v-select>
          <v-textarea
            outlined
            name="rsvpcomment"
            label="RSVP Comment"
            placeholder="I'd love to attend!"
            v-model="RSVP.comment"
            counter
            :rules="[rules.requiredComment]"
            required
            rows="3"
            maxlength="200"
          ></v-textarea>
        </v-form>

        Confirmed Attendees ({{ rsvpList.length }}):
        <v-list
          two-line
          dense
          subheader
          rounded
          counter
          maxlength="50"
          class="sandstone px-0 overflow-y-auto"
          max-height="150"
        >
          <v-list-item
            v-for="rsvp in rsvpList"
            :key="rsvp.invited_user.username"
          >
            <v-list-item-avatar>
              <v-avatar class="mr-2" size="42">
                <v-img
                  class="elevation-6"
                  :src="rsvp.invited_user.user_profile.avatar"
                ></v-img>
              </v-avatar>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title
                >{{ rsvp.invited_user.username }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ rsvp.attending }}: {{ rsvp.comment }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions class="sandstone">
        <v-btn @click="closeDialog" class="garbage desertsand--text"
          >Cancel<v-icon right>mdi-cancel</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <v-btn :disabled="!valid" @click="submitRSVP" class="primary"
          >Submit<v-icon right>mdi-send</v-icon></v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "RSVPDialog",
  components: {},
  props: {
    event: Number,
    rsvpList: Array,
    showDialog: Boolean,
    userRsvp: {
      type: Object,
      required: false
    }
  },
  data: () => ({
    loading: true,
    submittingRSVP: false,
    RSVP: {},
    valid: false,
    rules: {
      requiredComment: value =>
        (value || "").length > 5 ||
        "You must provide a comment of at least 6 characters.",

      requiredStatus: typevalue =>
        (typevalue || "").length > 0 || "You must choose a status type."
    }
  }),

  computed: {},
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },

    submitRSVP() {
      this.submittingRSVP = true;
      // Check for and format dates:
      let endpoint = `/api/events/rsvpz/`;
      let method = "POST";
      if (this.RSVP.id) {
        method = "PATCH";
        endpoint = `/api/events/rsvpz/${this.RSVP.id}/`;
      }
      var payload = {
        attending: this.RSVP.attending,
        event: this.event, // lookup by ID
        comment: this.RSVP.comment
      };
      console.log(payload);
      try {
        apiService(endpoint, method, payload).then(data => {
          console.log(data);
          if (!data) {
            this.submittingRSVP = false;
            console.log("Error");
          } else if (data.id) {
            this.$emit("updateRSVP", data);
            this.submittingRSVP = false;
            this.closeDialog();
          } else {
            console.log(data);
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.submittingRSVP = false;
          }
          this.submittingRSVP = false;
        });
      } catch (err) {
        console.log(err);
        this.submittingRSVP = false;
      }
    }
  },

  mounted() {
    if (this.userRsvp) {
      this.RSVP = this.userRsvp;
    } else {
      this.RSVP = {};
    }
  }
};
</script>
<style lang="stylus"></style>
