<template>
  <v-dialog v-model="dialog" scrollable height="400" max-width="425">
    <v-card>
      <v-card-title class="sandstone">
        Simple Flip
        <v-spacer></v-spacer>
        <v-btn @click="closeDialog" class="desertsand"
          >Close<v-icon right>mdi-close</v-icon></v-btn
        >
      </v-card-title>
      <v-card-text class="desertsand pa-5 text-center">
        Click on Card to Flip
        <transition name="cardfade">
          <v-card min-height="200" v-if="showcard" @click="flip" pa-0>
            <v-card-text align="center">
              <v-container fill-height fluid>
                <v-row
                  align="center"
                  justify="center"
                  no-gutters
                  style="height: 175px;"
                >
                  <v-col align="center">
                    <div v-if="sideA">
                      <h1>
                        {{ pairs[currentPair].lexeme_1_details.lemma }}
                      </h1>
                    </div>
                    <div v-if="sideB">
                      <h1>
                        {{ pairs[currentPair].lexeme_2_details.lemma }}
                      </h1>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </transition>
        <div class="mt-1">
          <audio
            v-if="sideA && pairs[currentPair].lexeme_1_audio.audio_file"
            controls
            :src="pairs[currentPair].lexeme_1_audio.audio_file"
          ></audio>
          <audio
            v-if="sideB && pairs[currentPair].lexeme_2_audio.audio_file"
            controls
            :src="pairs[currentPair].lexeme_2_audio.audio_file"
          ></audio>
        </div>
        <!-- <div>
               Audio Pronunciation: 
                  <v-btn small v-if="pairs[currentPair].lexeme_2_audio.audio_file" icon @click="playAudio(pairs[currentPair].lexeme_2_audio.audio_file)"><v-icon>mdi-volume-high</v-icon></v-btn>
            </div> -->
        <br />
      </v-card-text>
      <v-card-actions class="sandstone">
        <v-spacer />
        <v-btn
          class="desertsand"
          :disabled="currentPair == 0"
          @click="currentPair--"
          >Previous</v-btn
        >
        <v-spacer />
        {{ currentPair + 1 }} of {{ pairs.length }}
        <v-spacer />
        <v-btn
          class="desertsand"
          :disabled="currentPair == pairs.length - 1"
          @click="currentPair++"
          >Next</v-btn
        >
        <v-spacer />
      </v-card-actions>
    </v-card>

    <v-dialog max-width="300" v-model="audioDialog" v-if="audioDialog">
      <v-card>
        <audio controls autoplay :src="selectedAudio"></audio>
        <v-card-actions class="justify-center">
          <v-btn @click="audioDialog = false" class="garbage desertsand--text"
            >Close</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<script>
export default {
  name: "SimpleFlip",
  components: {},
  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    pairs: Array
  },
  data: () => ({
    currentPair: 0,
    sideA: true,
    sideB: false,
    showcard: true,
    audioDialog: false,

    stack: {
      id: 5
    }
  }),
  methods: {
    flip() {
      this.sideA = !this.sideA;
      this.sideB = !this.sideB;

      this.showcard = false;
      setTimeout(() => (this.showcard = true), 250);
    },
    closeDialog() {
      this.$emit("closeDialog");
    },
    playAudio(audio) {
      this.selectedAudio = audio;
      this.audioDialog = true;
    }
  },
  mounted() {}
};
</script>

<style>
.cardfade-enter-active,
.cardfade-leave-active {
  transition: opacity 0.25s ease-in-out, transform 0.25s ease-in-out;
}

/* .cardfade-enter-active {
   transition-delay: 0.45s;
} */

.cardfade-enter {
  opacity: 0;
  transform: rotate3d(0, 1, 0, 90deg);
}
.cardfade-enter-to {
  opacity: 1;
  transform: rotate3d(0, 1, 0, 0deg);
}

.cardfade-leave {
  opacity: 1;
  transform: rotate3d(0, 1, 0, 0deg);
}

.cardfade-leave-to {
  opacity: 0;
  transform: rotate3d(0, 1, 0, -90deg);
}
</style>
