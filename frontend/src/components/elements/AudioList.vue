<template>
  <div class="youtubelist">
    <v-row wrap dense v-if="!filteredCount && !loadingAudios">
      <v-col cols="12">
        <v-card>
          <v-card-text class="desertsand calligraphy--text">
            There are no audio elements which match your language/topic
            preferences. You may need to update your profile to add
            learning languages and topics...or maybe we just don't
            have enough content yet!
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row wrap dense v-if="filteredCount">
      <v-col
        cols="12"
        v-for="audio in filteredElements"
        :key="audio.id"
      >
        <AudioMicro
          :audio="audio"
          :hidden="audio.user_has_hidden"
          @hideElement="audio.user_has_hidden = !audio.user_has_hidden"
        />
      </v-col>
    </v-row>
    <v-btn
      v-show="next || loadingAudios"
      @click="getAudios"
      :loading="loadingAudios"
      class="elements desertsand--text"
      block
    >
      Load More Audio <v-icon right>mdi-chevron-down</v-icon>
    </v-btn>
    <v-overlay :value="loadingAudios" absolute>
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AudioMicro from "@/components/elements/AudioMicro.vue";
export default {
  name: "AudioList",
  components: {
    AudioMicro
  },
  data() {
    return {
      audios: [],
      loadingAudios: false,
      next: null
    };
  },
  props: {
    preferenceFilter: {
      required: false,
      default: false,
    }
  },
  computed: {
    filteredElements() {
      if (this.preferenceFilter){
        return this.audios.filter(element => {
          return !element.filtered
        })
      } else {
        return this.audios;
      }
    },
    filteredCount(){
      return this.filteredElements.length;
    }
  },

  methods: {
    getAudios() {
      let endpoint = `/api/elements/audioz/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingAudios = true;
      apiService(endpoint).then(data => {
        if (data) {
          this.audios.push(...data.results);
          this.loadingAudios = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
            this.loadingAudios = false;
          }
        }
      });
    }
  },
  created() {
    this.getAudios();
  }
};
</script>
