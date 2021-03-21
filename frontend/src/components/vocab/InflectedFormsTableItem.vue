<template>
  <div class="desertsand calligraphy--text pa-0">
    <InflectedDefinitionsTable
      :inflectedid="word.id"
      :definitions="word.definitions"
    />
    <hr />
    <InflectedPronunciationsTable
      :inflectedid="word.id"
      :pronunciations="word.pronunciations"
    />
    <hr />
    <InflectedSentencesTable
      :inflectedid="word.id"
      :sentences="word.sentences"
      :direction="word.direction"
      :language="word.language"
    />
  </div>
</template>

<script>
import InflectedDefinitionsTable from "@/components/vocab/InflectedDefinitionsTable.vue";
import InflectedPronunciationsTable from "@/components/vocab/InflectedPronunciationsTable.vue";
import InflectedSentencesTable from "@/components/vocab/InflectedSentencesTable.vue";
export default {
  name: "InflectedFormsTableItem",
  props: {
    word: {}
  },
  components: {
    InflectedDefinitionsTable,
    InflectedPronunciationsTable,
    InflectedSentencesTable
  }
};
</script>

<style></style>
