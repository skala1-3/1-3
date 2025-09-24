<script setup>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'vue-chartjs';
import { computed } from 'vue';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
});

const chartData = computed(() => ({
  labels: props.data.map((item) => item.year),
  datasets: [
    {
      label: 'Scope 1',
      data: props.data.map((item) => item.scope1),
      borderColor: '#FF6384',
      backgroundColor: '#FF6384',
    },
    {
      label: 'Scope 2',
      data: props.data.map((item) => item.scope2),
      borderColor: '#36A2EB',
      backgroundColor: '#36A2EB',
    },
    {
      label: 'Scope 3',
      data: props.data.map((item) => item.scope3),
      borderColor: '#FFCE56',
      backgroundColor: '#FFCE56',
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
      text: '연도별 배출량 추이',
      font: { size: 14 },
    },
  },
  scales: {
    y: {
      title: {
        display: true,
        text: '배출량 (tCO2e)',
        font: { size: 12 },
      },
      ticks: {
        font: { size: 10 },
      },
    },
    x: {
      ticks: {
        font: { size: 10 },
      },
    },
  },
};
</script>

<template>
  <Line :data="chartData" :options="options" />
</template>