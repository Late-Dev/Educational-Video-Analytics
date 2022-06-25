<template>
    <button class="base-button" :class="applyClasses">
        <slot></slot>
    </button>
</template>

<script setup>
import { defineProps, computed } from 'vue'


const applyClasses = computed(()=>{
    const typeClass = 'base-button--' + props.type
    const sizeClass = 'base-button--' + props.size
    return [typeClass, sizeClass]
})

const props = defineProps({
    type: {
        type:String,
        default: 'primary'
    },
    size: {
        type:String,
        default: 'medium'
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
    // types
    &--primary{
        border: 2px solid $color-primary;
        background-color: white;
        color: $color-primary;
        &:hover{
            border: 2px solid $color-primary-dark;
            color: $color-primary-dark
        }
    }
    &--secondary{
        border: 2px solid $color-primary;
        background-color: $color-primary;
        color: white;
        &:hover{
            border: 2px solid $color-primary-dark;
            background-color: $color-primary-dark;
        }
    }

    //sizes
    &--small{
        height: 40px;
    }
    &--medium{
        height: 56px;
    }
    &--large{
        height: 64px;
    }
    
}

</style>