<template>
  <v-container fluid>
    <v-card class="mb-2">
      <v-card-title class="calligraphy desertsand--text">
        Lesson Builder: <span class="font-weight-black">"{{ isNewLesson ? " New Lesson" : lesson.title }}"</span>
      </v-card-title>

      <v-card-text class="calligraphy px-1">
        <v-row wrap dense>
          <v-col cols="12">
            <v-card>
              <v-card-title class="desertsand py-1 font-weight-b">
               Metadata
                <v-spacer />

               <v-btn fab icon class="mx-1 primary--text" @click="showingMetadata=!showingMetadata">
                  <v-icon v-if="showingMetadata">mdi-menu-up</v-icon>
                  <v-icon v-else>mdi-menu-down</v-icon>
               </v-btn>


              </v-card-title>
              <v-card-text v-show="showingMetadata" class="desertsand pt-4">
                <v-form
                  ref="lessonmetadata"
                  v-model="metadataValid"
                  @submit.prevent
                >
                  <v-text-field
                    v-model="lesson.title"
                    name="lessontitle"
                    label="Lesson Title*"
                    placeholder="Give your lesson a title..."
                    :rules="[rules.requiredTitle]"
                    outlined
                    class="pb-0 mb-0"
                    @change="unsavedChanges=true"
                  ></v-text-field>

                  <v-textarea
                    outlined
                    name="objective"
                    label="Learning Objective*"
                    placeholder="What is the learning objective of your lesson?"
                    v-model="lesson.objective"
                    :rules="[rules.requiredObjective]"
                    counter
                    rows="3"
                    maxlength="400"
                    @change="unsavedChanges=true"
                  ></v-textarea>
                  <v-row wrap dense>
                     <v-col>
                        <v-autocomplete
                           v-model="lesson.skill_level"
                           name="nativelanguage"
                           :items="skillLevels"
                           label="Skill Level*"
                           placeholder="Skill Level"
                           :rules="[rules.requiredSkillLevel]"
                           required
                           outlined
                           color="topics"
                           prepend-icon="mdi-help-circle"
                           @click:prepend="skillDialog=true"
                           @change="unsavedChanges=true"
                        ></v-autocomplete>
                     </v-col>
                     <v-col>
                        <v-autocomplete
                           v-model="lesson.lesson_type"
                           name="lessontype"
                           :items="lessonTypes"
                           label="Lesson Type*"
                           placeholder="Lesson Type"
                           :rules="[rules.requiredLessonType]"
                           required
                           outlined
                           prepend-icon="mdi-help-circle"
                           @click:prepend="lessonTypeDialog=true"
                           @change="unsavedChanges=true"
                        ></v-autocomplete>

                     </v-col>
                  </v-row>

                  <v-autocomplete
                    v-model="lesson.native_language"
                    name="nativelanguage"
                    :items="allLanguages"
                    label="Native Learner's Language*"
                    placeholder="choose a native language"
                    :rules="[rules.requiredLanguage]"
                    required
                    :loading="loadingLanguages"
                    outlined
                    @change="unsavedChanges=true"
                  ></v-autocomplete>

                  <v-autocomplete
                    v-model="lesson.target_language"
                    name="targetlanguage"
                    :items="allLanguages"
                    label="Acquisition Language*"
                    placeholder="choose a target language"
                    :rules="[rules.requiredLanguage]"
                    required
                    :loading="loadingLanguages"
                    outlined
                    @change="unsavedChanges=true"
                  ></v-autocomplete>

                  <v-autocomplete
                    v-model="lesson.topic"
                    name="eventtopic"
                    :items="allTopics"
                    label="Primary Topic*"
                    placeholder="choose the primary topic"
                    :rules="[rules.requiredTopic]"
                    required
                    :loading="loadingTopics"
                    outlined
                    @change="unsavedChanges=true"
                  ></v-autocomplete>

                  <v-textarea
                    outlined
                    name="citation"
                    label="Source Citation(s)*"
                    placeholder="Please provide citations for sources? (If none, please state: 'Original Work')"
                    v-model="lesson.citation"
                    :rules="[rules.requiredCitation]"
                    counter
                    rows="3"
                    maxlength="600"
                    @change="unsavedChanges=true"
                  ></v-textarea>
                </v-form>
                <p v-if="isNewLesson" class="primary--text text--darken-2 mb-0">
                  You must submit valid metadata in order to
                  build a new quiz prior to attaching questions.
                </p>

              </v-card-text>

               <v-dialog v-model="skillDialog" max-width="450">
                  <v-card>
                     <v-card-title>Skill Levels</v-card-title>
                     <v-card-text>
                        <p>
                        These skill levels are based on ACTFL and the ILR levels; please click on
                        those names for in-depth information. As a summary though, this should suffice:
                        </p>
                        <p>
                        0+ New Learner; very young native child<br>
                        1 Early learner; young native child<br>
                        1+ Learner; adolescent native<br>
                        2 Functionally-fluent learner; uneducated native<br>
                        2+ Fluent learner; high-school educated native<br>
                        3 Fluent as second-language; post secondary educated native<br>
                        3+ Highly-fluent second-language; college educated native<br>
                        4 Advanced second-language; postgraduate native<br>
                        4+ doctoral native<br>
                        5 Authority in the specific topic and context<br>
                        </p>
                        <p>It should be noted that these levels do not describe a learner in a static state; rather,
                        a learner may be a level 2 in one topic area and a level 4 in another. This can be frequently
                        seen as a discrepency between listening, reading, and speaking. An example could be a 
                        sports newscaster who can possibly reach above a level 4 in a sports context, but who may
                        only speak below a level 2 in a nuclear engineering context.</p>

                     </v-card-text>
                  </v-card>
               </v-dialog>
               <v-dialog v-model="lessonTypeDialog" max-width="450">
                  <v-card>
                     <v-card-title>Lesson Types</v-card-title>
                     <v-card-text>
                        <p>
                        The following is not all-inclusive, but represents the most common types of 
                        language learning lessons which the PidginForge platform can currently support:
                        </p>
                        <p>
                        Reading Comprehension - A lesson that is focused on improving a learner's ability
                        to comprehend text. <br>
                        Listening Comprehension - A lesson that is focued on improving a learning's ability
                        to understand spoken language.<br>
                        Explicit Grammar - A lesson focused on teaching grammar concepts in the target language.<br>
                        Content-Based (CBI) - A lesson where the objective is to learn the content as the primary goal;
                         these lessons tend to mimic the way a native would learn a language. For some learners they
                         provide additional motivation.
                        <br>
                        Problem/Project-Based (PBI) - These lessons usually require the learner to produce some
                        sort of product and require analysis and synthesis. <br>
                        </p>
                        <p>
                           In the future, PidginForge hopes to branch out into augmented/virtual reality
                           in order to incorporate role-playing and other experiential learning activities.
                           Until that time, those activies will be best presented through a more synchronous
                           teaching approach (e.g. face-to-face in-person instruction, or vitual over platforms
                           like Zoom).
                        </p>

                     </v-card-text>
                  </v-card>
               </v-dialog>
            <v-card-actions v-if="isNewLesson" class="desertsand">
              <v-spacer />
              <v-btn 
                class="primary desertsand--text" 
                :disabled="!metadataValid"
                :loading="building"
                @click="buildNewLesson"
              >
                Build Lesson
                <v-icon right>mdi-domain</v-icon>
              </v-btn>
              <v-spacer />
            </v-card-actions>
            </v-card>
          </v-col>

          <v-col cols="12" v-if="!isNewLesson">
            <v-card>
              <v-card-title class="desertsand py-1">
                Content Editor
                <v-spacer />
                <v-btn
                  small
                  class="primary desertsand--text"
                  @click="togglePreview"
                >
                  <span v-if="!previewMode">Preview Mode</span>
                  <span v-if="previewMode">Edit Mode</span>
                </v-btn>
               <v-btn icon class="mx-1 primary--text" @click="showingContentEditor=!showingContentEditor">
                  <v-icon v-if="showingContentEditor">mdi-menu-up</v-icon>
                  <v-icon v-else>mdi-menu-down</v-icon>
               </v-btn>


              </v-card-title>
              <v-card-text
                v-show="showingContentEditor"
                class="desertsand py-0 px-1"
              >
                <editor-menu-bar
                  v-if="!previewMode"
                  :editor="editor"
                  v-slot="{ commands, isActive, getNodeAttrs, getMarkAttrs }"
                >
                  <div>
                    <v-toolbar dense flat class="desertsand">
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
                        :class="{ 'is-active': isActive.heading({ level: 1 }) }"
                        @click="commands.heading({ level: 1 })"
                      >
                        <v-icon>
                          mdi-format-header-1
                        </v-icon>
                      </v-btn>
                      <v-btn
                        icon
                        small
                        color="calligraphy"
                        :class="{ 'is-active': isActive.heading({ level: 2 }) }"
                        @click="commands.heading({ level: 2 })"
                      >
                        <v-icon>
                          mdi-format-header-2
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

                      <v-menu
                        top
                        :close-on-content-click="false"
                        v-model="linkDialog"
                      >
                        <template v-slot:activator="{ on }">
                          <v-btn
                            icon
                            small
                            color="calligraphy"
                            class="menubar__button"
                            :class="{ 'is-active': isActive.link() }"
                            v-on="on"
                            @click="showLinkMenu(getMarkAttrs('link'))"
                          >
                            <v-icon name="code">mdi-link</v-icon>
                          </v-btn>
                        </template>

                        <v-card max-width="320">
                          <v-card-title class="sandstone py-1">
                            Add Hyperlink
                          </v-card-title>
                          <v-card-text class="desertsand">
                            <v-form
                              v-if="linkDialog"
                              @submit.prevent="
                                setLinkUrl(commands.link, linkUrl)
                              "
                            >
                              <v-text-field
                                v-model="linkUrl"
                                label="URL"
                                ref="linkInput"
                                placeholder="https://"
                                outlined
                                @keydown.esc="linkDialog = false"
                                class="pt-3 mb-0 pb-0"
                              ></v-text-field>
                              <div class="pa-0">
                                <v-btn
                                  color="garbage"
                                  text
                                  @click="setLinkUrl(commands.link, null)"
                                  >Remove</v-btn
                                >
                                <v-btn
                                  color="primary"
                                  text
                                  @submit.prevent="
                                    setLinkUrl(commands.link, linkUrl)
                                  "
                                  >Update</v-btn
                                >
                              </div>
                            </v-form>
                          </v-card-text>
                        </v-card>
                      </v-menu>

                      <v-btn
                        icon
                        small
                        color="calligraphy"
                        class="menubar__button"
                        :class="{ 'is-active': isActive.code_block() }"
                        @click="commands.code_block"
                      >
                        <v-icon name="code">mdi-code-tags</v-icon>
                      </v-btn>

                      <v-btn
                        icon
                        small
                        color="calligraphy"
                        class="menubar__button"
                        @click="commands.horizontal_rule"
                      >
                        <v-icon>mdi-minus</v-icon>
                      </v-btn>

                      <v-btn
                        icon
                        small
                        color="calligraphy"
                        class="menubar__button"
                        :class="{ 'is-active': isActive.bullet_list() }"
                        @click="commands.bullet_list"
                      >
                        <v-icon>mdi-format-list-bulleted</v-icon>
                      </v-btn>

                      <v-btn
                        icon
                        small
                        color="calligraphy"
                        class="menubar__button"
                        :class="{ 'is-active': isActive.ordered_list() }"
                        @click="commands.ordered_list"
                      >
                        <v-icon>mdi-format-list-numbered</v-icon>
                      </v-btn>

                      <v-divider class="mx-1" inset vertical></v-divider>

                      <v-btn
                        icon
                        small
                        color="calligraphy"
                        :class="{
                          'is-active': isActive.alignment({
                            orientation: 'left'
                          })
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
                        icon
                        small
                        color="calligraphy"
                        :class="{
                          'is-active': isActive.lexeme()
                        }"
                        @click="
                          addWordToBank(
                            commands.lexeme,
                            getMarkAttrs('definition')
                          )
                        "
                      >
                        <v-icon>
                          mdi-card-text-outline
                        </v-icon>
                      </v-btn>
                    </v-toolbar>
                  </div>
                </editor-menu-bar>
                <div class="editor">
                  <editor-content
                    :editor="editor"
                    :style="editorFontClass"
                    class="editor__content"
                    id="editorbox"
                  />
                </div>
              </v-card-text>
              <v-card-actions
                class="desertsand py-1"
                v-show="showingContentEditor"
              >
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
                <v-btn icon @click="printText"
                  ><v-icon>mdi-printer</v-icon></v-btn
                >
                <v-spacer></v-spacer>
                Character Count: {{ characterCount }}
              </v-card-actions>
            </v-card>
          </v-col>

        </v-row>
      </v-card-text>
      <v-card-actions class="calligraphy" v-if="!isNewLesson">
        <v-spacer />
        <v-btn small class="garbage desertsand--text" @click="confirmDeleteDialog=true">Delete Lesson<v-icon right>mdi-delete</v-icon></v-btn>
        <v-btn small class="elements desertsand--text" :loading="publishing" @click="togglePublish">
          <span v-if="!lesson.published">Publish <v-icon right>mdi-publish</v-icon></span>
          <span v-else>Return to Draft<v-icon right>mdi-file-edit</v-icon></span>
        </v-btn>
        <v-btn
          small
          class="primary"
          :disabled="!metadataValid || !unsavedChanges"
          @click="saveLesson"
          :loading="saving"
        >Save <v-icon right>mdi-content-save</v-icon></v-btn>
        <v-spacer />
      </v-card-actions>
    </v-card>

    <v-card class="calligraphy mb-2" v-if="!isNewLesson">
       <v-card-title class="calligraphy desertsand--text py-1">
          Quiz Bank
         <v-spacer></v-spacer>

         <v-btn icon class="mx-1 primary--text" @click="showingQuizBank=!showingQuizBank">
            <v-icon v-if="showingQuizBank">mdi-menu-up</v-icon>
            <v-icon v-else>mdi-menu-down</v-icon>
         </v-btn>

       </v-card-title>
      <v-card-text v-show="showingQuizBank" class="calligraphy pa-1">
         <QuizBank ref="quizbank" />         
      </v-card-text>
    </v-card>
    <v-card class="calligraphy mb-2"  v-if="!isNewLesson">
      <v-card-title class="calligraphy desertsand--text py-1">
         Vocab Bank
         <v-spacer></v-spacer>

         <v-btn icon class="mx-1 primary--text" @click="showingVocabBank=!showingVocabBank">
            <v-icon v-if="showingVocabBank">mdi-menu-up</v-icon>
            <v-icon v-else>mdi-menu-down</v-icon>
         </v-btn>

      </v-card-title>
      <v-card-text v-show="showingVocabBank" class="calligraphy pa-1">
          <v-btn 
            v-if="!lesson.primary_vocab" 
            :loading="creatingBank" 
            class="primary"
            @click="createVocabBank"
          >
            Create New Vocab Bank
          </v-btn>
         <VocabBank
            v-else
            :vocab-list="vocabList"
            :native-language="this.lesson.native_language"
            :target-language="this.lesson.target_language"
            :vocab-bank-i-d="lesson.primary_vocab"
            @setLexemeDefinition="setLexemeDefinition"
            ref="vocabbank"
         />
      </v-card-text>
   </v-card>

    <v-dialog
      v-model="confirmDeleteDialog"
      persistent
      max-width="300"
    >
      <v-card class="calligraphy desertsand--text">
        <v-card-title class="headline">Confirm Delete?</v-card-title>
        <v-card-text class="desertsand calligraphy--text pt-1">
          You've worked so hard; are you sure that you want to flush
          all of that work down the toilet and deprive the world of
          your masterpiece?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            small
            color="primary desertsand--text"
            @click="confirmDeleteDialog = false"
            >Cancel<v-icon right>mdi-close</v-icon></v-btn
          >
          <v-btn
            small
            color="garbage desertsand--text"
            @click="deleteLesson"
            :loading="submittingDelete"
            >Delete<v-icon right>mdi-delete</v-icon></v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-overlay :value="loadingLesson">
      <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
    </v-overlay>
  </v-container>
</template>

<script>
import VocabBank from "@/components/vocab/VocabBank.vue";
import QuizBank from "@/components/quizzes/QuizBank.vue";
import { apiService } from "@/common/api.service.js";
import { Editor, EditorContent, EditorMenuBar } from "tiptap";
import {
  Blockquote,
  CodeBlock,
  HorizontalRule,
  OrderedList,
  BulletList,
  ListItem,
  TodoItem,
  TodoList,
  HardBreak,
  Heading,
  Bold,
  Italic,
  Link,
  Strike,
  Underline,
  History
} from "tiptap-extensions";
import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";
import { default as Highlighter } from "@/components/tiptaptoo/Highlighter.js";
import { default as Lexeme } from "@/components/tiptaptoo/Lexeme.js";
import { default as YouTubeEmbed } from "@/components/tiptaptoo/YouTube.js";

export default {
  name: "LessonBuilder",
  components: {
    EditorContent,
    EditorMenuBar,
    VocabBank,
    QuizBank
  },
  props: {
    lessonslug: {
      type: String,
      required: false
    }
  },
  data: () => ({
    isNewLesson: true,
    loaded: false,
    building: false,
    saving: false,
    unsavedChanges: false,
    confirmDeleteDialog: false,
    submittingDelete: false,
    skillDialog: false,
    publishing: false,
    lessonTypeDialog: false,
    loadingLesson: false,
    loadingLanguages: false,
    loadingTopics: false,
    allTopics: [],
    allLanguages: [],
    metadataValid: false,
    creatingBank: false,
    linkDialog: false,
    lesson: {},
    showingMetadata: true,
    showingContentEditor: true,
    showingVocabBank: true,
    showingQuizBank: true,
    editorFontSize: 1,
    linkUrl: null,
    linkMenuIsActive: false,

    skillLevels: ["0+, Novice Low", "1, Novice Mid", "1+, Novice High", "2, Intermediate Low", "2+, Intermediate Mid", "3, Intermediate High", "3+, Advanced Low", "4, Advanced Mid", "4+, Advanced High", "5, Superior"],
    lessonTypes: ["Reading Comprehension",
                  "Listening Comprehension", 
                  "Explicit Grammar",
                  "Content-Based ",
                  "Problem-Based",
                  "Other",
    ],
    rules: {
      requiredTitle: value =>
        (value || "").length > 3 ||
        "Title length must be at least 4 characters.",

      requiredObjective: value =>
        (value || "").length > 9 ||
        "Objective length must be at least 9 characters.",

      requiredType: typevalue =>
        (typevalue || "").length > 0 || "You must choose an event type.",

      requiredSkillLevel: value =>
        (value || "").length > 0 || "You must choose a skill level.",
      
      requiredLessonType: lessontype =>
        (lessontype || "").length > 0 || "You must choose a lesson type.",

      requiredLanguage: languagevalue =>
        (languagevalue || "").length > 0 || "You must choose a language.",

      requiredTopic: topicvalue =>
        (topicvalue || "").length > 0 || "You must choose a primary topic.",

      requiredCitation: value =>
        (value || "").length > 5 ||
         "You must provied a source citation.",

    },

    vocabList: {},
    previewMode: false,
    editor: new Editor({
      editable: true,
      extensions: [
        new Blockquote(),
        new BulletList(),
        new CodeBlock(),
        new HorizontalRule(),
        new ListItem(),
        new OrderedList(),
        new TodoItem(),
        new TodoList(),
        new Link(),
        new HardBreak(),
        new Heading({ levels: [1, 2, 3] }),
        new Bold(),
        new Alignment(),
        new TextDirection(),
        new History(),
        new Highlighter(),
        new Italic(),
        new Lexeme(),
        new Link(),
        new Strike(),
        new Underline(),
        new YouTubeEmbed()
      ],
      editorProps: {
        handleClickOn: (view, pos, node, nodePos, event) => {
          if (node.type.name === "lexeme") {
            //   console.log(`Skip to ${node.attrs.timehack}`);
            console.log(`Lexeme: ${node.text} means ${node.attrs.definition}`);
            //   this.$emit("skipToTime", node.attrs.timehack);
          } else {
            return view, pos, node, nodePos, event;
          }
        },
        onUpdate: () => {
          this.unsavedChanges = true;
          console.log("Unsaved changes");
        },

      },
      content: `          
          سجل كولومبي يبلغ من العمر 26 عاما رقما قياسيا عالميا جديدا بالصعود بدراجته 76 درجة سلم في مبنى مؤلف من 38 طابقا وسجل خافيير زاباتا 23 دقيقة و17 ثانية ويوم الخميس الماضي عندما صعد بدراجته 760 درجة سلم في مبنى كولتيجير في مدينة ميدلين الشمالية الغربية.  وقالت وسائل الإعلام المحلية إن الرقم القياسي السابق مسجل باسم إسباني صعد 747 درجة سلم في فندق في برسلونة في 25 دقيقة و23 ثانية.
وأهم شرط في المرتين كان عدم لمس قدم المتسابق للأرض حتى النهاية.  وأشرف على محاولة زاباتا التي جرى تصويرها قائدُ شرطة ميدلين وقاض من الاتحاد الدولي للدراجات.  وكل ما تمكن زاباتا من قوله للصحفيين، بعد أن اختتم محاولته وقيل له إنه دخل موسوعة جينس للأرقام القياسية، "أنا بحاجة لاستنشاق هواء، كدتُ أموت هناك"

          
          

          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis obcaecati exercitationem cum harum cupiditate dicta nostrum quod necessitatibus fugiat, quis ex maxime commodi accusamus repudiandae reiciendis et quisquam iusto qui.</p>
          ...lesson content goes here...

         `
    }),
    vocabz: [
      { word: "تشترك", definition: "participates" },
      { word: "تشترك", definition: "participates" },
      { word: "تشترك", definition: "participates" }
    ]
  }),
  computed: {
    editorFontClass() {
      return `font-size:${this.editorFontSize}em`;
    },
    characterCount() {
      return this.editor.view.state.doc.textContent.length;
    }
  },
  methods: {
    togglePreview() {
      this.previewMode = !this.previewMode;
      this.editor.setOptions({
        editable: !this.previewMode
      });
    },
    togglePublish(){
      this.publishing = true;
      let payload = {
        published: !this.lesson.published
      }
      let endpoint = `/api/lessons/lessonz/${this.lesson.slug}/`;
      let method = "PATCH";
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data) {
            console.log(data.published)
            this.lesson.published = data.published;
            this.publishing=false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.publishing = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.publishing = false; 
      }
    },
    saveLesson(){
      this.saving = true;
      let payload = {
        title: this.lesson.title,
        objective: this.lesson.objective,
        skill_level: this.lesson.skill_level,
        lesson_type: this.lesson.lesson_type,
        native_language: this.lesson.native_language,
        target_language: this.lesson.target_language,
        topic: this.lesson.topic,
        citation: this.lesson.citation, 
        content: this.editor.getJSON(),
      }
      let endpoint = `/api/lessons/lessonz/${this.lesson.slug}/`;
      let method = "PATCH";
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data) {
            console.log(data)
            this.saving = false;
            this.unsavedChanges = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.saving = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.saving = false; 
      }
    },
    buildNewLesson() {
      let payload = {
        title: this.lesson.title,
        objective: this.lesson.objective,
        skill_level: this.lesson.skill_level,
        lesson_type: this.lesson.lesson_type,
        native_language: this.lesson.native_language,
        target_language: this.lesson.target_language,
        topic: this.lesson.topic,
        citation: this.lesson.citation, 
        published: false,
        content: "blank",
      }
      let endpoint = `/api/lessons/lessonz/`;
      let method = "POST";
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data) {
            this.lesson = data;
            this.editor.setContent(this.lesson.content);
            this.building = false;
            this.isNewLesson = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.building = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.building = false; 
      }
    },
    loadLesson(slug) {
      this.loadingLesson = true;
      console.log(`Loading lesson: ${slug}`);
      // get from api....data =>
      // this.editor.setContent(data.content);
      let endpoint = `/api/lessons/lessonz/${slug}/`;
      try {
        apiService(endpoint).then(data => {
          if (data) {
            this.lesson = data;
            this.editor.setContent(this.lesson.content);
            this.isNewLesson = false;
            this.loadingLesson = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.loadingLesson = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.loadingLesson = false; 
      }
    },
    async deleteLesson() {
      this.submittingDelete = true;
      // get from api....data =>
      // this.editor.setContent(data.content);
      let endpoint = `/api/lessons/lessonz/${this.lesson.slug}/`;
      try {
        await apiService(endpoint, "DELETE");
        this.$router.push("/");
      } catch (err) {
        // console.log(err);
        this.submittingDelete = false;
      }
    },
    createVocabBank(){
      this.creatingBank = true;
      
      let endpoint = `/api/lessons/createvocab/`;
      let method = "POST";
      let payload = {
        lesson_id: this.lesson.id,
      }
      try {
        apiService(endpoint, method, payload).then(data => {
            if (data){
              console.log(data);
              this.lesson.primary_vocab = data.vocab_bank_id;
              this.creatingBank = false;
            } else {
              console.log("There was a major problem with the request.");
              // console.log(data.message);
              this.creatingBank = false;
            }
        });
      } catch (err) {
      console.log(err);
        this.creatingBank = false;
      }
    },
    showLinkMenu(attrs) {
      this.linkUrl = attrs.href;
      this.linkDialog = true;
    },
    hideLinkMenu() {
      this.linkUrl = null;
      this.linkDialog = false;
      this.linkMenuIsActive = false;
    },
    setLinkUrl(command, url) {
      command({ href: url });
      this.hideLinkMenu();
    },
    addWordToBank(command, node, definition) {
      let selectedNode = this.editor.view.state.doc.cut(
        this.editor.selection.from,
        this.editor.selection.to
      );
      let lexemeText = selectedNode.textContent;
      // console.log(this.editor.view.doc.cut(sliceBetween(this.editor.selection.from, this.editor.selection.to))
      let newLexeme = {
        lexeme: lexemeText,
        definition: definition
      };
      this.$refs.vocabbank.addLexeme(command, newLexeme);
    },

    // @submit.prevent="setLinkUrl(commands.link, linkUrl)">
    setLexemeDefinition(lexemePackage) {
      // command({ definition: definition })
      let command = lexemePackage.returnCommand;
      // this.editor.commands.lexeme({ definition: package.editedItem.definition });
      this.editor.focus();
      console.log(command);
      console.log(lexemePackage.editedItem.translation);
      command({ translation: lexemePackage.editedItem.translation });
      // console.log(definition)
    },

    //   if(this.returnCommand){
    //    console.log(this.returnCommand)
    //    let lexemePackage = {
    //       editedItem: this.editedItem,
    //       returnCommand: this.returnCommand,
    //    }
    //    this.$emit('setLexemeDefinition', lexemePackage);
    //   };



    printText() {
      var html = document.getElementById("editorbox").innerHTML;
      var a = window.open("", "", "height=300, width=300");
      var dateStamp = new Date();
      a.document.write(
        `
          <html>
          <head>
          <title>PF Printer...</title>
          </head>
            <style>
              .header {
                position: fixed;
                top: 0;
                left: 50%;
                transform: translate(-50%, 0);
              }
              .footer {
                position: fixed;
                bottom: 0;
                left: 50%;
                transform: translate(-50%, 0);
              }
              .content {
                font-family:Arial, Helvetica, sans-serif;
                line-height: 1.25em;
                font-size: ${this.editorFontSize}em;
              }
            </style>
            <body>
                <div class="header">${this.lesson.title}</div>
                <div class="content">${html}</div>
                <div class="footer">PidginForge on ${dateStamp.toLocaleString()}</div>
            </body>  
          </html>
          <style>
          `
      );
      a.print();
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
    }
  },
  mounted() {
    this.loadingLesson = true;
    this.getLanguages();
    this.getTopics();
    if (this.lessonslug) {
      console.log("loading")
      this.loadLesson(this.lessonslug);
    } else {
      console.log("making new lesson")
      this.isNewLesson = true;
      this.lesson = {};
      this.loadingLesson = false;
    }
  },
  beforeDestroy() {
    this.editor.destroy();
  }
};
</script>

<style>
.editor > * {
  /* padding: 4px, 4px;
  margin: 4px, 4px; */
}

.ProseMirror {
  color: black;
  background-color: white;
  padding: 10px 10px 10px 10px;
  height: 450px;
  font-size: 1.25em;
  line-height: 1.85em;
  overflow: auto;
  resize: vertical;
  border-color: black;
  border-style: solid;
  border-width: 1px;
  border-radius: 5px;
}

.is-active {
  border-color: orange;
  background-color: darkorange;
  border-style: solid;
  border-width: 1px;
}
</style>
