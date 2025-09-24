<script setup>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'vue-chartjs';
import { computed } from 'vue';

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const chartData = computed(() => ({
  labels: ['Scope 1', 'Scope 2', 'Scope 3'],
  datasets: [
    {
      data: [props.data.scope1, props.data.scope2, props.data.scope3],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
    },
  ],
}));

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        font: { size: 12 },
      },
    },
    title: {
      display: true,
      text: '전체 배출량 비중',
      font: { size: 14 },
    },
  },
};
</script>

<template>
  <Pie :data="chartData" :options="options" />
</template>