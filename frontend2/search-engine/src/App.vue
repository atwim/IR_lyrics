<template>
  <v-app>
    <v-main>
      <SearchEngineHomePage/>
    </v-main>
  </v-app>
</template>

<script>
import SearchEngineHomePage from './components/SearchEngineMainComponent.vue'

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
