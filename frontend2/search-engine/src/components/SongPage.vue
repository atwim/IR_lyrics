<script>
export default {
  props: {
    selectedSong: null
  }
}
</script>

<template>
  <v-card
      class="mx-auto my-8 rounded-xl"
      max-width="700"
      elevation="16"
  >
    <v-card-item>
      <v-card-title>
        {{selectedSong.Title}}
      </v-card-title>
      <v-card-subtitle>
        {{selectedSong.Artist}}
      </v-card-subtitle>

    </v-card-item>

    <v-card-text>
      {{selectedSong.Lyrics}}
    </v-card-text>
  </v-card>
</template>
