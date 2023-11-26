<script>
export default {
  props: {
    song: null
  },

}
</script>

<template>
  <v-card
      class="mx-auto my-8"
      max-width="344"
      elevation="16"
  >
    <v-card-item>
      <v-card-title>
        {{song.Title}}
      </v-card-title>
      <v-card-subtitle>
       {{song.Artist}}
      </v-card-subtitle>
      <v-card-subtitle>
        Card subtitle secondary text
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      {{song.Lyrics.split(" ").slice(0,100).join(" ") + "..."}}
    </v-card-text>
  </v-card>
</template>

<style scoped>

</style>