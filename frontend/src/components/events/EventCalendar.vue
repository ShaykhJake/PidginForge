<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64" color="desertsand">
        <v-toolbar flat color="desertsand" class="pa-0">
          <v-btn outlined class="mr-3 d-none d-sm-flex" color="grey darken-2" @click="setToday">
            Today
          </v-btn>
          <v-btn outlined small class="mr-2 d-flex d-sm-none" color="grey darken-2" @click="setToday">
            Today
          </v-btn>

          <v-spacer></v-spacer>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small>mdi-chevron-left</v-icon>
          </v-btn>
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-btn fab text small color="grey darken-2" @click="next">
            <v-icon small>mdi-chevron-right</v-icon>
          </v-btn>
      
          <v-spacer></v-spacer>
          <v-btn outlined class="primary--text d-none d-sm-flex" @click="selectedEvent={}; showEventEditor=true">Add Event<v-icon right>mdi-plus-box</v-icon></v-btn>
          <v-btn icon fab class="primary--text d-flex d-sm-none" @click="selectedEvent={}; showEventEditor=true"><v-icon right>mdi-plus-box</v-icon></v-btn>
          <v-spacer></v-spacer>
          <v-menu bottom right>
            <template v-slot:activator="{ on }">
              <v-btn
                outlined
                color="grey darken-2"
                class="d-none d-sm-flex"
                v-on="on"
              >
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>mdi-menu-down</v-icon>
              </v-btn>
              <v-btn
                outlined
                small
                color="grey darken-2"
                class="d-flex d-sm-none"
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
          v-if="selectedElement && selectedOpen"
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
              Added by <span class="primary--text font-weight-black">{{ selectedEvent.curator['username'] }}</span> on {{ selectedEvent.curationdate }}<hr>
               <v-chip x-small outlined class="primary primary--text darken-2 mr-1">Event Type: {{ selectedEvent.event_type }}</v-chip>
               <v-chip x-small outlined class="languages languages--text mr-1">Language Pair: {{ selectedEvent.native_language }} &#8594; {{ selectedEvent.target_language}}</v-chip>
               <v-chip x-small outlined class="topics topics--text mr-1">Topic Area: {{ selectedEvent.topic }}</v-chip>
               <v-chip x-small outlined class="garbage garbage--text mr-1">Access: {{selectedEvent.public ? 'Public' : 'Invite Only' }}</v-chip><br>              <hr>
              <h2> {{ selectedEvent.name }}</h2>
              <p>{{ selectedEvent.caption }}</p>
              Location: {{ selectedEvent.location }}<br>
              Starting: {{ selectedEvent.start }}<br>
              Ending: {{ selectedEvent.end }}<br>
              Invited: {{ selectedEvent.guest_list.length }}
              Attending: {{ selectedEvent.rsvp_list_count }}

            </v-card-text>
            <v-card-actions class="sandstone">
              <v-btn
                text
                color="garbage desertsand--text"
                @click="selectedOpen = false"
              >
                Close<v-icon right>mdi-close</v-icon>
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                text
                color="primary desertsand--text"
                @click="showEventEditor = true"
              >
                View Details
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
    <EventEditor
      v-if="showEventEditor"
      @updateEvent="updateEvent"
      @addNewEvent="addNewEvent"
      @updateRSVP="updateRSVP"
      :scheduled-event="selectedEvent.curator ? selectedEvent : null"
      :editor-dialog="showEventEditor"
      @eventDeleted="popDeletedEvent"
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

      colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
      // names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
      events: [],
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
      formatLocalDateString(date){
         // 01, 02, 03, ... 29, 30, 31
         var dd = (date.getDate() < 10 ? '0' : '') + date.getDate();
         // 01, 02, 03, ... 10, 11, 12
         var MM = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);
         // 1970, 1971, ... 2015, 2016, ...
         var yyyy = date.getFullYear();
         // create the format you want
         return (`${yyyy}-${MM}-${dd}`);
      },
      formatLocalDateTimeString(date){
         // 01, 02, 03, ... 29, 30, 31
         var dd = (date.getDate() < 10 ? '0' : '') + date.getDate();
         // 01, 02, 03, ... 10, 11, 12
         var MM = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);
         // 1970, 1971, ... 2015, 2016, ...
         var yyyy = date.getFullYear();
         
         var hh = (date.getHours() < 10 ? '0' : '') + date.getHours();
         var mm = (date.getMinutes() < 10 ? '0' : '') + date.getMinutes();

         // create the format you want
         return (`${yyyy}-${MM}-${dd} ${hh}:${mm}`);
      },
      getEventsList() {
         this.loadingEvents = true;
         let endpoint = `/api/events/eventz/`;
         try {
         apiService(endpoint).then(data => {
            if (data != null) {
               this.eventsList = data;
               this.eventsList.forEach( event => {
                  this.addNewEvent(event);
               });
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
         if(event.event_type){
         var typeToColorMap = {
            "holiday": "elements",
            "meeting": "primary",
            "performance": "blue",
            "conference": "languages",
            "party": "green",
            "study session": "topics",
            "lecture": "garbage",
            "historical event": "calligraphy",
         }
            return typeToColorMap[event.event_type.toLowerCase()] || 'primary'
         } else {
            return 'primary'
         }
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
      getEvents() {

      },
      updateRSVP(rsvp) {
         let obj = this.events.find((o, i) => {
            if (o.id === rsvp.event) {
               this.events.splice(i,1);
               // arr[i] = { name: 'new string', value: 'this', other: 'that' };
               o.user_rsvp = rsvp;
               this.addNewEvent(o);
               return obj;
            }
         });
      },
      updateEvent(event) {
         let obj = this.events.find((o, i) => {
            if (o.slug === event.slug) {
               this.events.splice(i,1);
               // arr[i] = { name: 'new string', value: 'this', other: 'that' };
               this.addNewEvent(event);
               return obj; // stop searching
            }
         });
      },
      addNewEvent(newEvent) {
         var start = new Date(newEvent.start_datetime)
         var end = new Date(newEvent.end_datetime)
         if(newEvent.all_day){
            // newEvent.start = newEvent.start_datetime.substr(0,10)
            // newEvent.end = newEvent.start_datetime.substr(0,10)
            newEvent.start = this.formatLocalDateString(start)
            newEvent.end = this.formatLocalDateString(end)
         } else {
            // newEvent.start = `${newEvent.start_datetime.substr(0,10)} ${newEvent.start_datetime.substring(11,16)}`;
            // console.log(newEvent.start)
            // newEvent.end = `${newEvent.end_datetime.substr(0,10)} ${newEvent.end_datetime.substring(11,16)}`
            // console.log(newEvent.end)
            newEvent.start=this.formatLocalDateTimeString(start)
            newEvent.end=this.formatLocalDateTimeString(end)
         }
         this.events.push(newEvent);         
      },
      popDeletedEvent(slug){
         let obj = this.events.find((o, i) => {
            if (o.slug === slug) {
               this.events.splice(i,1);
               // arr[i] = { name: 'new string', value: 'this', other: 'that' };
               return obj; // stop searching
            }
         });
      },
      updateRange ({ start, end }) {
         // console.log(this.events)
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