<template>
  <div>

      <v-card
         class="sandstorm mb-2"
      >
         <v-card-title class="sandstone py-1">
            {{ `Question #${questionIndex + 1}: "${question.stem.substr(0,25)}..."`}}

            <v-spacer></v-spacer>
            <v-btn 
                  small
                  @click="deleteQuestion(questionIndex)"
                  class="garbage desertsand--text mx-1"
            >
                  Delete
                  <v-icon right>mdi-delete</v-icon>
            </v-btn>

            <v-btn 
                  small
                  class="primary desertsand--text mx-1"
                  :disabled="questionIndex == 0"
                  @click="changeOrder('up', questionIndex)"
            >
                  Move Up
                  <v-icon right>
                  mdi-arrow-up
                  </v-icon>
            </v-btn>

            <v-btn 
                  small 
                  class="primary desertsand--text mx-1"
                  :disabled="questionIndex == totalQuestions-1"
                  @click="changeOrder('down', questionIndex)"

            >
                  Move Down
                  <v-icon right>
                  mdi-arrow-down
                  </v-icon>
            </v-btn>

            <v-btn fab icon class="mx-1 primary--text" @click="showingQuestion=!showingQuestion">
               <v-icon v-if="showingQuestion">mdi-menu-up</v-icon>
               <v-icon v-else>mdi-menu-down</v-icon>
            </v-btn>

            </v-card-title>

            <v-card-text class="desertsand pt-2" v-show="showingQuestion">

               <div v-if="false">
                  <h3>Rich Content:</h3>
                  <v-switch 
                     v-model="question.rich_content.enabled"
                     :input-value="question.rich_content.enabled"
                     hint="Turning this on allows you to use audio, video, rich text, or photos as 
                     content for the question stem (best for comprehension)."
                     persistent-hint
                     class="mt-0"
                  ></v-switch>
                  <div v-if="question.rich_content.enabled">
                     <v-select
                     v-model="question.rich_content.content_type"
                     :items="contentTypes"
                     label="Rich Content Type"
                     class="mt-2"
                     outlined
                  ></v-select>
                     <div v-if="question.rich_content.content_type==='Audio'">
                        Audio
                     </div>
                     <div v-if="question.rich_content.content_type==='Video'">
                        Video
                     </div>
                     <div v-if="question.rich_content.content_type==='Rich Text'">
                        Rich Text

                     </div>
                     <div v-if="question.rich_content.content_type==='Image'">
                        Image
                     </div>
                  </div>
                  <hr>
               </div>
   
               <h2>Question Stem:</h2>
               <v-switch 
                  v-model="question.stem_rtl"
                  label="Right-to-Left"
                  hint="Changes the text direction for the stem."
                  persistent-hint
                  class="mt-0"
               ></v-switch>

               
               <div :style="`${question.stem_rtl ? 'direction: rtl;' : 'direction: ltr;'}`">
                  <v-textarea
                     v-model="question.stem"
                     outlined
                     label="Question Stem Text"
                     placeholder="question stem text"
                     counter
                     maxlength="150"
                     rows="2"
                     class="mt-5"
                  ></v-textarea>

               </div>

               <hr>
               <h2>Answer Alternatives ({{question.alternatives.length}}):
                  <v-btn fabsmall class="primary desertsand--text ml-2" @click="addAlternative">
                     Add Alternative
                     <v-icon right>mdi-plus-circle</v-icon>
                  </v-btn>
               </h2>
               <v-switch 
                  v-model="question.alternatives_rtl"
                  label="Right-to-Left"
                  hint="Changes the text direction for the set of alternatives."
                  persistent-hint
                  class="mt-0"
               ></v-switch>
               <v-switch 
                  v-model="question.multiple_select"
                  label="Multiple Select"
                  hint="Off is for standard multiple choice; on allows users to choose multiple answers"
                  persistent-hint
                  class="mt-0"
               ></v-switch>
               <v-switch 
                  v-model="question.randomize_alternatives"
                  label="Randomize Order"
                  hint="When on, this will randomize the order in which the alternatives appear to the test taker"
                  persistent-hint
                  class="mt-0"
               ></v-switch>
               <div :style="`${ question.alternatives_rtl ? 'direction:rtl' : 'direction: ltr'}`">
                  <div v-if="!question.multiple_select">
                     <v-radio-group 
                        v-model="question.answer_key"
                        :input-value="question.answer_key"
                        class="my-1"
                     >
                              <v-card
                                 v-for="(alternative, altIndex) in question.alternatives" 
                                 :key="alternative.id"
                                 dense
                                 class="sandstone mb-2"
                              >
                                 <v-card-actions class="sandstone">
                                    Answer Alternative #{{ altIndex + 1}}
                                    <v-spacer></v-spacer>
                                    <v-btn 
                                       small
                                       @click="deleteAlternative(altIndex)"
                                       class="garbage desertsand--text mx-1"
                                    >
                                       Delete
                                       <v-icon right>mdi-delete</v-icon>
                                    </v-btn>
                                    <v-btn 
                                       small
                                       class="primary desertsand--text mx-1"
                                       :disabled="altIndex == 0"
                                       @click="changeOrder('up', altIndex)"
                                    >
                                       Move Up
                                       <v-icon right>
                                          mdi-arrow-up
                                       </v-icon>
                                    </v-btn>
                                    <v-btn 
                                       small 
                                       class="primary desertsand--text mx-1"
                                       :disabled="altIndex == question.alternatives.length-1"
                                       @click="changeOrder('down', altIndex)"

                                    >
                                       Move Down
                                       <v-icon right>
                                          mdi-arrow-down
                                       </v-icon>
                                    </v-btn>


                                 </v-card-actions>
                                 <v-card-text :class="alternative_class(question.answer_key, alternative.id)">
                                    <v-radio 
                                       label="Correct"
                                       :value="alternative.id"
                                       color="green--darken-2"
                                    >
                                    </v-radio>
                                    <v-textarea
                                       v-model="alternative.text"
                                       outlined
                                       label="Alternative Text"
                                       placeholder="alternative text"
                                       counter
                                       color="primary"
                                       maxlength="150"
                                       rows="2"
                                    ></v-textarea>
                                 </v-card-text>
                              </v-card>
                     </v-radio-group>

                  </div>
               
                  <div v-else>
                     <v-card
                        v-for="(alternative, altIndex) in question.alternatives" 
                        :key="alternative.id"
                        dense
                        class="sandstone mb-2"
                     >
                        <v-card-actions class="sandstone">
                           Answer Alternative #{{ altIndex + 1}}
                           <v-spacer></v-spacer>
                           <v-btn 
                              small
                              class="primary desertsand--text mx-1"
                              :disabled="altIndex == 0"
                              @click="changeOrder('up', altIndex)"
                           >
                              Move Up
                              <v-icon right>
                                 mdi-arrow-up
                              </v-icon>
                           </v-btn>
                           <v-btn 
                              small 
                              class="primary desertsand--text mx-1"
                              :disabled="altIndex == question.alternatives.length-1"
                              @click="changeOrder('down', altIndex)"

                           >
                              Move Down
                              <v-icon right>
                              mdi-arrow-down
                              </v-icon>
                           </v-btn>
                           <v-btn 
                              small
                              @click="deleteAlternative(altIndex)"
                              class="garbage desertsand--text mx-1"
                           >
                              Delete
                              <v-icon right>mdi-delete</v-icon>
                           </v-btn>

                        </v-card-actions>
                        <v-card-text :class="alternative_class(question.answer_key, alternative.id)">
                           <v-checkbox
                              dense
                              v-model="question.answer_key"
                              label="correct" 
                              :value="alternative.id"
                              color="green--darken-2"
                           ></v-checkbox>
                           <v-textarea
                              v-model="alternative.text"
                              outlined
                              label="Alternative Text"
                              placeholder="alternative text"
                              counter
                              color="primary"
                              maxlength="150"
                              rows="2"
                           ></v-textarea>                  
                        </v-card-text>
                     </v-card>
                  </div>
               </div>

            </v-card-text>
         </v-card>

  </div>
</template>

<script>
export default {
   name: "MCQQuestionEditor",
   props: {
      question: Object,
      questionIndex: Number,
      totalQuestions: Number,

   },
   components: {

   },
   data() {
      return {
         isNewQuestion: false,
         contentTypes: [
            "Audio", "Video", "Rich Text", "Image"
         ],
         showingQuestion: true,
      }
   },
   computed:{
      
   },
   methods:{
      alternative_class(answer_key, alternative_key){
         if(!this.question.multiple_select){
            if(alternative_key === answer_key){
               return "alternative correct";
            } else {
               return "alternative incorrect";
            }
         } else {
            if(answer_key.includes(alternative_key)){
               return "alternative correct";
            } else {
               return "alternative incorrect";
            }

         }
      },
      addAlternative(){
         var altids = [];
         for(let i = 0; i < this.question.alternatives.length; i++){
            altids.push(this.question.alternatives[i].id)
         }
         for(let i = 0; i < this.question.alternatives.length + 1; i++){
            if(!altids.includes(i.toString())){
               var newaltid = i.toString();
               break
            }
         };
         let newAlternative={
            text: "new alternative",
            id: newaltid,
         }
         this.question.alternatives.push(newAlternative);
      },
      deleteAlternative(index){
         this.question.alternatives.splice(index,1);
      },
      deleteQuestion(index){
         this.$emit("deleteQuestion", index);
      },
      changeOrder(direction, index){
         this.$emit("changeQuestionOrder", { direction: direction, index: index})
         // if (direction === "up"){
         //    let tmp = this.question.alternatives[index];
         //    this.question.alternatives.splice(index,1);
         //    this.question.alternatives.splice(index-1,0,tmp);
         // } else {
         //    let tmp = this.question.alternatives[index];
         //    this.question.alternatives.splice(index,1);
         //    this.question.alternatives.splice(index+1,0,tmp);
         // }
      },
   }
}
</script>
<style>
.alternative {
   margin-bottom: 2px;
   margin-top: 0px;
}
.correct {
   background-color: rgb(172, 238, 172);

}
.incorrect {
   background-color: rgb(231, 161, 161);

}
.rtl {
   direction: rtl;
}
.ltr {
   direction: ltr;
}



</style>