<template>
    <EmptyCart>
        <template #header>{{header}}</template>
        <LineChart v-bind="lineChartProps"></LineChart>
    </EmptyCart>

</template>

<script setup>
import {defineProps, computed} from 'vue'
import EmptyCart from './EmptyCard.vue'
import { LineChart, useLineChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
    header:{
        type: String
    },
    dataValues:{
        type: Array
    }
})

const testData = computed(() => ({
      datasets: [
        {
          data: props.dataValues,
        },
      ],
    }));


const options = computed(() => ({
      scales: {
        myScale: {
          type: "linear",
        },
      },
      plugins: {
      },
    }));



const { lineChartProps } = useLineChart({
    // @ts-ignore
      chartData: testData,
      options,
    });

</script>