<template>
  <div class="pie-chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
});

const chartCanvas = ref(null);
let chartInstance = null;

const createChart = () => {
  if (chartInstance) {
    chartInstance.destroy(); // Destroy the previous chart instance if it exists
  }

  if (!props.data || props.data.length === 0) {
    console.warn('No data provided for the chart.');
    return;
  }

  const labels = props.data.map((item) => item.reason || 'Unknown');
  const quantities = props.data.map((item) => item.total_quantity || 0);

  chartInstance = new Chart(chartCanvas.value, {
    type: 'pie',
    data: {
      labels,
      datasets: [
        {
          label: 'Waste by Reason',
          data: quantities,
          backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
      },
    },
  });
};

onMounted(() => {
  if (chartCanvas.value) {
    createChart();
  }
});

watch(
  () => props.data,
  () => {
    createChart();
  },
  { immediate: true }
);
</script>

<style scoped>
.pie-chart-container {
  margin-bottom: 20px;
  width: 300px; /* Set fixed width */
  height: 300px; /* Set fixed height */
  margin: 0 auto; /* Center the chart */
}
</style>
