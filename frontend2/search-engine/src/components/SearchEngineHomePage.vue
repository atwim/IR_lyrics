<script>
import SongCard from "@/components/SongCard.vue";
import SongPage from "@/components/SongPage.vue";

export default {
  components: {SongPage, SongCard},
  data() {
    return {
      query: null,
      loading: false,
      song_list: [],
      submitted_query: false,
      page_number: 1,
      total_pages: 0,
      selectedSong: null
    }
  },

  methods: {
   async fetch_songs_by_query() {
      //console.log('query: ', this.query);
      try {
        if (this.query) {
          this.selectedSong = null;
          this.loading = true
          this.submitted_query=true
          console.log(this.page_number);
          const res = await fetch(
              "http://localhost:8000/search/lyrics/" + this.query + "/?page=" + this.page_number + "&size=10")
          const songs = await res.json()
          this.song_list = songs.items;
          // in case we don't have a round number, give another page: 1.3 -> 2
          this.total_pages = Math.ceil(songs.total / 10);
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
    // TODO: how to tell the user you are in the last page? (v-pagination like component)
    // both getPrevPage and getNextPage
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
      variant="solo">
    <template v-slot:prepend>
      <v-btn @click="fetch_songs_by_query()" icon> <v-icon>mdi-magnify</v-icon> </v-btn>
    </template>
    <template v-slot:append>
      <v-avatar><v-img src="https://cdn-icons-png.flaticon.com/512/3844/3844724.png"></v-img></v-avatar>
    </template>
  </v-combobox>

<div v-if="selectedSong === null">
  <div v-if="submitted_query"
       class="d-flex align-center justify-center">
    <div v-if="loading">
      <v-progress-circular indeterminate color="red"></v-progress-circular>
    </div>
    <div v-else>
      <div v-if="song_list.length">
        <v-row v-for="song in song_list" :key="song.id">
          <v-col> <SongCard :song="song" @songCardClicked="getSongPage"></SongCard> </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-alert type="info" class="my-4 rounded-xl" >No match found.</v-alert>
      </div>
    </div>
  </div>

<!--  <v-pagination-->
<!--      v-if="total_pages > 1"-->
<!--      v-model="page_number"-->
<!--      :length="total_pages"-->
<!--      rounded="circle"-->
<!--      class="pa-4"-->
<!--      @click="onPageChange"-->
<!--  ></v-pagination>-->

    <div v-if="total_pages > 1"
         class="d-flex align-center justify-center pa-4">
      <v-btn @click="getPrevPage()">PREV</v-btn>
      <div><p class="pa-2">current page: {{page_number}} / {{total_pages}}</p></div>
      <v-btn @click="getNextPage()">NEXT</v-btn>
    </div>
</div>

  <song-page v-if="selectedSong" :selectedSong="selectedSong"></song-page>

</template>
