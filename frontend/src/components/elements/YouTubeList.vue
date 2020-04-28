<template>
  <div>
  <div class="youtubelist" >
    <v-row wrap dense v-if="!filteredCount && !loadingVideos">
      <v-col cols="12">
        <v-card>
          <v-card-text class="desertsand calligraphy--text">
            There are no videos which match your language/topic preferences.
            You may need to update your profile to add
            learning languages and topics...or maybe we just don't
            have enough content yet!
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row wrap dense v-if="filteredCount">
      <v-col
        cols="12"
        v-for="video in filteredElements"
        :key="video.id"
      >
        <YouTubeMicro
          :you-tube-element="video"
          :hidden="video.user_has_hidden"
          @hideElement="video.user_has_hidden = !video.user_has_hidden"
        />
      </v-col>
    </v-row>
    <v-btn
      v-show="loadingVideos || next "
      @click="getVideos"
      :loading="loadingVideos"
      class="elements desertsand--text"
      block
    >
      Load More Videos <v-icon right>mdi-chevron-down</v-icon>
    </v-btn>
  </div>
  <v-overlay :value="loadingVideos" absolute>
      <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import YouTubeMicro from "@/components/elements/YouTubeMicro.vue";
export default {
  name: "YouTubeList",
  components: {
    YouTubeMicro
  },
  data() {
    return {
      videos: [],
      loadingVideos: false,
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
        return this.videos.filter(element => {
          return !element.filtered
        })
      } else {
        return this.videos;
      }
    },
    filteredCount(){
      let list = this.filteredElements;
      return list.length;
    }
  },

  methods: {
    getVideos() {
      let endpoint = `/api/elements/youtubez/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingVideos = true;
      apiService(endpoint).then(data => {
        this.videos.push(...data.results);
        this.loadingVideos = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    }
  },
  created() {
    this.getVideos();
  }
};
</script>
