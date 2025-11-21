import os

# Create admin templates directory if it doesn't exist
os.makedirs('app/templates/admin', exist_ok=True)

# Create admin/dashboard.html
with open('app/templates/admin/dashboard.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Admin Dashboard - Inventory Management System{% endblock %}

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
    
    .table-responsive {
        border-radius: 10px;
        overflow: hidden;
    }
    
    .badge {
        font-size: 0.75rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Admin Dashboard</h1>
        <div class="btn-group" role="group">
            <a href="{{ url_for('admin.add_product') }}" class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Add Product
            </a>
            <a href="{{ url_for('admin.add_stock') }}" class="btn btn-success">
                <i class="fas fa-plus me-2"></i>Add Stock
            </a>
            <a href="{{ url_for('admin.reports') }}" class="btn btn-info">
                <i class="fas fa-file-pdf me-2"></i>Reports
            </a>
        </div>
    </div>
    
    <!-- Statistics Cards -->
    <div class="row mb-4">
        <div class="col-md-3 mb-4">
            <div class="card stat-card bg-primary text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title">{{ total_products }}</h4>
                            <p class="card-text">Total Products</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-box fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-4">
            <div class="card stat-card bg-success text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title">UGX{{ "%.2f"|format(total_stock_value) }}</h4>
                            <p class="card-text">Stock Value</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-dollar-sign fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-4">
            <div class="card stat-card bg-info text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title">UGX{{ "%.2f"|format(total_sales) }}</h4>
                            <p class="card-text">Total Sales</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-chart-line fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3 mb-4">
            <div class="card stat-card bg-warning text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title">{{ low_stock_products }}</h4>
                            <p class="card-text">Low Stock Items</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-exclamation-triangle fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Charts and Tables -->
    <div class="row">
        <div class="col-md-8 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Sales Chart (Last 7 Days)</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="salesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Best Selling Products</h5>
                </div>
                <div class="card-body">
                    {% if best_sellers %}
                        <div class="list-group list-group-flush">
                            {% for product in best_sellers %}
                                <div class="list-group-item d-flex justify-content-between align-items-center">
                                    <div>
                                        <h6 class="mb-1">{{ product.name }}</h6>
                                        <small class="text-muted">Units sold</small>
                                    </div>
                                    <span class="badge bg-primary rounded-pill">{{ product.total_sold }}</span>
                                </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-muted">No sales data available</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Low Stock Products</h5>
                </div>
                <div class="card-body">
                    {% if low_stock %}
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>SKU</th>
                                        <th>Stock</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for product in low_stock %}
                                        <tr class="table-warning">
                                            <td>{{ product.name }}</td>
                                            <td>{{ product.sku }}</td>
                                            <td>{{ product.quantity_in_stock }}</td>
                                            <td>
                                                <a href="{{ url_for('admin.add_stock') }}" class="btn btn-sm btn-success">
                                                    <i class="fas fa-plus"></i> Add Stock
                                                </a>
                                            </td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted">All products have sufficient stock</p>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Recent Sales Activities</h5>
                </div>
                <div class="card-body">
                    {% if recent_activities %}
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>Quantity</th>
                                        <th>Total</th>
                                        <th>Employee</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for sale in recent_activities %}
                                        <tr>
                                            <td>{{ sale.product.name }}</td>
                                            <td>{{ sale.quantity_sold }}</td>
                                            <td>UGX{{ "%.2f"|format(sale.total_amount) }}</td>
                                            <td>{{ sale.employee.username }}</td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted">No recent sales activities</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Sales Chart
    const ctx = document.getElementById('salesChart').getContext('2d');
    const salesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: {{ dates|tojson }},
            datasets: [{
                label: 'Sales Amount',
                data: {{ amounts|tojson }},
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                }
            }
        }
    });
</script>
{% endblock %}""")

# Create admin/products.html
with open('app/templates/admin/products.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Products - Inventory Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Products</h1>
        <a href="{{ url_for('admin.add_product') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Add Product
        </a>
    </div>
    
    <div class="card">
        <div class="card-body">
            {% if products %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>SKU</th>
                                <th>Cost Price</th>
                                <th>Selling Price</th>
                                <th>Stock</th>
                                <th>Total Value</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for product in products %}
                                <tr class="{% if product.quantity_in_stock < 10 %}table-warning{% endif %}">
                                    <td>{{ product.name }}</td>
                                    <td>{{ product.sku }}</td>
                                    <td>UGX{{ "%.2f"|format(product.cost_price) }}</td>
                                    <td>UGX{{ "%.2f"|format(product.selling_price) }}</td>
                                    <td>{{ product.quantity_in_stock }}</td>
                                    <td>UGX{{ "%.2f"|format(product.total_value) }}</td>
                                    <td>
                                        <div class="btn-group" role="group">
                                            <a href="{{ url_for('admin.add_stock') }}" class="btn btn-sm btn-success">
                                                <i class="fas fa-plus"></i> Add Stock
                                            </a>
                                        </div>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-box fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No products found</h4>
                    <p class="text-muted">Add your first product to get started</p>
                    <a href="{{ url_for('admin.add_product') }}" class="btn btn-primary">
                        <i class="fas fa-plus me-2"></i>Add Product
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}""")

# Create admin/add_product.html
with open('app/templates/admin/add_product.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Add Product - Inventory Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Add Product</h1>
        <a href="{{ url_for('admin.products') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>Back to Products
        </a>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <form method="POST">
                        {{ form.hidden_tag() }}
                        
                        <div class="mb-3">
                            {{ form.name.label(class="form-label") }}
                            {{ form.name(class="form-control") }}
                            {% if form.name.errors %}
                                <div class="text-danger">
                                    {% for error in form.name.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.sku.label(class="form-label") }}
                            {{ form.sku(class="form-control") }}
                            {% if form.sku.errors %}
                                <div class="text-danger">
                                    {% for error in form.sku.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.cost_price.label(class="form-label") }}
                            {{ form.cost_price(class="form-control", step="0.01") }}
                            {% if form.cost_price.errors %}
                                <div class="text-danger">
                                    {% for error in form.cost_price.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.selling_price.label(class="form-label") }}
                            {{ form.selling_price(class="form-control", step="0.01") }}
                            {% if form.selling_price.errors %}
                                <div class="text-danger">
                                    {% for error in form.selling_price.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.quantity_in_stock.label(class="form-label") }}
                            {{ form.quantity_in_stock(class="form-control") }}
                            {% if form.quantity_in_stock.errors %}
                                <div class="text-danger">
                                    {% for error in form.quantity_in_stock.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex gap-2">
                            {{ form.submit(class="btn btn-primary") }}
                            <a href="{{ url_for('admin.products') }}" class="btn btn-secondary">Cancel</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""")

# Create admin/add_stock.html
with open('app/templates/admin/add_stock.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Add Stock - Inventory Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Add Stock</h1>
        <a href="{{ url_for('admin.products') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>Back to Products
        </a>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <form method="POST">
                        {{ form.hidden_tag() }}
                        
                        <div class="mb-3">
                            {{ form.product_id.label(class="form-label") }}
                            {{ form.product_id(class="form-select") }}
                            {% if form.product_id.errors %}
                                <div class="text-danger">
                                    {% for error in form.product_id.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.quantity.label(class="form-label") }}
                            {{ form.quantity(class="form-control") }}
                            {% if form.quantity.errors %}
                                <div class="text-danger">
                                    {% for error in form.quantity.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex gap-2">
                            {{ form.submit(class="btn btn-success") }}
                            <a href="{{ url_for('admin.products') }}" class="btn btn-secondary">Cancel</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""")

# Create admin/sales.html
with open('app/templates/admin/sales.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Sales - Inventory Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Sales History</h1>
        <div class="btn-group" role="group">
            <a href="{{ url_for('admin.reports') }}" class="btn btn-info">
                <i class="fas fa-file-pdf me-2"></i>Generate Report
            </a>
        </div>
    </div>
    
    <div class="card">
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
                                <th>Employee</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for sale in sales %}
                                <tr>
                                    <td>{{ sale.id }}</td>
                                    <td>{{ sale.product.name }}</td>
                                    <td>{{ sale.quantity_sold }}</td>
                                    <td>UGX{{ "%.2f"|format(sale.price_per_unit) }}</td>
                                    <td>UGX{{ "%.2f"|format(sale.total_amount) }}</td>
                                    <td>{{ sale.employee.username }}</td>
                                    <td>{{ sale.timestamp.strftime('%Y-%m-%d %H:%M') }}</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No sales recorded yet</h4>
                    <p class="text-muted">Sales will appear here once employees start recording them</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}""")

# Create admin/reports.html
with open('app/templates/admin/reports.html', 'w') as f:
    f.write("""{% extends "base.html" %}

{% block title %}Reports - Inventory Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Generate Reports</h1>
        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
        </a>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Select Date Range</h5>
                </div>
                <div class="card-body">
                    <form method="POST" action="{{ url_for('admin.generate_report', report_type='sales') }}">
                        {{ form.hidden_tag() }}
                        
                        <div class="mb-3">
                            {{ form.start_date.label(class="form-label") }}
                            {{ form.start_date(class="form-control") }}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.end_date.label(class="form-label") }}
                            {{ form.end_date(class="form-control") }}
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" formaction="{{ url_for('admin.generate_report', report_type='sales') }}" class="btn btn-primary">
                                <i class="fas fa-file-pdf me-2"></i>Sales Report
                            </button>
                            <button type="submit" formaction="{{ url_for('admin.generate_report', report_type='stock') }}" class="btn btn-success">
                                <i class="fas fa-file-pdf me-2"></i>Stock Report
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Report Information</h5>
                </div>
                <div class="card-body">
                    <div class="accordion" id="reportInfoAccordion">
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="salesReportHeading">
                                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#salesReportCollapse" aria-expanded="true" aria-controls="salesReportCollapse">
                                    Sales Report
                                </button>
                            </h2>
                            <div id="salesReportCollapse" class="accordion-collapse collapse show" aria-labelledby="salesReportHeading" data-bs-parent="#reportInfoAccordion">
                                <div class="accordion-body">
                                    <p>The sales report includes:</p>
                                    <ul>
                                        <li>Total sales amount</li>
                                        <li>Total units sold</li>
                                        <li>Number of transactions</li>
                                        <li>Detailed sales information</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="stockReportHeading">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#stockReportCollapse" aria-expanded="false" aria-controls="stockReportCollapse">
                                    Stock Report
                                </button>
                            </h2>
                            <div id="stockReportCollapse" class="accordion-collapse collapse" aria-labelledby="stockReportHeading" data-bs-parent="#reportInfoAccordion">
                                <div class="accordion-body">
                                    <p>The stock report includes:</p>
                                    <ul>
                                        <li>Stock additions within date range</li>
                                        <li>Current stock levels</li>
                                        <li>Stock value calculations</li>
                                        <li>Low stock indicators</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""")

print("Admin templates created successfully!")