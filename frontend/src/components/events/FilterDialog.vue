<template>
  <v-dialog v-model="showDialog" width="290" persistent scrollable>
    <v-card class="sandstone calligraphy--text">
      <v-card-title>
        Filter Settings
      </v-card-title>
      <v-card-text class="desertsand calligraphy--text px-2">
        <v-checkbox
          v-model="filterSettings.byRSVP"
          label="Filter by RSVP 'Yes'"
        ></v-checkbox>

        <v-autocomplete
          v-model="filterSettings.eventType"
          :items="allEventTypes"
          outlined
          dense
          chips
          label="Event Type(s)"
          multiple
          item-color="topics darken-4"
        >
          <template v-slot:selection="data">
            <v-chip
              color="topics darken-1 desertsand--text"
              v-bind="data.attrs"
              :input-value="data.selected"
              close
              small
              @click="data.select"
              @click:close="removeEventType(data.item)"
            >
              {{ data.item }}
            </v-chip>
          </template>
          <template v-slot:item="data">
            <template v-if="typeof data.item !== 'object'">
              <v-list-item-content v-text="data.item"></v-list-item-content>
            </template>
            <template v-else>
              <v-list-item-content>
                <v-list-item-title
                  v-html="data.item.username"
                ></v-list-item-title>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>

        <v-autocomplete
          v-model="filterSettings.nativeLanguage"
          :items="allLanguages"
          outlined
          chips
          dense
          label="Native Language(s)"
          item-color="languages darken-2"
          multiple
        >
          <template v-slot:selection="data">
            <v-chip
              color="languages desertsand--text"
              v-bind="data.attrs"
              :input-value="data.selected"
              small
              close
              @click="data.select"
              @click:close="removeNativeLanguage(data.item)"
            >
              {{ data.item }}
            </v-chip>
          </template>
          <template v-slot:item="data">
            <template v-if="typeof data.item !== 'object'">
              <v-list-item-content v-text="data.item"></v-list-item-content>
            </template>
            <template v-else>
              <v-list-item-content>
                <v-list-item-title
                  v-html="data.item.username"
                ></v-list-item-title>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>

        <v-autocomplete
          v-model="filterSettings.targetLanguage"
          :items="allLanguages"
          outlined
          chips
          dense
          label="Target Language(s)"
          item-color="languages darken-2"
          multiple
        >
          <template v-slot:selection="data">
            <v-chip
              color="languages desertsand--text"
              v-bind="data.attrs"
              :input-value="data.selected"
              small
              close
              @click="data.select"
              @click:close="removeTargetLanguage(data.item)"
            >
              {{ data.item }}
            </v-chip>
          </template>
          <template v-slot:item="data">
            <template v-if="typeof data.item !== 'object'">
              <v-list-item-content v-text="data.item"></v-list-item-content>
            </template>
            <template v-else>
              <v-list-item-content>
                <v-list-item-title
                  v-html="data.item.username"
                ></v-list-item-title>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>

        <v-autocomplete
          v-model="filterSettings.eventCurator"
          :items="allProfiles"
          dense
          outlined
          small-chips
          label="Event Curator(s)"
          item-text="username"
          item-value="username"
          multiple
        >
          <template v-slot:selection="data">
            <v-chip
              color="primary"
              v-bind="data.attrs"
              :input-value="data.selected"
              close
              small
              @click="data.select"
              @click:close="removeCurator(data.item)"
            >
              <v-avatar left>
                <v-img :src="data.item.avatar"></v-img>
              </v-avatar>
              {{ data.item.username }}
            </v-chip>
          </template>
          <template v-slot:item="data">
            <template v-if="typeof data.item !== 'object'">
              <v-list-item-content v-text="data.item"></v-list-item-content>
            </template>
            <template v-else>
              <v-list-item-avatar>
                <img :src="data.item.avatar" />
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title
                  v-html="data.item.username"
                ></v-list-item-title>
                <v-list-item-subtitle>{{
                  data.item.biography
                }}</v-list-item-subtitle>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>
      </v-card-text>
      <v-card-actions class="sandstone">
        <v-btn @click="resetFilters" class="garbage desertsand--text"
          >Reset<v-icon right>mdi-refresh</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <v-btn @click="submitFilter" class="primary"
          >Close<v-icon right>mdi-filter</v-icon></v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "FilterDialog",
  components: {},
  props: {
    filterSettings: Object,
    showDialog: Boolean
  },
  data: () => ({
    allProfiles: [],
    allTopics: [],
    allLanguages: [],
    allEventTypes: [
      "holiday",
      "meeting",
      "performance",
      "conference",
      "party",
      "study session",
      "lecture",
      "historical event"
    ],
    items: ["Foo", "Bar", "Baz"],
    valid: false,
    rules: {}
  }),

  computed: {},
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
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
    getProfileList() {
      var localProfileList = localStorage.getItem("profilelist");
      if (localProfileList.length > 1) {
        console.log("Shop local!");
        this.allProfiles = JSON.parse(localProfileList);
      } else {
        this.loadingProfiles = true;
        let endpoint = `/api/users/profilelist/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allProfiles = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingProfiles = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },
    resetFilters() {
      this.filterSettings.eventCurator = [];
      this.filterSettings.targetLanguage = [];
      this.filterSettings.eventType = [];
      this.filterSettings.nativeLanguage = [];
      this.filterSettings.topic = [];
      this.filterSettings.byRSVP = false;
      this.$emit("updateFilter", this.filterSettings);
    },
    submitFilter() {
      //  this.filterSettings = {
      //     byRSVP: this.byRSVP,
      //     eventType: this.eventType,
      //     topic: this.topic,
      //     nativeLanguage: this.nativeLanguage,
      //     targetLanguage: this.targetLanguage,
      //     eventCurator: this.eventCurator,
      //  }
      //  console.log(this.filterSettings)
      //  this.$emit("updateFilter", this.filterSettings)
      this.closeDialog();
    },
    removeCurator(item) {
      const index = this.filterSettings.eventCurator.indexOf(item.username);
      if (index >= 0) this.filterSettings.eventCurator.splice(index, 1);
    },
    removeTargetLanguage(item) {
      const index = this.filterSettings.targetLanguage.indexOf(item);
      if (index >= 0) this.filterSettings.targetLanguage.splice(index, 1);
    },
    removeNativeLanguage(item) {
      const index = this.filterSettings.nativeLanguage.indexOf(item);
      if (index >= 0) this.filterSettings.nativeLanguage.splice(index, 1);
    },
    removeTopic(item) {
      const index = this.filterSettings.topic.indexOf(item);
      if (index >= 0) this.filterSettings.topic.splice(index, 1);
    },
    removeEventType(item) {
      const index = this.filterSettings.eventType.indexOf(item);
      if (index >= 0) this.filterSettings.eventType.splice(index, 1);
    }
  },

  mounted() {
    if (this.userRsvp) {
      this.RSVP = this.userRsvp;
    } else {
      this.RSVP = {};
    }
    this.getLanguages();
    this.getTopics();
    this.getProfileList();
  }
};
</script>
<style lang="stylus"></style>
