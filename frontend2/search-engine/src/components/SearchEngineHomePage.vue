<script>
export default {
  data() {
    return {
      query: null,
      q2: null,
      song_list: []
    }
  },

  methods: {
    async fetch_songs_by_query() {
      console.log('query: ', this.query);
      if (this.query) {
        const res = await fetch(`http://localhost:8080/search/lyrics/${this.query}`)
        const songs = await res.json()
        this.song_list = songs
      }
    }
  },

  watch: {

  }




}

</script>

<template>
  <v-combobox
      
      auto-select-first
      class="flex-full-width"
      density="comfortable"
      item-props
      hide-no-data
      menu-icon=""
      placeholder="Search a lyric"
      prepend-inner-icon="mdi-magnify"
      rounded
      v-model="query"

      theme="light"
      variant="solo"
  ></v-combobox>

  <v-btn @click="fetch_songs_by_query()">
    submit
  </v-btn>


    {{query}}
  <input v-model="q2" />
  {{q2}}

</template>

<style scoped>

</style>