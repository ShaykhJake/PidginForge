<template>
  <v-dialog v-model="dialog" scrollable persistent height="400" max-width="425">
    <v-card v-if="currentPair != null">
      <v-card-title class="sandstone">
        Multiple Choice: {{ pairs.length }} Pairs
        <v-spacer></v-spacer>
        <v-btn @click="closeDialog" class="desertsand"
          >Close<v-icon right>mdi-close</v-icon></v-btn
        >
      </v-card-title>
      <v-card-text class="desertsand pa-5 text-center">
        Score: {{ currentScore }}% ({{ cardsCorrect }} out of
        {{ cardsAttempted }})

        <transition name="cardfade">
          <v-card pa-0 v-if="showcard">
            <v-card-text align="center">
              <v-container fill-height fluid>
                <v-row align="center" justify="center" no-gutters>
                  <v-col align="center">
                    <div v-if="side == 1">
                      <h1>
                        {{ randomPairs[currentPair].lexeme_1_details.lemma }}
                        <br />
                      </h1>
                      <div
                        v-if="
                          randomPairs[currentPair].lexeme_1_audio.audio_file
                        "
                      >
                        <audio
                          controls
                          :src="
                            randomPairs[currentPair].lexeme_1_audio.audio_file
                          "
                        ></audio>
                      </div>
                    </div>
                    <div v-if="side == 2">
                      <h1>
                        {{ randomPairs[currentPair].lexeme_2_details.lemma }}
                      </h1>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </transition>
        <audio
          v-if="selectedAudio"
          controls
          autoplay
          :src="selectedAudio"
        ></audio>

        <br />
        <v-divider class="mb-2" />
        <transition-group name="cardfade">
          <v-btn
            v-for="choice in choices"
            :key="choice"
            :class="answerClass(choice)"
            block
            @click="checkAnswer(choice)"
          >
            <v-icon
              v-if="status != 'prompt' && choice != currentPair"
              class="red--text text--darken-2"
            >
              mdi-window-close
            </v-icon>
            <v-icon
              v-if="status != 'prompt' && choice == currentPair"
              class="green--text text--darken-2"
            >
              mdi-check
            </v-icon>
            <!-- {{ side == 1 ? randomPairs[choices[choice]].lexeme_2_details.lemma : randomPairs[choices[choice]].lexeme_1_details.lemma}} -->
            {{
              side == 1
                ? randomPairs[choice].lexeme_2_details.lemma
                : randomPairs[choice].lexeme_1_details.lemma
            }}
          </v-btn>
        </transition-group>

        <!-- <transition name="cardfade">
            <v-btn v-if="showcard" :class="answerClass(0)" block @click="checkAnswer(0)">{{ side == 1 ? randomPairs[choices[0]].lexeme_2_details.lemma : randomPairs[choices[0]].lexeme_1_details.lemma }}</v-btn><br>
         </transition>
         <transition name="cardfade">
            <v-btn :class="answerClass(1)" block v-if="showcard && pairs.length > 1" @click="checkAnswer(1)">{{ side == 1 ? randomPairs[choices[1]].lexeme_2_details.lemma : randomPairs[choices[1]].lexeme_1_details.lemma}}</v-btn><br>
         </transition>
         <transition name="cardfade">
            <v-btn :class="answerClass(2)" block v-if="showcard && pairs.length > 2" @click="checkAnswer(2)">{{ side == 1 ? randomPairs[choices[2]].lexeme_2_details.lemma : randomPairs[choices[2]].lexeme_1_details.lemma}}</v-btn><br>
         </transition>
         <transition name="cardfade">
            <v-btn :class="answerClass(3)" block v-if="showcard && pairs.length > 3" @click="checkAnswer(3)">{{ side == 1 ? randomPairs[choices[3]].lexeme_2_details.lemma : randomPairs[choices[3]].lexeme_1_details.lemma}}</v-btn><br>
         </transition> -->
      </v-card-text>
      <v-card-actions class="sandstone">
        <v-spacer />
        <v-btn @click="loadCard()" :disabled="status == 'prompt'"
          >Next Lexeme</v-btn
        >
        <v-spacer />
      </v-card-actions>

      <v-snackbar v-model="snackbar" :timeout="snacktimeout" top>
        {{ snacktext }}

        <template v-slot:action="{ attrs }">
          <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "MultipleChoice",
  components: {},
  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    pairs: Array
  },
  data: () => ({
    snackbar: false,
    snacktext: "",
    snacktimeout: 2000,
    showcard: false,
    selectedAudio: null,
    // cardkey: 0,
    currentPair: null,
    status: "prompt",
    randomPairs: [],
    choices: [],
    answerChoice: null,
    promptClass: "prompt",
    correctClass: "correct",
    incorrectClass: "incorrect",
    cardsAttempted: 0,
    cardsCorrect: 0,
    correctAnswer: null,
    side: 1,
    sideA: true,
    sideB: false,
    stack: {
      id: 5
    }
  }),
  computed: {
    statusClass: function() {
      return {
        "white answer-choices": this.status === "prompt",
        "green answer-choices": this.status === "correct",
        "red answer-choices": this.status === "incorrect"
      };
    },
    currentScore: function() {
      if (this.cardsAttempted > 0) {
        return Math.round((this.cardsCorrect / this.cardsAttempted) * 100);
      } else {
        return 0;
      }
    }
  },
  methods: {
    answerClass(value) {
      if (this.status == "prompt") {
        return "mb-2 white answer-choices";
        // } else if (this.choices[value] == this.currentPair && this.status === 'correct'){
        //    return 'green';
      } else if (
        value === this.answerChoice &&
        this.answerChoice === this.currentPair
      ) {
        return "mb-2 green lighten-3 answer-choices";
      } else if (
        value === this.answerChoice &&
        this.answerChoice != this.currentPair
      ) {
        return "mb-2 red lighten-3 answer-choices";
      } else {
        return "mb-2 white";
      }
    },
    closeDialog() {
      this.$emit("closeDialog");
    },
    buildChoices() {
      // Ensure Correct Choice is Available
      // Save Correct Choice
      // Randomize Choices
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },
    loadCard() {
      this.answerChoice = null;
      if (this.currentPair < this.randomPairs.length - 1) {
        this.currentPair++;
      } else {
        this.currentPair = 0;
      }
      
      this.side = Math.floor(Math.random() * 2) + 1;
      this.choices = [];
      const wordSet = new Set()
      wordSet.add(this.randomPairs[this.currentPair].lexeme_1_details.lemma)
      wordSet.add(this.randomPairs[this.currentPair].lexeme_2_details.lemma)
      for (let i = 0; i < this.randomPairs.length; i++) {
        if (this.currentPair != i && 
        !wordSet.has(this.randomPairs[i].lexeme_1_details.lemma) && 
        !wordSet.has(this.randomPairs[i].lexeme_2_details.lemma)) {
            this.choices.push(i);
            wordSet.add(this.randomPairs[i].lexeme_1_details.lemma)
            wordSet.add(this.randomPairs[i].lexeme_2_details.lemma)
        }
      }
      this.choices = this.shuffleArray(this.choices);
      this.choices = this.choices.slice(0,3);
      this.choices.push(this.currentPair);
      this.choices = this.shuffleArray(this.choices);
      this.status = "prompt";
      this.showcard = false;
      setTimeout(() => (this.showcard = true), 250);
    },
    checkAnswer(choice) {
      if (this.status != "prompt") {
        this.loadCard();
      } else {
        this.answerChoice = choice;
        // this.showcardB=true;
        // this.cardkey++
        this.cardsAttempted++;
        if (choice == this.currentPair) {
          // console.log(this.randomPairs[this.currentPair].id)
          this.$emit("correctAnswer", this.randomPairs[this.currentPair]);
          this.status = "correct";
          this.cardsCorrect++;
          // setTimeout(() => this.loadCard(), 250);
          // this.loadCard();
        } else {
          // this.showcardA=false;
          this.$emit("incorrectAnswer", this.randomPairs[this.currentPair]);
          this.status = "incorrect";

          // setTimeout(() => this.loadCard(), 1000);
          // setTimeout(() => this.showcard = true, 250);
        }
      }
    },
    playAudio(audio) {
      this.selectedAudio = audio;
    }
  },
  mounted() {
    // this.randomPairs = Array.from(Array(this.pairs.length).keys()),
    this.randomPairs = this.pairs;
    this.randomPairs = this.shuffleArray(this.randomPairs);
    this.currentPair = 0;
    this.loadCard();
  }
};
</script>

<style scoped>
.answer-choices {
  font-size: 1.5em;
}

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

audio {
  width: 300px;
  height: 25px;
  margin-top: 5px;
}
</style>
