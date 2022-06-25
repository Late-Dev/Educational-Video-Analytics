<template>
  <div class="container">
    <MainHeader></MainHeader>
    <MainContent></MainContent>
    <UploadPopup v-if="mainStore.popupOpened"></UploadPopup>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import MainHeader from './components/MainHeader.vue';
import MainContent from './components/MainContent.vue';
import UploadPopup from './components/UploadPopup.vue';
import { useMainStore } from "@/store/index";

export default defineComponent({
  name: 'App',
  components: {
    MainHeader,
    MainContent,
    UploadPopup
  },
  setup(){
    const mainStore = useMainStore()

    return {
      mainStore
    }
  }
});
</script>

<style lang="scss">
#app {
  font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
body {
  background-color: $color-bg;
  margin: 0;
}
.container {
  width: 1350px;
  padding: 0 20px;
  margin: auto;
}
</style>
