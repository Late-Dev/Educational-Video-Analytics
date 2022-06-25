<template>

    <div class="upload-popup__wrapper" @click.self="mainStore.closePopup" >
        <div class="upload-popup" >
            <div class="upload-popup__close"  @click="mainStore.closePopup">
                <img src="@/assets/close.svg" alt="">
            </div>
            <div>
                <DragNDrop></DragNDrop>
            </div>
            <div class="upload-popup__row">
                <div class="upload-popup__class">
                    <BaseInput label="Класс"/>
                </div>
                <div class="upload-popup__time">
                    <BaseSelect></BaseSelect>
                </div>
                
            </div>
            <div class="upload-popup__row">
                <BaseInput label="Предмет"/>
            </div>
            <div class="upload-popup__row">
                <BaseInput label="Преподаватель"/>
            </div>
            <div class="upload-popup__row">
                <BaseButton>загрузить</BaseButton>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import DragNDrop from "./DragNDrop.vue";
import BaseInput from "./BaseInput.vue";
import BaseButton from "./BaseButton.vue";
import BaseSelect from "./BaseSelect.vue";

import { useMainStore } from "@/store/index";
import { onMounted, onUnmounted } from "vue";

onMounted(()=>{
    window.addEventListener('keyup', escCloseModal)
})

onUnmounted(()=>{
    window.removeEventListener('keyup',escCloseModal)
})

function escCloseModal(e :any) {
     if(e.keyCode === 27) {
         mainStore.closePopup()
    }
}


const mainStore = useMainStore();

</script>

<style scoped lang="scss">
.upload-popup{
    height: 640px;
    width: 540px;
    background: white;
    margin: 150px auto;
    border-radius: 24px;
    padding: 90px;
    box-sizing: border-box;
    &__row{
        margin-top: 25px;
        display: flex;
        height: 56px;
    }

    &__class{
        width: 140px;
    }

    &__time{
        width: 195px;
        margin-left: auto;
    }

    &__wrapper{
        position: fixed;
        top:0;
        left:0;
        height: 100vh;
        width: 100vw;
        background: rgba($color: #000000, $alpha: 0.25);
    }
    &__close{
        position: relative;
        top: -60px;
        right:-60px;
        float: right;
        cursor: pointer;
    }
}



</style>