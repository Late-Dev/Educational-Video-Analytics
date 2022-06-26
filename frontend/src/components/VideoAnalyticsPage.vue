<template>
    <div>
        <EmptyCard>
            <video :src="mainStore.video.url" controls></video>
            <BarChart v-bind="barChartProps"></BarChart>
        </EmptyCard>
    </div>
</template>

<script setup lang="ts">
import EmptyCard from "./EmptyCard.vue"
import { useMainStore } from "@/store/index";
import { ref, computed, onMounted} from 'vue'

import { BarChart, useBarChart } from "vue-chart-3";
import { Chart, ChartData, ChartOptions, registerables } from "chart.js";
import { getVideoCard } from '@/api/index'


const mainStore = useMainStore();

onMounted(async ()=>{
  const resp = await getVideoCard(mainStore.video._id)
  console.log(resp)
  videoCard.value = resp.data
})

const videoCard = ref({} as any)

Chart.register(...registerables);

// bar_data" : { "names" : [ "гнев", "грусть", "отвращение", "радость", "спокойствие", "страх", "удивление" ], "values" : [ 0.07174072510112016, 0.100061056220386, 0.025056007966937802, 0.28290127535625237, 0.468341065879695, 0.025505640514629852, 0.02639422875556299 ]

const dataValues = computed(()=>videoCard.value.bar_data.values);

const dataLabels = computed(()=>videoCard.value.bar_data.names);

const toggleLegend = ref(true); 
// console.log(toggleLegend)

const testData = computed<ChartData<"bar">>(() => ({
      labels: dataLabels.value,
      datasets: [
        {
          data: dataValues.value,
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
    }));

const options = computed<ChartOptions<"bar">>(() => ({
      scales: {
        myScale: {
          type: "logarithmic",
          position: toggleLegend.value ? "left" : "right",
        },
      },
      plugins: {
        legend: {
          position: 'top'
        },
      },
    }));


const { barChartProps } = useBarChart({
    // @ts-ignore
      chartData: testData,
      options,
    });

// console.log(barChartRef)


</script>