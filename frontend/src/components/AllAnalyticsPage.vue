<template>

    <div>
        <BaseHeader>Общая аналитика</BaseHeader>
        <EmptyCard>
            <template #header>
                Фильтр
            </template>
            <BaseSelect label="Аналитика"></BaseSelect>
        </EmptyCard>
    </div>

</template>
<script setup>

import BaseHeader from './BaseHeader.vue';
import EmptyCard from './EmptyCard.vue';
import BaseSelect from './BaseSelect.vue';
import { onMounted } from 'vue';
import { getAnalytics } from '@/api/index'

onMounted(async ()=>{
    getAnalytics()
})


</script>