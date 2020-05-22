<template>
  <div class="youtubelist">
    <v-row wrap dense v-if="!filteredCount && !loadingTextElements">
      <v-col cols="12">
        <v-card>
          <v-card-text class="desertsand calligraphy--text">
            There are no text elements which match your language/topic
            preferences. You may need to update your profile to add learning
            languages and topics...or maybe we just don't have enough content
            yet!
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row wrap dense v-if="filteredCount">
      <v-col
        cols="12"
        v-for="textElement in filteredElements"
        :key="textElement.id"
      >
        <textElementMicro
          :textElement="textElement"
          :hidden="textElement.user_has_hidden"
          @hideElement="
            textElement.user_has_hidden = !textElement.user_has_hidden
          "
        />
      </v-col>
    </v-row>
    <v-btn
      v-show="next || loadingTextElements"
      @click="getTextElements"
      :loading="loadingTextElements"
      class="elements desertsand--text"
      block
    >
      Load More TextElement <v-icon right>mdi-chevron-down</v-icon>
    </v-btn>
    <v-overlay :value="loadingTextElements" absolute>
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import TextElementMicro from "@/components/elements/TextElementMicro.vue";
export default {
  name: "TextElementList",
  components: {
    TextElementMicro
  },
  data() {
    return {
      textElements: [],
      loadingTextElements: false,
      next: null
    };
  },
  props: {
    preferenceFilter: {
      required: false,
      default: false
    }
  },
  computed: {
    filteredElements() {
      if (this.preferenceFilter) {
        return this.textElements.filter(element => {
          return !element.filtered;
        });
      } else {
        return this.textElements;
      }
    },
    filteredCount() {
      return this.filteredElements.length;
    }
  },

  methods: {
    getTextElements() {
      let endpoint = `/api/elements/textz/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingTextElements = true;
      apiService(endpoint).then(data => {
        if (data) {
          this.textElements.push(...data.results);
          this.loadingTextElements = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
            this.loadingTextElements = false;
          }
        }
      });
    }
  },
  created() {
    this.getTextElements();
  }
};
</script>
