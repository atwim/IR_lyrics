<template>
  <v-app>
    <v-main>
      <SearchEngineHomePage/>
    </v-main>
  </v-app>
</template>

<script>
import SearchEngineHomePage from './components/SearchEngineHomePage.vue'

export default {
  name: 'App',

  components: {
    SearchEngineHomePage,
  },

  data: () => ({
    //
  }),
}
</script>
