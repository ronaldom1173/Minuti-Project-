<template>
  <div class="dashboard">
    <!-- <div class="dashboard-header">
      <h1>Dashboard</h1>
      <p class="subtitle">Minuti Coffee Waste Management</p>
    </div> -->

    <!-- Stats Section -->
    <div class="stats-container">
      <div class="stat-card">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <path d="M3 7L12 13L21 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ productCount }}</div>
          <div class="stat-label">Active Products</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ categories.length }}</div>
          <div class="stat-label">Categories</div>
        </div>
      </div>
    </div>

    <!-- Waste Events by Day Chart -->
    <div class="chart-section">
      <h2>Waste Events (Last 7 Days)</h2>
      <div class="calendar-container">
        <div v-if="isLoadingChart" class="loading-indicator">
          <div class="spinner"></div>
          <p>Loading chart data...</p>
        </div>
        <div v-else-if="wasteDayData.length === 0" class="no-data">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="no-data-icon">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
            <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="16" x2="12" y2="16" stroke="currentColor" stroke-width="2"/>
          </svg>
          <p>No waste data available for the past 7 days</p>
        </div>
        <div v-else class="calendar-grid">
          <div v-for="(day, index) in wasteDayData" :key="index" class="calendar-day" :class="{ 'has-data': day.items.length > 0 }">
            <div class="day-header">{{ day.name }}</div>
            <div class="day-content">
              <div v-if="day.items.length > 0" class="day-items">
                <div v-for="(item, i) in day.items" :key="i" class="day-item">
                  <span class="item-badge">{{ item.name }} ({{ item.quantity }})</span>
                </div>
              </div>
              <div v-else class="day-empty">No data</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Products Table Section -->
    <div class="products-section">
      <div class="section-header">
        <h2>Active Products</h2>
        
        <div class="controls">
          <div class="search-container">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="search-icon">
              <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
              <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Search products..."
              class="search-input"
            />
          </div>
          
          <div class="sort-control">
            <select v-model="sortKey" class="sort-select">
              <option value="name">Sort by Name</option>
              <option value="base_price">Sort by Price</option>
              <option value="category">Sort by Category</option>
            </select>
            
            <button @click="toggleSortOrder" class="sort-button">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" :class="['sort-icon', !sortAsc ? 'flipped' : '']">
                <path d="M6 9L12 3L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <path d="M6 15L12 21L18 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <div class="products-table-container">
        <table class="products-table">
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Category</th>
              <th>Description</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in filteredAndSortedProducts" :key="item.product_id || index">
              <td class="product-name-cell">{{ item.name }}</td>
              <td>
                <span v-if="item.category" class="category-badge">
                  {{ item.category }}
                </span>
                <span v-else>—</span>
              </td>
              <td class="description-cell">{{ item.description || '—' }}</td>
              <td class="price-cell">${{ parseFloat(item.base_price || 0).toFixed(2) }}</td>
            </tr>
            
            <tr v-if="filteredAndSortedProducts.length === 0">
              <td colspan="4" class="empty-state">
                <div class="empty-content">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="empty-icon">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                    <line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <p>No products found</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// State
const products = ref([]);
const productMap = ref({});
const searchQuery = ref('');
const sortKey = ref('name');
const sortAsc = ref(true);
const wasteDayData = ref([]);
const isLoadingChart = ref(true);

// Fetch products
const fetchProducts = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/products');
    products.value = res.data;
    
    // Create a map of product IDs to product names for waste data
    productMap.value = products.value.reduce((acc, product) => {
      acc[product.product_id] = product.name;
      return acc;
    }, {});
  } catch (error) {
    console.error('Failed to fetch products:', error);
  }
};

// Fetch waste data for last 7 days
const fetchWasteEvents = async () => {
  try {
    isLoadingChart.value = true;
    
    // Get dates for the last 7 days
    const dates = [];
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const today = new Date();
    
    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      dates.push({
        date,
        dayName: dayNames[date.getDay()],
        formattedDate: formatDate(date)
      });
    }
    
    // Fetch waste data
    const res = await axios.get('http://127.0.0.1:5000/waste');
    const wasteData = res.data;
    
    // Create day data structure
    wasteDayData.value = dates.map(dayInfo => {
      // Filter waste items for this day
      const dayItems = wasteData.filter(waste => {
        const wasteDate = new Date(waste.waste_date);
        return isSameDay(wasteDate, dayInfo.date);
      });
      
      // Group items by product and sum quantities
      const groupedItems = {};
      dayItems.forEach(item => {
        const productName = productMap.value[item.product_id] || 'Unknown Product';
        if (!groupedItems[productName]) {
          groupedItems[productName] = {
            name: productName,
            quantity: 0
          };
        }
        groupedItems[productName].quantity += item.quantity;
      });
      
      return {
        name: dayInfo.dayName,
        date: dayInfo.date,
        formattedDate: dayInfo.formattedDate,
        items: Object.values(groupedItems)
      };
    });
    
  } catch (error) {
    console.error('Failed to fetch waste events:', error);
    wasteDayData.value = [];
  } finally {
    isLoadingChart.value = false;
  }
};

// Helper function to format date as YYYY-MM-DD
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// Helper function to check if two dates are the same day
const isSameDay = (date1, date2) => {
  return date1.getFullYear() === date2.getFullYear() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getDate() === date2.getDate();
};

// Toggle sort order
const toggleSortOrder = () => {
  sortAsc.value = !sortAsc.value;
};

// Computed properties
const filteredAndSortedProducts = computed(() => {
  let result = [...products.value];
  
  // Filter active products
  result = result.filter(product => product.active === 1);
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(product => 
      product.name.toLowerCase().includes(query) || 
      (product.description && product.description.toLowerCase().includes(query)) ||
      (product.category && product.category.toLowerCase().includes(query))
    );
  }
  
  // Sort by selected key
  result.sort((a, b) => {
    let valA = a[sortKey.value];
    let valB = b[sortKey.value];
    
    // Handle numeric values (like price)
    if (sortKey.value === 'base_price') {
      valA = parseFloat(valA) || 0;
      valB = parseFloat(valB) || 0;
    } else {
      // Handle string values
      valA = (valA || '').toString().toLowerCase();
      valB = (valB || '').toString().toLowerCase();
    }
    
    return sortAsc.value ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
  });
  
  return result;
});

// Get unique categories
const categories = computed(() => {
  const uniqueCategories = new Set();
  products.value.forEach(product => {
    if (product.category && product.active === 1) {
      uniqueCategories.add(product.category);
    }
  });
  return Array.from(uniqueCategories).sort();
});

// Product statistics
const productCount = computed(() => {
  return products.value.filter(p => p.active === 1).length;
});

// Lifecycle hooks
onMounted(() => {
  fetchProducts().then(() => {
    fetchWasteEvents();
  });
});
</script>

<style scoped>
.dashboard {
  padding: 24px;
}

.dashboard-header {
  margin-bottom: 24px;
}

.dashboard-header h1 {
  font-size: 28px;
  color: #6F4E37;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #666;
  font-size: 16px;
  margin: 0;
}

/* Stats Cards */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  display: flex;
  align-items: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background-color: rgba(111, 78, 55, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
  color: #6F4E37;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

/* Calendar Chart */
.chart-section {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 32px;
}

.chart-section h2 {
  margin: 0 0 20px 0;
  font-size: 18px;
  color: #6F4E37;
}

.calendar-container {
  position: relative;
  min-height: 250px;
}

.loading-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.8);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(111, 78, 55, 0.1);
  border-radius: 50%;
  border-top-color: #6F4E37;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #999;
}

.no-data-icon {
  width: 48px;
  height: 48px;
  color: #ccc;
  margin-bottom: 16px;
}

/* Calendar Grid */
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
  min-height: 200px;
}

.calendar-day {
  background-color: #f9f9f9;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 200px;
  border: 1px solid #eee;
}

.calendar-day.has-data {
  background-color: rgba(111, 78, 55, 0.05);
  border-color: rgba(111, 78, 55, 0.2);
}

.day-header {
  background-color: #6F4E37;
  color: white;
  padding: 8px;
  text-align: center;
  font-size: 13px;
  font-weight: 500;
}

.day-content {
  padding: 10px;
  height: 100%;
  overflow-y: auto;
}

.day-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.day-item {
  font-size: 12px;
}

.item-badge {
  background-color: rgba(111, 78, 55, 0.1);
  color: #6F4E37;
  padding: 6px 8px;
  border-radius: 4px;
  display: block;
  text-align: center;
  font-weight: 500;
}

.day-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 12px;
}

/* Products Section */
.products-section {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 32px;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  flex-wrap: wrap;
  gap: 16px;
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
  color: #6F4E37;
}

.controls {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.search-container {
  position: relative;
  width: 250px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #999;
}

.search-input {
  padding: 10px 10px 10px 36px;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 100%;
  font-size: 14px;
}

.search-input:focus {
  border-color: #6F4E37;
  outline: none;
  box-shadow: 0 0 0 3px rgba(111, 78, 55, 0.1);
}

.sort-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  background-color: white;
}

.sort-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.sort-button:hover {
  background-color: #f5f5f5;
}

.sort-icon {
  width: 16px;
  height: 16px;
  color: #666;
  transition: transform 0.2s;
}

.sort-icon.flipped {
  transform: rotate(180deg);
}

/* Products Table */
.products-table-container {
  overflow-x: auto;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th {
  padding: 14px 16px;
  text-align: left;
  font-weight: 600;
  color: #666;
  background-color: #f9f9f9;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

.products-table td {
  padding: 16px;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

.products-table tr:hover td {
  background-color: #f5f5f5;
}

.product-name-cell {
  font-weight: 500;
  color: #333;
}

.description-cell {
  color: #666;
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.price-cell {
  font-weight: 600;
  color: #6F4E37;
}

.category-badge {
  display: inline-block;
  padding: 4px 8px;
  background-color: rgba(111, 78, 55, 0.1);
  color: #6F4E37;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

/* Empty State */
.empty-state {
  padding: 48px !important;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: #ccc;
  margin-bottom: 16px;
}

.empty-content p {
  color: #999;
  margin: 0;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .calendar-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }
  
  .calendar-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .controls {
    width: 100%;
  }
  
  .search-container {
    width: 100%;
  }
  
  .sort-control {
    width: 100%;
    justify-content: space-between;
  }
  
  .sort-select {
    flex: 1;
  }
  
  .description-cell {
    max-width: 150px;
  }
}

@media (max-width: 480px) {
  .calendar-grid {
    grid-template-columns: 1fr;
  }
}
</style>