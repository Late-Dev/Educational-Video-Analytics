<template>
    <div class="base-input">
        <input 
        id="id"
        :type="type"
        :value="valueInput"
        @input="updateInput">
        <div class="base-input__floating-label" :class="{'base-input__floating-label--filled': valueInput.length>0}">{{label}}</div>
        <img class="base-input__clear" @click="valueInput=''" src="@/assets/close.svg" alt="">
    </div>
</template>

<script setup>
import {defineProps, defineEmits, ref} from 'vue'

const emits = defineEmits(['update:modelValue'])

 defineProps({
    id: {
      type: String,
      default: "",
    },
    label: {
      type: String,
      default: "",
    },
    modelValue: {
      type: [String, Number],
      default: "",
    },
    type: {
      type: String,
      default: "text",
    }
})

const valueInput = ref('')

function updateInput(event) {
    valueInput.value = event.target.value
    emits("update:modelValue", event.target.value);
}
</script>

<style scoped lang="scss">

.base-input{
    height: 56px;
    width: 100%;
    @include input-like;
    &__floating-label{
        position: relative;
        pointer-events: none;
        left: 20px;
        top: -46px;
        transition: 0.2s ease all;
        font-size: 16px;
        color: #A0A3BD;
        height: 0;
    }
    input{
        margin: 10px 18px;
        height: 40px;
        width: 80%;
        word-wrap: no-wrap;
        font-size: 16px;
        line-height: 28px;
        margin-top: 15px;
    }
    input:focus{
        // outline-style: solid;
        // outline-color: solid;
        outline: none;
        // border: 1px solid #14142B;
    }
    input:focus + .base-input__floating-label,
    .base-input__floating-label--filled
    {
        top: -55px;
        left: 20px;
        font-size: 14px;
        opacity: 1;
        color: #6E7191;
    }

    &__clear{
        position: relative;
        top: -49px;
        float: right;
        right: 15px;
        cursor: pointer;
    }
}

</style>
