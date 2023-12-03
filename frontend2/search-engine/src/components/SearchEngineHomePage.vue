<script>
import SongCard from "@/components/SongCard.vue";
import SongPage from "@/components/SongPage.vue";

// 1.1 check that props song is working (songs are sent to SongCard)
// 1.2 check logic for v-row
// 2. review loading (show a loading while the songs are taken from backend)
// 3. error handling

export default {
  components: {SongPage, SongCard},
  data() {
    return {
      query: null,
      loading: false,
      song_list: [],
      submitted_query: false,
      page_number: 1,
      total_pages: 1,
      selectedSong: null
    }
  },

  methods: {



    async fetch_songs_by_query() {
      //console.log('query: ', this.query);
      try {
        if (this.query) {
          // this loading is not used for now
          this.loading = true
          this.submitted_query=true
          // this.song_list = await Search.custom("search/lyrics/" + this.query).page(1).limit(20).post()
          const res =
              await fetch("http://localhost:8000/search/lyrics/" + this.query + "/?page=" + this.page_number + "&size=50")
          const songs = await res.json()
          this.song_list = songs.items;
          // in case we don't have a round number, give another page: 1.3 -> 2
          // Math.ceil(songs.items.length / 10)
          // TODO: find a way to have total_pages
          this.total_pages = 1;

        }
      } catch (err) {
        // TODO: handle the error
        console.log("error occured: ", err);
        this.song_list = [];
      } finally {
        // this loading is not used for now
        this.loading = false;
      }

    },
    onPageChange(newPage) {
      this.page_number = newPage;
      this.fetch_songs_by_query();
    },
    getSongPage(song){
     this.selectedSong = song;

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
      class="flex-full-width pa-4"
      density="comfortable"
      item-props
      hide-no-data
      menu-icon=""
      placeholder="Search a lyric"
      clearable
      rounded
      v-model="query"
      theme="light"
      variant="solo"
  >
    <template v-slot:prepend>
      <v-btn @click="fetch_songs_by_query()" icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </template>
    <template v-slot:append>
      <v-avatar>
        <v-img src="https://cdn-icons-png.flaticon.com/512/3844/3844724.png"></v-img>
      </v-avatar>
    </template>
  </v-combobox>

<div v-if="selectedSong === null">
  <div v-if="submitted_query"
       class="d-flex align-center justify-center">
    <div v-if="loading">
      <v-progress-circular
          indeterminate
          color="red"
      ></v-progress-circular>
    </div>
    <div v-else>
      <div v-if="song_list.length">
        <v-row v-for="song in song_list" :key="song.id">
          <v-col>
            <SongCard :song="song"
                      @songCardClicked="getSongPage"></SongCard>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-alert type="info" class="my-4 rounded-xl" >No match found.</v-alert>
      </div>
    </div>
  </div>

  <v-pagination
      v-if="total_pages > 1"
      v-model="page_number"
      :length="total_pages"
      rounded="circle"
      class="pa-4"
      @input="onPageChange"
  ></v-pagination>
</div>

  <song-page v-if="selectedSong"
             :selectedSong="selectedSong"></song-page>

</template>
