<template>
  <v-container>
     <EventCalendar />

  </v-container>
</template>

<script>
import EventCalendar from "@/components/events/EventCalendar.vue";
export default {
  name: "Events",
  data() {
    return {
    }
  },
   components: {
    EventCalendar,
  }
}
</script>

<style>

</style>