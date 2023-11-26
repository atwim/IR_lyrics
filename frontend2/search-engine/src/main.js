import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import axios from 'axios'
import {Model} from 'vue-api-query'
loadFonts()

Model.$http = axios

createApp(App)
  .use(vuetify)
  .mount('#app')
