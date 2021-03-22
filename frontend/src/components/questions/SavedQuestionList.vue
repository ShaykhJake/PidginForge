<template>
  <div class="question">
    <v-card elevation="5">
      <v-card-title class="sandstone pa-1">
        Saved Questions
        <v-spacer />
        <small> ({{ favorites.length }} of {{ totalCount }} loaded) </small>
      </v-card-title>
      <v-card-text class="calligraphy pa-0">
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
                name: 'Question-Viewer',
                params: {
                  slug: favorite.slug,
                },
              })
            "
          >
            <v-list-item-avatar>
              <v-avatar class="mr-2" size="42">
                <v-img
                  class="elevation-6"
                  :src="favorite.author.user_profile.avatar"
                ></v-img>
              </v-avatar>

              <v-icon v-text="favorite.author.user_profile.avatar"></v-icon>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ favorite.title }} </v-list-item-title>

              <v-list-item-subtitle class="elements--text">
                <v-chip small color="languages" class="mr-2" outlined>{{
                  favorite.learninglanguage
                }}</v-chip>
              </v-list-item-subtitle>
              <v-list-item-subtitle>
                <v-chip
                  v-for="tag in favorite.tags"
                  :key="tag.uuid"
                  small
                  color="tags"
                  outlined
                  class="mr-1"
                  >{{ tag }}</v-chip
                >
              </v-list-item-subtitle>
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
    name: "SavedQuestionList",
    data() {
      return {
        totalCount: 0,
        favorites: [],
        loadingFavorites: false,
        next: null,
      };
    },
    props: {},
    computed: {},

    methods: {
      getFavorites() {
        let endpoint = `/api/questions/list/?saved=True`;
        if (this.next) {
          endpoint = this.next;
        }
        this.loadingFavorites = true;
        apiService(endpoint).then((data) => {
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
      },
    },
    created() {
      this.getFavorites();
    },
  };
</script>
<style scoped></style>
