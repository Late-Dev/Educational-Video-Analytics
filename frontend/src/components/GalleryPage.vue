<template>
    <div class="gallery">
        <BaseHeader>Видеогалерея</BaseHeader>
        <EmptyCard class="filter">
            <template #header>
                Фильтр
            </template>
            <div class="filter__filters">           
                <div class="filter__row">                    
                    <BaseSelect @input="(value)=>{ subfilter = value}"  label="Предмет" :options="filter.subOption"></BaseSelect>
                    <BaseSelect @input="(value)=>{ classfilter = value}" label="Класс" class="filter__class" :options="filter.classOption"></BaseSelect>
                    <BaseSelect label="Преподаватель"  @input="(value)=>{ teacherfilter = value}"  :options="filter.teacherOption"></BaseSelect>
                </div>
                <div class="filter__datetime">
                    <BaseSelect @input="(value)=>{ timefilter = value}"  label="Время начала"  :options="lessons"></BaseSelect>
                    <BaseSelect @input="(value)=>{ datesfilter = value}"  label="Дата"  :options="filter.datesoption"></BaseSelect>
                </div>
             </div>

        </EmptyCard>
        <div class="gallery__videos">
            <VideoCard @click="openVideo(video)" v-for="video in filteredvideos" :video="video" :key="video" />
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import BaseHeader from './BaseHeader.vue'
import EmptyCard from './EmptyCard.vue';
import {getVideoList} from '@/api/index';
import VideoCard from './VideoCard.vue';
import BaseSelect from './BaseSelect.vue';
import { useMainStore } from "@/store/index";

const mainStore = useMainStore();


const videos = ref([])

const filter = computed(()=>{
    const subjects = [...new Set(videos.value.map((item)=>item.subject))]
    const classes = [...new Set(videos.value.map((item)=>item.school_class))]
    const teachers = [...new Set(videos.value.map((item)=>item.teacher))]

    const subOption = subjects.map(item=>({label:item, value: item}))
    const classOption = classes.map(item=>({label:item, value: item}))
    const teacherOption = teachers.map(item=>({label:item, value: item}))

    const dates = [...new Set(videos.value.map((item)=>{
        const dt = Date.parse(item.lesson_start_time)
        const fulldate = new Date(dt)
        const day = fulldate.toLocaleDateString()
        return day
        }))]

    const datesoption = dates.map(item=>({label:item, value: item}))
     
    return {subOption, classOption, teacherOption, datesoption}
})

const subfilter = ref('')
const classfilter = ref('')
const teacherfilter = ref('')
const timefilter = ref('')
const datesfilter = ref('')


const lessons = ref([
    {label:'8:30-9:15', value:'8:30'},
    {label:'9:30-10:15', value:'9:30'},
    {label:'10:30-11:15', value:'10:30'},
    {label:'11:30-12:15', value:'11:30'},
    {label:'12:30-13:15', value:'12:30'},
    {label:'13:25-14:10', value:'13:25'},
    {label:'14:25-15:10', value:'14:25'},
    ])




function openVideo(video){
    mainStore.changePage('videoanalytics')
    mainStore.video = video
}

const filteredvideos = computed(()=>{
    return videos.value.filter((video)=>{
        if(subfilter.value && video.subject !== subfilter.value){
            return
        }
        if(classfilter.value && video.school_class !== classfilter.value){
            return
        }
        if(teacherfilter.value && video.teacher !== teacherfilter.value){
            return
        }
        const videotime = video.lesson_start_time
        const dt = Date.parse(videotime)
        const fulldate = new Date(dt)
        const day = fulldate.toLocaleDateString()

        const lsntime = fulldate.getHours()+':'+fulldate.getMinutes()

        if(timefilter.value && lsntime !== timefilter.value){
            return
        }
        if(datesfilter.value && day !== datesfilter.value){
            return
        }

        return video
    })
})


// const BUCKET_DOWNLOAD_NAME = 'http://localhost:9000/videos/' // processed-videos
const BUCKET_DOWNLOAD_NAME = process.env.VUE_APP_BUCKET_DOWNLOAD_NAME

onMounted(async ()=>{
    const resp = await getVideoList()
    const data = resp.data
    videos.value = data.map((video)=>{video.url=BUCKET_DOWNLOAD_NAME+video.url 
    return video})
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

.filter{
    &__row{
        display: flex;
        width: 825px;
        gap: 25px;
    }

    &__item{
        flex-shrink: 2;
    }
    &__class{
        max-width: 160px;
    }
    &__filters{
        display: flex;
    }
    &__datetime{
        display: flex;
        margin-left: 75px;
        flex-grow: 1;
        gap: 25px;
    }
}
</style>