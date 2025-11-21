import os

# Create employee templates directory if it doesn't exist
os.makedirs('app/templates/employee', exist_ok=True)

# Create employee/dashboard.html
with open('app/templates/employee/dashboard.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Employee Dashboard - CKS Business Management System{% endblock %}

{% block styles %}
<style>
    .stat-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
    }
    
    .recent-sales {
        max-height: 400px;
        overflow-y: auto;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Employee Dashboard</h1>
        <div class="btn-group" role="group">
            <a href="{{ url_for('employee.add_sale') }}" class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Record Sale
            </a>
            <a href="{{ url_for('employee.products') }}" class="btn btn-info">
                <i class="fas fa-boxes me-2"></i>View Products
            </a>
        </div>
    </div>
    
    <!-- Statistics Cards -->
    <div class="row mb-4">
        <div class="col-md-4 mb-4">
            <div class="card stat-card bg-primary text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title">${{ "%.2f"|format(total_sales) }}</h4>
                            <p class="card-text">My Sales</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-chart-line fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card stat-card bg-success text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title">{{ sales_count }}</h4>
                            <p class="card-text">Transactions</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-shopping-cart fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card stat-card bg-info text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title">{{ available_products }}</h4>
                            <p class="card-text">Available Products</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-boxes fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Recent Sales -->
    <div class="row">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-receipt me-2"></i>My Recent Sales
                    </h5>
                </div>
                <div class="card-body recent-sales">
                    {% if recent_sales %}
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>Quantity</th>
                                        <th>Price/Unit</th>
                                        <th>Total</th>
                                        <th>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for sale in recent_sales %}
                                        <tr>
                                            <td>{{ sale.product.name }}</td>
                                            <td>{{ sale.quantity_sold }}</td>
                                            <td>${{ "%.2f"|format(sale.price_per_unit) }}</td>
                                            <td>${{ "%.2f"|format(sale.total_amount) }}</td>
                                            <td>{{ sale.timestamp.strftime('%Y-%m-%d %H:%M') }}</td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <div class="text-center py-5">
                            <i class="fas fa-receipt fa-3x text-muted mb-3"></i>
                            <h4 class="text-muted">No sales recorded yet</h4>
                            <p class="text-muted">Start recording sales to see them here</p>
                            <a href="{{ url_for('employee.add_sale') }}" class="btn btn-primary">
                                <i class="fas fa-plus me-2"></i>Record Your First Sale
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Auto-refresh dashboard every 30 seconds
    setInterval(function() {
        location.reload();
    }, 30000);
</script>
{% endblock %}""")

# Create employee/products.html
with open('app/templates/employee/products.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Products - CKS Business Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Available Products</h1>
        <a href="{{ url_for('employee.add_sale') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Record Sale
        </a>
    </div>
    
    <div class="card">
        <div class="card-body">
            {% if products %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>SKU</th>
                                <th>Selling Price</th>
                                <th>Stock Available</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for product in products %}
                                <tr class="{% if product.quantity_in_stock < 10 %}table-warning{% endif %}">
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="me-3">
                                                {% if product.quantity_in_stock == 0 %}
                                                    <i class="fas fa-exclamation-circle text-danger"></i>
                                                {% elif product.quantity_in_stock < 10 %}
                                                    <i class="fas fa-exclamation-triangle text-warning"></i>
                                                {% else %}
                                                    <i class="fas fa-check-circle text-success"></i>
                                                {% endif %}
                                            </div>
                                            <div>
                                                <strong>{{ product.name }}</strong>
                                                <div class="text-muted small">SKU: {{ product.sku }}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td>{{ product.sku }}</td>
                                    <td>${{ "%.2f"|format(product.selling_price) }}</td>
                                    <td>{{ product.quantity_in_stock }}</td>
                                    <td>
                                        <a href="{{ url_for('employee.add_sale') }}" class="btn btn-sm btn-success">
                                            <i class="fas fa-shopping-cart"></i> Sell
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-box fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No products available in stock</h4>
                    <p class="text-muted">All products are currently out of stock. Please contact administrator.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}""")

# Create employee/add_sale.html
with open('app/templates/employee/add_sale.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Record Sale - CKS Business Management System{% endblock %}

{% block styles %}
<style>
    .sale-form {
        max-width: 600px;
        margin: 0 auto;
    }
    
    .product-info {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .price-display {
        font-size: 18px;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    .form-floating {
        margin-bottom: 20px;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Record Sale</h1>
        <a href="{{ url_for('employee.dashboard') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
        </a>
    </div>
    
    <div class="row">
        <div class="col-md-8">
            <div class="card sale-form">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-shopping-cart me-2"></i>Sale Details
                    </h5>
                </div>
                <div class="card-body">
                    <form method="POST" id="saleForm">
                        {{ form.hidden_tag() }}
                        
                        <div class="form-floating mb-3">
                            {{ form.product_id.label(class="form-label") }}
                            {{ form.product_id(class="form-select") }}
                            {% if form.product_id.errors %}
                                <div class="text-danger">
                                    {% for error in form.product_id.errors %}
                                        <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="form-floating mb-3">
                            {{ form.quantity.label(class="form-label") }}
                            {{ form.quantity(class="form-control") }}
                            {% if form.quantity.errors %}
                                <div class="text-danger">
                                    {% for error in form.quantity.errors %}
                                        <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="d-grid gap-2">
                            {{ form.submit(class="btn btn-success") }}
                            <a href="{{ url_for('employee.dashboard') }}" class="btn btn-secondary">Cancel</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-info-circle me-2"></i>Product Info
                    </h5>
                </div>
                <div class="card-body product-info" id="productInfo">
                    <p class="text-muted">Select a product to see details</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Product selection change handler
    document.getElementById('product_id').addEventListener('change', function() {
        const productId = this.value;
        
        if (productId) {
            // Fetch product details (in real app, this would be an AJAX call)
            // For demo, we'll use hardcoded data
            const products = {
                1: { name: 'Laptop Computer', sku: 'LAPTOP001', selling_price: 1200, quantity_in_stock: 15 },
                2: { name: 'Wireless Mouse', sku: 'MOUSE001', selling_price: 25, quantity_in_stock: 50 },
                3: { name: 'USB Keyboard', sku: 'KEYBOARD001', selling_price: 40, quantity_in_stock: 30 }
            };
            
            const product = products[productId];
            if (product) {
                updateProductInfo(product);
            }
        } else {
            document.getElementById('productInfo').innerHTML = '<p class="text-muted">Select a product to see details</p>';
        }
    });
    
    function updateProductInfo(product) {
        document.getElementById('productInfo').innerHTML = `
            <h6>${product.name}</h6>
            <p><strong>SKU:</strong> ${product.sku}</p>
            <p><strong>Selling Price:</strong> <span class="price-display">$${product.selling_price.toFixed(2)}</span></p>
            <p><strong>Stock Available:</strong> ${product.quantity_in_stock} units</p>
        `;
    }
    
    // Form submission with loading state
    document.getElementById('saleForm').addEventListener('submit', function(e) {
        const submitBtn = document.querySelector('button[type="submit"]');
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        // Simulate loading (remove this in production)
        setTimeout(() => {
            // Form will submit normally
        }, 500);
    });
    
    // Auto-focus on product selection
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('product_id').focus();
    });
</script>
{% endblock %}""")

# Create employee/sales.html
with open('app/templates/employee/sales.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}My Sales - CKS Business Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">My Sales</h1>
        <div class="btn-group" role="group">
            <a href="{{ url_for('employee.add_sale') }}" class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Record Sale
            </a>
            <a href="{{ url_for('employee.dashboard') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
            </a>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <h5 class="card-title mb-0">
                <i class="fas fa-receipt me-2"></i>Sales History
            </h5>
        </div>
        <div class="card-body">
            {% if sales %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Product</th>
                                <th>Quantity</th>
                                <th>Price/Unit</th>
                                <th>Total</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for sale in sales %}
                                <tr>
                                    <td>{{ sale.id }}</td>
                                    <td>{{ sale.product.name }}</td>
                                    <td>{{ sale.quantity_sold }}</td>
                                    <td>${{ "%.2f"|format(sale.price_per_unit) }}</td>
                                    <td>${{ "%.2f"|format(sale.total_amount) }}</td>
                                    <td>{{ sale.timestamp.strftime('%Y-%m-%d %H:%M') }}</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-receipt fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No sales recorded yet</h4>
                    <p class="text-muted">Start recording sales to see them here</p>
                    <a href="{{ url_for('employee.add_sale') }}" class="btn btn-primary">
                        <i class="fas fa-plus me-2"></i>Record Your First Sale
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}""")

print("Employee templates created successfully!")