<template>
    <EmptyCart>
        <template #header>{{header}}</template>
                    <BarChart v-bind="barChartProps"></BarChart>

    </EmptyCart>

</template>

<script setup> 
import {defineProps, computed} from 'vue'
import EmptyCart from './EmptyCard.vue'
import { BarChart, useBarChart } from "vue-chart-3";
import { Chart,  registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
    header:{
        type: String
    },
    dataValues:{
        type: Array
    },
    dataLabels:{
        type:Array
    }
})


const testData = computed(() => ({
  labels: props.dataLabels,
  datasets: [
      {
        data: props.dataValues,
        backgroundColor: [
            "#ED2E7E",
            "#6A96FF",
            "#8F40F4",
            "#F4B740",
            "#B2FF36",
            "#00BA88",
            "#DC8CEC",
          ],
      },
    ],
  })
);


const options = computed(() => ({
      scales: {
        myScale: {
          type: "linear",
        },
      },
      plugins: {
      },
  })
);


const { barChartProps } = useBarChart({
    // @ts-ignore
      chartData: testData,
      options,
    });




</script>