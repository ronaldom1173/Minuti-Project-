<!-- AnalyticsDashboard.vue -->
<template>
  <div class="analytics-dashboard">
    <!-- ░░░ OVERVIEW ───────────────────────────────────────────────────░░░ -->
    <div v-if="tab === 'overview'" class="analytics-section">
      <!-- Quick‑stats cards -->
      <div class="stats-cards">
        <div class="stat-card">
          <div class="stat-value">{{ topWasteStats.totalItems }}</div>
          <div class="stat-label">Total Wasted Items</div>
          <div class="stat-trend" :class="topWasteStats.trend > 0 ? 'up' : 'down'">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="trend-icon">
              <polyline :points="topWasteStats.trend > 0 ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"/>
            </svg>
            {{ Math.abs(topWasteStats.trend) }}% from last period
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-value">${{ topWasteStats.totalCost }}</div>
          <div class="stat-label">Cost Impact</div>
          <div class="stat-trend" :class="topWasteStats.costTrend > 0 ? 'up' : 'down'">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="trend-icon">
              <polyline :points="topWasteStats.costTrend > 0 ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"/>
            </svg>
            {{ Math.abs(topWasteStats.costTrend) }}% from last period
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-value">{{ topWasteStats.mainReason || 'N/A' }}</div>
          <div class="stat-label">Top Waste Reason</div>
          <div class="stat-info">{{ topWasteStats.reasonPercent }}% of all waste</div>
        </div>
      </div>

      <!-- Top Wasted Products ------------------------------------------->
      <div class="dashboard-card product-waste-card">
        <div class="card-header">
          <h3>Top Wasted Products</h3>
          <div class="time-badge">Last 30 Days</div>
        </div>

        <div class="product-waste-list">
          <div
            v-for="(item, idx) in topWastedProducts"
            :key="idx"
            class="product-waste-item"
          >
            <div class="product-waste-rank">{{ idx + 1 }}</div>
            <div class="product-waste-info">
              <div class="product-waste-name">{{ item.name }}</div>
              <div class="product-waste-bar-container">
                <div
                  class="product-waste-bar"
                  :style="{ width: getBarWidth(item) }"
                />
                <span class="product-waste-value">{{ item.total_quantity }}</span>
              </div>
            </div>
          </div>

          <div v-if="!topWastedProducts.length" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="empty-icon">
              <circle cx="12" cy="12" r="10" />
              <line x1="8" y1="12" x2="16" y2="12" />
            </svg>
            <p>No waste data available for the past 30 days</p>
          </div>
        </div>
      </div>

      <!-- Production Patterns & Insights (recommendations removed) ------->
      <div class="dashboard-card">
        <div class="card-header">
          <h3>Production Patterns & Insights</h3>
          <div class="time-badge">Last 30 Days</div>
        </div>

        <div class="patterns-grid">
          <!-- Weekly Heat‑map only -->
          <div class="pattern-card">
            <h4>Weekly Waste Pattern</h4>
            <div class="weekday-heatmap">
              <div
                v-for="day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']"
                :key="day"
                class="weekday-cell"
                :class="getDayHeatClass(day)"
              >
                <div class="day-label">{{ day }}</div>
                <div class="day-value">{{ getDayWasteCount(day) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action link to detailed reports ------------------------------->
      <div class="action-link">
        <button
          @click="showComponent('Analytics'); setAnalyticsTab('report')"
          class="action-button"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="button-icon">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
          </svg>
          Generate Detailed Report
        </button>
      </div>
    </div>

    <!-- ░░░ REPORT TAB ───────────────────────────────────────────────────░░░ -->
    <div v-else-if="tab === 'report'" class="analytics-section">
      <!-- Date Selection Panel -->
      <div class="report-tools-panel">
        <div class="date-selection">
          <h3>Report Generator</h3>
          <p class="helper-text">Select date range to generate your waste report</p>

          <div class="date-inputs">
            <div class="date-field">
              <label for="start-date">Start Date</label>
              <div class="input-with-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="input-icon">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                <input id="start-date" type="date" v-model="startDate" />
              </div>
            </div>

            <div class="date-field">
              <label for="end-date">End Date</label>
              <div class="input-with-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="input-icon">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                <input id="end-date" type="date" v-model="endDate" />
              </div>
            </div>
          </div>

          <div class="date-presets">
            <button @click="setDateRange('today')"   class="preset-button">Today</button>
            <button @click="setDateRange('week')"    class="preset-button">This Week</button>
            <button @click="setDateRange('month')"   class="preset-button">This Month</button>
            <button @click="setDateRange('quarter')" class="preset-button">This Quarter</button>
          </div>

          <div class="action-buttons">
            <button @click="fetchData" class="primary-button">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="button-icon">
                <path d="M21 12a9 9 0 01-9 9 9 9 0 010-18 9 9 0 019 9z"/>
                <polyline points="12 5 12 12 16 14"/>
              </svg>
              Generate Report
            </button>

            <button
              @click="exportCSV"
              class="secondary-button"
              :disabled="!hasReportData"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="button-icon">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              Export CSV
            </button>
          </div>
        </div>
      </div>

      <!-- Reports Display -->
      <div class="reports-display" v-if="hasReportData">
        <!-- Summary cards -->
        <div class="report-summary">
          <div class="summary-card">
            <div class="summary-value">{{ reportSummary.totalItems }}</div>
            <div class="summary-label">Items Wasted</div>
          </div>

          <div class="summary-card">
            <div class="summary-value">${{ reportSummary.totalCost }}</div>
            <div class="summary-label">Total Cost</div>
          </div>

          <div class="summary-card">
            <div class="summary-value">{{ reportSummary.topReason }}</div>
            <div class="summary-label">Primary Reason</div>
          </div>

          <div class="summary-card">
            <div class="summary-value">{{ reportSummary.uniqueProducts }}</div>
            <div class="summary-label">Unique Products</div>
          </div>
        </div>

        <!-- Charts -->
        <div class="report-charts">
          <!-- Waste by Product -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>Waste by Product</h3>
              <div class="chart-subtitle">Product-specific waste analysis</div>
            </div>
            <div class="chart-container">
              <Graph :data="wasteSummary" />
            </div>
          </div>

          <!-- Waste Cost -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>Waste Cost Analysis</h3>
              <div class="chart-subtitle">Financial impact of waste</div>
            </div>
            <div class="chart-container">
              <CostGraph :data="wasteCost" />
            </div>
          </div>

          <!-- Waste by Reason -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>Waste by Reason</h3>
              <div class="chart-subtitle">Root cause analysis</div>
            </div>
            <div class="chart-container pie-container">
              <PieChart :data="wasteByReason" />
            </div>

            <div class="reason-stats">
              <div v-for="item in wasteByReason" :key="item.reason" class="reason-item">
                <div class="reason-label">{{ formatReason(item.reason) }}</div>
                <div class="reason-bar-container">
                  <div
                    class="reason-bar"
                    :style="{ width: getReasonWidth(item) }"
                  />
                  <span class="reason-value">{{ item.total_quantity }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Data table -->
        <div class="data-table-card">
          <div class="table-header">
            <h3>Detailed Waste Data</h3>
            <div class="table-actions">
              <button @click="exportCSV" class="table-action-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="button-icon-small">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Export Data
              </button>
            </div>
          </div>

          <div class="data-table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Quantity</th>
                  <th>Base Price</th>
                  <th>Total Cost</th>
                  <th>Primary Reason</th>
                  <th>Date Range</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in wasteCost.slice(0, 10)" :key="idx">
                  <td>{{ item.product_name }}</td>
                  <td>{{ item.total_quantity }}</td>
                  <td>${{ parseFloat(item.base_price).toFixed(2) }}</td>
                  <td>${{ parseFloat(item.total_cost_lost).toFixed(2) }}</td>
                  <td>{{ productPrimaryReasons[item.product_name] || 'Various' }}</td>
                  <td>{{ dateRangeStr }}</td>
                </tr>
              </tbody>
            </table>

            <div v-if="wasteCost.length > 10" class="table-footer">
              Showing 10 of {{ wasteCost.length }} entries. Export to CSV for full data.
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="empty-report-state">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="empty-icon">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
        <p class="empty-title">Select a date range to generate report</p>
        <p class="empty-text">
          Choose your preferred start and end dates and click “Generate Report” to analyze waste data.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';
import PieChart  from './PieChart.vue';
import Graph     from './Graph.vue';
import CostGraph from './CostGraph.vue';

/* Props & Emits */
const props = defineProps({ tab: String });
const emit  = defineEmits(['update:tab', 'component-change']);

/* Reactive State (overview + report) */
const startDate  = ref('');
const endDate    = ref('');
const wasteCost  = ref([]);
const wasteByReason   = ref([]);
const wasteSummary    = ref([]);
const topWastedProducts = ref([]);
const productPrimaryReasons = ref({});  // for table in report
const weeklyWastePattern = ref({Mon:0,Tue:0,Wed:0,Thu:0,Fri:0,Sat:0,Sun:0});
// NEW ‑ holds every /waste row that falls inside the date range
const wasteRows = ref([]);


/* Overview stats */
const topWasteStats = ref({
  totalItems   : 0,
  totalCost    : 0,
  trend        : -5,
  costTrend    : -8,
  mainReason   : '',
  reasonPercent: 0
});

/* ───────────── computed helpers (report) ───────────── */
const hasReportData = computed(() =>
  wasteCost.value.length     ||
  wasteByReason.value.length ||
  wasteSummary.value.length
);

/* Accurate summary built from raw rows (wasteRows) */
const reportSummary = computed(() => {
  if (!hasReportData.value) {
    return { totalItems: 0, totalCost: 0, topReason: 'N/A', uniqueProducts: 0 };
  }

  // ① Correct total items
  const totalItems = wasteRows.value.reduce((sum, r) => sum + (r.quantity || 0), 0);

  // ② Total cost (same as before)
  const totalCost = wasteCost.value
    .reduce((sum, i) => sum + parseFloat(i.total_cost_lost || 0), 0)
    .toFixed(2);

  // ③ Most common reason
  let topReason = 'N/A', max = 0;
  wasteByReason.value.forEach(r => {
    if (r.total_quantity > max) {
      max = r.total_quantity;
      topReason = formatReason(r.reason);
    }
  });

  return {
    totalItems,
    totalCost,
    topReason,
    uniqueProducts: wasteSummary.value.length
  };
});

/* User‑friendly string that exactly matches the chosen inputs */
const dateRangeStr = computed(() =>
  startDate.value && endDate.value ? `${startDate.value} – ${endDate.value}` : ''
);


const formatDateRange = computed(() => {
  if (!startDate.value || !endDate.value) return '';
  const s=new Date(startDate.value), e=new Date(endDate.value);
  return `${s.toLocaleDateString()} - ${e.toLocaleDateString()}`;
});

/* ───────────── UI helpers ───────────── */
const getBarWidth = item => {
  if (!topWastedProducts.value.length) return '0%';
  const max = Math.max(...topWastedProducts.value.map(p=>p.total_quantity||0));
  return `${Math.min(Math.max(item.total_quantity/max*100,10),100)}%`;
};
const getReasonWidth = item => {
  if (!wasteByReason.value.length) return '0%';
  const max = Math.max(...wasteByReason.value.map(r=>r.total_quantity||0));
  return `${item.total_quantity/max*100}%`;
};
const formatReason = r =>
  r?.replace(/_/g,' ').toLowerCase().replace(/\b\w/g,s=>s.toUpperCase());

/* ───────────── Overview loader ───────────── */
/* ───────────── Overview loader ───────────── */
const fetchOverviewData = async () => {
  try {
    /* 0. 30‑day window for the CURRENT period */
    const today  = new Date();                 // T
    const start  = new Date(today);            // T‑30
    start.setDate(today.getDate() - 30);

    /* 1. visual “Top Wasted Products” list */
    const prodRes = await axios.get(
      'http://127.0.0.1:5000/top-wasted-products-30days'
    );
    topWastedProducts.value = prodRes.data;

    /* 2. pull raw rows once, filter to current window --------------- */
    const rows = (await axios.get('http://127.0.0.1:5000/waste')).data
      .filter(r => {
        const ts = new Date(r.waste_date).getTime();
        return ts >= start.getTime() && ts <= today.getTime();
      });

    topWasteStats.value.totalItems = rows.reduce(
      (s, r) => s + (r.quantity || 0), 0
    );

    calculateWeeklyWastePattern(rows);

    /* 3. aggregated endpoints for CURRENT period -------------------- */
    const params = {
      start_date: start.toISOString().split('T')[0],
      end_date:   today.toISOString().split('T')[0]
    };

    const [costRes, reasonRes] = await Promise.all([
      axios.get('http://127.0.0.1:5000/all-waste-cost',     { params }),
      axios.get('http://127.0.0.1:5000/all-waste-by-reason',{ params })
    ]);

    topWasteStats.value.totalCost = costRes.data
      .reduce((s, c) => s + parseFloat(c.total_cost_lost || 0), 0)
      .toFixed(2);

    if (reasonRes.data.length) {
      const numeric = reasonRes.data.map(r => ({
        ...r,
        total_quantity: Number(r.total_quantity || 0)
      }));

      const main = numeric.reduce((a, b) =>
        a.total_quantity > b.total_quantity ? a : b
      );
      const sum  = numeric.reduce((s, r) => s + r.total_quantity, 0);

      topWasteStats.value.mainReason    = formatReason(main.reason);
      topWasteStats.value.reasonPercent = sum ? Math.round(main.total_quantity / sum * 100) : 0;
    }

    /* 4.  PRIOR 30‑day period for comparison ------------------------ */
    const prevEnd   = new Date(start);         // T‑30
    const prevStart = new Date(prevEnd);       // T‑60
    prevStart.setDate(prevEnd.getDate() - 30);

    const prevParams = {
      start_date: prevStart.toISOString().split('T')[0],
      end_date:   prevEnd  .toISOString().split('T')[0]
    };

    const [prevCostRes, prevReasonRes] = await Promise.all([
      axios.get('http://127.0.0.1:5000/all-waste-cost',     { params: prevParams }),
      axios.get('http://127.0.0.1:5000/all-waste-by-reason',{ params: prevParams })
    ]);

    const prevItems = prevReasonRes.data
      .reduce((s, r) => s + Number(r.total_quantity || 0), 0);

    const prevCost  = prevCostRes.data
      .reduce((s, c) => s + parseFloat(c.total_cost_lost || 0), 0);

    /* 5.  percent change vs. previous period ------------------------ */
    topWasteStats.value.trend = prevItems
      ? Math.round(((topWasteStats.value.totalItems - prevItems) / prevItems) * 100)
      : 0;

    topWasteStats.value.costTrend = prevCost
      ? Math.round(((parseFloat(topWasteStats.value.totalCost) - prevCost) / prevCost) * 100)
      : 0;

  } catch (e) {
    console.error('Overview load error', e);
  }
};


/* ───────────── Report loader ───────────── */
/* ───────────── Report loader ───────────── */
const fetchData = async () => {
  // 0. guard‑rail
  if (!startDate.value || !endDate.value) {
    alert('Please select both start and end dates.');
    return;
  }

  /* 1. query‑string params shared by every backend endpoint */
  const params = {
    start_date: startDate.value,
    end_date:   endDate.value
  };

  try {
    /* 2. hit the three aggregated endpoints in parallel */
    const [costRes, reasonRes, summaryRes] = await Promise.all([
      axios.get('http://127.0.0.1:5000/all-waste-cost',               { params }),
      axios.get('http://127.0.0.1:5000/all-waste-by-reason',          { params }),
      axios.get('http://127.0.0.1:5000/all-waste-summary-per-product',{ params })
    ]);

    // store the aggregates for charts + cards + table
    wasteCost.value      = costRes.data;
    wasteByReason.value  = reasonRes.data;
    wasteSummary.value   = summaryRes.data;

    /* 3. fetch full /waste rows once, then trim to the chosen range */
    const allRows = (await axios.get('http://127.0.0.1:5000/waste')).data;
    wasteRows.value = allRows.filter(r => {
      const ts = new Date(r.waste_date).getTime();
      return ts >= new Date(startDate.value).getTime() &&
             ts <= new Date(endDate.value).getTime();
    });

    /* 4. derive per‑product primary reasons from those rows */
    fetchProductReasons();   // helper lives outside this function
  }
  catch (e) {
    console.error('Report fetch error', e);
    alert('Failed to load data. Check console.');
  }
};


/* Builds the most common reason per product using wasteRows */
const fetchProductReasons = () => {
  const grouped = {};                // { productName: { reason: count } }
  wasteRows.value.forEach(r => {
    if (!grouped[r.name]) grouped[r.name] = {};
    grouped[r.name][r.reason] = (grouped[r.name][r.reason] || 0) + (r.quantity || 1);
  });

  const primary = {};
  Object.entries(grouped).forEach(([prod, reasons]) => {
    let max = 0, chosen = '';
    Object.entries(reasons).forEach(([reason, count]) => {
      if (count > max) { max = count; chosen = reason; }
    });
    primary[prod] = formatReason(chosen);
  });

  productPrimaryReasons.value = primary;
};


const exportCSV = () => {
  if (!startDate.value || !endDate.value) {
    alert('Please select both start and end dates.'); return;
  }
  window.open(
    `http://127.0.0.1:5000/export-waste-csv?start_date=${startDate.value}&end_date=${endDate.value}`,
    '_blank'
  );
};

/* ───────────── heat‑map helpers ───────────── */
const calculateWeeklyWastePattern = rows => {
  const map={0:'Sun',1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'};
  const counts={Mon:0,Tue:0,Wed:0,Thu:0,Fri:0,Sat:0,Sun:0};
  rows.forEach(r=>{
    counts[map[new Date(r.waste_date).getDay()]] += r.quantity||0;
  });
  weeklyWastePattern.value = counts;
};
const getDayWasteCount = d => weeklyWastePattern.value[d]||0;
const getDayHeatClass = d => {
  const max=Math.max(...Object.values(weeklyWastePattern.value));
  if(!max) return 'heat-1';
  const p=getDayWasteCount(d)/max;
  return p>=.8?'heat-5':p>=.6?'heat-4':p>=.4?'heat-3':p>=.2?'heat-2':'heat-1';
};

/* ───────────── date helpers ───────────── */
const setDateRange = preset=>{
  const today=new Date(); let start=new Date();
  switch(preset){
    case 'today': start=today; break;
    case 'week' : start=new Date(today); start.setDate(today.getDate()-today.getDay()); break;
    case 'month': start=new Date(today.getFullYear(),today.getMonth(),1); break;
    case 'quarter':
    const quarterStartMonth = Math.floor(today.getMonth() / 3) * 3;
    start = new Date(today.getFullYear(), quarterStartMonth, 1);
    break;
  }
  startDate.value = start.toISOString().split('T')[0];
  endDate.value   = today.toISOString().split('T')[0];
};

/* ───────────── misc helpers ───────────── */
const showComponent = c => emit('component-change',c);
const setAnalyticsTab = t => emit('update:tab',t);

/* ───────────── lifecycle ───────────── */
onMounted(()=>{
  const today=new Date();
  startDate.value=new Date(today.getFullYear(),today.getMonth(),1)
                  .toISOString().split('T')[0];
  endDate.value=today.toISOString().split('T')[0];
  if(props.tab==='overview') fetchOverviewData();
});
watch(()=>props.tab,t=>t==='overview'&&fetchOverviewData(),{immediate:true});
</script>





<style scoped>
.analytics-dashboard {
  padding: var(--space-md);
}

/* Stats Cards */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: var(--primary-dark);
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.stat-trend.up {
  color: var(--danger);
}

.stat-trend.down {
  color: var(--success);
}

.trend-icon {
  width: 14px;
  height: 14px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.stat-info {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Dashboard Cards */
.dashboard-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 32px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  font-size: 18px;
  color: var(--primary-dark);
  margin: 0;
}

.time-badge {
  background-color: var(--primary);
  color: white;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 20px;
}

/* Product Waste List */
.product-waste-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-waste-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-waste-rank {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: rgba(111, 78, 55, 0.1);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 13px;
}

.product-waste-info {
  flex: 1;
}

.product-waste-name {
  font-size: 14px;
  margin-bottom: 6px;
  color: var(--text-primary);
}

.product-waste-bar-container {
  position: relative;
  height: 8px;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.product-waste-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: var(--primary);
  border-radius: 4px;
}

.product-waste-value {
  position: absolute;
  right: -24px;
  top: -7px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* Patterns Grid */
.patterns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.pattern-card {
  background-color: var(--background);
  border-radius: 8px;
  padding: 15px;
}

.pattern-card h4 {
  font-size: 15px;
  margin: 0 0 15px 0;
  color: var(--primary-dark);
}

/* Weekday Heatmap */
.weekday-heatmap {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.weekday-cell {
  aspect-ratio: 1;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px 0;
}

.day-label {
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 5px;
}

.day-value {
  font-size: 14px;
  font-weight: 600;
}

/* Heat levels */
.heat-1 {
  background-color: rgba(0, 188, 140, 0.1);
  color: #00bc8c;
}

.heat-2 {
  background-color: rgba(0, 188, 140, 0.2);
  color: #00bc8c;
}

.heat-3 {
  background-color: rgba(255, 193, 7, 0.2);
  color: #d69000;
}

.heat-4 {
  background-color: rgba(255, 128, 64, 0.2);
  color: #f25900;
}

.heat-5 {
  background-color: rgba(255, 64, 64, 0.3);
  color: #cf0000;
}

/* Recommendations */
.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recommendation-item {
  background-color: rgba(255, 193, 7, 0.1);
  border-left: 3px solid #ffc107;
  padding: 10px;
  border-radius: 0 4px 4px 0;
}

.recommendation-day {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 5px;
  color: var(--primary-dark);
}

.recommendation-content {
  font-size: 13px;
  color: var(--text-secondary);
}

.highlighted {
  font-weight: 500;
  color: var(--primary);
}

.empty-recommendation {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  color: var(--text-tertiary);
}

.info-icon {
  width: 24px;
  height: 24px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  margin-bottom: 8px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  color: var(--text-tertiary);
}

.empty-icon {
  width: 40px;
  height: 40px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  margin-bottom: 15px;
}

/* Action Link */
.action-link {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: var(--space-md) var(--space-lg);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.button-icon {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* Report Generator Section */
.report-tools-panel {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 30px;
}

.date-selection h3 {
  font-size: 18px;
  color: var(--primary-dark);
  margin: 0 0 8px 0;
}

.helper-text {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0 0 20px 0;
}

.date-inputs {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.date-field {
  flex: 1;
}

.date-field label {
  display: block;
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  stroke: var(--text-tertiary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.input-with-icon input {
  width: 100%;
  padding: 10px 10px 10px 35px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: 14px;
}

.input-with-icon input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(111, 78, 55, 0.1);
}

.date-presets {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.preset-button {
  padding: 8px 12px;
  background-color: rgba(111, 78, 55, 0.1);
  color: var(--primary);
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-button:hover {
  background-color: rgba(111, 78, 55, 0.2);
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.primary-button, .secondary-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.primary-button {
  background-color: var(--primary);
  color: white;
}

.primary-button:hover {
  background-color: var(--primary-dark);
}

.secondary-button {
  background-color: var(--secondary);
  color: var(--primary-dark);
}

.secondary-button:hover {
  background-color: var(--accent);
}

.secondary-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Reports Display */
.reports-display {
  margin-top: 30px;
}

/* Report Summary */
.report-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.summary-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  padding: 15px;
  text-align: center;
}

.summary-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 8px;
}

.summary-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Report Charts */
.report-charts {
  display: grid;
  grid-template-columns: 1fr;
  gap: 48px;
  margin-bottom: 30px;
}

.chart-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px 20px 48px;
  overflow: visible;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-header h3 {
  font-size: 18px;
  color: var(--primary-dark);
  margin: 0 0 4px 0;
}

.chart-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
}

.chart-container {
  height: 300px;
  margin-bottom: 15px;
}

.pie-container {
  height: 250px;
}

/* Reason Stats */
.reason-stats {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.reason-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.reason-label {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 14px;
}

.reason-bar-container {
  position: relative;
  height: 8px;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.reason-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: var(--primary-light);
  border-radius: 4px;
}

.reason-value {
  position: absolute;
  right: -24px;
  top: -7px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* Data Table */
.data-table-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 30px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.table-header h3 {
  font-size: 18px;
  color: var(--primary-dark);
  margin: 0;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.table-action-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background-color: rgba(111, 78, 55, 0.1);
  color: var(--primary);
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.table-action-button:hover {
  background-color: rgba(111, 78, 55, 0.2);
}

.button-icon-small {
  width: 14px;
  height: 14px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.data-table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 10px 15px;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.data-table th {
  font-weight: 600;
  color: var(--text-secondary);
  background-color: rgba(0, 0, 0, 0.02);
  font-size: 13px;
}

.data-table td {
  font-size: 14px;
}

.table-footer {
  text-align: center;
  padding: 15px 0 0;
  font-size: 13px;
  color: var(--text-secondary);
}

/* Empty Report State */
.empty-report-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 30px;
  background-color: var(--surface);
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.empty-icon {
  width: 60px;
  height: 60px;
  stroke: var(--text-tertiary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.empty-text {
  color: var(--text-tertiary);
  max-width: 450px;
  margin: 0 auto;
}

/* Responsive Adjustments */
@media (min-width: 768px) {
  .report-charts {
    grid-template-columns: repeat(2, 1fr);
    gap: 40px 48px;
  }
  
  .chart-card:last-child {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .date-inputs {
    flex-direction: column;
    gap: 15px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .summary-card {
    padding: 10px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .patterns-grid {
    grid-template-columns: 1fr;
  }
  
  .weekday-heatmap {
    gap: 3px;
  }
  
  .weekday-cell {
    padding: 5px 0;
  }
  
  .day-label {
    font-size: 10px;
  }
  
  .day-value {
    font-size: 12px;
  }
}
</style>