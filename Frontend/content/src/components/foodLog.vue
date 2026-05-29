<template>
  <div class="products-manager">
    <!-- Add Product Form Card -->
    <div class="form-card">
      <div class="card-header">
        <h3>Add New Product</h3>
        <!-- Modified: Removed the circle from SVG -->
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="card-icon">
          <line x1="12" y1="8" x2="12" y2="16"></line>
          <line x1="8" y1="12" x2="16" y2="12"></line>
        </svg>
      </div>
      
      <form @submit.prevent="submitProduct" class="add-product-form">
        <div class="form-row">
          <div class="form-group">
            <label for="product-name">Product Name</label>
            <input 
              id="product-name" 
              type="text" 
              v-model="product.name" 
              placeholder="Enter product name" 
              required
            />
          </div>
          
          <div class="form-group">
            <label for="product-category">Category</label>
            <div class="dropdown-wrapper">
              <input
                id="product-category"
                type="text"
                v-model="product.category"
                @focus="showCategoryDropdown = true"
                @input="filterCategories"
                @blur="hideDropdownWithDelay"
                placeholder="Select or type category"
                autocomplete="off"
              />
              <div v-if="showCategoryDropdown && filteredCategories.length" class="dropdown-menu">
                <div 
                  v-for="cat in filteredCategories" 
                  :key="cat" 
                  @mousedown.prevent="selectCategory(cat)"
                  class="dropdown-item"
                >
                  {{ cat }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group full-width">
            <label for="product-description">Description</label>
            <input 
              id="product-description" 
              type="text" 
              v-model="product.description" 
              placeholder="Product description (optional)"
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="product-price">Base Price ($)</label>
            <input 
              id="product-price" 
              type="text" 
              v-model="product.base_price" 
              placeholder="0.00" 
              pattern="^\d+(\.\d{1,2})?$"
              required 
            />
          </div>
          
          <div class="form-group checkbox-group">
            <div class="checkbox-label">Status</div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="product.active">
              <span class="toggle-slider"></span>
              <span class="toggle-label">{{ product.active ? 'Active' : 'Inactive' }}</span>
            </label>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="submit-btn">
            Add Product
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="btn-icon">
              <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
              <path d="M12 8v8"></path>
              <path d="M8 12h8"></path>
            </svg>
          </button>
        </div>
      </form>
    </div>
    
    <!-- Products List Section -->
    <div class="products-list-section">
      <div class="section-header">
        <h3>Product Inventory</h3>
        
        <div class="search-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="search-icon">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search products..." 
            class="search-input" 
          />
        </div>
      </div>
      
      <div class="products-table-container">
        <table class="products-table">
          <thead>
            <tr>
              <th @click="sortBy('name')" class="sortable-header">
                <div class="header-content">
                  Product Name
                  <div class="sort-indicator" :class="{ active: sortKey === 'name' }">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'name' }">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                </div>
              </th>
              <th @click="sortBy('category')" class="sortable-header">
                <div class="header-content">
                  Category
                  <div class="sort-indicator" :class="{ active: sortKey === 'category' }">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'category' }">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                </div>
              </th>
              <th @click="sortBy('base_price')" class="sortable-header">
                <div class="header-content">
                  Price
                  <div class="sort-indicator" :class="{ active: sortKey === 'base_price' }">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'base_price' }">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                </div>
              </th>
              <th @click="sortBy('active')" class="sortable-header">
                <div class="header-content">
                  Status
                  <div class="sort-indicator" :class="{ active: sortKey === 'active' }">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sort-icon" :class="{ flipped: !sortAsc && sortKey === 'active' }">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                </div>
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in filteredAndSortedProducts" :key="item.product_id || index">
              <td>{{ item.name }}</td>
              <td>
                <span v-if="item.category" class="category-badge">
                  {{ item.category }}
                </span>
                <span v-else>—</span>
              </td>
              <td>${{ parseFloat(item.base_price || 0).toFixed(2) }}</td>
              <td>
                <span :class="['status-badge', item.active ? 'active' : 'inactive']">
                  {{ item.active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <button @click="openEditModal(item)" class="action-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="action-icon">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                  Edit
                </button>
              </td>
            </tr>
            
            <!-- Empty State - Modified: Removed the circle from SVG -->
            <tr v-if="filteredAndSortedProducts.length === 0">
              <td colspan="5" class="empty-state">
                <div class="empty-content">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="empty-icon">
                    <line x1="8" y1="12" x2="16" y2="12"></line>
                  </svg>
                  <p>No products found</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Edit Product Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Edit Product</h3>
          <button @click="closeModal" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="close-icon">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label for="edit-name">Product Name</label>
            <input 
              id="edit-name" 
              type="text" 
              v-model="editProduct.name" 
              placeholder="Product name" 
            />
          </div>
          
          <div class="form-group">
            <label for="edit-category">Category</label>
            <input 
              id="edit-category" 
              type="text" 
              v-model="editProduct.category" 
              placeholder="Category" 
            />
          </div>
          
          <div class="form-group">
            <label for="edit-description">Description</label>
            <input 
              id="edit-description" 
              type="text" 
              v-model="editProduct.description" 
              placeholder="Description" 
            />
          </div>
          
          <div class="form-group">
            <label for="edit-price">Base Price ($)</label>
            <input 
              id="edit-price" 
              type="text" 
              v-model="editProduct.base_price" 
              placeholder="0.00" 
              pattern="^\d+(\.\d{1,2})?$" 
            />
          </div>
          
          <div class="form-group checkbox-group">
            <div class="checkbox-label">Status</div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="editProduct.active">
              <span class="toggle-slider"></span>
              <span class="toggle-label">{{ editProduct.active ? 'Active' : 'Inactive' }}</span>
            </label>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="deleteProduct" class="delete-btn">
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
            <button @click="updateProduct" class="save-btn">
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

// Product form state
const product = ref({
  name: '',
  description: '',
  base_price: '',
  category: '',
  active: true
});

// Products list state
const products = ref([]);
const showModal = ref(false);
const editProduct = ref({});
const searchQuery = ref('');
const sortKey = ref('name');
const sortAsc = ref(true);

// Category dropdown state
const showCategoryDropdown = ref(false);
const filteredCategories = ref([]);

// Fetch all products
const fetchProducts = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/products');
    products.value = res.data;
  } catch (error) {
    console.error('Failed to fetch products:', error);
  }
};

// Filter categories for dropdown
const filterCategories = () => {
  const input = product.value.category.toLowerCase();
  filteredCategories.value = uniqueCategories.value.filter(cat =>
    cat.toLowerCase().includes(input)
  );
};

// Select a category from dropdown
const selectCategory = (cat) => {
  product.value.category = cat;
  showCategoryDropdown.value = false;
};

// Hide dropdown with delay to allow click
const hideDropdownWithDelay = () => {
  setTimeout(() => showCategoryDropdown.value = false, 150);
};

// Sort products
const sortBy = (key) => {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = true;
  }
};

// Filter and sort products
const filteredAndSortedProducts = computed(() => {
  return [...products.value]
    .filter(p =>
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (p.category && p.category.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (p.description && p.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
    )
    .sort((a, b) => {
      let valA = a[sortKey.value];
      let valB = b[sortKey.value];

      // Handle numeric values like base_price
      if (sortKey.value === 'base_price') {
        valA = parseFloat(valA);
        valB = parseFloat(valB);
      } else {
        // Handle string values
        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();
      }

      return sortAsc.value ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    });
});

// Get unique categories
const uniqueCategories = computed(() => {
  const set = new Set(products.value.map(p => p.category).filter(Boolean));
  return Array.from(set);
});

// Add a new product
const submitProduct = async () => {
  try {
    const base = parseFloat(product.value.base_price);
    const isValid = !isNaN(base) && base >= 0;

    if (!isValid) {
      alert('Enter a valid base price');
      return;
    }

    await axios.post('http://127.0.0.1:5000/products', {
      name: product.value.name,
      description: product.value.description || '',
      category: product.value.category || '',
      base_price: parseFloat(base.toFixed(2)),
      active: product.value.active
    });

    await fetchProducts();

    // Reset form
    product.value = {
      name: '',
      description: '',
      base_price: '',
      category: '',
      active: true
    };
  } catch (error) {
    console.error('Failed to create product:', error);
    alert('Error adding product. Please try again.');
  }
};

// Edit product modal
const openEditModal = (product) => {
  editProduct.value = {
    ...product,
    active: product.active === 1 || product.active === true
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// Update a product
const updateProduct = async () => {
  try {
    if (!editProduct.value.product_id) return;

    await axios.put(`http://127.0.0.1:5000/products/${editProduct.value.product_id}`, editProduct.value);
    await fetchProducts();
    closeModal();
  } catch (error) {
    console.error('Failed to update product:', error);
    alert('Error updating product. Please try again.');
  }
};

// Delete a product
const deleteProduct = async () => {
  try {
    if (!editProduct.value.product_id) return;

    if (confirm('Are you sure you want to delete this product?')) {
      await axios.delete(`http://127.0.0.1:5000/products/${editProduct.value.product_id}`);
      await fetchProducts();
      closeModal();
    }
  } catch (error) {
    console.error('Failed to delete product:', error);
    alert('Error deleting product. Please try again.');
  }
};

// Fetch products on component mount
onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.products-manager {
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
.add-product-form {
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

.form-group input {
  width: 100%;
  padding: var(--space-md);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: var(--text-md);
  transition: all 0.2s ease;
}

.form-group input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(111, 78, 55, 0.1);
  outline: none;
}

/* Dropdown Styling */
.dropdown-wrapper {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: var(--surface);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 0 0 8px 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.dropdown-item {
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: rgba(111, 78, 55, 0.1);
}

/* Checkbox/Toggle Styling */
.checkbox-group {
  display: flex;
  flex-direction: column;
}

.checkbox-label {
  margin-bottom: var(--space-xs);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 150px;
  height: 44px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 22px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 36px;
  width: 36px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--success);
}

input:focus + .toggle-slider {
  box-shadow: 0 0 1px var(--success);
}

input:checked + .toggle-slider:before {
  transform: translateX(104px);
}

.toggle-label {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 50px;
  color: white;
  font-weight: 500;
  transition: .4s;
}

input:checked ~ .toggle-label {
  left: 15px;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
}

/* Fixed submit button styling */
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
  font-size: var(--text-sm);
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

/* Products List Section */
.products-list-section {
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

/* Search Input */
.search-wrapper {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: var(--space-md);
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  stroke: var(--text-tertiary);
  stroke-width: 2;
  fill: none;
}

.search-input {
  width: 100%;
  padding: var(--space-md) var(--space-md) var(--space-md) calc(var(--space-md) * 2.5);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-size: var(--text-md);
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(111, 78, 55, 0.1);
  outline: none;
}

/* Improved Products Table */
.products-table-container {
  overflow-x: auto;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: var(--space-lg);
}

.products-table th,
.products-table td {
  padding: var(--space-md);
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

/* Add these styles for better readability */
.products-table th {
  background-color: rgba(111, 78, 55, 0.05);
  font-weight: 600;
}

.products-table tbody tr:hover {
  background-color: rgba(111, 78, 55, 0.02);
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

/* Status and Category Badges */
.status-badge {
  display: inline-block;
  padding: var(--space-xs) var(--space-sm);
  border-radius: 20px;
  font-size: var(--text-xs);
  font-weight: 500;
}

.status-badge.active {
  background-color: rgba(56, 142, 60, 0.1);
  color: var(--success);
}

.status-badge.inactive {
  background-color: rgba(211, 47, 47, 0.1);
  color: var(--danger);
}

.category-badge {
  display: inline-block;
  padding: var(--space-xs) var(--space-sm);
  border-radius: 20px;
  background-color: rgba(111, 78, 55, 0.1);
  color: var(--primary);
  font-size: var(--text-xs);
}

/* Action Button */
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

/* Fixed: Removed circle from empty icon */
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
  
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-wrapper {
    width: 100%;
  }
  
  .products-table th,
  .products-table td {
    padding: var(--space-sm);
  }
  
  .form-card,
  .products-list-section {
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