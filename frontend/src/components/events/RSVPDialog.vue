<template>
  <v-dialog 
   v-model="showDialog" 
   width="275"
   persistent
   scrollable
  >
  <v-card class="sandstone calligraphy--text">
    <v-card-title>
       Event RSVP
    </v-card-title>
    <v-card-text class="desertsand calligraphy--text px-2">
       <v-form v-model="valid">
         <v-select
            v-model="RSVP.status"
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

    Confirmed Attendees ({{ guestList.length }}):
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
        v-for="guest in guestList"
        :key="guest.username"

      >
        <v-list-item-avatar>
          <v-avatar class="mr-2" size="42">
            <v-img
              class="elevation-6"
              :src="guest.avatar"
            ></v-img>
          </v-avatar>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title
            >{{ guest.username }}
            </v-list-item-title
          >
          <v-list-item-subtitle> 
             {{ guest.comment }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    </v-card-text>
    <v-card-actions class="sandstone">
      <v-btn @click="closeDialog" class="garbage desertsand--text">Cancel<v-icon right>mdi-cancel</v-icon></v-btn>
      <v-btn :disabled="!valid" class="primary">Submit<v-icon right>mdi-send</v-icon></v-btn>
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
    guestList: Array,
    showDialog: Boolean,
    userRSVP: {
       type: Object,
       required: false,
    }
  },
  data: () => ({
    loading: true,
    RSVP: {},
    valid: false,
   rules: {
      requiredComment: value =>
        (value || "").length > 5 ||
        "You must provide a comment of at least 6 characters.",

      requiredStatus: typevalue =>
        (typevalue || "").length > 0 ||
        "You must choose a status type.",
    },
  }),


  computed: {
  },
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    getProfileSnippet() {
      this.loading = true;
      let endpoint = `/api/users/snippet/${this.curatorObject.username}`;
      apiService(endpoint).then(data => {
        if (data) {

          this.loading = false;
        } else {
           console.log("error")
        }
      });
    },
   },
   mounted (){
      if(this.userRSVP){
         this.RSVP = this.userRSVP;
      } else {
         this.RSVP = {}
      }
   }
}
</script>
<style lang="stylus">
</style>
