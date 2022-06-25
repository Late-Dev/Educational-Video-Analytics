<template>
    <DropZone 
    :maxFiles="1"
    :maxFileSize="10000000000"
    :uploadOnDrop="false"
    :dropzoneClassName="{'dropzone': files.length===0, 'dropzone--filled': files.length>0}"
    dropzoneMessageClassName="dropzone__message"
    :dropzoneItemClassName="{'dropzone__item':true, 'dropzone__item--loading': loading}"
    :acceptedFiles="['video']"
    @addedFile="addedFile"
    >
    <template #message>
        Перетащите видео сюда или <span class="dropzone__message--open">выберите вручную</span>
    </template>
    </DropZone>
</template>

<script setup>
import axios from 'axios';
import DropZone from 'dropzone-vue';
import { ref, defineEmits } from 'vue';


const emits = defineEmits(['upload'])


// const BUCKET_UPLOAD_NAME = 'http://localhost:9000/videos/'
const BUCKET_UPLOAD_NAME = process.env.VUE_APP_BUCKET_UPLOAD_NAME

async function upload(file, name){
    loading.value = true
    await axios.put(BUCKET_UPLOAD_NAME+name+file.name, file).then(()=>{
        loading.value = false
        // emits('upload', resp.config.url) //TODO сюда возвращаю name+file.name
        emits('upload', name+file.name)
    })
}

const files = ref([])
const loading = ref(true)

function addedFile(file){
    files.value.push(file)
    upload(file.file, file.id);
}

</script>

<style scoped lang="scss">

.dropzone{
    box-sizing: border-box;
    padding: 55px;
    height: 144px;
    width: 100%;
    border-radius: 12px;
    border: 1px dashed $color-primary-dark;
    background: $color-primary-bg;

    &--filled{
        padding: 35px 25px;
        display: flex;
    }
    
    :deep(.dropzone__message){
        font-weight: 700;
        font-size: 16px;
        line-height: 140%;
        text-align: center;
        letter-spacing: 1px;
    }
    :deep(.dropzone__message--open){
        color: $color-primary;
        cursor: pointer;
    }
    :deep(.dropzone__item){
        background: $color-primary-darkmode;
        border-radius: 12px;
        width: 100%;

    }
    :deep(.dropzone__item--loading){
        background: green;

    }

    :deep(.dropzone__item-controls){
        top: 24px;
        right: 20px;
        .gg-close{
            color: white;
        }
        .gg-close::after,
        .gg-close::before{
            width: 20px;
            height: 3px;
        }
    }
    :deep(.dropzone__progress){
        display: none;
    }

    :deep(.dropzone__details){
        display: flex;
        font-weight: 600;
        font-size: 14px;
        line-height: 20px;
        letter-spacing: 0.25px;
        color: white;
        background-color: transparent;
        .dropzone{
            &__file-size{
                display: none;
            }
            &__filename{
                span{
                    background-color: transparent;
                }
                border: none;
            }
        }
    }
}

</style>