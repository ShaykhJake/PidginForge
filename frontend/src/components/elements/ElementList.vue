<template>
  <div>
    <v-row justify-center dense wrap>
      <v-col cols="12">
        <v-card>
          <v-toolbar class="desertsand calligraphy--text" dense>
            <v-toolbar-title
              >New Learning Elements
              <small v-if="totalCount > 0"
                >({{ elements.length }} of {{ totalCount }} loaded)</small
              >
              <small v-else>(no results)</small>
            </v-toolbar-title>
            <v-spacer></v-spacer>

            <!-- <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                      <v-btn
                        icon
                        v-on="on"
                        @click="videoPreferenceFilter = !videoPreferenceFilter"
                        :class="
                          !videoPreferenceFilter ? 'elements--text' : 'elements'
                        "
                      >
                        <v-icon>filter_list</v-icon>
                      </v-btn>
                    </template>
                    <span>Filter By Preferences</span>
                  </v-tooltip> -->

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" icon @click="refreshList">
                  <v-icon color="elements">refresh</v-icon>
                </v-btn>
              </template>
              <span>Refresh List</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" icon @click="showElementEditor = true">
                  <v-icon color="elements">library_add</v-icon>
                </v-btn>
              </template>
              <span>Add Element</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  v-on="on"
                  icon
                  @click="showElements = !showElements"
                  class="garbage--text"
                >
                  <v-icon v-if="!showElements">mdi-eye</v-icon>
                  <v-icon v-if="showElements">mdi-eye-off</v-icon>
                </v-btn>
              </template>
              <span v-if="!showElements">View Elements</span>
              <span v-else>Hide Elements</span>
            </v-tooltip>
          </v-toolbar>

          <v-card-text
            v-show="showElements"
            class="content-box calligraphy pa-1"
          >
            <div>
              <div class="element-list">
                <v-row
                  wrap
                  dense
                  v-if="elements.length < 1 && !loading"
                >
                  <v-col cols="12">
                    <v-card>
                      <v-card-text class="desertsand calligraphy--text">
                        There are no elements which match your language
                        preferences. You may need to update your profile to add
                        learning languages...or maybe we just don't
                        have enough content yet!
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
                <v-row wrap dense v-if="elements.length < 0 && !loading">
                  <v-col cols="12">
                    <v-card>
                      <v-card-text class="desertsand calligraphy--text">
                        There are no elements which match your language/topic
                        preferences. You may need to update your profile to add
                        learning languages and topics...or maybe we just don't
                        have enough content yet!
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
                <v-row wrap dense v-if="elements.length > 0">
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                    lg="3"
                    v-for="element in elements"
                    :key="element.id"
                  >
                    <ElementMicro
                      :element="element"
                      :hidden="element.user_has_hidden"
                      @hideElement="element.user_has_hidden = true"
                    />
                  </v-col>
                </v-row>
                <v-btn
                  v-show="next"
                  @click="getElements"
                  :loading="loading"
                  class="elements desertsand--text"
                  block
                >
                  Load More Elements <v-icon right>mdi-chevron-down</v-icon>
                </v-btn>
                <v-overlay :value="loading" absolute>
                  <v-progress-circular
                    indeterminate
                    size="64"
                  ></v-progress-circular>
                </v-overlay>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <ElementEditor
      v-if="showElementEditor"
      :editor-dialog="showElementEditor"
      :is-new-element="true"
      @closeDialog="showElementEditor = false"
    />
  </div>
</template>

<script>
  import { apiService } from "@/common/api.service.js";
  import ElementMicro from "@/components/elements/ElementMicro.vue";
  export default {
    name: "ElementList",
    components: {
      ElementMicro,
      ElementEditor: () =>
        import(
          /* webpackPrefetch: true */ "@/components/elements/ElementEditor.vue"
        ),
    },
    data() {
      return {
        elements: [],
        totalCount: 0,
        loading: false,
        next: null,
        showElements: true,
        showElementEditor: false,
      };
    },
    props: {
      preferenceFilter: {
        required: false,
        default: false,
      },
    },
    computed: {
      filteredElements() {
        if (this.preferenceFilter) {
          return this.elements.filter((element) => {
            return !element.filtered;
          });
        } else {
          return this.elements;
        }
      },
      filteredCount() {
        let list = this.filteredElements;
        return list.length;
      },
    },

    methods: {
      getElements() {
        let endpoint = `/api/elements/list/?by_preference=True`;
        if (this.next) {
          endpoint = this.next;
        }
        this.loading = true;
        apiService(endpoint).then((data) => {
          this.totalCount = data.count;
          this.elements.push(...data.results);
          this.loading = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
          }
        });
      },
      refreshList() {
        this.elements = [];
        this.next = null;
        this.getElements();
      },
    },
    created() {
      this.getElements();
    },
  };
</script>
