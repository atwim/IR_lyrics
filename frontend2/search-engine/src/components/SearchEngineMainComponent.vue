<script>
import SongCard from "@/components/SongCard.vue";
import SongPage from "@/components/SongPage.vue";

export default {
  components: {SongPage, SongCard},
  // 1. buttons genre feedback
  // 2. homepage buttons

  data() {
    return {
      query: null,
      loading: false,
      song_list: [],
      genre_list: [],
      submitted_query: false,
      page_number: 1,
      total_pages: 0,
      selectedGenre: '',
      selectedSong: null
    }
  },
  watch: {
      query(newQuery, oldQuery){
      console.log(this.loading)
      if(newQuery !== oldQuery && this.loading === true)
        this.page_number = 1;
    }
  },
  async mounted() {
    await this.fetchGenres()
  },
  methods: {
    async fetchGenres(){
      const res1 = await fetch(
          "http://localhost:8000/genre-list")
      this.genre_list = await res1.json()
    },


   async fetch_songs_by_query() {
      try {
        if (this.query) {

          this.selectedSong = null;
          this.loading = true
          this.submitted_query=true

          const res = await fetch(
              "http://localhost:8000/search/lyrics/" + this.query + "/?genre="+this.selectedGenre+"&page=" + this.page_number + "&size=10")
          const songs = await res.json()
          this.song_list = songs.items;
          // in case we don't have a round number, give another page: 1.3 -> 2
          this.total_pages = Math.ceil(songs.total / 10);
        }
      } catch (err) {
        console.log("error occured: ", err);
        this.song_list = [];
      } finally {
        this.loading = false;
      }

    },

    getPrevPage() {
      if(this.page_number > 1)
        this.page_number -= 1;

      this.fetch_songs_by_query();
    },
    getNextPage() {
      if(this.page_number < this.total_pages)
        this.page_number += 1;

      this.fetch_songs_by_query();
    },
    getSongPage(song){
     this.page_number = 1;
     this.selectedSong = song;
    },
    returnToHomePage(){
      this.query = null,
      this.loading = false,
      this.song_list = [],
      this.submitted_query = false,
      this.page_number = 1,
      this.total_pages = 0,
      this.selectedGenre = '',
      this.selectedSong = null
    },
    enterNewQuery(){
      this.fetch_songs_by_query();
      this.page_number = 1
    }
  }
}

</script>

<template>

<div v-if="!submitted_query">
    <v-img src="https://cdn-icons-png.flaticon.com/512/3844/3844724.png"
           :width="200"
           class="mx-auto mt-15 mb-4">
        <template v-slot:placeholder>
          <div class="d-flex align-center justify-center fill-height">
            <v-progress-circular
                color="grey-lighten-4"
                indeterminate
            ></v-progress-circular>
          </div>
        </template>
    </v-img>
</div>



  <v-combobox
      auto-select-first
      class=" pa-4"
      density="comfortable"
      item-props
      hide-no-data
      menu-icon=""
      placeholder="Search a lyric"
      clearable
      rounded
      v-model="query"
      theme="light"
      @keyup.enter="enterNewQuery()"
      variant="solo">
    <template v-slot:prepend>
      <v-btn @click="enterNewQuery()" icon> <v-icon>mdi-magnify</v-icon> </v-btn>
    </template>
    <template v-slot:append v-if="submitted_query">
     <v-btn @click="returnToHomePage()" icon>  <v-avatar><v-img src="https://cdn-icons-png.flaticon.com/512/3844/3844724.png"></v-img></v-avatar></v-btn>
    </template>
  </v-combobox>

  <h1 v-if="!submitted_query"
      class="d-flex align-center justify-center"> Welcome to MusicLyrics!</h1>

  <div v-if="!submitted_query">
    <p style="text-align: center" class="pa-2"> Search by genre: </p>
  </div>

<div v-if="!submitted_query" class="d-flex justify-center ma-4">
  <v-btn class="mr-4"  @click="selectedGenre = genre_list[0]">{{genre_list[0]}}</v-btn>
  <v-btn class="mr-4"  @click="selectedGenre = genre_list[1]">{{genre_list[1]}}</v-btn>
  <v-btn class="mr-4"  @click="selectedGenre = genre_list[2]">{{genre_list[2]}}</v-btn>
  <v-btn class="mr-4"  @click="selectedGenre = genre_list[3]">{{genre_list[3]}}</v-btn>
  <v-btn class="mr-4"  @click="selectedGenre = ''"> Remove filters </v-btn>
</div>

  <div v-if="selectedGenre && selectedSong === null">
    <p style="text-align: center" > Search songs in the {{ selectedGenre }} Genre </p>
  </div>

<div v-if="selectedSong === null">

  <div v-if="submitted_query"  class="d-flex align-center justify-center">

    <div v-if="loading">
      <v-progress-circular indeterminate color="red"></v-progress-circular>
    </div>

    <div v-else>
      <div v-if="song_list.length">
        <v-row v-for="song in song_list" :key="song.id"> <v-col> <SongCard :song="song" @songCardClicked="getSongPage" :is-relevant-list="false"></SongCard> </v-col> </v-row>
      </div>

      <div v-else>
        <v-alert type="info" class="my-4 rounded-xl" >No match found.</v-alert>
      </div>
    </div>
  </div>

    <div v-if="total_pages > 1"
         class="d-flex align-center justify-center pa-4">
      <v-btn @click="getPrevPage()">PREV</v-btn>
      <div><p class="pa-2">current page: {{page_number}} / {{total_pages}}</p></div>
      <v-btn @click="getNextPage()">NEXT</v-btn>
    </div>
</div>

  <song-page v-if="selectedSong" :selectedSong="selectedSong" @songCardClicked="getSongPage"></song-page>

</template>
