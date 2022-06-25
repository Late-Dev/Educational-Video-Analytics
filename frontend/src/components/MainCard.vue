<template>
    <div class="main-card">
        <div class="main-card__header">
            <h2>{{data.name}}</h2>
        </div>
        <div class="main-card__image">
            <img :src="data.image" alt="">
        </div>
        <div class="main-card__description">
            <span>{{data.description}}</span>
        </div>
        <div class="main-card__button">
            <BaseButton>{{data.cta}}</BaseButton>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { defineProps } from 'vue';
import BaseButton from './BaseButton.vue'

defineProps({
  data: {} as any
})


</script>

<style lang="scss" scoped>

.main-card {
    background-color: white;
    height: 680px;
    width: 430px;
    border-radius: 24px;
    box-shadow: 0px 8px 16px rgba(17, 17, 17, 0.06);
    padding: 50px 40px;
    box-sizing: border-box;
    cursor: pointer;
    transition: box-shadow 0.2s ease-in-out;
    
    &__header{
        h2{
            font-weight: 700;
            font-size: 36px;
            line-height: 50px;
            letter-spacing: 3px;
            margin: 0;
            color: $color-text-main;
        }
    }
    &__image{
        margin-top: 25px;
        height: 275px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    &__description{
        height: 115px;
        margin-top: 25px;
        span{
            font-size: 18px;
            line-height: 38px;
            letter-spacing: 0.75px;
            color: $color-text-main;
        }
    }
    &__button{
        width: 100%;
        margin-top: 25px;
    }
    &:hover{
        transition: box-shadow 0.2s ease-in-out;
        box-shadow: 0px 20px 24px rgba(17, 17, 17, 0.06);
    }
}

</style>