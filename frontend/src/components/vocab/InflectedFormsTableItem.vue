<template>
   <div>
      <h3>Definitions</h3>
         <hr>
         <v-card>
            <v-card-text pa-0>
               <InflectedDefinitionsTable 
                  :inflectedid="word.id"
                  :definitions="word.definitions"
               />
            </v-card-text>
         </v-card>

         
      <h3>Pronunciations</h3>
         <hr>
         <v-card>
            <v-card-text pa-0>
               <InflectedPronunciationsTable 
                  :inflectedid="word.id"
                  :pronunciations="word.pronunciations"
               />
            </v-card-text>
         </v-card>


      <h3>Sentences</h3>
         <hr>
   </div>
</template>

<script>
import InflectedDefinitionsTable from "@/components/vocab/InflectedDefinitionsTable.vue"
import InflectedPronunciationsTable from "@/components/vocab/InflectedPronunciationsTable.vue"
export default {
   name: "InflectedFormsTableItem",
   props: {
      word: {}
   },
   components: {
      InflectedDefinitionsTable,
      InflectedPronunciationsTable,
   }
}
</script>

<style>

</style>