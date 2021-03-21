<template>
  <div class="lessonlist">
    <v-card>
      <v-card-title class="sandstone pa-1">
        Saved Elements <v-spacer></v-spacer>
        <small>({{ favorites.length }} of {{ totalCount }} loaded)</small>
      </v-card-title>
      <v-card-text class="calligraphy pa-0">
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
                name: 'Element-Viewer',
                params: {
                  slug: favorite.slug
                }
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
        <v-btn
          v-if="next"
          @click="getFavorites"
          :loading="loadingFavorites"
          class="elements desertsand--text"
          block
        >
          Load More<v-icon right>mdi-chevron-down</v-icon>
        </v-btn>
        <v-overlay :value="loadingFavorites" absolute>
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "SavedElementList",
  data() {
    return {
      favorites: [],
      loadingFavorites: false,
      totalCount: 0,
      next: null
    };
  },
  props: {},
  computed: {},

  methods: {
    getFavorites() {
      let endpoint = `/api/elements/list/?saved=True`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingFavorites = true;
      apiService(endpoint).then(data => {
        if (data) {
          this.totalCount = data.count;
          this.favorites.push(...data.results);
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
