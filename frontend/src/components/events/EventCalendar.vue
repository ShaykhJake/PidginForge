<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64" color="desertsand">
        <v-toolbar flat color="desertsand">
          <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
            Today
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="next">
            <v-icon small>mdi-chevron-right</v-icon>
          </v-btn>
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn outlined class="primary--text" @click="selectedEvent={}; showEventEditor=true">Add Event<v-icon right>mdi-plus-box</v-icon></v-btn>
          <v-spacer></v-spacer>
          <v-menu bottom right>
            <template v-slot:activator="{ on }">
              <v-btn
                outlined
                color="grey darken-2"
                v-on="on"
              >
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>mdi-menu-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>Day</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>Week</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>Month</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>4 days</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>
      <v-sheet height="600">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
          :event-color="getEventColor"
          :now="today"
          :type="type"
          @click:event="showEvent"
          @click:more="viewDay"
          @click:date="viewDay"
          @change="updateRange"
        ></v-calendar>
        <v-menu
          v-if="selectedElement"
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
          max-width="275"
        >
          <v-card
            color="desertsand"
            min-width="250px"
            flat
          >
            <v-toolbar
              :color="getEventColor(selectedEvent)" 
              class="desertsand--text"
              dense
            >
              <v-btn v-if="isCurator" icon class="desertsand--text">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn icon class="desertsand--text">
                <v-icon v-if="selectedElement.user_has_saved">mdi-heart-broken</v-icon>
                <v-icon v-else>mdi-heart</v-icon>
              </v-btn>

              <v-btn icon disabled>
                <v-icon>mdi-eye-off</v-icon>
              </v-btn>
              <v-btn icon disabled>
                <v-icon>mdi-flag</v-icon>
              </v-btn>

            </v-toolbar>
            <v-card-text color="desertsand">
              Added by {{ selectedEvent.curator['username'] }} on {{ selectedEvent.curationdate }}<hr>
               <v-chip x-small outlined class="primary primary--text mr-1">Event Type: {{ selectedEvent.type }}</v-chip>
               <v-chip x-small outlined class="languages languages--text mr-1">Language Pair: {{ selectedEvent.native_language }} &#8594; {{ selectedEvent.target_language}}</v-chip>
               <v-chip x-small outlined class="topics topics--text mr-1">Topic Area: {{ selectedEvent.topic }}</v-chip>
               <v-chip x-small outlined class="garbage garbage--text mr-1">Access: {{selectedEvent.access_type }}</v-chip><br>              <hr>
              <h2> {{ selectedEvent.name }}</h2>
              <p>{{ selectedEvent.caption }}</p>
              Location: {{ selectedEvent.location }}<br>
              Starting: {{ selectedEvent.start }}<br>
              Ending: {{ selectedEvent.end }}<br>
              Invited #: {{ selectedEvent.guest_list_count }}
              RSVP'd #: {{ selectedEvent.rsvp_list_count }}

            </v-card-text>
            <v-card-actions>
              <v-btn
                text
                color="garbage desertsand--text"
                @click="selectedOpen = false"
              >
                Close<v-icon right>mdi-cancel</v-icon>
              </v-btn>

              <v-btn
                text
                color="primary desertsand--text"
                @click="showEventEditor = true"
              >
                Details
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
    <EventEditor
      v-if="showEventEditor"
      @updateViewer="updateViewer"
      :scheduled-event="selectedEvent.curator ? selectedEvent : null"
      :editor-dialog="showEventEditor"
      @closeDialog="showEventEditor=false"
    />
  </v-row>
</template>

<script>
   import { apiService } from "@/common/api.service.js";
  import EventEditor from "@/components/events/EventEditor.vue";

  export default {
    data: () => ({
      showEventEditor: false,
      focus: '',
      type: 'month',
      typeToLabel: {
        month: 'Month',
        week: 'Week',
        day: 'Day',
        '4day': '4 Days',
      },
      start: null,
      end: null,
      today : new Date().toISOString().substr(0, 10),
      selectedEvent: {},
      selectedElement: null,
      selectedOpen: false,
      eventsList: {},


      colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
      // names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
      events: [
            { color: "cyan",
              name: "fun",
              type: "conference",
              start: "2020-4-8 18:45",
              end: "2020-4-8 19:45",
              caption: "Gonna have lots of fun",
              access_type: "Public",
              curator: "ShaykhJake",
              curationdate: "2020-4-30",
              native_language: "English",
              target_language: "Arabic-MSA",
              topic: "Economics",
              user_has_access: "false",
              follower_count: "5",
              study_group: "coolrussians",

              details: "Gonna party hard!",
              hyperlink: "<a href='http://www.google.com' target='_blank'>Link to Event</a>"
            },
            { color: "cyan",
              name: "Important",
              type: "meeting",
              start: "2020-4-15 18:45",
              end: "2020-4-17 19:45",
              caption: "Gonna have lots of fun",
              access_type: "Invitation",
              curator: "Jeff",
              curationdate: "2020-4-30",
              native_language: "English",
              target_language: "Arabic-MSA",
              topic: "Economics",
              user_has_access: "false", // this is based on whether the event is public, user has been invited, or user is part of a group
              follower_count: "5",
              study_group: "coolrussians",

              details: "Gonna party hard!",
              hyperlink: "<a href='http://www.google.com' target='_blank'>Link to Event</a>"
            }
         ]
    }),
    components: {
       EventEditor,
    },
    computed: {
      title () {
        const { start, end } = this
        if (!start || !end) {
          return ''
        }

        const startMonth = this.monthFormatter(start)
        const endMonth = this.monthFormatter(end)
        const suffixMonth = startMonth === endMonth ? '' : endMonth

        const startYear = start.year
        const endYear = end.year
        const suffixYear = startYear === endYear ? '' : endYear

        const startDay = start.day + this.nth(start.day)
        const endDay = end.day + this.nth(end.day)

        switch (this.type) {
          case 'month':
            return `${startMonth} ${startYear}`
          case 'week':
          case '4day':
            return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`
          case 'day':
            return `${startMonth} ${startDay} ${startYear}`
        }
        return ''
      },
      activeUser() {
         return window.localStorage.getItem("username");
      },
      isCurator() {
         return this.selectedEvent.curator == this.activeUser
      },

      monthFormatter () {
        return this.$refs.calendar.getFormatter({
          timeZone: 'UTC', month: 'long',
        })
      },
    },
    mounted () {
      this.$refs.calendar.checkChange();
      this.getEventsList();
    },
    methods: {

      getEventsList() {
         this.loadingEvents = true;
         let endpoint = `/api/events/eventz/`;
         try {
         apiService(endpoint).then(data => {
            if (data != null) {
               this.eventsList = data;
               this.events= data;
               console.log(this.eventsList)
            } else {
               console.log("Something bad happened...");
               this.error = true;
            }
            this.loadingEvents = false;
         });
         } catch (err) {
         console.log(err);
         }
      },

      viewDay ({ date }) {
        this.focus = date
        this.type = 'day'
      },
      getEventColor (event) {
      //   let eventType = event.type;
        var typeToColorMap = {
           Holiday: "elements",
           Meeting: "primary",
           Performance: "blue",
           Conference: "languages",
           Studysession: "topics",
           Lecture: "garbage",
        }
         return typeToColorMap[event.event_type] || 'primary'

         // return event.color
      },
      setToday () {
        this.focus = this.today
      },
      prev () {
        this.$refs.calendar.prev()
      },
      next () {
        this.$refs.calendar.next()
      },
      showEvent ({ nativeEvent, event }) {
        const open = () => {
          this.selectedEvent = event
          this.selectedElement = nativeEvent.target
          setTimeout(() => this.selectedOpen = true, 10)
        }

        if (this.selectedOpen) {
          this.selectedOpen = false
          setTimeout(open, 10)
        } else {
          open()
        }

        nativeEvent.stopPropagation()
      },
      addEvent () {
         
      },
      getEvents() {

      },
      updateViewer(newEvent) {
         this.events.push(newEvent);
      },
      updateRange ({ start, end }) {
         console.log(this.events)
        this.start = start
        this.end = end
      },
      nth (d) {
        return d > 3 && d < 21
          ? 'th'
          : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
      },
      rnd (a, b) {
        return Math.floor((b - a + 1) * Math.random()) + a
      },
      formatDate (a, withTime) {
        return withTime
          ? `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}`
          : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
      },
    },
  }
</script>

<style>

</style>