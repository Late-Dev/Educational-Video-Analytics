<template>
    <div class="header">
        <div class="header__logo">
            <img src="@/assets/LateDev.svg" @click="mainStore.changePage('home')" alt="">
        </div>
        <div v-if="mainStore.page !== 'home'" class="header__navigation">
            <nav>
                <ul>
                    <li :class="{'header__navigation--active': mainStore.page==='analytics'}" @click="mainStore.changePage('analytics')">Аналитика</li>
                    <li :class="{'header__navigation--active': mainStore.page==='gallery'}" @click="mainStore.changePage('gallery')">Видеогалерея</li>
                    <li >
                        <BaseButton  @click="mainStore.openPopup" type="secondary">Добавить видео</BaseButton>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useMainStore } from "@/store/index";
import { isAlive } from "@/api/index";
import { onMounted } from "vue";
import BaseButton from "./BaseButton.vue";

onMounted(async()=>{
    const res = await isAlive()
    console.log(res.data)
})

const mainStore = useMainStore();



</script>

<style lang="scss">
.header{
    padding: 34px 0;
    display: flex;
    align-items: center;
    &__logo{
        img{
            padding: 5px 0;
            cursor: pointer;
        }
    }
    &__navigation{
        display: flex;
        margin-left: auto;
        
        ul{
            margin: 0;
            display: flex;
            gap: 60px;
            align-items: center;
            li{
                list-style-type: none;
                color: $color-primary;
                font-weight: 600;
                font-size: 16px;
                line-height: 28px;  
                cursor: pointer;
            }
            .header__navigation--active {
                color: $color-primary-dark;
            }
        }
        
    }
}
</style>

