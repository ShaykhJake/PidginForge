<template>
  <div>
    <v-card>
      <v-toolbar class="desertsand calligraphy--text" dense>
        <v-toolbar-title
          >New Vocab Stacks
          <small v-if="totalCount > 0"
            >({{ stacks.length }} of {{ totalCount }} loaded)</small
          >
          <small v-else>(no results)</small>
        </v-toolbar-title>
        <v-spacer></v-spacer>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on" class="primary--text" @click="refreshList">
              <v-icon>refresh</v-icon>
            </v-btn>
          </template>
          <span>Refresh List</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              icon
              v-on="on"
              class="primary--text"
              :to="{
                name: 'Stacks-Viewer',
              }"
            >
              <v-icon>style</v-icon>
            </v-btn>
          </template>
          <span>Create a Stack</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              icon
              @click="showStacks = !showStacks"
              class="garbage--text"
            >
              <v-icon v-if="!showStacks">mdi-eye</v-icon>
              <v-icon v-if="showStacks">mdi-eye-off</v-icon>
            </v-btn>
          </template>
          <span v-if="!showStacks">View Stacks</span>
          <span v-else>Hide Stacks</span>
        </v-tooltip>
      </v-toolbar>

      <v-card-text v-show="showStacks" class="content-box calligraphy pa-1">
        <div class="stacklist">
          <v-row wrap dense v-if="stacks.length < 1 && !loadingStacks">
            <v-col cols="12">
              <v-card>
                <v-card-text class="desertsand calligraphy--text">
                  There are no stacks which match your language/topic
                  preferences. You may need to update your profile to add
                  learning languages and topics...or maybe we just don't have
                  enough content yet!
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-row dense wrap v-if="stacks.length > 0">
            <v-col
              cols="12"
              sm="6"
              md="4"
              lg="3"
              v-for="stack in stacks"
              :key="stack.id"
            >
              <StackMicro :stack="stack" />
            </v-col>
          </v-row>
          <v-btn
            v-if="next"
            @click="getStacks"
            :loading="loadingStacks"
            class="primary desertsand--text"
            block
          >
            Load More Stacks <v-icon right>mdi-chevron-down</v-icon>
          </v-btn>
          <v-overlay :value="loadingStacks" absolute>
            <v-progress-circular indeterminate size="64"></v-progress-circular>
          </v-overlay>
        </div>
      </v-card-text>
    </v-card>

    <!-- <StackEditor
        v-if="showStackEditor"
        :editor-dialog="showStackEditor"
        @closeDialog="showStackEditor = false"
      /> -->
  </div>
</template>

<script>
  import { apiService } from "@/common/api.service.js";
  import StackMicro from "@/components/vocab/StackMicro.vue";
  export default {
    name: "StackList",
    data() {
      return {
        stacks: [],
        next: null,
        totalCount: 0,
        loadingStacks: false,
        showStacks: true,
        addStackDialog: false,
        stackEditorLoaded: false,
        showStackEditor: false,
      };
    },
    components: {
      StackMicro,
    },
    computed: {},

    methods: {
      loadStackEditor() {
        console.log("trust");
        this.stackEditorLoaded = true;
        this.showStackEditor = !this.showStackEditor;
      },

      getStacks() {
        let endpoint = "/api/vocab/stacks/list/?by_preference=True";
        if (this.next) {
          endpoint = this.next;
        }
        this.loadingStacks = true;
        apiService(endpoint).then((data) => {
          this.totalCount = data.count;
          this.stacks.push(...data.results);

          this.loadingStacks = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
          }
        });
      },
      refreshList() {
        this.stacks = [];
        this.next = null;
        this.getStacks();
      },
    },
    created() {
      this.getStacks();
    },
  };
</script>
<style scoped></style>
