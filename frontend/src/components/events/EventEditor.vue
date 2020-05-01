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
        <v-btn icon outlined color="garbage desertsand--text" @click="closeDialog"
          ><v-icon>mdi-close</v-icon></v-btn
        >
      </v-card-title>

      <v-card-text class="pa-5 desertsand">
         <v-row v-if="!editing">
            <v-col>
                  <v-row dense>
                     <v-col cols="auto">
                        <v-avatar>
                           <v-img class="elevation-6" :src="newScheduledEvent.curator.user_profile ? newScheduledEvent.curator.user_profile.avatar : 'https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/default.jpg' "></v-img>
                        </v-avatar>
                     </v-col>
                     <v-col>
                        Added by {{ newScheduledEvent.curator['username'] }} 
                        on {{ newScheduledEvent.curation_date || 'December 7, 1941' }}
                     </v-col>
                  </v-row>
                  <v-row>
                     <v-col>
                        <p>
                           <v-chip small outlined class="primary primary--text mr-1">Event Type: {{ newScheduledEvent.type }}</v-chip>
                           <v-chip small outlined class="languages languages--text mr-1">Language Pair: {{ newScheduledEvent.native_language }} &#8594; {{ newScheduledEvent.target_language}}</v-chip>
                           <v-chip small outlined class="topics topics--text mr-1">Topic Area: {{ newScheduledEvent.topic }}</v-chip>
                           <v-chip small outlined class="garbage garbage--text mr-1">Access: {{newScheduledEvent.access_type }}</v-chip><br>
                        </p>
                        <h1>{{ newScheduledEvent.name }}</h1>
                        <p>{{ newScheduledEvent.caption }}</p>
                        Start Date/Time: <strong>{{ newScheduledEvent.start }}</strong><br>
                        End Date/Time: <strong>{{ newScheduledEvent.end }}</strong><br>
                        Location: <strong>{{ newScheduledEvent.location }}</strong><br>
                     </v-col>
                  </v-row>
            </v-col>
         </v-row>
         <v-row wrap dense justify="center" v-if="editing">
          <v-col cols="12">
                <v-form
                  ref="details"
                  v-model="valid"
                  @submit.prevent
                  v-if="loaded"
                >
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
                  
                  <span class="overline">For location: If virtual, please specify platform (e.g. 'Zoom'); if holiday, please specify region</span>
                  <v-text-field
                    v-model="newScheduledEvent.location"
                    name="eventlocation"
                    label="Event Location*"
                    placeholder="event location, platform, or region"
                    :rules="[rules.requiredLocation]"
                    outlined
                    class="pb-0 mb-0"
                  ></v-text-field>
                  
                  <v-row dense wrap>
                     <span class="overline">All times are currently in GMT</span>
                     <v-col>
                        <v-menu
                        v-model="startDateMenu"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                        >
                        <template v-slot:activator="{ on }">
                           <v-text-field
                              v-model="newScheduledEvent.start_date"
                              label="Start Date"
                              outlined
                              dense
                              append-icon="event"
                              readonly
                              v-on="on"
                           ></v-text-field>
                        </template>
                        <v-date-picker v-model="newScheduledEvent.start_date" @input="startDateMenu = false"></v-date-picker>
                        </v-menu>
                     </v-col>
                     <v-col>

                        <v-menu
                        ref="starttimemenu"
                        v-model="startTimeMenu"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        :return-value.sync="newScheduledEvent.start_time"
                        transition="scale-transition"
                        offset-y
                        max-width="290px"
                        min-width="290px"
                        >
                        <template v-slot:activator="{ on }">
                           <v-text-field
                              v-model="newScheduledEvent.start_time"
                              label="Start Time"
                              outlined
                              dense
                              append-icon="access_time"
                              readonly
                              v-on="on"
                           ></v-text-field>
                        </template>
                        <v-time-picker
                           v-if="startTimeMenu"
                           v-model="newScheduledEvent.start_time"
                           format="24hr"
                           full-width
                           @click:minute="$refs.starttimemenu.save(newScheduledEvent.start_time)"
                        ></v-time-picker>
                        </v-menu>
                     </v-col>
                  </v-row>
                  <v-row  dense wrap>
                     <v-col>

                        <v-menu
                        v-model="endDateMenu"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                        >
                        <template v-slot:activator="{ on }">
                           <v-text-field
                              v-model="newScheduledEvent.end_date"
                              outlined
                              dense
                              label="End Date"
                              append-icon="event"
                              readonly
                              v-on="on"
                           ></v-text-field>
                        </template>
                        <v-date-picker v-model="newScheduledEvent.end_date" @input="endDateMenu = false"></v-date-picker>
                        </v-menu>
                     </v-col>
                     <v-col>
                        <v-menu
                        ref="endtimemenu"
                        v-model="endTimeMenu"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        :return-value.sync="newScheduledEvent.end_time"
                        transition="scale-transition"
                        offset-y
                        max-width="290px"
                        min-width="290px"
                        >
                        <template v-slot:activator="{ on }">
                           <v-text-field
                              v-model="newScheduledEvent.end_time"
                              outlined
                              dense
                              label="End Time"
                              append-icon="access_time"
                              readonly
                              v-on="on"
                           ></v-text-field>
                        </template>
                        <v-time-picker
                           v-if="endTimeMenu"
                           v-model="newScheduledEvent.end_time"
                           format="24hr"
                           full-width
                           @click:minute="$refs.endtimemenu.save(newScheduledEvent.end_time)"
                        ></v-time-picker>
                        </v-menu>
                     </v-col>
                  </v-row>

                  <v-select
                    v-model="newScheduledEvent.type"
                    name="eventtype"
                    :items="allTypes"
                    label="Event Type*"
                    placeholder="choose event type"
                    :rules="[rules.requiredType]"
                    required
                    :loading="loadingTypes"
                    outlined
                  ></v-select>

                  <v-select
                    v-model="newScheduledEvent.nativelanguage"
                    name="nativelanguage"
                    :items="allLanguages"
                    label="Native Language*"
                    placeholder="choose a native language"
                    :rules="[rules.requiredLanguage]"
                    required
                    :loading="loadingLanguages"
                    outlined
                  ></v-select>

                  <v-select
                    v-model="newScheduledEvent.targetlanguage"
                    name="targetlanguage"
                    :items="allLanguages"
                    label="Target Language*"
                    placeholder="choose a target language"
                    :rules="[rules.requiredLanguage]"
                    required
                    :loading="loadingLanguages"
                    outlined
                  ></v-select>

                  <v-select
                    v-model="newScheduledEvent.topic"
                    name="eventtopic"
                    :items="allTopics"
                    label="Primary Topic*"
                    placeholder="choose the primary topic"
                    :rules="[rules.requiredTopic]"
                    required
                    :loading="loadingTopics"
                    outlined
                  ></v-select>
                  <div justify="center">
                  Event Access:
                  <v-radio-group v-model="newScheduledEvent.public" row>
                     <v-radio label="Public" :value="true"></v-radio>
                     <v-radio label="Invitation Only" :value="false"></v-radio>
                  </v-radio-group>
                  </div>

                  <v-autocomplete
                     v-model="newScheduledEvent.invited_users"
                     v-if="newScheduledEvent.public===false"
                     :items="allUsers"
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
                           @click:close="remove(data.item)"
                        >
                           <v-avatar left>
                              <v-img :src="data.item.avatar"></v-img>
                           </v-avatar>
                           {{ data.item.username }}
                        </v-chip>
                     </template>
                     <template v-slot:item="data">
                        <template v-if="typeof data.item !== 'object'">
                           <v-list-item-content v-text="data.item"></v-list-item-content>
                        </template>
                        <template v-else>
                           <v-list-item-avatar>
                           <img :src="data.item.avatar">
                           </v-list-item-avatar>
                           <v-list-item-content>
                           <v-list-item-title v-html="data.item.username"></v-list-item-title>
                           <v-list-item-subtitle>Language 1 - Language 2</v-list-item-subtitle>
                           </v-list-item-content>
                        </template>
                     </template>
                  </v-autocomplete>

                  <v-autocomplete
                     v-model="newScheduledEvent.invited_groups"
                     v-if="newScheduledEvent.public===false"
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
                           <v-list-item-content v-text="data.item"></v-list-item-content>
                        </template>
                        <template v-else>
                           <v-list-item-avatar>
                           <img :src="data.item.avatar">
                           </v-list-item-avatar>
                           <v-list-item-content>
                           <v-list-item-title v-html="data.item.name"></v-list-item-title>
                           <v-list-item-subtitle>Language 1 - Language 2</v-list-item-subtitle>
                           </v-list-item-content>
                        </template>
                     </template>
                  </v-autocomplete>
                </v-form>
          </v-col>
        </v-row>
        <v-row no-gutters dense class="mt-0 pt-0">
           <v-col>
            <span class="body-1">Event Details:</span>
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
                     <v-btn color="calligraphy" icon @click="changeEditorFontSize('down')">
                        <v-icon>mdi-magnify-minus</v-icon>
                     </v-btn>
                        Text Size
                     <v-btn icon color="calligraphy" @click="changeEditorFontSize('up')">
                        <v-icon>mdi-magnify-plus</v-icon>
                     </v-btn>

                     <v-divider class="mx-1" inset vertical></v-divider>
                  <v-spacer></v-spacer>
                  Count: <span :class="characterCountClass">{{ characterCount }}</span> / 500
                  </v-toolbar>
               </div>
            </editor-menu-bar>
            <editor-content :editor="editor" :style="editorFontClass" :class="editing ? 'editor-box' : ''" />

           </v-col>
        </v-row>
         <v-row dense v-if="!isNewEvent">
           <v-col>
               <v-btn v-if="isCurator && !editing" @click="toggleEditable(true)" class="mr-2 primary desertsand--text mr-2">Edit<v-icon right>mdi-pencil</v-icon></v-btn>
               <v-btn v-if="isCurator" class="mr-2 garbage desertsand--text">Delete Event<v-icon right>mdi-trash-can</v-icon></v-btn>
               <v-btn v-if="!isCurator" class="primary desertsand--text mr-2">Save<v-icon right>mdi-heart</v-icon></v-btn>
               <v-btn v-if="!isCurator" @click="showRSVPDialog = true" class="elements desertsand--text mr-2">RSVP
                  <v-badge
                     :content="newScheduledEvent.rsvp_list_count"
                     color="elements darken-2"
                  >
                     <v-icon right>mdi-message-reply-text</v-icon>
                  </v-badge>
               </v-btn>
               <v-btn v-if="!isCurator" class="topics desertsand--text mr-2">Export<v-icon right>mdi-calendar-export</v-icon></v-btn>
           </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="calligraphy">
        <v-spacer></v-spacer>
        <v-btn v-if="editing" color="garbage desertsand--text" @click="closeDialog"
          >Cancel<v-icon right>mdi-close</v-icon></v-btn
        >
         <v-btn v-if="!editing" color="garbage desertsand--text" @click="closeDialog"
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
      @closeDialog="showRSVPDialog=false"
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
  Underline,
} from "tiptap-extensions";
import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";


export default {
  name: "EventEditor",
  components: {
    EditorContent,
    EditorMenuBar,
    RSVPDialog,

  },
  props: {
    editorDialog: {
      type: Boolean,
      default: false,
    },
    scheduledEvent: {
      type: Object,
      required: false,
    }
  },
  data: () => ({
    // userData: Object,
    showRSVPDialog: false,
    unsavedChanges: false,
    editing: false,
    startTimeMenu: false,
    isNewEvent: false,
    endTimeMenu: false,
    startDateMenu: false,
    endDateMenu: false,
    newScheduledEvent: {
       curator: {
       },
       avatar: {

       },
       public: true,
       invited_users: [
       ],
       invited_groups: [],
    },
    loaded: false,
    today : new Date().toISOString().substr(0, 10),
    existingSlug: "",
    existingTitle: "",
    submittingEvent: false,
    valid: true,
    success: false,
    allLanguages: [],
    loadingTypes: false,
    access: "public",
    loadingLanguages: false,
    loadingTopics: false,
    loadingUsers: false,
    loadingGroups: false,
    
    allTypes: ['meeting', 'conference', 'study session', 'lecture'],
    userGroups: [
       { name: "Radical Russian", id: "1234" },
       { name: "Awesome Arabic", id: "1244" },
       { name: "Gnarly Norwegian", id: "1224" },
    ],
    allUsers: [
       { username: "ShaykhJake", comment: "Super stoked!", id: "33333", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
       { username: "Jeff", comment: "Can't wait!!", id: "33332", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
       { username: "Chad", comment: "Me too!", id: "33334", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
    ],
    guestList: [
       { username: "ShaykhJake", comment: "Super stoked!", id: "33333", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
       { username: "Jeff", comment: "Can't wait!!", id: "33332", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
       { username: "Chad", comment: "Me too!", id: "33334", avatar: "https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"},
    ],
    allTopics: [],
    rules: {
      requiredTitle: value =>
        (value || "").length > 5 ||
        "You must provide a title of at least 6 characters.",

      requiredCaption: value =>
        (value || "").length > 5 ||
        "You must provide a caption of at least 6 characters.",

      requiredLocation: value =>
        (value || "").length > 5 ||
        "You must provide a caption of at least 6 characters.",

      requiredType: typevalue =>
        (typevalue || "").length > 0 ||
        "You must choose an event type.",
      requiredLanguage: languagevalue =>
        (languagevalue || "").length > 0 ||
        "You must choose a language.",
      requiredTopic: topicvalue =>
        (topicvalue || "").length > 0 || "You must choose a primary topic.",
      requiredCitation: citationvalue =>
        !!citationvalue || "You must provied a source citation.",
      maxTags: tagsvalue =>
        (tagsvalue || "").length < 6 || "Maximum of 5 tags allowed!",
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
          new Underline(),
        ],
        content: `
          ...type/paste event details in here...
         `,
      })

  }),
  computed: {
    characterCountClass(){
       if(this.characterCount > 500){
          return "error";
       } else {
          return "";
       }
    },
   activeUser() {
      return window.localStorage.getItem("username");
   },
   isCurator() {
      if(this.newScheduledEvent.curator){
         return this.newScheduledEvent.curator.username == this.activeUser
      } else if (this.isNewEvent) {
         return true 
      } else {
         return false
      }
   },

    editorFontClass(){
      return `font-size:${this.editorFontSize}em`
    },
    characterCount(){
      return this.editor.view.state.doc.textContent.length
    },
    // justText(){  // SAVE THIS FOR USING LATER!!!
    //   return this.editor.view.state.doc.textContent
    // }
  },
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    chooseNewFile() {
      this.loadNewFile = true;
    },
    toggleEditable(state){
        this.editing = state;
        this.editor.setOptions({
            editable: this.editing
        });
    },
    removeTag(item) {
      this.newScheduledEvent.tags.splice(this.newScheduledEvent.tags.indexOf(item), 1);
      this.newScheduledEvent.tags = [...this.newScheduledEvent.tags];
    },
    changeEditorFontSize(direction){
      if(direction==="up"){
        if(this.editorFontSize < 3.5){
          this.editorFontSize += 0.15
        }
      } else {
        if(this.editorFontSize > 0.5){
          this.editorFontSize -= 0.15
        }
      }
    },
    clearWarnings() {
      this.alertActive = false;
    },
    passDuration(duration) {
      this.duration = duration;
    },
    getLanguages() {
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
    },

    getTopics() {
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
    },
    updateViewer(scheduledEvent) {
      this.$emit("updateViewer", scheduledEvent);
    },
    submitSave(){
       this.unsavedChanges=false;
       console.log("hello!");
    },
    submitScheduledEvent() {
      // The following grabs the blob, converts to a JPEG, wraps it, and sends it to the API
      // this.submittingEvent = true;
      // let endpoint = `/api/eventz/`;
      // let method = "POST";
      // if (this.newScheduledEvent.slug !== undefined) {
      //   endpoint += `${this.newScheduledEvent.slug}/`;
      //   method = "PATCH";
      // }
      var payload = {
         name: this.newScheduledEvent.name,
         start: this.newScheduledEvent.start_date + " " + this.newScheduledEvent.start_time,
         end: [this.newScheduledEvent.end_date, this.newScheduledEvent.end_time].join(" "),
         type: this.newScheduledEvent.type,
         native_language: this.newScheduledEvent.native_language,
         target_language: this.newScheduledEvent.target_language,
         topic: this.newScheduledEvent.topic,
         event_access: this.newScheduledEvent.event_access,
         details: this.editor.getJSON(),
         caption: this.newScheduledEvent.caption,
      }
      console.log(payload)
      this.updateViewer(payload);
      this.closeDialog();
      // apiService(endpoint, method, payload).then(data => {
      //   console.log(data);
      //   if (data.slug) {
      //     if (this.isNewEvent) {
      //       this.$router.push({
      //         name: "Events",
      //       });
      //     } else {
      //       // this.alertActive = false;
      //       this.updateViewer(data);
      //       this.closeDialog();
      //     }
      //   } else {
      //     console.log(data)
      //     console.log("There was a major problem with the request.");
      //     // console.log(data.message);
      //   }
      //   this.submittingEvent = false;
      // });
    }
  },
  mounted() {
    if(this.scheduledEvent){
      this.toggleEditable(false);
      this.newScheduledEvent = this.scheduledEvent;
      this.editor.setContent(this.scheduledEvent.details);
    } else {
      // we are editing a new object
      this.toggleEditable(true);
      this.isNewEvent = true;
      // this.newScheduledEvent = {}
    }
    this.loaded = true;
  },
  created() {
    this.getLanguages();
    this.getTopics();

  }
};
</script>
<style>
  .editor-box > * {
    border-color: black;
    color: black;
    background-color:green;
    border-style: solid;
    border-width: 1px;
    padding: 4px, 4px;
    width: 100%;
    height: 525px;
    overflow-x: hidden;
    overflow-x: auto;
    font-size:1.25em;
    font-family:Arial, Helvetica, sans-serif;
    line-height: 1.5;
  }

  .is-active {
    border-color: orange;
    background-color: black;
    border-style: solid;
    border-width: 2px;
  }
</style>
