<template>
  <div>
    <v-card class="ma-0 pa-0" elevation="5">
      <v-card-title class="sandstone pa-1"
        >Saved Vocab
        <v-spacer />
        <small> ({{ favorites.length }} of {{ totalCount }} loaded) </small>
      </v-card-title>
      <v-card-text class="desertsand pa-0">
        <v-list
          two-line
          dense
          subheader
          class="desertsand overflow-y-auto"
          max-height="250"
          height="250"
        >
          <v-list-item
            v-for="favorite in favorites"
            :key="favorite.id"
            @click="
              $router.push({
                name: 'Learn-Stack',
                params: { slug: favorite.slug }
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

            <v-list-item-content>
              <v-list-item-title>{{ favorite.name }} </v-list-item-title>
              <v-list-item-subtitle class="calligraphy--text"
                >Word Count: {{ favorite.pair_count }};
                {{ favorite.stats.mastery }} % mastery of
                {{ favorite.pair_count }} cards seen.</v-list-item-subtitle
              >
              <v-list-item-subtitle>
                <v-chip color="languages" small outlined>
                  {{ favorite.learning_language }}
                  </v-chip> </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-btn
          v-show="next"
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
  name: "SavedStackList",
  data() {
    return {
      favorites: [],
      loadingFavorites: false,
      next: null,
      totalCount: 0
    };
  },
  props: {},
  computed: {},

  methods: {
    getFavorites() {
      let endpoint = `/api/vocab/stacks/list/?saved=True`;
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
