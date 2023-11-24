<script>
import SongCard from "@/components/SongCard.vue";


// 1.1 check that props song is working (songs are sent to SongCard)
// 1.2 check logic for v-row
// 2. review loading (show a loading while the songs are taken from backend)
// 3. error handling

export default {
  components: {SongCard},
  data() {
    return {
      query: null,
      loading: false,
      song_list: []
    }
  },

  methods: {
    async fetch_songs_by_query() {
      console.log('query: ', this.query);
      try {
        if (this.query) {
          // this loading is not used for now
          this.loading=true
          const res = await fetch(`http://localhost:8080/search/lyrics/${this.query}`)
          const songs = await res.json()
          this.song_list = songs;
        }
      } catch (err) {
        // TODO: handle the error
        console.log("error occured");
        this.song_list = [];
      } finally {
        // this loading is not used for now
        this.loading = false;
      }

    }
  },
  watch: {
    // function to debug the query, everytime query changes its console logged.
    query: function(newQuery) {
      console.log('query changed:', newQuery);
    }
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
      clearable
      rounded
      v-model="query"

      theme="light"
      variant="solo"
  ></v-combobox>

  <v-btn @click="fetch_songs_by_query()">
    submit
  </v-btn>


    print query: {{query}}

    <v-row v-for="song in song_list"
           :key="song.id">
      <SongCard   :song="song">
      </SongCard>
    </v-row>
</template>

<style scoped>

</style>