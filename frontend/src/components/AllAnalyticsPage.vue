<template>

    <div>
        <BaseHeader>Общая аналитика</BaseHeader>
        <EmptyCard>
            <template #header>
                Фильтр
            </template>
            <div class="row">

                <BaseSelect :options="[
                    {value:'teacher', label:'Учитель'},
                    {value:'student', label:'Ученик'},
                    {value:'subject', label:'Предмет'}
                ]" label="Тип аналитики"
                @input="(data)=>{typeAnal = data}"
                 />
                <BaseSelect v-if="typeAnal=='teacher'"
                :options="[
                            {label: 'Анна Андреевна Рязанова', value: 'Анна Андреевна Рязанова'},
                            {label: 'Альбина Николаевна Крупнина', value: 'Альбина Николаевна Крупнина'},
                            {label: 'Галина Александровна Неуймина', value: 'Галина Александровна Неуймина'},
                            ]"
                @input="(data)=>{typeVal = data}"
                label="Учитель" />
                <BaseSelect @input="(data)=>{typeVal = data}" v-if="typeAnal=='student'" label="Ученик" />
                <BaseSelect @input="(data)=>{typeVal = data}"  v-if="typeAnal=='subject'"
                :options="[
                            {label: 'Физика', value: 'Физика'},
                            {label: 'Математика', value: 'Математика'},
                            {label: 'Английский', value: 'Английский'},
                            ]"
                
                label="Предмет" />
                <BaseSelect
                :options="[
                    {value:'teacher', label:'Учитель'},
                    {value:'student', label:'Ученик'},
                    {value:'subject', label:'Предмет'}
                ]"
                @input="(data)=>{groupBy = data}"

                label="Группировка" />
            </div>
            <div class="btn">

                <BaseButton  @click="search">Найти</BaseButton>
            </div>
        </EmptyCard>
        <BarChartCard :dataValues="graph.values" :dataLabels="graph.names"  :key="graph" v-for="graph in graphs">
           
        </BarChartCard>
    </div>

</template>
<script setup>

import BaseHeader from './BaseHeader.vue';
import EmptyCard from './EmptyCard.vue';
import BaseSelect from './BaseSelect.vue';
import { onMounted, ref } from 'vue';
import { getAnalytics } from '@/api/index'
import BaseButton from './BaseButton.vue';
import BarChartCard from './BarChartCard.vue';




const typeAnal = ref('')

const typeVal = ref('')

const groupBy = ref('')

onMounted(async ()=>{
})

const graphs = ref('')

async function search(){
    const resp = await getAnalytics(typeAnal.value, typeVal.value, groupBy.value)
    graphs.value = resp.data
}




</script>

<style>
.row{
    display: flex;
    gap:25px;
}

.btn{
    width: 300px;
    margin-top: 25px;
    margin-left: auto;
}

</style>