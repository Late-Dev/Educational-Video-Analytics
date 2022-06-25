<template>
    <div class="gallery">
        <BaseHeader>Видеогалерея</BaseHeader>
        <EmptyCard class="filter">
            <template #header>
                Фильтр
            </template>

        </EmptyCard>
        <div class="gallery__videos">
            <VideoCard v-for="video in videos" :video="video" :key="video" />
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import BaseHeader from './BaseHeader.vue'
import EmptyCard from './EmptyCard.vue';
import {getVideoList} from '@/api/index';
import VideoCard from './VideoCard.vue';

const videos = ref([])

onMounted(async ()=>{
    const resp = await getVideoList()
    videos.value = resp.data
    console.log(resp.data)
})


</script>


<style scoped lang="scss">
.gallery{
    &__videos{
        margin-top: 35px;
        display: flex;
        gap: 30px;
        flex-wrap: wrap;
    }
}
</style>