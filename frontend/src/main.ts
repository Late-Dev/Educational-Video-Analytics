import { createApp } from 'vue'
import { createPinia } from 'pinia'
// @ts-ignore
import DropZone from 'dropzone-vue';


const pinia = createPinia()
import App from './App.vue'

import 'dropzone-vue/dist/dropzone-vue.common.css';

createApp(App).use(pinia).use(DropZone).mount('#app')
