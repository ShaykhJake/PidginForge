<template>
  <div class="single-answer">
    <p class="text-muted">
      <strong>{{ answer.author.username }}</strong> &#8901;
      {{ answer.created_at }}
    </p>
    <p>{{ answer.body }}</p>
    <div v-if="isAnswerAuthor">
      <v-btn
        class="success"
        router
        :to="{ name: 'Answer-Editor', params: { id: answer.id } }"
        ><v-icon>edit</v-icon>Edit</v-btn
      >
      <v-btn class="error" @click="triggerDeleteAnswer"
        ><v-icon>delete_forever</v-icon>Delete</v-btn
      >
    </div>
    <div v-else>
      <v-btn
        small
        fab
        class="deep-orange darken-4"
        @click="toggleLike"
        :class="{
          'deep-orange darken-4 white--text': userLikedAnswer,
          'deep-orange darken-4 text--black': !userLikedAnswer
        }"
      >
        <strong
          ><v-icon small>favorite</v-icon><span>{{ likesCounter }}</span>
        </strong>
      </v-btn>
    </div>
    <hr />
  </div>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "AnswerComponent",
  props: {
    answer: {
      type: Object,
      required: true
    },
    requestUser: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      userLikedAnswer: this.answer.user_has_voted,
      likesCounter: this.answer.likes_count
    };
  },
  computed: {
    isAnswerAuthor() {
      return this.answer.author.username === this.requestUser;
    }
  },
  methods: {
    toggleLike() {
      this.userLikedAnswer === false ? this.likeAnswer() : this.unlikeAnswer();
    },
    likeAnswer() {
      this.userLikedAnswer = true;
      this.likesCounter += 1;
      let endpoint = `/api/answers/${this.answer.id}/like/`;
      apiService(endpoint, "POST");
    },
    unlikeAnswer() {
      this.userLikedAnswer = false;
      this.likesCounter -= 1;
      let endpoint = `/api/answers/${this.answer.id}/like/`;
      apiService(endpoint, "DELETE");
    },
    triggerDeleteAnswer() {
      this.$emit("delete-answer", this.answer);
    }
  }
};
</script>
<style scoped></style>
