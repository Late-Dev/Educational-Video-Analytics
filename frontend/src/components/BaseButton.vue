<template>
    <button class="base-button" :class="'base-button--'+type">
        <slot></slot>
    </button>
</template>

<script setup>
import {defineProps} from 'vue'

defineProps({
    type: {
        type:String,
        default: 'primary'
    }
})
</script>

<style scoped lang="scss">
.base-button{
    box-sizing: border-box;

    /* Auto layout */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 18px 32px;

    /* Primary/Default */
    border-radius: 40px;
    width: 100%;
    font-weight: 600;
    font-size: 16px;
    line-height: 28px;
    cursor: pointer;
    &--primary{
        border: 2px solid $color-primary;
        background-color: white;
        color: $color-primary;
        &:hover{
            border: 2px solid $color-primary-dark;
            color: $color-primary-dark
        }
    }
}

</style>