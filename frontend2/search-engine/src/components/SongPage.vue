<script>
import SongCard from "@/components/SongCard.vue";

export default {
  components: {SongCard},
  data(){
    return {
      relevant_songs_list: [],
    }
  },
  props: {
    selectedSong: null
  },
  async mounted() {
    const res = await fetch(
        "http://localhost:8000/relevant-documents/" + this.selectedSong.docid)
    const relevant_songs = await res.json()
    this.relevant_songs_list = relevant_songs;

    // TODO: style
  }
}
</script>

<template>
  <v-card
      class="mx-auto my-8 rounded-xl"
      max-width="700"
      elevation="16">
    <v-card-item>
      <v-card-title>{{selectedSong.Title}}</v-card-title>
      <v-card-subtitle>{{selectedSong.Artist}}</v-card-subtitle>
    </v-card-item>
    <v-card-text>{{selectedSong.Lyrics}}</v-card-text>
  </v-card>
  <p>Related songs: </p>
  <div v-if="relevant_songs_list.length">
    <v-row>
      <v-col v-for="song in relevant_songs_list" :key="song.id" cols="12" sm="3" md="3" lg="3">
        <SongCard :song="song"></SongCard>
      </v-col>
    </v-row>
  </div>
</template>
