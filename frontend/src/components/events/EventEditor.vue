<template>
  <v-dialog
    v-model="editorDialog"
    scrollable
    persistent
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-card class="ma-0 desertsand" max-width="500">
      <v-card-title class="pb-1 calligraphy desertsand--text">
        <v-spacer></v-spacer>
        <span v-if="isNewEvent">Create New Event</span>
        <span v-else>Event: {{ this.newScheduledEvent.name }}</span>
        <v-spacer></v-spacer>
        <v-btn
          icon
          outlined
          color="garbage desertsand--text"
          @click="closeDialog"
          ><v-icon>mdi-close</v-icon></v-btn
        >
      </v-card-title>

      <v-card-text class="pa-5 desertsand">
        <v-row v-if="!editing">
          <v-col>
            <v-row dense>
              <v-col cols="auto">
                <v-avatar>
                  <v-img
                    class="elevation-6"
                    :src="
                      newScheduledEvent.curator.user_profile
                        ? newScheduledEvent.curator.user_profile.avatar
                        : 'https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/default.jpg'
                    "
                  ></v-img>
                </v-avatar>
              </v-col>
              <v-col>
                Added by
                <span class="primary--text font-weight-black"
                  >{{ newScheduledEvent.curator["username"] }}
                </span>
                on {{ prettyDate(newScheduledEvent.curationdate) }}
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <p>
                  <v-chip small outlined class="primary primary--text mr-1"
                    >Event Type: {{ newScheduledEvent.event_type }}</v-chip
                  >
                  <v-chip small outlined class="languages languages--text mr-1"
                    >Language Pair:
                    {{ newScheduledEvent.native_language }} &#8594;
                    {{ newScheduledEvent.target_language }}</v-chip
                  >
                  <v-chip small outlined class="topics topics--text mr-1"
                    >Topic Area: {{ newScheduledEvent.topic }}</v-chip
                  >
                  <v-chip small outlined class="garbage garbage--text mr-1"
                    >Access:
                    {{
                      newScheduledEvent.public ? "Public" : "Invitation Only"
                    }}</v-chip
                  ><br />
                </p>
                <h1>{{ newScheduledEvent.name }}</h1>
                <p>{{ newScheduledEvent.caption }}</p>
                <hr />
                Start Date/Time:
                <strong
                  >{{ displayStartDateTime
                  }}{{
                    newScheduledEvent.all_day ? " (all-day event)" : ""
                  }}</strong
                ><br />
                End Date/Time: <strong>{{ displayEndDateTime }}</strong
                ><br />
                Location: <strong>{{ newScheduledEvent.location }}</strong
                ><br />
                <hr />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-row wrap dense justify="center" v-if="editing">
          <v-col cols="12">
            <v-form ref="details" v-model="valid" @submit.prevent v-if="loaded">
              <v-text-field
                v-model="newScheduledEvent.name"
                name="eventname"
                label="Event Name*"
                placeholder="give this item a name (what is displayed on the calendar)"
                :rules="[rules.requiredTitle]"
                outlined
                class="pb-0 mb-0"
              ></v-text-field>

              <v-textarea
                outlined
                name="caption"
                label="Caption*"
                placeholder="a really fun event"
                v-model="newScheduledEvent.caption"
                :rules="[rules.requiredCaption]"
                counter
                rows="2"
                maxlength="200"
              ></v-textarea>

              <v-text-field
                v-model="newScheduledEvent.location"
                name="eventlocation"
                label="Event Location (or platform)*"
                placeholder="event location, platform, or region"
                :rules="[rules.requiredLocation]"
                outlined
                class="pb-0 mb-0"
              ></v-text-field>

              <v-row wrap dense>
                <v-col cols="12" sm="6">
                  <v-dialog
                    ref="daterangedialog"
                    v-model="dateRangeDialog"
                    :return-value.sync="workingDateRange"
                    persistent
                    width="290px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="displayDateRange"
                        label="Date(s)"
                        prepend-icon="event"
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="workingDateRange"
                      range
                      :locale="navigatorLocale"
                      :selected-items-text="displayDateRange"
                      @input="startDateMenu = false"
                    >
                      <v-spacer></v-spacer>
                      <v-btn
                        text
                        color="primary"
                        @click="dateRangeDialog = false"
                        >Cancel</v-btn
                      >
                      <v-btn
                        text
                        color="primary"
                        @click="$refs.daterangedialog.save(workingDateRange)"
                        >OK</v-btn
                      >
                    </v-date-picker>
                  </v-dialog>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-checkbox v-model="allDayEvent" label="All Day Event">
                  </v-checkbox>
                </v-col>

                <v-col v-if="!allDayEvent" cols="6" sm="4">
                  <v-dialog
                    ref="starttimedialog"
                    v-model="startTimeDialog"
                    :return-value.sync="workingStartTime"
                    persistent
                    width="290px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="workingStartTime"
                        label="Start Time"
                        prepend-icon="access_time"
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-time-picker
                      v-if="startTimeDialog"
                      v-model="workingStartTime"
                      full-width
                      format="24hr"
                      :max="maxTime"
                    >
                      <v-spacer></v-spacer>
                      <v-btn
                        text
                        color="garbage--text"
                        @click="startTimeDialog = false"
                        >Cancel</v-btn
                      >
                      <v-btn
                        text
                        color="primary"
                        @click="$refs.starttimedialog.save(workingStartTime)"
                        >OK</v-btn
                      >
                    </v-time-picker>
                  </v-dialog>
                </v-col>
                <v-col v-if="!allDayEvent" cols="6" sm="4">
                  <v-dialog
                    ref="endtimedialog"
                    v-model="endTimeDialog"
                    :return-value.sync="workingEndTime"
                    persistent
                    width="290px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="workingEndTime"
                        label="End Time"
                        prepend-icon="access_time"
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-time-picker
                      v-if="endTimeDialog"
                      v-model="workingEndTime"
                      full-width
                      format="24hr"
                      :min="minTime"
                    >
                      <v-spacer></v-spacer>
                      <v-btn
                        text
                        color="garbage--text"
                        @click="endTimeDialog = false"
                        >Cancel</v-btn
                      >
                      <v-btn
                        text
                        color="primary"
                        @click="$refs.endtimedialog.save(workingEndTime)"
                        >OK</v-btn
                      >
                    </v-time-picker>
                  </v-dialog>
                </v-col>
                <v-col cols="12">
                  <v-dialog v-model="timeZoneDialog" scrollable width="290px">
                    <template v-slot:activator="{ on }">
                      <v-btn v-on="on" text x-small class="primary--text mb-5">
                        Info About Dealing With Time Zones
                      </v-btn>
                    </template>
                    <v-card class="desertsand calligraphy--text">
                      <v-card-title class="sandstone">
                        Time Zones
                      </v-card-title>
                      <v-card-text>
                        <p class="body-1">
                          All dates and times are calculated based on your
                          operating system's locale.<br /><br />
                          These datetimes will automatically be converted to
                          GMT/UTC datetimes when stored on the server.<br /><br />
                          When displayed on the calendar, they will be converted
                          back from GMT/UTC into each user's local settings.<br /><br />
                          Please note that if you are storing datetimes for
                          timezones other than your own, you will need to know
                          the timezone offset relative to yours. <br /><br />
                          <strong>For example:</strong> If you live in New York,
                          but are entering an event that is taking place in
                          London at 17:00, you will need to enter 12:00, because
                          New York's time zone is 5 hours behind London.
                        </p>
                      </v-card-text>
                      <v-card-actions class="sandstone">
                        <v-spacer></v-spacer
                        ><v-btn
                          class="garbage desertsand--text"
                          @click="timeZoneDialog = false"
                          >Close</v-btn
                        >
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-col>
              </v-row>

              <v-autocomplete
                v-model="newScheduledEvent.event_type"
                name="eventtype"
                :items="allTypes"
                label="Event Type*"
                placeholder="choose event type"
                :rules="[rules.requiredType]"
                required
                :loading="loadingTypes"
                outlined
              ></v-autocomplete>

              <v-autocomplete
                v-model="newScheduledEvent.native_language"
                name="nativelanguage"
                :items="allLanguages"
                label="Native Language*"
                placeholder="choose a native language"
                :rules="[rules.requiredLanguage]"
                required
                :loading="loadingLanguages"
                outlined
              ></v-autocomplete>

              <v-autocomplete
                v-model="newScheduledEvent.target_language"
                name="targetlanguage"
                :items="allLanguages"
                label="Target Language*"
                placeholder="choose a target language"
                :rules="[rules.requiredLanguage]"
                required
                :loading="loadingLanguages"
                outlined
              ></v-autocomplete>

              <v-autocomplete
                v-model="newScheduledEvent.topic"
                name="eventtopic"
                :items="allTopics"
                label="Primary Topic*"
                placeholder="choose the primary topic"
                :rules="[rules.requiredTopic]"
                required
                :loading="loadingTopics"
                outlined
              ></v-autocomplete>
              <div justify="center">
                Event Access:
                <v-radio-group v-model="newScheduledEvent.public" row>
                  <v-radio label="Public" :value="true"></v-radio>
                  <v-radio label="Invitation Only" :value="false"></v-radio>
                </v-radio-group>
              </div>

              <v-autocomplete
                v-model="newScheduledEvent.guest_list"
                v-if="newScheduledEvent.public === false"
                :items="allProfiles"
                outlined
                chips
                color="blue-grey lighten-2"
                label="Invited Users"
                item-text="username"
                item-value="username"
                multiple
              >
                <template v-slot:selection="data">
                  <v-chip
                    color="primary"
                    v-bind="data.attrs"
                    :input-value="data.selected"
                    close
                    @click="data.select"
                    @click:close="removeGuest(data.item)"
                  >
                    <v-avatar left>
                      <v-img :src="data.item.avatar"></v-img>
                    </v-avatar>
                    {{ data.item.username }}
                  </v-chip>
                </template>
                <template v-slot:item="data">
                  <template v-if="typeof data.item !== 'object'">
                    <v-list-item-content
                      v-text="data.item"
                    ></v-list-item-content>
                  </template>
                  <template v-else>
                    <v-list-item-avatar>
                      <img :src="data.item.avatar" />
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title
                        v-html="data.item.username"
                      ></v-list-item-title>
                      <v-list-item-subtitle>{{
                        data.item.biography
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </template>
                </template>
              </v-autocomplete>

              <v-autocomplete
                v-model="newScheduledEvent.invited_groups"
                v-if="false"
                :items="userGroups"
                outlined
                chips
                color="blue-grey lighten-2"
                label="Invited Groups"
                item-text="name"
                item-value="name"
                multiple
              >
                <template v-slot:selection="data">
                  <v-chip
                    color="primary"
                    v-bind="data.attrs"
                    :input-value="data.selected"
                    close
                    @click="data.select"
                    @click:close="remove(data.item)"
                  >
                    <v-avatar left>
                      <v-img :src="data.item.avatar"></v-img>
                    </v-avatar>
                    {{ data.item.name }}
                  </v-chip>
                </template>
                <template v-slot:item="data">
                  <template v-if="typeof data.item !== 'object'">
                    <v-list-item-content
                      v-text="data.item"
                    ></v-list-item-content>
                  </template>
                  <template v-else>
                    <v-list-item-avatar>
                      <img :src="data.item.avatar" />
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title
                        v-html="data.item.name"
                      ></v-list-item-title>
                      <v-list-item-subtitle
                        >Language 1 - Language 2</v-list-item-subtitle
                      >
                    </v-list-item-content>
                  </template>
                </template>
              </v-autocomplete>
            </v-form>
          </v-col>
        </v-row>
        <v-row no-gutters dense class="mt-0 pt-0">
          <v-col>
            <span class="body-1">Extended Event Details:</span>
            <editor-menu-bar
              v-if="loaded && editing"
              :editor="editor"
              v-slot="{ commands, isActive }"
            >
              <div class="desertsand--text">
                <v-toolbar dense flat class="sandstone">
                  <v-btn
                    small
                    icon
                    color="calligraphy"
                    :class="{ 'is-active': isActive.bold() }"
                    @click="commands.bold"
                  >
                    <v-icon>
                      mdi-format-bold
                    </v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{ 'is-active': isActive.italic() }"
                    @click="commands.italic"
                  >
                    <v-icon>
                      mdi-format-italic
                    </v-icon>
                  </v-btn>
                  <v-divider class="mx-1" inset vertical></v-divider>
                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{ 'is-active': isActive.paragraph() }"
                    @click="commands.paragraph"
                  >
                    <v-icon>
                      mdi-format-paragraph
                    </v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                    @click="commands.heading({ level: 3 })"
                  >
                    <v-icon>
                      mdi-format-header-3
                    </v-icon>
                  </v-btn>

                  <v-divider class="mx-1" inset vertical></v-divider>

                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{
                      'is-active': isActive.alignment({ orientation: 'left' })
                    }"
                    @click="commands.alignment({ orientation: 'left' })"
                  >
                    <v-icon>
                      mdi-format-align-left
                    </v-icon>
                  </v-btn>

                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{
                      'is-active': isActive.alignment({
                        orientation: 'center'
                      })
                    }"
                    @click="commands.alignment({ orientation: 'center' })"
                  >
                    <v-icon>
                      mdi-format-align-center
                    </v-icon>
                  </v-btn>

                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{
                      'is-active': isActive.alignment({
                        orientation: 'right'
                      })
                    }"
                    @click="commands.alignment({ orientation: 'right' })"
                  >
                    <v-icon>
                      mdi-format-align-right
                    </v-icon>
                  </v-btn>

                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{
                      'is-active': isActive.text_direction({
                        direction: 'ltr'
                      })
                    }"
                    @click="commands.text_direction({ direction: 'ltr' })"
                  >
                    <v-icon>
                      mdi-format-textdirection-l-to-r
                    </v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{
                      'is-active': isActive.text_direction({
                        direction: 'rtl'
                      })
                    }"
                    @click="commands.text_direction({ direction: 'rtl' })"
                  >
                    <v-icon>
                      mdi-format-textdirection-r-to-l
                    </v-icon>
                  </v-btn>

                  <v-divider class="mx-1" inset vertical></v-divider>
                  <v-btn
                    color="calligraphy"
                    icon
                    @click="changeEditorFontSize('down')"
                  >
                    <v-icon>mdi-magnify-minus</v-icon>
                  </v-btn>
                  Text Size
                  <v-btn
                    icon
                    color="calligraphy"
                    @click="changeEditorFontSize('up')"
                  >
                    <v-icon>mdi-magnify-plus</v-icon>
                  </v-btn>

                  <v-divider class="mx-1" inset vertical></v-divider>
                  <v-spacer></v-spacer>
                  Count:
                  <span :class="characterCountClass">{{ characterCount }}</span>
                  / 500
                </v-toolbar>
              </div>
            </editor-menu-bar>
            <editor-content
              :editor="editor"
              :style="editorFontClass"
              :class="editing ? 'editor-box' : ''"
            />
          </v-col>
        </v-row>
        <v-row dense v-if="!isNewEvent">
          <v-col>
            <v-btn
              v-if="isCurator && !editing"
              @click="toggleEditable(true)"
              class="mr-2 primary desertsand--text mr-2 mt-1"
              >Edit<v-icon right>mdi-pencil</v-icon></v-btn
            >
            <v-btn
              v-if="isCurator"
              class="mr-2 garbage desertsand--text mt-1"
              @click="deleteConfirmDialog = true"
              >Delete Event<v-icon right>mdi-trash-can</v-icon></v-btn
            >
            <v-btn v-if="!isCurator" class="primary desertsand--text mr-2 mt-1"
              >Save<v-icon right>mdi-heart</v-icon></v-btn
            >
            <v-btn
              v-if="!isCurator"
              @click="showRSVPDialog = true"
              class="elements desertsand--text mr-2 mt-1"
              >RSVP
              <v-badge
                :content="newScheduledEvent.rsvp_list_count"
                color="elements darken-2"
              >
                <v-icon right>mdi-message-reply-text</v-icon>
              </v-badge>
            </v-btn>
            <v-btn
              v-if="isCurator"
              class="elements desertsand--text mr-2 mt-1"
              @click="createRecurrence"
              >Create Recurrence<v-icon right>mdi-redo</v-icon></v-btn
            >
            <v-btn
              class="topics desertsand--text mr-2 mt-1"
              @click="exportEvent"
              >Export<v-icon right>mdi-calendar-export</v-icon></v-btn
            >

            <v-dialog v-model="deleteConfirmDialog" width="290px">
              <v-card class="desertsand calligraphy--text">
                <v-card-title class="sandstone">
                  Confirm Delete Event?
                </v-card-title>
                <v-card-text>
                  <p class="body-1">
                    <strong
                      >Are you sure that you want to delete this event?</strong
                    >
                    <br /><br />It will be permanently deleted from the database
                    along with associated invitations, RSVPs, comments, and
                    what-not. <br /><br />
                    There is no harm in leaving this event on the calendar for
                    posterity!
                  </p>
                </v-card-text>
                <v-card-actions class="sandstone">
                  <v-btn
                    class="garbage desertsand--text"
                    @click="deleteConfirmDialog = false"
                  >
                    Cancel<v-icon right>mdi-close</v-icon>
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn
                    class="primary"
                    @click="deleteEvent"
                    :loading="deletingEvent"
                    >Delete<v-icon right>mdi-delete</v-icon></v-btn
                  >
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="calligraphy">
        <v-spacer></v-spacer>
        <v-btn
          v-if="editing"
          color="garbage desertsand--text"
          @click="closeDialog"
          >Cancel<v-icon right>mdi-close</v-icon></v-btn
        >
        <v-btn
          v-if="!editing"
          color="garbage desertsand--text"
          @click="closeDialog"
          >Close<v-icon right>mdi-close</v-icon></v-btn
        >
        <v-btn
          v-if="editing"
          color="success"
          @click="submitScheduledEvent"
          :disabled="!valid || !loaded || characterCount > 500"
          :loading="submittingEvent"
          >Submit<v-icon right>mdi-thumb-up</v-icon></v-btn
        >

        <v-spacer></v-spacer>
        <!-- TODO: need to ensure that the user information is reloaded after saving -->
      </v-card-actions>
    </v-card>
    <RSVPDialog
      v-if="showRSVPDialog"
      :show-dialog="showRSVPDialog"
      :rsvp-list="newScheduledEvent.rsvp_list"
      :user-rsvp="newScheduledEvent.user_rsvp"
      :event="newScheduledEvent.id"
      @closeDialog="showRSVPDialog = false"
      @updateRSVP="updateRSVP"
    />
    <iCalDownloader
      v-if="showExportDialog"
      :show-dialog="showExportDialog"
      :export-list="exportList"
      @closeDialog="showExportDialog = false"
    />
  </v-dialog>
</template>
<script>
import { apiService } from "@/common/api.service.js";
import RSVPDialog from "@/components/events/RSVPDialog.vue";
import { Editor, EditorContent, EditorMenuBar } from "tiptap";
import {
  Blockquote,
  HardBreak,
  Heading,
  Bold,
  Italic,
  Link,
  Strike,
  Underline
} from "tiptap-extensions";
import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";
import iCalDownloader from "@/components/events/iCalDownloader.vue";

export default {
  name: "EventEditor",
  components: {
    EditorContent,
    EditorMenuBar,
    RSVPDialog,
    iCalDownloader
  },
  props: {
    editorDialog: {
      type: Boolean,
      default: false
    },
    scheduledEvent: {
      type: Object,
      required: false
    }
  },
  data: () => ({
    // userData: Object,
    showRSVPDialog: false,
    unsavedChanges: false,
    editing: false,
    isNewEvent: false,
    allDayEvent: false,
    newScheduledEvent: {
      curator: {},
      avatar: {},
      public: true,
      guest_list: []
      //  invited_groups: [],
    },
    loaded: false,
    today: new Date().toString().substr(0, 10),
    existingSlug: "",
    existingTitle: "",
    submittingEvent: false,
    invitesList: [],
    //  start: new Date().toISOString().substr(0, 10),

    editableStartTime: "",
    startTimeDialog: false,
    editableEndTime: "",
    endTimeDialog: false,
    dateRangeDialog: false,

    workingStart: new Date(),
    workingEnd: new Date(),

    workingDateRange: [],
    workingStartTime: "",
    workingEndTime: "",
    displayStartDateTime: "",
    displayEndDateTime: "",

    timeZoneDialog: false,
    deleteConfirmDialog: false,
    deletingEvent: false,

    valid: true,
    success: false,
    allLanguages: [],
    loadingTypes: false,

    exportList: [],
    showExportDialog: false,

    loadingLanguages: false,
    loadingTopics: false,
    loadingProfiles: false,
    allUsers: [],
    loadingGroups: false,

    allTypes: [
      "Meeting",
      "Conference",
      "Study Session",
      "Lecture",
      "Holiday",
      "Historical Event",
      "Performance",
      "Party"
    ],
    //  userGroups: [
    //     { name: "Radical Russian", id: "1234" },
    //     { name: "Awesome Arabic", id: "1244" },
    //     { name: "Gnarly Norwegian", id: "1224" },
    //  ],
    //  allUsers: [
    //     { username: "ShaykhJake", comment: "Super stoked!", id: "33333", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
    //     { username: "Jeff", comment: "Can't wait!!", id: "33332", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
    //     { username: "Chad", comment: "Me too!", id: "33334", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
    //  ],
    guestList: [
      {
        username: "ShaykhJake",
        comment: "Super stoked!",
        id: "33333",
        avatar:
          "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"
      },
      {
        username: "Jeff",
        comment: "Can't wait!!",
        id: "33332",
        avatar:
          "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"
      },
      {
        username: "Chad",
        comment: "Me too!",
        id: "33334",
        avatar:
          "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"
      }
    ],
    allTopics: [],
    rules: {
      requiredTitle: value =>
        (value || "").length > 3 ||
        "Title length must be at least 4 characters.",

      requiredCaption: value =>
        (value || "").length > 3 ||
        "Caption length must be at least 4 characters.",

      requiredLocation: value =>
        (value || "").length > 3 ||
        "Location length must be least 4 characters.",

      requiredType: typevalue =>
        (typevalue || "").length > 0 || "You must choose an event type.",
      requiredLanguage: languagevalue =>
        (languagevalue || "").length > 0 || "You must choose a language.",
      requiredTopic: topicvalue =>
        (topicvalue || "").length > 0 || "You must choose a primary topic.",
      requiredCitation: citationvalue =>
        !!citationvalue || "You must provied a source citation."
    },
    editorFontSize: 1,
    editor: new Editor({
      editable: false,
      extensions: [
        new Blockquote(),
        new HardBreak(),
        new Heading({ levels: [3] }),
        new Bold(),
        new Alignment(),
        new TextDirection(),
        new Italic(),
        new Link(),
        new Strike(),
        new Underline()
      ],
      content: `
          ...type/paste event details in here...
         `
    })
  }),
  computed: {
    characterCountClass() {
      if (this.characterCount > 500) {
        return "error";
      } else {
        return "";
      }
    },
    navigatorLocale() {
      return window.navigator.language;
    },
    displayDateRange() {
      var optionsOne = {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric"
      };
      var optionsMany = { month: "short", day: "numeric", year: "numeric" };
      //  var options = { dateStyle: 'short' };
      if (this.workingDateRange && this.workingDateRange.length > 1) {
        // console.log(this.workingDateRange)
        var startDate = new Date(`${this.workingDateRange[0]}T00:00`);
        var endDate = new Date(`${this.workingDateRange[1]}T00:00`);
        // Check and correct date inversion
        if (this.workingDateRange[0] === this.workingDateRange[1]) {
          let oneDay = new Date(`${this.workingDateRange[0]}T00:00`);
          // console.log(window.navigator.language)
          return `${oneDay.toLocaleDateString(
            window.navigator.language,
            optionsOne
          )}`;
        } else if (startDate > endDate) {
          [this.workingDateRange[0], this.workingDateRange[1]] = [
            this.workingDateRange[1],
            this.workingDateRange[0]
          ];
          // console.log(true)
          var rangeString = `${endDate.toLocaleDateString(
            window.navigator.language,
            optionsMany
          )} - ${startDate.toLocaleDateString(
            window.navigator.language,
            optionsMany
          )}`;
          return rangeString;
        } else {
          rangeString = `${startDate.toLocaleDateString(
            window.navigator.language,
            optionsMany
          )} - ${endDate.toLocaleDateString(
            window.navigator.language,
            optionsMany
          )}`;
          return rangeString;
        }
      } else {
        let oneDay = new Date(`${this.workingDateRange[0]}T00:00`);
        //  console.log(window.navigator.language)
        return `${oneDay.toLocaleDateString(
          window.navigator.language,
          optionsOne
        )}`;
      }
    },
    minTime() {
      // Calculates the earliest time for the End Time
      if (this.isSingleDay()) {
        return this.editableStartTime;
      } else {
        return "00:00";
      }
    },
    maxTime() {
      if (this.isSingleDay()) {
        return this.editableEndTime;
      } else {
        return "23:59";
      }
    },
    activeUser() {
      return window.localStorage.getItem("username");
    },

    isCurator() {
      if (this.newScheduledEvent && this.newScheduledEvent.curator) {
        return this.newScheduledEvent.curator.username == this.activeUser;
      } else if (this.isNewEvent) {
        return true;
      } else {
        return false;
      }
    },
    editorFontClass() {
      return `font-size:${this.editorFontSize}em`;
    },
    characterCount() {
      return this.editor.view.state.doc.textContent.length;
    }
    // justText(){  // SAVE THIS FOR USING LATER!!!
    //   return this.editor.view.state.doc.textContent
    // }
  },
  methods: {
    prettyDate(ISOString) {
      var date = new Date(ISOString);
      return date.toLocaleDateString();
    },
    exportEvent() {
      this.exportList = [this.newScheduledEvent];
      this.showExportDialog = true;
    },
    updateRSVP(rsvp) {
      this.$emit("updateRSVP", rsvp);
      this.closeDialog();
    },
    removeGuest(item) {
      const index = this.newScheduledEvent.guest_list.indexOf(item.username);
      if (index >= 0) this.newScheduledEvent.guest_list.splice(index, 1);
    },
    isSingleDay() {
      if (this.workingDateRange && this.workingDateRange > 1) {
        const startDate = new Date(this.workingDateRange[0]);
        const endDate = new Date(this.workingDateRange[1]);
        return endDate > startDate ? false : true;
      } else {
        return true;
      }
    },
    formatNewDate(date, time) {
      var newDate = new Date(`${date}T${time}`);
      // console.log(newDate)
      return newDate;
    },
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
    formatLocalTimeString(date) {
      var hh = (date.getHours() < 10 ? "0" : "") + date.getHours();
      var mm = (date.getMinutes() < 10 ? "0" : "") + date.getMinutes();
      return `${hh}:${mm}`;
    },
    closeDialog() {
      this.$emit("closeDialog");
    },
    chooseNewFile() {
      this.loadNewFile = true;
    },
    toggleEditable(state) {
      this.editing = state;
      this.editor.setOptions({
        editable: this.editing
      });
    },

    changeEditorFontSize(direction) {
      if (direction === "up") {
        if (this.editorFontSize < 3.5) {
          this.editorFontSize += 0.15;
        }
      } else {
        if (this.editorFontSize > 0.5) {
          this.editorFontSize -= 0.15;
        }
      }
    },

    clearWarnings() {
      this.alertActive = false;
    },

    getLanguages() {
      var localLanguages = localStorage.getItem("languages");
      if (localLanguages.length > 1) {
        console.log("Shop local!");
        this.allLanguages = JSON.parse(localLanguages);
      } else {
        this.loadingLanguages = true;
        let endpoint = `/api/categories/languages/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allLanguages = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingLanguages = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },

    getTopics() {
      var localTopics = localStorage.getItem("topics");
      if (localTopics.length > 1) {
        console.log("Shop local!");
        this.allTopics = JSON.parse(localTopics);
      } else {
        this.loadingTopics = true;
        let endpoint = `/api/categories/topics/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allTopics = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingTopics = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },
    getProfileList() {
      var localProfileList = localStorage.getItem("profilelist");
      if (localProfileList.length > 1) {
        console.log("Shop local!");
        this.allProfiles = JSON.parse(localProfileList);
      } else {
        this.loadingProfiles = true;
        let endpoint = `/api/users/profilelist/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allProfiles = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingProfiles = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },

    parseInvites() {
      for (var user of this.newScheduledEvent.guest_list) {
        this.invitesList.push(user.invited_user);
      }
      // console.log(this.invitesList)
    },
    compileInvites() {
      let temp_invites = [];
      for (var username of this.invitesList) {
        temp_invites.push({ invited_user: username });
        // console.log(username);
      }
      // console.log(temp_invites);
      this.newScheduledEvent.guest_list = temp_invites;
    },

    deleteEvent() {
      if (this.newScheduledEvent.slug) {
        this.deletingEvent = true;
        let endpoint = `/api/events/eventz/${this.newScheduledEvent.slug}/`;
        try {
          apiService(endpoint, "DELETE").then(() => {
            this.deletingEvent = false;
            this.deleteConfirmDialog = false;
            this.closeDialog();
            this.$emit("eventDeleted", this.newScheduledEvent.slug);
          });
        } catch (err) {
          console.log(err);
          this.deletingEvent = false;
        }
      }
    },
    submitScheduledEvent() {
      this.submittingEvent = true;
      // Check for and format dates:
      if (this.allDayEvent) {
        this.workingStartTime = "00:00";
        this.workingEndTime = "00:00";
      }
      if (this.workingDateRange && this.workingDateRange.length > 1) {
        var newStart = this.formatNewDate(
          this.workingDateRange[0],
          this.workingStartTime
        );
        var newEnd = this.formatNewDate(
          this.workingDateRange[1],
          this.workingEndTime
        );
      } else if (this.workingDateRange) {
        newStart = this.formatNewDate(
          this.workingDateRange[0],
          this.workingStartTime
        );
        newEnd = this.formatNewDate(
          this.workingDateRange[0],
          this.workingEndTime
        );
      } else {
        this.submittingEvent = false;
        console.log("There is a problem with the form");
        return false;
      }
      let endpoint = `/api/events/eventz/`;
      let method = "POST";
      if (!this.isNewEvent) {
        method = "PATCH";
        endpoint = `/api/events/eventz/${this.newScheduledEvent.slug}/`;
      }
      // this.compileInvites()
      var payload = {
        name: this.newScheduledEvent.name,
        caption: this.newScheduledEvent.caption,
        // TODO - Need to do a bunch of work to ensure that Times & Dates are properly set in Zulu/GMT
        location: this.newScheduledEvent.location,
        start_datetime: newStart,
        end_datetime: newEnd,
        event_type: this.newScheduledEvent.event_type,
        native_language: this.newScheduledEvent.native_language,
        target_language: this.newScheduledEvent.target_language,
        topic: this.newScheduledEvent.topic,
        public: this.newScheduledEvent.public,
        details: this.editor.getJSON(),
        guest_list: this.newScheduledEvent.guest_list,
        all_day: this.allDayEvent
      };
      if (this.newScheduledEvent.parent_event) {
        payload.parent_event = this.newScheduledEvent.parent_event;
      }
      // console.log(payload)
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data) {
            if (this.newScheduledEvent.slug) {
              this.$emit("updateEvent", data);
            } else {
              this.$emit("addNewEvent", data);
            }
            this.closeDialog();
            this.submittingEvent = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.submittingEvent = false;
          }
          this.submittingEvent = false;
        });
      } catch (err) {
        console.log(err);
        this.submittingEvent = false;
      }
    },
    createRecurrence() {
      var duplicate = this.newScheduledEvent;
      duplicate.parent_event = this.newScheduledEvent.id;
      duplicate.slug = "";
      this.newScheduledEvent = duplicate;
      this.toggleEditable(true);
      this.isNewEvent = true;
    }
  },
  mounted() {
    if (this.scheduledEvent) {
      this.toggleEditable(false);
      this.newScheduledEvent = this.scheduledEvent;
      this.editor.setContent(this.scheduledEvent.details);

      this.allDayEvent = this.newScheduledEvent.all_day;
      if (this.allDayEvent) {
        // this.workingStart = new Date(`${this.newScheduledEvent.start}T00:00`);
        // this.workingEnd = new Date(`${this.newScheduledEvent.end}T23:59`);
        this.workingStart = new Date(
          `${this.newScheduledEvent.start_datetime.substr(0, 10)}T00:00`
        );
        this.workingEnd = new Date(
          `${this.newScheduledEvent.end_datetime.substr(0, 10)}T00:00`
        );
        this.displayStartDateTime = this.workingStart.toLocaleDateString();
        this.displayEndDateTime = this.workingEnd.toLocaleDateString();
      } else {
        // console.log(this.newScheduledEvent.start)
        this.workingStart = new Date(this.newScheduledEvent.start_datetime);
        this.workingEnd = new Date(this.newScheduledEvent.end_datetime);
        this.displayStartDateTime = this.workingStart.toLocaleString();
        this.displayEndDateTime = this.workingEnd.toLocaleString();
      }
      this.workingDateRange[0] = this.formatLocalDateString(this.workingStart);
      this.workingDateRange[1] = this.formatLocalDateString(this.workingEnd);
      this.workingStartTime = this.formatLocalTimeString(this.workingStart);
      this.workingEndTime = this.formatLocalTimeString(this.workingEnd);

      // this.parseInvites();
    } else {
      // we are editing a new object

      this.workingStart = new Date();
      this.workingEnd = new Date();

      this.workingStartTime = this.formatLocalTimeString(this.workingStart);
      this.workingEndTime = this.formatLocalTimeString(this.workingEnd);

      this.workingDateRange[0] = this.workingStart.toISOString().substr(0, 10);

      this.toggleEditable(true);
      this.isNewEvent = true;
      // this.newScheduledEvent = {}
    }
    this.loaded = true;
  },
  created() {
    this.getLanguages();
    this.getTopics();
    this.getProfileList();
  }
};
</script>
<style>
.editor-box > * {
  border-color: black;
  color: black;
  background-color: green;
  border-style: solid;
  border-width: 1px;
  padding: 4px, 4px;
  width: 100%;
  height: 525px;
  overflow-x: hidden;
  overflow-x: auto;
  font-size: 1.25em;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.5;
}

.is-active {
  border-color: orange;
  background-color: black;
  border-style: solid;
  border-width: 2px;
}
</style>
