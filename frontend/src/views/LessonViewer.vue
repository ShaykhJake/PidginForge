<template>
  <v-container fluid>
    <v-card class="mb-2">
      <v-card-title class="desertsand black--text font-weight-black">
        {{ lesson.title }}
      </v-card-title>
      <v-toolbar dense flat class="desertsand">
        <v-btn 
          small 
          class="primary desertsand--text"
          :to="{
            name: 'Lesson-Builder',
            params: {
              lessonslug: lesson.slug
            }
          }"
          v-if="lesson.curator && requestUser==lesson.curator.username"
        >
          Edit Lesson
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn icon class="primary--text">
          <v-icon>mdi-flag</v-icon>
        </v-btn>
        <v-btn icon class="primary--text">
          <v-icon>mdi-eye-off</v-icon>  
        </v-btn>
        <v-btn icon class="primary--text">
          <v-icon>mdi-heart</v-icon>
        </v-btn>
        <v-btn icon class="primary--text">
          <v-icon>mdi-source-fork</v-icon>
        </v-btn>
        
        <v-divider vertical></v-divider>
        <LessonVoter 
          :slug="lesson.slug"
          :up-vote-count="lesson.upvote_count"
          :down-vote-count="lesson.downvote_count"
          :user-vote="lesson.user_vote"
          @updateVote="updateVote"
        />
          
      </v-toolbar>

      <v-card-text class="desertsand pa-1">
        <v-row wrap dense>
          <v-col cols="12">
            <v-card outlined flat>
              <v-card-title class="sandstone py-1 calligraphy--text">
               Metadata
                <v-spacer />

               <v-btn icon class="mx-1 primary--text" @click="showingMetadata=!showingMetadata">
                  <v-icon v-if="showingMetadata">mdi-menu-up</v-icon>
                  <v-icon v-else>mdi-menu-down</v-icon>
               </v-btn>


              </v-card-title>
              <v-card-text v-show="showingMetadata" class="sandstone pt-4">
                <ul>
                  <li>Learning Objective: <strong>{{ lesson.objective }}</strong></li>
                  <li>Skill Level:  <strong>{{ lesson.skill_level }}</strong></li>
                  <li>Lesson Type:  <strong>{{ lesson.lesson_type }}</strong></li>
                  <li>Native Language:  <strong>{{ lesson.native_language }}</strong></li>
                  <li>Target Language: <strong> {{ lesson.target_language }}</strong></li>
                  <li>Primary Topic: <strong> {{ lesson.topic }}</strong></li>
                  <li>Source Citation:  <strong>{{ lesson.citation }}</strong></li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-card flat outlined>
              <v-card-title class="sandstone calligraphy--text py-1">
                Lesson Content
                <v-spacer />
               <v-btn icon class="mx-1 primary--text" @click="showingContentEditor=!showingContentEditor">
                  <v-icon v-if="showingContentEditor">mdi-menu-up</v-icon>
                  <v-icon v-else>mdi-menu-down</v-icon>
               </v-btn>
              </v-card-title>

              <v-card-text
                v-show="showingContentEditor"
                class="sandstone py-0 px-2"
              >
                <editor-menu-bar
                  v-show="false"
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
                class="sandstone px-3"
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
              </v-card-actions>
            </v-card>
          </v-col>

        </v-row>
      </v-card-text>
    </v-card>

    <v-card class="calligraphy mb-2" v-if="false">
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


    <v-card class="calligraphy mb-2">
      <v-card-title class="calligraphy desertsand--text py-1">
         Vocab Bank
         <v-spacer></v-spacer>

         <v-btn icon class="mx-1 primary--text" @click="showingVocabBankViewer=!showingVocabBankViewer">
            <v-icon v-if="showingVocabBankViewer">mdi-menu-up</v-icon>
            <v-icon v-else>mdi-menu-down</v-icon>
         </v-btn>

      </v-card-title>

      <v-card-text v-show="showingVocabBankViewer" class="calligraphy pa-1">

          <VocabBank
            v-if="lesson.primary_vocab"
            :vocab-list="vocabList"
            :source-language="this.lesson.source_language"
            :target-language="this.lesson.target_language"
            :vocab-bank-i-d="lesson.primary_vocab"
            @setLexemeDefinition="setLexemeDefinition"
            ref="vocabbank2"
          />

      </v-card-text>
   </v-card>

    <v-overlay :value="loadingLesson">
      <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
    </v-overlay>
  </v-container>
</template>

<script>
import VocabBank from "@/components/vocab/VocabBank.vue";
import QuizBank from "@/components/quizzes/QuizBank.vue";
import LessonVoter from "@/components/lessons/LessonVoter.vue";
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
  name: "LessonViewer",
  components: {
    EditorContent,
    EditorMenuBar,
    VocabBank,
    QuizBank,
    LessonVoter,
  },
  props: {
    lessonslug: {
      type: String,
      required: false
    }
  },
  data: () => ({
    isNewLesson: true,
    requestUser: "",
    loaded: false,
    building: false,
    skillDialog: false,
    publishing: false,
    lessonTypeDialog: false,
    loadingLesson: false,
    loadingLanguages: false,
    loadingTopics: false,
    allTopics: [],
    allLanguages: [],
    metadataValid: false,
    linkDialog: false,
    lesson: {},
    showingMetadata: true,
    showingContentEditor: true,
    showingVocabBankViewer: true,
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

      requiredSkillLevel: languagevalue =>
        (languagevalue || "").length > 0 || "You must choose a skill level.",
      
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
      editable: false,
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
        }
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
  },
  methods: {
    updateVote(data) {
      this.lesson.user_vote = data.newuservote;
      this.lesson.downvote_count = data.newdowncount;
      this.lesson.upvote_count = data.newupcount;
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
    saveLesson(){  // Save user progress???
      // this.saving = true;
      // let payload = {
      //   title: this.lesson.title,
      //   objective: this.lesson.objective,
      //   skill_level: this.lesson.skill_level,
      //   lesson_type: this.lesson.lesson_type,
      //   native_language: this.lesson.native_language,
      //   target_language: this.lesson.target_language,
      //   topic: this.lesson.topic,
      //   citation: this.lesson.citation, 
      //   content: this.editor.getJSON(),
      // }
      // let endpoint = `/api/lessons/lessonz/${this.lesson.slug}/`;
      // let method = "PATCH";
      // try {
      //   apiService(endpoint, method, payload).then(data => {
      //     if (data) {
      //       console.log(data)
      //       this.saving = false;
      //     } else {
      //       console.log("There was a major problem with the request.");
      //       // console.log(data.message);
      //       this.saving = false;
      //     }
      //   });
      // } catch (err) {
      //   console.log(err);
      //   this.saving = false; 
      // }
    },
    buildNewLesson() { //fork new lesson?
      // let payload = {
      //   title: this.lesson.title,
      //   objective: this.lesson.objective,
      //   skill_level: this.lesson.skill_level,
      //   lesson_type: this.lesson.lesson_type,
      //   native_language: this.lesson.native_language,
      //   target_language: this.lesson.target_language,
      //   topic: this.lesson.topic,
      //   citation: this.lesson.citation, 
      //   published: false,
      //   content: "blank",
      // }
      // let endpoint = `/api/lessons/lessonz/`;
      // let method = "POST";
      // try {
      //   apiService(endpoint, method, payload).then(data => {
      //     if (data) {
      //       this.lesson = data;
      //       this.editor.setContent(this.lesson.content);
      //       this.building = false;
      //       this.isNewLesson = false;
      //     } else {
      //       console.log("There was a major problem with the request.");
      //       // console.log(data.message);
      //       this.building = false;
      //     }
      //   });
      // } catch (err) {
      //   console.log(err);
      //   this.building = false; 
      // }
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
            console.log(data);
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


  },
  mounted() {
    this.loadingLesson = true;
    this.loadLesson(this.lessonslug);
    this.requestUser = localStorage.getItem("username");
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
  background-color: oldlace;
  padding: 10px 10px 10px 10px;
  height: 650px;
  font-size: 1.25em;
  line-height: 1.35em;
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
