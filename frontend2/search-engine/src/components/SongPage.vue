<script>
import SongCard from "@/components/SongCard.vue";

export default {
  components: {SongCard},
  data(){
    return {
      relevant_songs_list: [],
      setSelectedSong: this.selectedSong,
      loading: false,
      isRelevant: true,
    }
  },
  props: {
    selectedSong: null
  },
  mounted() {
    this.fetchRelevant()
  },
  methods: {
    getSongPage(song){
      this.isRelevant = false;
      this.setSelectedSong = song;
      this.fetchRelevant();
      this.isRelevant = true;
    },
    async fetchRelevant(){
      try {
        this.loading = true;
        const res = await fetch(
            "http://localhost:8000/relevant-documents/" + this.setSelectedSong.docid)
        const relevant_songs = await res.json()
        this.relevant_songs_list = relevant_songs;
      } catch(err){
        console.log(err);
        this.relevant_songs_list = [];
      } finally {
        this.loading = false
      }

    }
  },
}
</script>

<template>
  <v-card
      class="mx-auto my-8 rounded-xl"
      max-width="700"
      elevation="16"
      style="white-space: pre-wrap; text-align: center"
  >
    <v-card-item>
      <v-card-title>{{setSelectedSong.Title}}</v-card-title>
      <v-card-subtitle>{{setSelectedSong.Artist}}</v-card-subtitle>
    </v-card-item>
    <v-card-text>{{setSelectedSong.Lyrics}}</v-card-text>
  </v-card>
  <div v-if="loading">
    <h2 style="text-align: center" class="pa-4">Loading related songs...</h2>
  </div>
  <div v-if="!loading && !relevant_songs_list.length">
    <h2 style="text-align: center" class="pa-4">No related songs found</h2>
  </div>
  <div v-if="!loading && relevant_songs_list.length">
      <h2 style="text-align: center">Related songs: </h2>
      <v-row class="pa-4">
        <v-col v-for="song in relevant_songs_list" :key="song.id" cols="12" sm="3" md="3" lg="3">
          <SongCard :song="song" @songCardClicked="getSongPage" :is-relevant-list="isRelevant"></SongCard>
        </v-col>
      </v-row>
    </div>


</template>
