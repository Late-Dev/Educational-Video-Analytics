<template>
    <div class="home-page" v-if="mainStore.page==='home'">
        <MainCard @click="mainStore.changePage('analytics')" :data="cards.analytics" />
        <MainCard @click="mainStore.openPopup"  :data="cards.upload" />
        <MainCard @click="mainStore.changePage('gallery')" :data="cards.gallery" />
    </div>
    <div class="analytics" v-if="mainStore.page==='analytics'">
        <AllAnalyticsPage />
    </div>
    <div class="gallery" v-if="mainStore.page==='gallery'">
        <GalleryPage></GalleryPage>
    </div>
    <div class="videoanalytics" v-if="mainStore.page==='videoanalytics'">
        <VideoAnalyticsPage></VideoAnalyticsPage>
    
    </div>
</template>

<script setup lang="ts">
import { useMainStore } from "@/store/index";
import MainCard from "./MainCard.vue"
import { ref } from "vue";

// @ts-ignore
import analytics from "@/assets/analytics.svg"
// @ts-ignore
import upload from "@/assets/upload.svg"
// @ts-ignore
import gallery from "@/assets/gallery.svg"
import GalleryPage from "./GalleryPage.vue";
import VideoAnalyticsPage from "./VideoAnalyticsPage.vue";
import AllAnalyticsPage from "./AllAnalyticsPage.vue";

const mainStore = useMainStore();

// interface Card {
//     image: any
//     name: String,
//     description: String
// }

const cards = ref({} as any)

cards.value = {
    analytics: {
        image: analytics,
        name: "Аналитика",
        description: "Отслеживайте настроение учеников основываясь на анализе собранных данных",
        cta: "Перейти"
    },
    upload: {
        image: upload,
        name: "Загрузка видео",
        description: "Добавляйте новые видео для подробной аналитики и более точных результатов",
        cta: "Загрузить"
    },
    gallery: {
        image: gallery,
        name: "Видеогалерея",
        description: "Просматривайте загруженные видео с подробной аналитикой",
        cta: "Перейти"
    }
}

</script>

<style lang="scss">

.home-page{
    display: flex;
    justify-content: space-between;
}

.videoanalytics{
    video{
        width: 100%;
    }
}

</style>