<template>
  <div class="waste-reports">
    <!-- Submit Waste Form -->
    <div class="form-card">
      <div class="card-header">
        <h3>Record Waste</h3>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="card-icon">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
      </div>
      
      <form @submit.prevent="submitWaste" class="waste-form">
        <div class="form-row">
          <div class="form-group">
            <label for="product-select">Product</label>
            <div class="select-wrapper">
              <select id="product-select" v-model="waste.product_id" required>
                <option disabled value="">Select a product</option>
                <option v-for="item in products" :key="item.product_id" :value="item.product_id">
                  {{ item.name }}
                </option>
              </select>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="select-arrow">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>
          
          <div class="form-group">
            <label for="quantity-input">Quantity</label>
            <div class="number-input-wrapper">
              <button type="button" @click="decrementQuantity" class="number-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="number-icon">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
              <input 
                id="quantity-input" 
                type="number" 
                v-model.number="waste.quantity" 
                min="1" 
                required 
              />
              <button type="button" @click="incrementQuantity" class="number-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="number-icon">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="reason-select">Reason</label>
            <div class="select-wrapper">
              <select id="reason-select" v-model="waste.reason" required>
                <option disabled value="">Select reason</option>
                <option v-for="r in reasons" :key="r" :value="r">{{ formatReason(r) }}</option>
              </select>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="select-arrow">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>
          
          <div class="form-group">
            <label>Date and Time</label>
            <div class="date-time-group">
              <div class="input-with-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="input-icon">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <input
                  type="date"
                  v-model="wasteDatePart"
                  required
                />
              </div>
              
              <div class="select-wrapper">
                <select v-model="wasteHourPart" required>
                  <option disabled value="">Hour</option>
                  <option v-for="opt in hourOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="select-arrow">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group full-width">
            <label for="notes-textarea">Notes (Optional)</label>
            <textarea 
              id="notes-textarea" 
              v-model="waste.notes" 
              rows="3" 
              placeholder="Additional details about this waste entry..."
            ></textarea>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="submit-btn">
            Submit Waste Entry
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="btn-icon">
              <path d="M5 12h14"></path>
              <path d="M12 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </form>
    </div>
    
    <!-- Waste History Section -->
    <div class="history-section">
      <div class="section-header">
        <h3>Waste History</h3>
        
        <div class="filters">
          <div class="filter-group">
            <label for="sort-select">Sort by</label>
            <div class="select-wrapper small">
              <select id="sort-select" v-model="sortKey">
                <option value="waste_date">Date</option>
                <option value="name">Product</option>
                <option value="quantity">Quantity</option>
                <option value="reason">Reason</option>
              </select>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="select-arrow">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>
          
          <button @click="toggleSortOrder" class="icon-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="button-icon" :class="{ 'flip': !sortAsc }">
              <path d="M7 10l5 5 5-5"></path>
              <path d="M7 15l5-5 5 5" style="opacity: 0"></path>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Waste Entries List -->
      <div class="waste-list">
        <div class="table-container">
          <table class="waste-table">
            <thead>
              <tr>
                <th @click="sortBy('name')" class="sortable-header">
                  <div class="header-content">
                    Product
                    <div class="sort-indicator" :class="{ active: sortKey === 'name' }">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'name' }">
                        <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                    </div>
                  </div>
                </th>
                <th @click="sortBy('quantity')" class="sortable-header">
                  <div class="header-content">
                    Quantity
                    <div class="sort-indicator" :class="{ active: sortKey === 'quantity' }">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'quantity' }">
                        <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                    </div>
                  </div>
                </th>
                <th @click="sortBy('reason')" class="sortable-header">
                  <div class="header-content">
                    Reason
                    <div class="sort-indicator" :class="{ active: sortKey === 'reason' }">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'reason' }">
                        <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                    </div>
                  </div>
                </th>
                <th @click="sortBy('waste_date')" class="sortable-header">
                  <div class="header-content">
                    Date
                    <div class="sort-indicator" :class="{ active: sortKey === 'waste_date' }">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'waste_date' }">
                        <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                    </div>
                  </div>
                </th>
                <th>Notes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(entry, index) in sortedWasteReports" :key="entry.waste_id || index">
                <td>{{ entry.name }}</td>
                <td class="quantity-cell">{{ entry.quantity }}</td>
                <td>
                  <span class="reason-badge" :class="getReasonClass(entry.reason)">
                    {{ formatReason(entry.reason) }}
                  </span>
                </td>
                <td>{{ formatDate(entry.waste_date) }}</td>
                <td class="notes-cell">
                  <span v-if="entry.notes" class="notes-preview">
                    {{ truncateNotes(entry.notes) }}
                  </span>
                  <span v-else class="empty-notes">—</span>
                </td>
                <td>
                  <button @click="openEditModal(entry)" class="action-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="action-icon">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                    Edit
                  </button>
                </td>
              </tr>
              
              <!-- Empty State -->
              <tr v-if="sortedWasteReports.length === 0">
                <td colspan="6" class="empty-state">
                  <div class="empty-content">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="empty-icon">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                      <polyline points="16 17 21 12 16 7"></polyline>
                      <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                    <p>No waste records found</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <!-- Edit Waste Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Edit Waste Entry</h3>
          <button @click="closeModal" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="close-icon">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label for="edit-product">Product</label>
            <div class="select-wrapper">
              <select id="edit-product" v-model="editWaste.product_id">
                <option v-for="item in products" :key="item.product_id" :value="item.product_id">
                  {{ item.name }}
                </option>
              </select>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="select-arrow">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>
          
          <div class="form-group">
            <label for="edit-quantity">Quantity</label>
            <input type="number" id="edit-quantity" v-model.number="editWaste.quantity" min="1" />
          </div>
          
          <div class="form-group">
            <label for="edit-reason">Reason</label>
            <div class="select-wrapper">
              <select id="edit-reason" v-model="editWaste.reason">
                <option v-for="r in reasons" :key="r" :value="r">{{ formatReason(r) }}</option>
              </select>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="select-arrow">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>
          
          <div class="form-group">
            <label>Date and Time</label>
            <div class="date-time-group">
              <div class="input-with-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="input-icon">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <input
                  type="date"
                  v-model="editWasteDatePart"
                  required
                />
              </div>
              
              <div class="select-wrapper">
                <select v-model="editWasteHourPart" required>
                  <option disabled value="">Hour</option>
                  <option v-for="option in hourOptions" :key="option.value" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="select-arrow">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="edit-notes">Notes</label>
            <textarea id="edit-notes" v-model="editWaste.notes" rows="3"></textarea>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="deleteWaste" class="delete-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="btn-icon">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            Delete
          </button>
          
          <div class="action-buttons">
            <button @click="closeModal" class="cancel-btn">Cancel</button>
            <button @click="updateWaste" class="save-btn">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="btn-icon">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// State for waste form
const editWasteDatePart = ref('');
const editWasteHourPart = ref('');

const getCurrentDateHour = () => {
  const now = new Date();
  now.setMinutes(0, 0, 0);
  return now.toISOString(); // "2023-04-06T14:00:00.000Z"
};

const wasteDatePart = ref(getCurrentDateHour().split('T')[0]);
const wasteHourPart = ref(getCurrentDateHour().split('T')[1].slice(0, 2) + ':00');

const waste = ref({
  product_id: '',
  quantity: 1,
  reason: '',
  waste_date: getCurrentDateHour(),
  notes: ''
});

// Time options
const formatHourLabel = (hour24) => {
  const hour = hour24 % 12 || 12;
  const suffix = hour24 < 12 ? 'AM' : 'PM';
  return `${hour} ${suffix}`;
};

const padHour = (h) => h.toString().padStart(2, '0');

const hourOptions = Array.from({ length: 24 }, (_, i) => ({
  value: `${padHour(i)}:00`,
  label: formatHourLabel(i)
}));

// Reasons list
const reasons = ['EXPIRED', 'DAMAGED', 'DROPPED', 'SPOILED', 'QUALITY_ISSUE', 'OTHER'];

// Table state
const products = ref([]);
const wasteReports = ref([]);
const sortKey = ref('waste_date');
const sortAsc = ref(false);
const showModal = ref(false);
const editWaste = ref({});

// Format reason for display
const formatReason = (reason) => {
  if (!reason) return '';
  return reason.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, s => s.toUpperCase());
};

// Get appropriate class for different reasons
const getReasonClass = (reason) => {
  if (!reason) return '';
  
  const reasonMap = {
    'EXPIRED': 'expired',
    'DAMAGED': 'damaged',
    'DROPPED': 'dropped',
    'SPOILED': 'spoiled',
    'QUALITY_ISSUE': 'quality',
    'OTHER': 'other'
  };
  
  return reasonMap[reason] || 'other';
};

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return '—';

  const date = new Date(dateString);
  
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
    timeZone: 'America/Chicago' 
  }).format(date);
};


// Truncate long notes
const truncateNotes = (notes, maxLength = 30) => {
  if (!notes) return '';
  return notes.length > maxLength ? notes.substring(0, maxLength) + '...' : notes;
};

// Quantity controls
const incrementQuantity = () => {
  waste.value.quantity++;
};

const decrementQuantity = () => {
  if (waste.value.quantity > 1) {
    waste.value.quantity--;
  }
};

// Sort functions
const toggleSortOrder = () => {
  sortAsc.value = !sortAsc.value;
};

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = true;
  }
};

const sortedWasteReports = computed(() => {
  return [...wasteReports.value].sort((a, b) => {
    let valA = a[sortKey.value];
    let valB = b[sortKey.value];
    
    // Special handling for dates
    if (sortKey.value === 'waste_date') {
      valA = new Date(valA).getTime();
      valB = new Date(valB).getTime();
      
      // Handle invalid dates
      if (isNaN(valA)) valA = 0;
      if (isNaN(valB)) valB = 0;
    } else {
      // Handle string values
      if (typeof valA === 'string') valA = valA.toLowerCase();
      if (typeof valB === 'string') valB = valB.toLowerCase();
    }
    
    return sortAsc.value ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
  });
});

// API calls
const fetchProducts = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/products');
    products.value = res.data.filter(product => product.active === 1);
  } catch (error) {
    console.error('Failed to fetch products:', error);
  }
};

const fetchWasteReports = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/waste');
    wasteReports.value = res.data;
  } catch (error) {
    console.error('Failed to fetch waste reports:', error);
  }
};

const submitWaste = async () => {
  try {
    const localDate = new Date(`${wasteDatePart.value}T${wasteHourPart.value}`);
    waste.value.waste_date = localDate.toISOString().slice(0, 19).replace('T', ' '); // Format for MySQL

    console.log('Submitting waste:', waste.value); 
    await axios.post('http://127.0.0.1:5000/waste', waste.value);
    await fetchWasteReports();
    
    // Reset form
    waste.value = {
      product_id: '',
      quantity: 1,
      reason: '',
      waste_date: getCurrentDateHour(),
      notes: ''
    };
    
    wasteDatePart.value = getCurrentDateHour().split('T')[0];
    wasteHourPart.value = getCurrentDateHour().split('T')[1].slice(0, 2) + ':00';
  } catch (error) {
    console.error('Failed to submit waste entry:', error);
    alert('Error submitting waste entry. Please try again.');
  }
};

// Edit waste entry
const openEditModal = (entry) => {
  try {
    const iso = new Date(entry.waste_date).toISOString();
    const [datePart, timePart] = iso.split('T');
    
    editWasteDatePart.value = datePart;
    editWasteHourPart.value = timePart.slice(0, 5); // HH:MM format
    
    editWaste.value = { ...entry };
  } catch (error) {
    console.error('Error parsing date:', error);
    
    // Fallback for date parsing issues
    editWasteDatePart.value = getCurrentDateHour().split('T')[0];
    editWasteHourPart.value = getCurrentDateHour().split('T')[1].slice(0, 5);
    editWaste.value = { ...entry };
  }
  
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};
//update waste entry
const updateWaste = async () => {
  try {
    if (!editWaste.value.waste_id) return;
    
    const localEditDate = new Date(`${editWasteDatePart.value}T${editWasteHourPart.value}`);
    editWaste.value.waste_date = localEditDate.toISOString();

    await axios.put(`http://127.0.0.1:5000/waste/${editWaste.value.waste_id}`, editWaste.value);
    await fetchWasteReports();
    closeModal();
  } catch (error) {
    console.error('Failed to update waste entry:', error);
    alert('Error updating waste entry. Please try again.');
  }
};

const deleteWaste = async () => {
  try {
    if (!editWaste.value.waste_id) return;
    
    if (confirm('Are you sure you want to delete this waste entry?')) {
      await axios.delete(`http://127.0.0.1:5000/waste/${editWaste.value.waste_id}`);
      await fetchWasteReports();
      closeModal();
    }
  } catch (error) {
    console.error('Failed to delete waste entry:', error);
    alert('Error deleting waste entry. Please try again.');
  }
};

// Fetch data on component mount
onMounted(() => {
  fetchProducts();
  fetchWasteReports();
});
</script>

<style scoped>
.waste-reports {
  padding: var(--space-md);
}

/* Form Card Styling */
.form-card {
  background-color: var(--surface);
  border-radius: 10px;
  padding: var(--space-lg);
  margin-bottom: var(--space-xl);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
}

.card-header h3 {
  font-size: var(--text-lg);
  color: var(--primary-dark);
  margin: 0;
}

.card-icon {
  width: 22px;
  height: 22px;
  stroke: var(--primary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* Form Styling */
.waste-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.form-row {
  display: flex;
  gap: var(--space-lg);
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group.full-width {
  width: 100%;
}

.form-group label {
  display: block;
  margin-bottom: var(--space-xs);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: var(--space-md);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: var(--text-md);
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(111, 78, 55, 0.1);
  outline: none;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

/* Select Styling */
.select-wrapper {
  position: relative;
}

.select-wrapper select {
  width: 100%;
  padding: var(--space-md);
  padding-right: var(--space-xl);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: var(--text-md);
  background-color: transparent;
  appearance: none;
  cursor: pointer;
}

.select-wrapper select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(111, 78, 55, 0.1);
  outline: none;
}

.select-arrow {
  position: absolute;
  right: var(--space-md);
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  stroke: var(--text-tertiary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  pointer-events: none;
}

.select-wrapper.small select {
  padding: var(--space-sm) var(--space-md);
  font-size: var(--text-sm);
}

/* Number Input Styling */
.number-input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.number-input-wrapper input {
  border: none;
  text-align: center;
  padding: var(--space-md) 0;
  width: 100%;
  -moz-appearance: textfield;
}

.number-input-wrapper input::-webkit-outer-spin-button,
.number-input-wrapper input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.number-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: rgba(111, 78, 55, 0.05);
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.number-btn:hover {
  background-color: rgba(111, 78, 55, 0.1);
}

.number-icon {
  width: 16px;
  height: 16px;
  stroke: var(--primary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* Date-Time Group */
.date-time-group {
  display: flex;
  gap: var(--space-md);
}

.date-time-group > * {
  flex: 1;
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: var(--space-md);
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
  padding-left: calc(var(--space-md) * 2.5);
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
}

.submit-btn {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: var(--space-md) var(--space-xl);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-icon {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* History Section */
.history-section {
  background-color: var(--surface);
  border-radius: 10px;
  padding: var(--space-lg);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
  flex-wrap: wrap;
  gap: var(--space-md);
}

.section-header h3 {
  font-size: var(--text-lg);
  color: var(--primary-dark);
  margin: 0;
}

/* Filters */
.filters {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}

.icon-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(111, 78, 55, 0.05);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 18px;
}

.icon-button:hover {
  background-color: rgba(111, 78, 55, 0.1);
}

.button-icon {
  width: 18px;
  height: 18px;
  stroke: var(--primary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  transition: transform 0.2s ease;
}

.button-icon.flip {
  transform: rotate(180deg);
}

/* Waste Table */
.table-container {
  overflow-x: auto;
}

.waste-table {
  width: 100%;
  border-collapse: collapse;
}

.waste-table th,
.waste-table td {
  padding: var(--space-md);
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.sortable-header {
  cursor: pointer;
}

.sortable-header:hover {
  background-color: rgba(111, 78, 55, 0.05);
}

.header-content {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.sort-indicator {
  opacity: 0.3;
  transition: opacity 0.2s ease;
}

.sort-indicator.active {
  opacity: 1;
}

.sort-icon {
  width: 16px;
  height: 16px;
  stroke: var(--primary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  transition: transform 0.2s ease;
}

.sort-icon.flipped {
  transform: rotate(180deg);
}

/* Reason Badges */
.reason-badge {
  display: inline-block;
  padding: var(--space-xs) var(--space-sm);
  border-radius: 20px;
  font-size: var(--text-xs);
  font-weight: 500;
}

.reason-badge.expired {
  background-color: rgba(211, 47, 47, 0.1);
  color: var(--danger);
}

.reason-badge.damaged {
  background-color: rgba(245, 124, 0, 0.1);
  color: var(--warning);
}

.reason-badge.dropped {
  background-color: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.reason-badge.spoiled {
  background-color: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
}

.reason-badge.quality {
  background-color: rgba(255, 193, 7, 0.1);
  color: #FFC107;
}

.reason-badge.other {
  background-color: rgba(158, 158, 158, 0.1);
  color: #757575;
}

/* Table Cell Styling */
.quantity-cell {
  font-weight: 600;
  color: var(--primary);
}

.notes-cell {
  max-width: 200px;
}

.notes-preview {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.empty-notes {
  color: var(--text-tertiary);
}

/* Action Buttons */
.action-btn {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-md);
  background-color: rgba(111, 78, 55, 0.1);
  color: var(--primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: var(--text-sm);
}

.action-btn:hover {
  background-color: var(--primary);
  color: white;
}

.action-icon {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* Empty State */
.empty-state {
  padding: var(--space-xxl) !important;
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
  stroke: var(--text-tertiary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  margin-bottom: var(--space-md);
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: var(--surface);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modal-fade-in 0.3s ease;
}

@keyframes modal-fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.modal-header h3 {
  margin: 0;
  font-size: var(--text-lg);
  color: var(--primary-dark);
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-xs);
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.close-icon {
  width: 18px;
  height: 18px;
  stroke: var(--text-tertiary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.modal-body {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.modal-footer {
  padding: var(--space-lg);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: var(--space-md);
}

.delete-btn, .cancel-btn, .save-btn {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-lg);
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.delete-btn {
  background-color: rgba(211, 47, 47, 0.1);
  color: var(--danger);
}

.delete-btn:hover {
  background-color: var(--danger);
  color: white;
}

.cancel-btn {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--text-secondary);
}

.cancel-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.save-btn {
  background-color: var(--primary);
  color: white;
}

.save-btn:hover {
  background-color: var(--primary-dark);
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: var(--space-md);
  }
  
  .date-time-group {
    flex-direction: column;
  }
  
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters {
    width: 100%;
    justify-content: space-between;
  }
  
  .icon-button {
    margin-top: 0;
  }
  
  .waste-table th,
  .waste-table td {
    padding: var(--space-sm);
  }
  
  .form-card,
  .history-section {
    padding: var(--space-md);
  }
  
  .modal-footer {
    flex-direction: column;
    gap: var(--space-md);
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .delete-btn, .action-buttons {
    width: 100%;
  }
  
  .cancel-btn, .save-btn {
    flex: 1;
  }
}
</style>