<template>
    <div class="gallery">
        <BaseHeader>Видеогалерея</BaseHeader>
        <EmptyCard class="filter">
            <template #header>
                Фильтр
            </template>

        </EmptyCard>

    </div>
</template>

<script setup>
import BaseHeader from './BaseHeader.vue'
import EmptyCard from './EmptyCard.vue';

</script>