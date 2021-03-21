<template>
  <div class="pa-2 calligraphy">
    <v-card class="desertsand calligraphy--text" min-width="300">
      <v-card-title class="sandstone py-1">
        Multiple Choice Quiz ({{ questionSet.length }} Questions)
        <v-spacer />
        <v-btn
          v-if="!userIsCurator"
          small
          class="primary desertsand--text"
          @click="editing = !editing"
        >
          <span v-if="editing">Preview Mode</span>
          <span v-if="!editing">Edit Mode</span>
        </v-btn>
      </v-card-title>
      <v-card-text class="calligraphy--text pt-4">
        <div v-if="!graded">
          <div v-for="(question, index) in questionSet" :key="index">
            <!-- Hide all questions, show only the one with index === to current question index -->
            <div
              v-show="index === currentQuestion"
              :style="
                question.stem_style === 'rtl'
                  ? 'direction: rtl; text-align: right'
                  : 'direction: ltr; text-align: left'
              "
            >
              <h3>{{ `${index + 1}) ` }}{{ question.stem }}</h3>

              <div
                :style="
                  question.alternatives_style === 'rtl'
                    ? 'direction: rtl; text-align: right'
                    : 'direction: ltr; text-align: left'
                "
              >
                <v-radio-group
                  v-if="question.answer_key.length <= 1"
                  v-model="userResponses[index]"
                  column
                  class="desertsand calligraphy--text"
                >
                  <div
                    v-for="alternative in question.alternatives"
                    :key="alternative.key"
                  >
                    <v-radio
                      :label="alternative.text"
                      :value="alternative.key"
                      class="desertsand calligraphy--text"
                    ></v-radio>
                  </div>
                </v-radio-group>
                <div v-else>
                  <v-checkbox
                    v-for="alternative in question.alternatives"
                    :key="alternative.key"
                    v-model="userResponses[index]"
                    :label="alternative.text"
                    :value="alternative.key"
                    style="height: 1em;"
                  ></v-checkbox>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="graded">
          <h2>Quiz Feedback</h2>
          <div>
            Total Score: {{ userScore }} out of {{ totalPoints }} ({{
              Math.round((userScore / totalPoints) * 100)
            }}%)
            <div
              v-for="(gradedResponse, index) in gradedResponses"
              :key="index"
            >
              <hr />
              Question #{{ index + 1 }}:
              <span
                :class="gradedResponse.correct ? 'green--text' : 'red--text'"
                >{{ gradedResponse.correct ? "Correct!" : "Incorrect" }}</span
              >
              <div class="pl-5">
                <strong>Your Response: {{ userResponses[index] }}</strong>
                {{ questionSet[index].stem }}
                <div v-if="questionSet[index].select_type === 'multiple'">
                  <div
                    v-for="(alternative, altindex) in questionSet[index]
                      .alternatives"
                    :key="altindex"
                  >
                    <div
                      v-if="
                        userResponses[index].includes(alternative.key) &&
                          questionSet[index].answer_key.includes(
                            alternative.key
                          )
                      "
                    >
                      <v-icon class="green--text"
                        >mdi-checkbox-marked-outline</v-icon
                      >
                      {{ questionSet[index].alternatives[altindex].text }}
                      <v-icon class="green--text">mdi-check-decagram</v-icon>
                    </div>
                    <div
                      v-else-if="
                        userResponses[index].includes(alternative.key) &&
                          !questionSet[index].answer_key.includes(
                            alternative.key
                          )
                      "
                    >
                      <v-icon class="red--text"
                        >mdi-checkbox-marked-outline</v-icon
                      >
                      {{ questionSet[index].alternatives[altindex].text }}
                      <v-icon class="red--text">mdi-check-close</v-icon>
                    </div>
                    <div
                      v-else-if="
                        !userResponses[index].includes(alternative.key) &&
                          questionSet[index].answer_key.includes(
                            alternative.key
                          )
                      "
                    >
                      <v-icon class="red--text"
                        >mdi-checkbox-blank-outline</v-icon
                      >
                      {{ questionSet[index].alternatives[altindex].text }}
                      <v-icon class="red--text">mdi-check-decagram</v-icon>
                    </div>
                    <div v-else>
                      <v-icon>mdi-checkbox-blank-outline</v-icon>
                      {{ questionSet[index].alternatives[altindex].text }}
                    </div>
                  </div>
                </div>
                <div v-else>
                  <div
                    v-for="(alternative, altindex) in questionSet[index]
                      .alternatives"
                    :key="altindex"
                  >
                    <div
                      v-if="
                        alternative.key === userResponses[index] &&
                          alternative.key === questionSet[index].answer_key[0]
                      "
                    >
                      <v-icon class="green--text">mdi-radiobox-marked</v-icon>
                      {{ questionSet[index].alternatives[altindex].text }}
                      <v-icon class="green--text">mdi-check-decagram</v-icon>
                    </div>
                    <div
                      v-else-if="
                        alternative.key === userResponses[index] &&
                          alternative.key != questionSet[index].answer_key[0]
                      "
                    >
                      <v-icon class="red--text">mdi-radiobox-marked</v-icon>
                      {{ questionSet[index].alternatives[altindex].text }}
                      <v-icon class="red--text">mdi-check-close</v-icon>
                    </div>
                    <div
                      v-else-if="
                        alternative.key != userResponses[index] &&
                          alternative.key === questionSet[index].answer_key[0]
                      "
                    >
                      <v-icon class="red--text">mdi-radiobox-blank</v-icon>
                      {{ questionSet[index].alternatives[altindex].text }}
                      <v-icon class="red--text">mdi-check-decagram</v-icon>
                    </div>
                    <div v-else>
                      <v-icon>mdi-radiobox-blank</v-icon>
                      {{ questionSet[index].alternatives[altindex].text }}
                    </div>
                  </div>
                </div>

                <strong>Answer Explanation:</strong>
                {{ questionSet[index].explanation }}
              </div>
            </div>
          </div>
        </div>
      </v-card-text>
      <v-card-actions v-if="editing" class="sandstone"> </v-card-actions>

      <v-card-actions v-if="!graded && !editing" class="sandstone">
        <v-btn
          v-if="currentQuestion > 0"
          v-on:click="loadPreviousQuestion"
          class="primary"
        >
          <v-icon left>mdi-arrow-left-bold</v-icon>Previous
        </v-btn>
        <v-spacer></v-spacer>
        <span class="subtitle-1"
          >Question #{{ currentQuestion + 1 }} of {{ questionSet.length }}</span
        >
        <v-spacer />
        <v-btn
          v-on:click="loadNextQuestion"
          v-if="currentQuestion < questionSet.length - 1"
          :disabled="userResponses[currentQuestion].length === 0"
          class="primary"
        >
          Next<v-icon right>mdi-arrow-right-bold</v-icon>
        </v-btn>
        <v-btn
          @click="gradeQuiz"
          v-if="currentQuestion === questionSet.length - 1"
          :disabled="!allAnswered"
          class="topics desertsand--text"
        >
          Grade Quiz<v-icon right>mdi-check-decagram</v-icon>
        </v-btn>
      </v-card-actions>
      <v-card-actions v-if="graded && !editing" class="sandstone">
        <v-spacer />
        <v-btn
          @click="resetQuiz"
          v-if="graded"
          class="elements desertsand--text"
        >
          Reset Quiz
        </v-btn>
        <v-spacer />
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
// import VueYouTubeEmbed from 'vue-youtube-embed'
export default {
  name: "MultipleChoiceQuiz",
  props: {
    questionSet: {}
  },
  components: {},
  data() {
    return {
      editing: true,
      answersSubmitted: false,
      answersLocked: false,
      userResponses: Array(this.questionSet.length).fill([]),
      currentQuestion: 0,
      questionResponses: {},
      gradedResponses: [],
      graded: false,
      userScore: 0,
      totalPoints: 0
    };
  },
  computed: {
    allAnswered() {
      let gradeReady = true;
      this.userResponses.forEach(response => {
        console.log(response);
        if (response.length < 1) {
          console.log("HELLO!");
          gradeReady = false;
        }
      });
      return gradeReady;
    }
    // correctCount(){
    //   let correct = 0;
    //   this.questionSet.forEach(element => {
    //     if
    //   });
    // },
  },
  methods: {
    // Initialize a Response Object
    // Loop Through Array to Calculate things
    // Set Current Question
    // Send Current Question info to Prop Item
    // Determin correct, and Provide Feedback
    // Proceed to Next Question
    // Go to next question
    resetQuiz() {
      this.userResponses = Array(this.questionSet.length).fill([]);
      this.graded = false;
      this.answersLocked = false;
      this.answersSubmitted = false;
      this.currentQuestion = 0;
      this.userScore = 0;
      this.totalPoints = 0;
    },
    loadNextQuestion() {
      this.currentQuestion++;
    },
    // Go to previous question
    loadPreviousQuestion() {
      this.currentQuestion--;
    },
    // Return "true" count in userResponses
    gradeQuiz() {
      this.totalPoints = this.questionSet.length;
      this.userScore = 0;
      this.questionSet.forEach((question, index) => {
        let gradedResponse = {
          correct: "",
          points: 0,
          responseStyle: "",
          question: {
            text: "",
            alternatives: [],
            answer_key: []
          },
          gradedAlternatives: []
        };
        var alternativePoints = 0;
        // First, determine if the question is multiple choice or multiple select
        if (question.select_type === "multiple") {
          // question is multiple select
          // loop through each answer to check for correct
          for (let i = 0; i < question.alternatives.length; i++) {
            var alternativeCorrect = Boolean;
            if (question.answer_key.includes(question.alternatives[i].key)) {
              // this alternative would be correct, now check if user selected it:
              if (
                this.userResponses[index].includes(question.alternatives[i].key)
              ) {
                // the user chose the correct answer
                alternativeCorrect = true;
                var userSelected = true;
              } else {
                alternativeCorrect = false;
                userSelected = false;
              }
            } else {
              if (
                this.userResponses[index].includes(question.alternatives[i].key)
              ) {
                alternativeCorrect = false;
                userSelected = true;
              } else {
                alternativeCorrect = true;
                userSelected = false;
              }
            }
            if (alternativeCorrect) {
              alternativePoints += 1;
              var alternativeStyle = "green";
            } else {
              alternativeStyle = "red";
            }
            gradedResponse.gradedAlternatives.push({
              correct: alternativeCorrect,
              style: alternativeStyle,
              userSelected: userSelected
            });
          }
          if (alternativePoints === question.alternatives.length) {
            gradedResponse.correct = true;
          } else {
            gradedResponse.correct = false;
          }
          gradedResponse.points =
            alternativePoints / question.alternatives.length;
          console.log(gradedResponse.points);
          this.gradedResponses.push(gradedResponse);
          this.userScore += gradedResponse.points;
        } else {
          // question is single select
          // determine if user's answer matches question key
          if (this.userResponses[index] === question.answer_key[0]) {
            gradedResponse.correct = true;
            gradedResponse.points = 1;
          } else {
            gradedResponse.correct = false;
            gradedResponse.points = 0;
          }
          console.log(gradedResponse.points);
          this.gradedResponses.push(gradedResponse);
          this.userScore += gradedResponse.points;
        }
      });
      this.graded = true;
    }
    // Random Quiz & Answers
  },
  mounted() {
    if (!this.questionSet) {
      this.questionSet = [
        {
          select_type: "multiple",
          stem: "Which of the following is/are non-essential nutrients?",
          stem_style: "ltr",
          alternatives_style: "ltr",
          alternatives: [
            {
              text: "pizza",
              key: "1",
              feedback:
                "a human can live for at least 100 years without pizza; it is not essential"
            },
            {
              text: "carbohydrates",
              key: "2",
              feedback:
                "despite what fascists say, the human body does not need carbohydrates"
            },
            {
              text: "fat",
              key: "3",
              feedback: "fat is essential"
            },
            {
              text: "protein",
              key: "4",
              feedback: "protein is essential"
            }
          ],
          answer_key: ["1", "2"],
          explanation:
            "Only protein and fat are essential; humans can get by without pizza and carbs!"
        },
        {
          select_type: "single",
          stem: "I am a tree.",
          stem_style: "ltr",
          alternatives_style: "ltr",
          alternatives: [
            {
              text: "true",
              key: "1",
              feedback: ""
            },
            {
              text: "false",
              key: "2",
              feedback: ""
            }
          ],
          answer_key: ["2"],
          explanation: "I am not a tree, I am a person."
        },
        {
          select_type: "single",
          stem: "شو اسمك يا كريم؟",
          stem_style: "rtl",
          alternatives_style: "rtl",
          alternatives: [
            {
              text: "كريم",
              key: "1",
              feedback: ""
            },
            {
              text: "يعقوب",
              key: "2",
              feedback: ""
            },
            {
              text: "عبدلله",
              key: "3",
              feedback: ""
            },
            {
              text: "ما فيه اسم",
              key: "4",
              feedback: ""
            }
          ],
          answer_key: ["1"],
          explanation: "You should know that your name is كريم!"
        }
      ];
    }
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this._keyListener);
  }
};
</script>
<style type="text/css"></style>
