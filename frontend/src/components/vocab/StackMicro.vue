<template>
  <div class="stack-micro">
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card class="pa-0 desertsand">
          <v-card-text class="pa-0">
            <v-row dense class="ma-0 pa-0">
              <v-col cols="12" class="pa-0"> </v-col>
            </v-row>
          </v-card-text>
          <v-card-title class="py-1 desertsand">
            <v-row dense no-gutters>
              <v-col>
                <span class="overline">
                  <span class="primary--text font-weight-black">
                    {{ stack.curator.username }}</span
                  >
                  built on {{ stack.curationdate }}:
                </span>
              </v-col>
            </v-row>
          </v-card-title>

          <v-card-text class="pa-0">
            <v-row dense class="ma-0 pa-0">
              <v-col cols="auto pr-2">
                <v-avatar mx-2 size="48">
                  <v-img
                    class="elevation-6"
                    :src="
                      stack.curator.user_profile.avatar
                        ? stack.curator.user_profile.avatar
                        : 'https://jakesdesk-media.s3.amazonaws.com/media/public/avatars/default.jpg'
                    "
                  ></v-img>
                </v-avatar>
              </v-col>

              <v-col>
                <p class="subtitle-2 black--text">{{ stack.name }}</p>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-title>
            <v-row dense no-gutters>
              <v-col align="center">
                <p class="overline font-weight-light mb-0">
                  <span class="languages--text">
                    {{ stack.learning_language }} &#8594;
                    {{ stack.native_language }}
                  </span>
                  <br />
                </p>
                <p class="primary--text overline mb-0">
                  {{ stack.pair_count }} Word Pairs
                </p>
              </v-col>
            </v-row>
          </v-card-title>

          <v-fade-transition>
            <v-overlay v-if="hover" absolute color="calligraphy" opacity="0.75">
              <v-btn
                block
                class="mb-2 primary"
                :to="{
                  name: 'Learn-Stack',
                  params: { slug: stack.slug }
                }"
                >View Stack <v-icon right>style</v-icon></v-btn
              >
              <v-btn
                block
                class="mb-2 saves"
                @click="toggleSave"
                :loading="saving"
              >
                <span :hidden="stack.user_has_saved"
                  >Save Stack<v-icon right>mdi-heart</v-icon></span
                >
                <span :hidden="!stack.user_has_saved"
                  >Unsave Stack<v-icon right>mdi-heart-broken</v-icon></span
                >
              </v-btn>
            </v-overlay>
          </v-fade-transition>
        </v-card>
      </template>
    </v-hover>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "StackMicro",
  props: {
    stack: Object
  },
  data() {
    return {
      loading: false,
      overlay: false,
      saving: false
    };
  },
  computed: {},

  methods: {
    // Get Current User
    // Save / Unsave Item
    toggleSave() {
      this.saving = true;
      let endpoint = `api/vocab/stacks/save/`;
      try {
        apiService(endpoint, "POST", { slug: this.stack.slug }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // this.$emit("hideElement")
              this.stack.user_has_saved = data.saved;
              if (this.stack.user_has_saved) {
                this.stack.saved_count += 1;
              } else {
                this.stack.saved_count -= 1;
              }
              // console.log(data.message)
            } else {
              // this.alertType = 'error';
            }
          } else {
            // this.alertType = 'error';
          }
          this.saving = false;
        });
      } catch (err) {
        console.log(err);
      }
    }
  }
};
</script>
<style scoped>
a {
  text-decoration: none;
}
.cardimg {
  opacity: 1;
}
</style>
