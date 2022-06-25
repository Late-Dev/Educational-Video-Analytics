<template>
    <div 
        class="select-input"    
        @blur="handleFocusOut"
        tabindex="0">
        <div @click.self="handleFocus" class="select-input__placeholder">{{selectedValue ?? label}}</div> 
        <div class="select-input__icon" :class="{'select-input__icon--opened': opened}">
            <img src="@/assets/Forward.svg" alt="">
        </div>
    
        <div class="select-menu" :class="{'select-menu--opened': opened}">
            <ul>
                <li @click="handleChoose(option)" v-for="option in options" :key="option " >                
                    {{option.label}}
                </li>

            </ul>
        </div>
    </div>
    
</template>

<script setup >
import { ref, defineProps, defineEmits } from 'vue';

const emits = defineEmits('input')

defineProps({
    label:{
        type: String,
        default: ''
    },
    options: {
        type: Array,
        default: ()=>[]
    }
})


const opened = ref(false)

const selectedValue = ref()


function handleFocus(){
    opened.value = true
}
function handleFocusOut(){
    opened.value = false
}

function handleChoose(opt){
    selectedValue.value = opt.value ?? opt.name
    opened.value = false
    emits('input', selectedValue.value)
}

</script>

<style scoped lang="scss">

.select-input{
    height: 56px;
    width: 100%;
    @include input-like;
    
    
    box-sizing: border-box;
    cursor: pointer;

    &__placeholder{
        padding: 16px 24px;
        font-style: normal;
        font-weight: 400;
        font-size: 16px;
        line-height: 28px;
        color: #14142B;
    }
    &__icon{
        position: relative;
        top: -31px;
        right: 22px;
        float: right;
        height: 0;
        transform: rotate(90deg);
        transition: transform 0.1s ease-in-out;
        &--opened{
            transform: rotate(0) translate(-10px, -7px);
            transition: transform 0.1s ease-in-out;
        }
    }
    
}

.select-menu{
    width: 100%;
    @include input-like;
    position: relative;
    display: none;
    padding: 0 24px;
    padding-bottom: 16px;
    box-sizing: border-box;
    
    flex-direction: column;
    z-index: 100;
    box-shadow: 0px 8px 16px rgba(17, 17, 17, 0.06);
    
    &--opened{
        display: flex;
    }
    ul{
        margin: 0;
        padding: 0;
        li{
            list-style-type: none;
            padding-top: 16px;
            cursor: pointer;
        }
    }
}

</style>

