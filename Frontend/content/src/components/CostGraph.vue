<template>
    <div class="graph-container">
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
    // Destroy the previous chart instance if it exists
    if (chartInstance) {
      chartInstance.destroy();
    }
  
    // Ensure the canvas element is available
    if (!chartCanvas.value) {
      console.error('Chart canvas element is not available.');
      return;
    }
  
    // Ensure the data is valid
    if (!props.data || props.data.length === 0) {
      console.warn('No data provided for the chart.');
      return;
    }
  
    // Extract labels and data from the props
    const labels = props.data.map((item) => item.product_name || 'Unknown');
    const Cost = props.data.map((item) => item.total_cost_lost || 0);
  
    // Create the chart instance
    chartInstance = new Chart(chartCanvas.value, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: '$ Amount Wasted',
            data: Cost,
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Items',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Amount',
            },
            beginAtZero: true,
          },
        },
      },
    });
  };
  
  // Ensure the chart is created after the component is mounted
  onMounted(() => {
    if (chartCanvas.value) {
      createChart();
    } else {
      console.error('Chart canvas element is not available on mount.');
    }
  });
  
  // Watch for changes in the data prop and update the chart
  watch(
    () => props.data,
    () => {
      if (chartCanvas.value) {
        createChart();
      } else {
        console.error('Chart canvas element is not available during data update.');
      }
    },
    { immediate: true }
  );
  </script>
  
  <style scoped>
  .graph-container {
    margin-bottom: 20px;
    width: 100%;
    height: 400px; /* Set a fixed height for the chart */
  }
  </style>