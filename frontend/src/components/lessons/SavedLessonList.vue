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
      max-height="250"
      height="250"
    >
      <v-list-item
        v-for="favorite in favorites"
        :key="favorite.id"
        @click="
          $router.push({
            name: 'Lesson-Viewer',
            params: { lessonslug: favorite.slug }
          })
        "
      >
        <v-list-item-avatar>
          <v-avatar class="mr-2" size="42">
            <v-img
              class="elevation-6"
              :src="favorite.curator['user_profile'].avatar"
            ></v-img>
          </v-avatar>

          <v-icon v-text="favorite.curator['user_profile'].avatar"></v-icon>
        </v-list-item-avatar>

        <v-list-item-content class="desertsand--text">
          <v-list-item-title>{{ favorite.title }} </v-list-item-title>
          <v-list-item-subtitle class="sandstone--text"
            >#TODO</v-list-item-subtitle
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
  name: "SavedLessonList",
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
    getFavorites() {
      let endpoint = `/api/lessons/saved/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingFavorites = true;
      apiService(endpoint).then(data => {
        if (data) {
          this.favorites.push(...data);
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
<style scoped></style>
