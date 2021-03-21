<template>
  <div class="lessonlist">
    <v-btn
      v-show="next || loadingFavorites"
      @click="getFavorites"
      :loading="loadingFavorites"
      class="elements desertsand--text"
      block
    >
      Load More Favorites <v-icon right>mdi-chevron-down</v-icon>
    </v-btn>
    <v-overlay :value="loadingFavorites" absolute>
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>

    <v-list
      two-line
      dense
      subheader
      class="calligraphy overflow-y-auto"
      max-height="300"
    >
      <v-list-item
        v-for="favorite in favorites"
        :key="favorite.id"
        @click="
          $router.push({
            name: 'Learn-Stack',
            params: { slug: favorite.stackInfo.slug }
          })
        "
      >
        <v-list-item-avatar>
          <v-avatar class="mr-2" size="42">
            <v-img
              class="elevation-6"
              :src="favorite.stackInfo.curator['user_profile'].avatar"
            ></v-img>
          </v-avatar>

          <v-icon
            v-text="favorite.stackInfo.curator['user_profile'].avatar"
          ></v-icon>
        </v-list-item-avatar>

        <v-list-item-content class="desertsand--text">
          <v-list-item-title>{{ favorite.stackInfo.name }} </v-list-item-title>
          <v-list-item-subtitle class="sandstone--text"
            >Word Count: {{ favorite.stackInfo.lexeme_pairs.length }};
            {{ favorite.stackInfo.mastery }} % Mastery</v-list-item-subtitle
          >
          <v-list-item-subtitle> </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "FavoriteStackList",
  data() {
    return {
      favorites: [],
      loadingFavorites: false,
      next: null
    };
  },
  props: {},
  computed: {},

  methods: {
    calculateStats() {
      this.favorites.forEach(function(stack) {
        console.log(stack);
        let correct = 0;
        let attempts = 0;
        stack.stackInfo.lexeme_pairs.forEach(function(pair) {
          correct += pair.pair_learning.number_correct;
          attempts += pair.pair_learning.attempts;
          let percent = Math.round((correct / attempts) * 100);
          stack.stackInfo.mastery = percent;
          // console.log(pair.pair_learning);
          console.log(percent);
        });
        // calculutate average of all words
        // calculate most recent date observed
      });

      // for (stack in this.favorites) {
      //   // console.log(stack);
      //   console.log(this.favorites[stack]);
      //
      //   for (let pairs in this.favorites[stack]) {
      //     console.log(this.favorites[stack][pairs]);
      //   }
      //
      // }
      return true;
    },
    getFavorites() {
      let endpoint = `/api/vocab/favoritestackz/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingFavorites = true;
      apiService(endpoint).then(data => {
        if (data) {
          // console.log(data);
          this.favorites.push(...data.results);
          this.calculateStats();
          this.loadingFavorites = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
            this.loadingFavorites = false;
          }
        }
      });
    }
  },
  created() {
    this.getFavorites();
  }
};
</script>
