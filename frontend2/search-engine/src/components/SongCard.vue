<script>
export default {
  props: {
    song: null
  }
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
        Song name
        {{song.title}}
      </v-card-title>
      <v-card-subtitle>
        Card subtitle secondary text
      </v-card-subtitle>
      <v-card-subtitle>
        Card subtitle secondary text
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      {{song.text}}
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </v-card-text>
  </v-card>
</template>

<style scoped>

</style>