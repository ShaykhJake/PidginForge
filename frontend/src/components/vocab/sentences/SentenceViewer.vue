<template>
  <v-dialog v-model="dialog" max-width="375" persistent scrollable>
     <v-card class="desertsand">
        <v-card-title class="sandstone">
           Sentence Viewer
        </v-card-title>
        <v-card-text class="px-2">
           <div v-if="loading" style="text-align: center;">
               <v-progress-circular
                  :size="70"
                  :width="7"
                  color="primary"
                  indeterminate
               ></v-progress-circular>
           </div>
           <div v-else>
              <div :style="`direction:${sentence.direction}`" class="sentenceBox title my-2">
                 {{ sentence.text }}
              </div>
              <div class="overline">
                 <v-chip class="languages languages--text mr-2" outlined x-small>
                  {{ sentence.language }}
                 </v-chip>
                 <br>
                 Curated by <span class="primary--text font-weight-black">{{ sentence.curator.username }}</span> on {{ sentence.curationdate }}
              </div>
               <hr class="my-2">
              <div class="mt-3">
                 <h3>Audio Recordings ({{audioArray.length}}) 
                  <v-btn class="primary" small @click="addAudio">Add</v-btn></h3>

                     <div 
                        class="listBox sandstone my-1"
                        v-if="audioArray.length > 0" 
                     >
                        <v-row 
                           v-for="item in audioArray" 
                           :key="item.id"
                           flat
                           class="mb-1"
                           dense
                        >

                        <v-col cols="1" align="center">
                              <v-btn
                                 small 
                                 icon 
                                 class="primary--text" 
                                 @click="playAudio(item.audio_file)"
                              >   
                                 <v-icon>
                                    mdi-volume-high
                                 </v-icon>
                              </v-btn>
                        </v-col>

                        <v-col class="body-1">
                           <div class="roundBox">
                              Sentence Audio ID #{{item.id}}
                           </div>
                              <div class="overline">
                                 Curated by 
                                 <span class="primary--text font-weight-black">
                                    {{ item.curator.username }}
                                 </span> 
                                 on {{ item.curationdate }}
                              </div>
                        </v-col>

                        <v-col cols="1" align="right">
                           <v-icon 
                              small 
                              @click="editAudio(item)" 
                              v-if="requestUser === item.curator.username"
                           >
                              mdi-pencil
                           </v-icon>
                           <v-icon 
                              small 
                              @click="deleteAudioSelection=item.id" 
                              v-if="requestUser === item.curator.username"
                           >
                              mdi-delete
                           </v-icon><br>

                        </v-col>
                           <v-overlay
                              absolute
                              :value="item.id === deleteAudioSelection ? true : false"
                              opacity=".8"
                           >
                              <div class="title" style="text-align:center;">
                                 Confirm Delete?   
                              </div>
                              
                              <v-btn
                                 small
                                 class="calligraphy desertsand--text mr-3"
                                 @click="deleteAudioSelection = null"
                              >
                                 Cancel
                              </v-btn>

                              <v-btn
                                 small
                                 class="primary"
                                 @click="deleteAudio(item.id)"
                              >
                                 Delete
                              </v-btn>

                           </v-overlay>
                        </v-row>
                     </div>

              </div>
              <div class="mb-2 mt-3">
                 <h3>Translations ({{translationArray.length}}) 
                  <v-btn @click="attachTranslation" class="primary" small>Add</v-btn></h3>
                     <div 
                        class="listBox sandstone my-1"
                        v-if="translationArray.length > 0" 
                     >
                        <div
                           v-for="item in translationArray" 
                           :key="item.id"
                           class="mb-1"
                        >
                           <v-row 

                              dense
                           >
                           <v-col class="body-1">
                              <div :style="`direction: ${item.direction}`" class="roundBox">
                                 {{ item.text }}
                              </div>
                                 <div class="overline">
                                    Curated by 
                                    <span class="primary--text font-weight-black">
                                       {{ item.curator.username }}
                                    </span> 
                                    on {{ item.curationdate }}
                                 </div>
                           </v-col>

                           <v-col cols="1" align="right">
                              <v-icon 
                                 small 
                                 @click="editTranslation(item)" 
                                 v-if="requestUser === item.curator.username"
                              >
                                 mdi-pencil
                              </v-icon>
                              <v-icon 
                                 small 
                                 @click="deleteTranslationSelection=item.id" 
                                 v-if="requestUser === item.curator.username"
                              >
                                 mdi-delete
                              </v-icon><br>

                           </v-col>
                           </v-row>
                           <v-overlay
                                 absolute
                                 :value="item.id === deleteTranslationSelection ? true : false"
                                 opacity=".8"
                              >
                                 <div class="title" style="text-align:center;">
                                    Confirm Delete?   
                                 </div>
                                 
                                 <v-btn
                                    small
                                    class="calligraphy desertsand--text mr-3"
                                    @click="deleteTranslationSelection = null"
                                 >
                                    Cancel
                                 </v-btn>

                                 <v-btn
                                    small
                                    class="primary"
                                    @click="deleteTranslation(item.id)"
                                 >
                                    Delete
                                 </v-btn>
                              </v-overlay>
                           </div>


                        </div>


              </div>
               <div class="mt-2">
                 <h3>Linked Words/Terms ({{inflectedWordArray.length}}) <v-btn class="primary" small>Add</v-btn></h3>

                     <div 
                        class="listBox sandstone my-1"
                        v-if="inflectedWordArray.length > 0" 
                     >
                        <div
                           v-for="item in inflectedWordArray" 
                           :key="item.id"
                           class="mb-1"
                        >
                           <v-row 

                              dense
                           >
                           <v-col class="body-1">
                              <div 
                                 :style="`direction: ${item.language.direction}`" 
                                 class="roundBox"
                                 @click="viewLexemeSelection=item.lexeme.slug" 
                              >
                                 {{ item.word }}
                              </div>
                                 <div class="overline">
                                    Curated by 
                                    <span class="primary--text font-weight-black">
                                       {{ item.curator.username }}
                                    </span> 
                                 </div>
                                 <div>
                                 </div>
                           </v-col>

                           <v-col cols="1" align="right">
                              <v-icon 
                                 small 
                                 @click="editTranslation(item)" 
                                 v-if="requestUser === item.curator.username"
                              >
                                 mdi-pencil
                              </v-icon>
                              <v-icon 
                                 small 
                                 @click="deleteTranslationSelection=item.id" 
                                 v-if="requestUser === item.curator.username"
                              >
                                 mdi-delete
                              </v-icon><br>

                           </v-col>
                           </v-row>
                           <v-overlay
                                 absolute
                                 :value="viewLexemeSelection ? true : false"
                                 opacity=".89"
                              >
                              <div style="text-align:center;">
                                 <div class="title">
                                    View Lexeme?
                                 </div>

                                 <span class="overline">Would you like to view the
                                    parent lexeme? This will route you away from the current
                                    page.
                                 </span>
                                 <br>
                                 <v-btn
                                    small
                                    class="calligraphy desertsand--text mr-3"
                                    @click="viewLexemeSelection = null"
                                 >
                                    Cancel
                                 </v-btn>

                                 <v-btn
                                    small
                                    class="primary"
                                    @click="$router.push({name: 'Lexeme-Curator', params: { lexemeslug: item.lexeme.slug },})"
                                 >
                                    View Lexeme
                                 </v-btn>
                              </div>

                              </v-overlay>
                           </div>


                        </div>






              </div>

           </div>

           
        </v-card-text>
        <v-card-actions class="sandstone">
           <v-btn class="garbage desertsand--text" @click="closeDialog">
              Close
           </v-btn>
        </v-card-actions>
     </v-card>

      <AttachAudio 
         v-if="attachAudioDialog"
         :dialog="attachAudioDialog"
         :sentence="sentence"
         :audio-record="selectedAudio"
         @closeDialog="attachAudioDialog=false"
         @pushAudio="pushAudio"
         @updateAudio="updateAudio"
      />
      <AttachTranslation
         v-if="attachTranslationDialog"
         :dialog="attachTranslationDialog"
         :sentence="sentence"
         :translation="selectedTranslation"
         @closeDialog="attachTranslationDialog=false"
         @pushTranslation="pushTranslation"
         @updateTranslation="updateTranslation"
      />
      <v-dialog max-width=315 v-model="playerDialog" v-if="playerDialog && audio">
         <v-card class="desertsand">
            <v-card-title class="sandstone">
               Audio Player
            </v-card-title>
            <v-card-text class="px-1">
               <div :style="`direction:${sentence.direction}`" class="sentenceBox title mt-2">
                 {{ sentence.text }}
              </div>
               <audio 
                  controls 
                  autoplay 
                  :src="audio"
                  class="mt-3"
               >
               </audio>

            </v-card-text>
            <v-card-actions class="justify-center sandstone">
               <v-btn @click="playerDialog=false; audio=null" class="garbage desertsand--text">Close</v-btn>
            </v-card-actions>
         </v-card>
      </v-dialog>

  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
// import { apiFileService } from "@/common/api.fileservice.js";

export default {
   name: "SentenceViewer",
   props: {
      sentenceID: [String, Number],
      dialog: {
         type: Boolean,
         default: false
      }
   },
   components: {
      AttachAudio: () => import("@/components/vocab/sentences/AttachAudio.vue"),
      AttachTranslation: () => import("@/components/vocab/sentences/AttachTranslation.vue"),
   },
   data: () => ({
      loading: true,
      attachAudioDialog: false,
      audio: null,
      audioArray: [],
      translationArray: [],
      inflectedWordArray: [],
      deleteTranslationOverlay: false,
      deleteAudioOverlay: false,
      deleteAudioSelection: null,
      deleteTranslationSelection: null,
      viewLexemeSelection: null,
      playerDialog: false,
      attachTranslationDialog: false,
      selectedTranslation: null,
      selectedAudio: null
   }),
   computed: {
      requestUser(){
       return localStorage.getItem("username");
    }, 
   },
   methods: {
      closeDialog(){
         this.$emit("closeDialog")
      },
      
      loadSentence(id){
         this.loading = true;
         console.log(id)
         const endpoint = `/api/vocab/sentencez/${id}/`;
         const method = "GET";

         try {
            apiService(endpoint, method).then(data => {
               if (data && data.id) {
                  this.sentence = data;
                  this.audioArray = this.sentence.audio;
                  this.translationArray = this.sentence.translations;
                  this.inflectedWordArray = this.sentence.inflectedforms;
                  this.loading=false;
               } else {
                  console.log(data)
                  console.log("Something bad happended!")
                  this.loading=false;
               }
            });
         } catch (err) {
            console.log(err);
            this.loading = false;
         } 
      },

      saveSentence(){

      },
      attachWord(){

      },
      detachWord(){

      },



      editTranslation(translation){
         this.selectedTranslation = translation;
         this.attachTranslationDialog = true;
      },

      updateTranslation(translation){
         const index = this.translationArray.indexOf(this.selectedTranslation);
         this.translationArray.splice(index, 1, translation);
         // console.log(translation)
         // this.translationArray.push(translation)

         // this.translationArray[index] = translation
      },
      attachTranslation(){
         this.selectedTranslation = {
            text: "",
            curator_note: "",
            sentence: this.sentence.id,
         }
         this.attachTranslationDialog = true;
      },
      pushTranslation(translation){
         this.translationArray.push(translation);
      },
      deleteTranslation(item){
         this.deleting = true;
         this.deleteTranslationSelection = null;
         const index = this.translationArray.indexOf(item);
         const endpoint = `/api/vocab/sentencetranslationz/${item.id}/`;
         const method = "DELETE";
         try {
            apiService(endpoint, method).then(() => {
               this.translationArray.splice(index, 1);
               this.deleting=false;
            });
         } catch (err) {
            console.log(err);
            this.deleting = false;
         } 
      },



      addAudio(){
         this.selectedAudio = null;
         this.attachAudioDialog = true;
      },
      pushAudio(audio){
         this.audioArray.push(audio);
      },
      editAudio(audio){
         this.selectedAudio = audio;
         this.attachAudioDialog = true;
      },
      updateAudio(audio){
         const index = this.audioArray.indexOf(this.selectedAudio);
         console.log(audio)
         this.audioArray.splice(index, 1, audio);
      },

      setNewAudio(audio){
         this.newAudio = audio;
      },

      deleteAudio(item){
         this.deleting = true;
         const index = this.audioArray.indexOf(item);
         const endpoint = `/api/vocab/sentenceaudioz/${item.id}/`;
         const method = "DELETE";
         this.deleteAudioSelection = null;

         try {
            apiService(endpoint, method).then(() => {
               this.audioArray.splice(index, 1);
               this.deleting=false;
            });
         } catch (err) {
            console.log(err);
            this.deleting = false;
         } 
      },

      playAudio(audio){
         this.audio = audio;
         this.playerDialog = true;
      }
   },
   mounted(){
      if(this.sentenceID){
         this.loading=true;
         this.loadSentence(this.sentenceID);
      }
   },
}
</script>

<style scoped>
.sentenceBox {
color: black;
  background-color: antiquewhite;
  border-left-style: solid;
  border-right-style: solid;
  border-width: 1px;
  border-radius: 5px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
}
.roundBox {
  color: black;
  background-color: antiquewhite;

  border-left-style: solid;
  border-right-style: solid;
  border-width: 1px;
  border-radius: 5px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
}
.listBox {
  height: 95px; 
  overflow: scroll;
  border-width: 1px;
  border-radius: 10px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
}

audio {
    /* filter: sepia(20%) saturate(70%) grayscale(1) contrast(99%) invert(12%) drop-shadow(3px 3px 3px orange); */
    /* filter: drop-shadow(2px 2px 2px orange); */
    width: 100%;
    height: 50px;
}
/* https://chromium.googlesource.com/chromium/blink/+/72fef91ac1ef679207f51def8133b336a6f6588f/Source/core/css/mediaControls.css?autodive=0%2F%2F%2F */
audio::-webkit-media-controls-panel {
    display: flex;
    flex-direction: row;
    align-items: center;
    /* We use flex-start here to ensure that the play button is visible even
     * if we are too small to show all controls.
     */
    justify-content: flex-start;
    -webkit-user-select: none;
    position: relative;
    z-index: 5;
    height: 50px;
    /* background-color: #DBD4C4; */
    background-color: rgba(219, 212, 196, 1.0);
    /* border-radius: 5px; */
    /* The duration is also specified in MediaControlElements.cpp and LayoutTests/media/media-controls.js */
    transition: opacity 0.3s;
}

</style>