<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="110" color="desertsand">
        <v-toolbar flat color="desertsand" class="pa-0">
          <v-btn
            outlined
            class="mr-3 d-none d-sm-flex"
            color="grey darken-2"
            @click="setToday"
          >
            Today
          </v-btn>
          <v-btn
            outlined
            dense
            small
            class="mr-0 d-flex d-sm-none"
            color="grey darken-2"
            @click="setToday"
          >
            Today
          </v-btn>

          <v-spacer></v-spacer>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small>mdi-chevron-left</v-icon>
          </v-btn>
          <v-toolbar-title class="px-1">{{ title }}</v-toolbar-title>
          <v-btn fab text small color="grey darken-2" @click="next">
            <v-icon small>mdi-chevron-right</v-icon>
          </v-btn>

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

        <v-toolbar dense flat color="calligraphy desertsand--text">
          <v-switch
            v-model="filtered"
            label="Filter"
            color="topics"
            class="mt-4 mr-2"
          ></v-switch>

          <v-btn
            @click="showFilterDialog = true"
            small
            outlined
            v-if="filtered"
            class="d-none d-sm-flex topics--text text--lighten-1"
            >Settings
            <v-badge
              color="topics darken-2 desertsand--text"
              :content="filteredEvents.length > 0 ? filteredEvents.length : '0'"
            >
              <v-icon>mdi-filter</v-icon>
            </v-badge>
          </v-btn>
          <v-btn
            @click="showFilterDialog = true"
            small
            icon
            v-if="filtered"
            class="d-flex d-sm-none topics--text text--lighten-1"
          >
            <v-badge
              color="topics darken-2 desertsand--text"
              :content="filteredEvents.length > 0 ? filteredEvents.length : '0'"
            >
              <v-icon>mdi-filter</v-icon>
            </v-badge>
          </v-btn>

          <v-spacer></v-spacer>
          <v-btn
            small
            outlined
            class="d-none d-sm-flex primary--text"
            @click="
              selectedEvent = {};
              showEventEditor = true;
            "
            >Add Event<v-icon right>mdi-plus-box</v-icon></v-btn
          >
          <v-btn
            small
            icon
            class="d-flex d-sm-none primary--text mr-1"
            @click="
              selectedEvent = {};
              showEventEditor = true;
            "
            ><v-icon>mdi-plus-box</v-icon></v-btn
          >
        </v-toolbar>
      </v-sheet>

      <v-sheet height="750">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="displayedEvents"
          :event-color="getEventColor"
          :event-overlap-mode="mode"
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
          <v-card color="desertsand" min-width="250px" flat>
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
              <div v-if="false">
                <v-btn icon class="desertsand--text">
                  <v-icon v-if="selectedElement.user_has_saved"
                    >mdi-heart-broken</v-icon
                  >
                  <v-icon v-else>mdi-heart</v-icon>
                </v-btn>

                <v-btn icon disabled>
                  <v-icon>mdi-eye-off</v-icon>
                </v-btn>
                <v-btn icon disabled>
                  <v-icon>mdi-flag</v-icon>
                </v-btn>
              </div>
            </v-toolbar>
            <v-card-text color="desertsand">
              Added by
              <span class="primary--text font-weight-black">{{
                selectedEvent.curator["username"]
              }}</span>
              on {{ selectedEvent.curationdate }}
              <hr />
              <v-chip
                x-small
                outlined
                class="primary primary--text darken-2 mr-1"
                >Event Type: {{ selectedEvent.event_type }}</v-chip
              >
              <v-chip x-small outlined class="languages languages--text mr-1"
                >Language Pair: {{ selectedEvent.native_language }} &#8594;
                {{ selectedEvent.target_language }}</v-chip
              >
              <v-chip x-small outlined class="topics topics--text mr-1"
                >Topic Area: {{ selectedEvent.topic }}</v-chip
              >
              <v-chip x-small outlined class="garbage garbage--text mr-1"
                >Access:
                {{ selectedEvent.public ? "Public" : "Invite Only" }}</v-chip
              ><br />
              <hr />
              <h2>{{ selectedEvent.name }}</h2>
              <p>{{ selectedEvent.caption }}</p>
              Location: {{ selectedEvent.location }}<br />
              Starting: {{ selectedEvent.start }}<br />
              Ending: {{ selectedEvent.end }}<br />
              Invited:
              {{
                selectedEvent.public
                  ? "Public"
                  : selectedEvent.guest_list.length
              }}<br />
              Attending: {{ selectedEvent.rsvp_list_count }}
            </v-card-text>
            <v-card-actions class="sandstone">
              <v-btn text color="garbage" @click="selectedOpen = false">
                Close<v-icon right>mdi-close</v-icon>
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="showEventEditor = true">
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
      @closeDialog="showEventEditor = false"
    />
    <FilterDialog
      v-if="showFilterDialog"
      @updateFilter="updateFilter"
      :filter-settings="filterSettings"
      v-bind:filterSettings.sync="filterSettings"
      :show-dialog="showFilterDialog"
      @closeDialog="showFilterDialog = false"
    />
    <v-col cols="12">
      <h2>Timeline View</h2>
      <v-timeline dense>
        <v-timeline-item
          v-for="timelineEvent in displayedEvents"
          :key="timelineEvent.id"
          small
        >
          <template v-slot:icon>
            <v-avatar>
              <img :src="timelineEvent.curator.user_profile.avatar" />
            </v-avatar>
          </template>
          <template v-slot:opposite>
            <span>{{ timelineEvent.start }}</span>
          </template>
          <v-card class="elevation-2">
            <v-card-title
              :class="`calligraphy desertsand--text subtitle-2 py-1`"
            >
              {{ prettyDate(timelineEvent.start_datetime) }}:
              {{ timelineEvent.name }}</v-card-title
            >
            <v-card-text class="desertsand">
              {{ timelineEvent.caption }}<br /><br />
              Location/Platform: {{ timelineEvent.location }}<br />
            </v-card-text>
            <v-card-actions dense class="calligraphy py-1">
              <v-btn
                @click="
                  selectedEvent = timelineEvent;
                  showEventEditor = true;
                "
                text
                small
                class="primary--text"
                >View Details</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-col>
  </v-row>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import EventEditor from "@/components/events/EventEditor.vue";
import FilterDialog from "@/components/events/FilterDialog.vue";

export default {
  name: "EventCalendar",
  data: () => ({
    showEventEditor: false,
    showFilterDialog: false,
    focus: "",
    type: "month",
    typeToLabel: {
      month: "Month",
      week: "Week",
      day: "Day",
      "4day": "4 Days"
    },
    start: null,
    end: null,
    filtered: false,
    filterSettings: {
      eventCurator: [],
      eventType: [],
      targetLanguage: [],
      nativeLanguage: [],
      byRSVP: false,
      topic: []
    },
    today: new Date().toISOString().substr(0, 10),
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    mode: "stack",
    colors: [
      "blue",
      "indigo",
      "deep-purple",
      "cyan",
      "green",
      "orange",
      "grey darken-1"
    ],
    // names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
    events: []
  }),
  components: {
    EventEditor,
    FilterDialog
  },
  computed: {
    title() {
      const { start, end } = this;
      if (!start || !end) {
        return "";
      }

      const startMonth = this.monthFormatter(start);
      const endMonth = this.monthFormatter(end);
      const suffixMonth = startMonth === endMonth ? "" : endMonth;

      const startYear = start.year;
      const endYear = end.year;
      const suffixYear = startYear === endYear ? "" : endYear;

      const startDay = start.day + this.nth(start.day);
      const endDay = end.day + this.nth(end.day);

      switch (this.type) {
        case "month":
          return `${startMonth} ${startYear}`;
        case "week":
        case "4day":
          return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`;
        case "day":
          return `${startMonth} ${startDay} ${startYear}`;
      }
      return "";
    },
    activeUser() {
      return window.localStorage.getItem("username");
    },
    isCurator() {
      return this.selectedEvent.curator == this.activeUser;
    },

    monthFormatter() {
      return this.$refs.calendar.getFormatter({
        timeZone: "UTC",
        month: "long"
      });
    },
    displayedEvents() {
      if (this.filtered) {
        return this.filteredEvents;
      } else {
        return this.events;
      }
    },
    filteredEvents() {
      console.log("Hello");
      var filter = this.filterSettings;
      return this.events.filter(event => {
        if (filter.byRSVP) {
          if (!event.user_rsvp || event.user_rsvp.attending === "Yes") {
            console.log("No results for RSVPs");
            return false;
          }
        }
        if (filter.eventCurator.length > 0) {
          if (!filter.eventCurator.includes(event.curator.username)) {
            console.log("No results for curators");
            return false;
          }
        }
        if (filter.eventType.length > 0) {
          if (!filter.eventType.includes(event.event_type.toLowerCase())) {
            console.log("No results for types");
            return false;
          }
        }
        if (filter.targetLanguage.length > 0) {
          if (!filter.eventType.includes(event.target_language)) {
            console.log("No results for target language");
            return false;
          }
        }
        if (filter.nativeLanguage.length > 0) {
          if (!filter.eventType.includes(event.native_language)) {
            console.log("No results for native language");
            return false;
          }
        }
        if (filter.topic.length > 0) {
          if (!filter.eventType.includes(event.topic)) {
            console.log("No results for topics");
            return false;
          }
        }

        return true;
      });
    }
  },
  methods: {
    formatLocalDateString(date) {
      // 01, 02, 03, ... 29, 30, 31
      var dd = (date.getDate() < 10 ? "0" : "") + date.getDate();
      // 01, 02, 03, ... 10, 11, 12
      var MM = (date.getMonth() + 1 < 10 ? "0" : "") + (date.getMonth() + 1);
      // 1970, 1971, ... 2015, 2016, ...
      var yyyy = date.getFullYear();
      // create the format you want
      return `${yyyy}-${MM}-${dd}`;
    },
    formatLocalDateTimeString(date) {
      // 01, 02, 03, ... 29, 30, 31
      var dd = (date.getDate() < 10 ? "0" : "") + date.getDate();
      // 01, 02, 03, ... 10, 11, 12
      var MM = (date.getMonth() + 1 < 10 ? "0" : "") + (date.getMonth() + 1);
      // 1970, 1971, ... 2015, 2016, ...
      var yyyy = date.getFullYear();

      var hh = (date.getHours() < 10 ? "0" : "") + date.getHours();
      var mm = (date.getMinutes() < 10 ? "0" : "") + date.getMinutes();

      // create the format you want
      return `${yyyy}-${MM}-${dd} ${hh}:${mm}`;
    },
    getEventsList() {
      this.loadingEvents = true;
      let endpoint = `/api/events/eventz/`;
      try {
        apiService(endpoint).then(data => {
          if (data != null) {
            this.eventsList = data;
            this.eventsList.forEach(event => {
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
    prettyDate(ISOString) {
      var date = new Date(ISOString);
      return date.toLocaleDateString();
    },
    filteredCount() {
      let list = this.filteredElements;
      return list.length;
    },

    viewDay({ date }) {
      this.focus = date;
      this.type = "day";
    },
    updateFilter(newFilter) {
      this.filterSettings = newFilter;
      // console.log(this.filterSettings)
    },
    getEventColor(event) {
      //   let eventType = event.type;
      if (event.event_type) {
        var typeToColorMap = {
          holiday: "elements",
          meeting: "primary",
          performance: "blue",
          conference: "languages",
          party: "green",
          "study session": "topics",
          lecture: "garbage",
          "historical event": "calligraphy"
        };
        return typeToColorMap[event.event_type.toLowerCase()] || "primary";
      } else {
        return "primary";
      }
    },

    setToday() {
      this.focus = this.today;
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        setTimeout(() => (this.selectedOpen = true), 10);
      };

      if (this.selectedOpen) {
        this.selectedOpen = false;
        setTimeout(open, 10);
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
    getEvents() {},
    updateRSVP(rsvp) {
      let obj = this.events.find((o, i) => {
        if (o.id === rsvp.event) {
          this.events.splice(i, 1);
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
          this.events.splice(i, 1);
          // arr[i] = { name: 'new string', value: 'this', other: 'that' };
          this.addNewEvent(event);
          return obj; // stop searching
        }
      });
    },
    addNewEvent(newEvent) {
      var start = new Date(newEvent.start_datetime);
      var end = new Date(newEvent.end_datetime);
      if (newEvent.all_day) {
        // newEvent.start = newEvent.start_datetime.substr(0,10)
        // newEvent.end = newEvent.start_datetime.substr(0,10)
        newEvent.start = this.formatLocalDateString(start);
        newEvent.end = this.formatLocalDateString(end);
      } else {
        // newEvent.start = `${newEvent.start_datetime.substr(0,10)} ${newEvent.start_datetime.substring(11,16)}`;
        // console.log(newEvent.start)
        // newEvent.end = `${newEvent.end_datetime.substr(0,10)} ${newEvent.end_datetime.substring(11,16)}`
        // console.log(newEvent.end)
        newEvent.start = this.formatLocalDateTimeString(start);
        newEvent.end = this.formatLocalDateTimeString(end);
      }
      this.events.push(newEvent);
    },
    popDeletedEvent(slug) {
      let obj = this.events.find((o, i) => {
        if (o.slug === slug) {
          this.events.splice(i, 1);
          // arr[i] = { name: 'new string', value: 'this', other: 'that' };
          return obj; // stop searching
        }
      });
    },
    updateRange({ start, end }) {
      // console.log(this.events)
      this.start = start;
      this.end = end;
    },
    nth(d) {
      return d > 3 && d < 21
        ? "th"
        : ["th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th"][d % 10];
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
    formatDate(a, withTime) {
      return withTime
        ? `${a.getFullYear()}-${a.getMonth() +
            1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}`
        : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`;
    }
  },
  mounted() {
    this.$refs.calendar.checkChange();
    this.getEventsList();
  }
};
</script>

<style>
.my-event {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  border-radius: 2px;
  background-color: #1867c0;
  color: #ffffff;
  border: 1px solid #1867c0;
  font-size: 12px;
  padding: 3px;
  cursor: pointer;
  margin-bottom: 1px;
  left: 4px;
  margin-right: 8px;
  position: relative;
}

.with-time {
  position: absolute;
  right: 4px;
  margin-right: 0px;
}
</style>
