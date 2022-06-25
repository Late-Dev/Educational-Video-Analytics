<template>
    <div class="video-card">
        <div class="video-card__preview"></div>
        <div class="video-card__date">{{ video.lesson_start_time}}</div>
        <div class="video-card__desc">
            <div class="video-card__subtitle">Предмет</div>
            <div class="video-card__item">{{video.subject}}</div>
        </div>
        <div class="video-card__desc">
            <div class="video-card__subtitle">Класс</div>
            <div class="video-card__item">{{video.school_class}}</div>
        </div>
        <div class="video-card__desc">
            <div class="video-card__subtitle">Преподаватель</div>
            <div class="video-card__item">{{video.teacher}}</div>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';

// defineProps({
//     subject:{
//         type: String
//     },
//     school_class:{
//         type: String
//     },
//     teacher:{
//         type: String
//     },
//     lesson_start_time:{
//         type: Date
//     },
//     url:{
//         type: URL
//     }
// })

defineProps({
    video: {
        type: Object
    }
})


</script>


<style scoped lang="scss">
.video-card{
    background-color: $color-white;
    width: 430px;
    height: 490px;
    padding: 35px 25px;
    box-sizing: border-box;
    box-shadow: 0px 8px 16px rgba(17, 17, 17, 0.06);
    border-radius: 12px;
    &__preview{
        width: 100%;
        min-height: 200px;
        background-color: grey;
        box-shadow: 0px 8px 16px rgba(17, 17, 17, 0.04);
        border-radius: 12px;
    }
    &__date{
        text-align: end;
        font-weight: 400;
        font-size: 16px;
        line-height: 28px;        letter-spacing: 0.75px;
        color: #A0A3BD;
    }
}

</style>