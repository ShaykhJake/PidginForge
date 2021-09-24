<template>
    <div>
    <v-container class="pa-2 pt-2 mx-auto justify-center" fill-height fluid>
      <v-card width="100%" max-width=700 class="desertsand" flat>
        <v-card-title class="justify-center">Content Search
          <v-icon color="primary" @click="showPreferences=!showPreferences" class="ml-2">settings</v-icon> 
          </v-card-title>
        <v-card-text>
        <v-text-field
            label="Search"
            single-line
            solo
            append-outer-icon="mdi-magnify"
            v-model="searchString"
            @click:append-outer="submitSearch"
        ></v-text-field>
          <v-card v-show="showPreferences" class="mb-2">
            <v-card-title>
              Search Preferences
            </v-card-title>
            <v-card-text>
              - Language(s)
              <v-select>LANGUAGE</v-select>
              - Content Type(s)
              <v-select>CONTENT TYPE</v-select>
            </v-card-text>
          </v-card>
          <v-card v-if="!resultsExist && searchExecuted">
            Your search returned no results.
          </v-card>
          <v-card v-if="resultsExist && searchExecuted">
            <v-card-title>Results</v-card-title>
            <v-card-text>
              <ul id="sample-results">
                <li v-for="result in results" :key="result.id">
                  <h4><a :href="result.content.link">{{ result.content.title}}</a></h4>
                  <p>{{ result.content.summary }}</p>
                </li>
              </ul>

                <v-btn
                  v-show="next"
                  @click="loadMoreResults"
                  :loading="loadingMore"
                  class="elements desertsand--text"
                  block
                >
                  More results...
                <v-icon right>mdi-chevron-down</v-icon>
                </v-btn>

            </v-card-text>
          </v-card>
        </v-card-text>
                        <v-overlay :value="loadingResults" absolute>
                  <v-progress-circular
                    indeterminate
                    size="64"
                  ></v-progress-circular>
                </v-overlay>

      </v-card>

    </v-container>
  </div>
</template>
<script>

export default {
  name: "Search",
  data() {
    return {
      thinking: false,
      loadingResults: false,
      loadingMore: false,
      searchString: null,
      showPreferences: false,
      next: true,
      resultsExist: false,
      searchExecuted: false,
      results: [],
      results2: [
        { 
          id: 1, 
          content: {
            title: "Result 1",
            summary: "This is a cool result",
            link: "https://this.google.com",
          }
        },
        {
        id: 2, 
          content: {
            title: "Result 2",
            summary: "This is a cool result",
            link: "https://this.google.com",
          }
        }
      ],
    };
  },
  components: {
  },
  props: {
    initialQuery: {
      required: false,
    }
  },
  methods: {
    submitSearch(){
      if(this.searchString){
        this.searchExecuted = false;
        this.results.splice(0);
        console.log(this.searchString);
        this.loadingResults = true;
        this.next = false;
        setTimeout(() => {
          this.searchExecuted=true;
          this.loadingResults=false;
          this.next = true;
          this.results.push(...this.results2);
          this.results.length > 0 ? this.resultsExist = true : this.resultsExist = false;
        },
        1500)
      }
    },
    loadMoreResults(){
      this.loadingMore=true;
      // setTimeout(console.log("hello"), 3000)
      setTimeout(() => {
          this.loadingMore=false;
          const id = this.results.length + 1;
          const content = `Result ${id}`;
          this.results.push({ id: id, content: { title: content, summary: "Another cool result", link: "https://this.google.com" }})
        },
        1000)
    }
  },
  created() {},
  mounted() {
    if(this.initialQuery != null){
      this.searchExecuted = true;
      this.searchString = this.initialQuery;
      console.log(this.initialQuery);
      this.submitSearch;
    } else {
      this.searchExecuted = false;
    }
  }
};
</script>
<style scoped>
.content-box > * {
  width: 100%;
  max-height: 650px;
  overflow-x: hidden;
  overflow-x: auto;
  /* overflow-y: hidden; */
  /* overflow-x: auto; */

  position: relative;
  /* position: absolute; */
  /* width: 100%; */
}
</style>
