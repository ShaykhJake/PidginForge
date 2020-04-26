<template>
  <v-dialog v-model="profileDialog" scrollable max-width="275">
    <template v-slot:activator="{ on }">
      <a v-on="on">
        {{ username }}
      </a>
    </template>
    <ProfileSnippet
      v-if="profileDialog"
      :username="username"
      :avatar="avatar"
    />
  </v-dialog>
</template>

<script>
import ProfileSnippet from "@/components/profile/ProfileSnippet.vue";
export default {
  name: "ProfilePopup",
  components: {
    ProfileSnippet
  },
  props: {
    username: String,
    avatar: String,
    nameClass: {
      type: String,
      required: false
    }
  },
  data: () => ({
    profileDialog: false,
    menu: false
  })
};
</script>
<style scoped></style>
