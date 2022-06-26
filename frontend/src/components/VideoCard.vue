<template>
    <div class="video-card" >
        <div class="video-card__preview">
            <video :src="video.url" s></video>
            <div class="video-card__status">
                <div class="video-card__status-test" 
                :class="{
                    'video-card__status-test--uploaded': video.status==='uploaded' ||video.status==='processing' ,
                    'video-card__status-test--success': video.status==='ready',
                    'video-card__status-test--error': video.status==='error',

                    }">{{video.status}}</div>
            </div>
        </div>
        <div class="video-card__date">{{ videotime}}</div>
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
import { computed } from '@vue/reactivity';
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


const props = defineProps({
    video: {
        type: Object
    }
})

const videotime = computed(()=>{
    const itemtime = props.video.lesson_start_time
    const dt = Date.parse(itemtime)
    const fulldate = new Date(dt)
    const day = fulldate.toLocaleDateString()
    return  fulldate.getHours() + ':' + fulldate.getMinutes() + ', '+ day
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
    cursor: pointer;

    &__status{
        height: 0px;
        position: relative;
        top: -50px;
        display: flex;
        justify-content: flex-end;
        &-test{
            height: 50px;
            position: relative;
            display: flex;
            border-radius: 12px 0px;
            padding: 10px 20px;
            font-weight: 400;
            font-size: 16px;
            line-height: 28px;
            letter-spacing: 0.75px;
            &--uploaded{
                color: #F4B740;
                background: #FFF4DF;
            }
            &--success{
                color: #00BA88;
                background: #DFFFF6;
            }
            &--error{
                color: #ED2E7E;
                background: #FFDFED;
            }

        }
    }

    &__preview{
        width: 100%;
        min-height: 200px;
        background-color: grey;
        box-shadow: 0px 8px 16px rgba(17, 17, 17, 0.04);
        border-radius: 12px;
        overflow: hidden;
        video{
            width:  100%;
            height: 100%;
        }
    }
    &__date{
        text-align: end;
        font-weight: 400;
        font-size: 16px;
        line-height: 28px;        letter-spacing: 0.75px;
        color: #A0A3BD;
    }
    &__subtitle{
        font-style: normal;
        font-weight: 400;
        font-size: 16px;
        line-height: 28px;
        letter-spacing: 0.75px;
        color: #A0A3BD;
    }
    &__desc{
        margin-top: 10px;
    }
}

</style>