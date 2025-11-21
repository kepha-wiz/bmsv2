import os

# Create all necessary directories
os.makedirs('app/templates', exist_ok=True)
os.makedirs('app/templates/auth', exist_ok=True)
os.makedirs('app/templates/admin', exist_ok=True)
os.makedirs('app/templates/employee', exist_ok=True)
os.makedirs('app/static/css', exist_ok=True)
os.makedirs('app/static/js', exist_ok=True)

# Create all templates with the fixed imports and new features
templates = {
    'base.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CKS Business Management System{% endblock %}</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

    <style>
        #sidebar {
            width: 250px;
            min-height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100;
            transition: all 0.3s;
        }
        
        #sidebar.collapsed {
            width: 80px;
        }
        
        .sidebar-toggle {
            position: absolute;
            right: -15px;
            top: 20px;
            background: #343a40;
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 101;
        }
        
        .main-content {
            margin-left: 250px;
            transition: all 0.3s;
            min-height: 100vh;
        }
        
        .main-content.expanded {
            margin-left: 80px;
        }
        
        @media (max-width: 768px) {
            #sidebar {
                display: none;
            }
            .main-content {
                margin-left: 0;
            }
        }
    </style>

    {% block styles %}{% endblock %}
</head>
<body class="d-flex">

    <!-- SIDEBAR -->
    <nav id="sidebar" class="bg-dark text-white p-3 d-none d-md-block">
        <div class="text-center mb-4">
            <button class="sidebar-toggle" onclick="toggleSidebar()">
                <i class="fas fa-bars"></i>
            </button>
            <h5 class="mt-3"><i class="fa fa-box"></i> CKS B.M.S</h5>
        </div>
        
        <ul class="nav flex-column">
            {% if current_user.is_authenticated %}
                {% if current_user.is_admin() %}
                    <!-- ADMIN LINKS -->
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'admin.dashboard' %}active fw-bold{% endif %}" href="{{ url_for('admin.dashboard') }}">
                            <i class="fa fa-chart-line"></i> <span class="sidebar-text">Dashboard</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'admin.products' %}active fw-bold{% endif %}" href="{{ url_for('admin.products') }}">
                            <i class="fa fa-boxes"></i> <span class="sidebar-text">Products</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'admin.add_product' %}active fw-bold{% endif %}" href="{{ url_for('admin.add_product') }}">
                            <i class="fa fa-plus-circle"></i> <span class="sidebar-text">Add Product</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'admin.add_stock' %}active fw-bold{% endif %}" href="{{ url_for('admin.add_stock') }}">
                            <i class="fa fa-layer-group"></i> <span class="sidebar-text">Add Stock</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'admin.stock_movement' %}active fw-bold{% endif %}" href="{{ url_for('admin.stock_movement') }}">
                            <i class="fa fa-exchange-alt"></i> <span class="sidebar-text">Stock Movement</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'admin.sales' %}active fw-bold{% endif %}" href="{{ url_for('admin.sales') }}">
                            <i class="fa fa-shopping-cart"></i> <span class="sidebar-text">Sales</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'admin.reports' %}active fw-bold{% endif %}" href="{{ url_for('admin.reports') }}">
                            <i class="fa fa-file-alt"></i> <span class="sidebar-text">Reports</span>
                        </a>
                    </li>
                {% else %}
                    <!-- EMPLOYEE LINKS -->
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'employee.dashboard' %}active fw-bold{% endif %}" href="{{ url_for('employee.dashboard') }}">
                            <i class="fa fa-chart-line"></i> <span class="sidebar-text">Dashboard</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'employee.products' %}active fw-bold{% endif %}" href="{{ url_for('employee.products') }}">
                            <i class="fa fa-boxes"></i> <span class="sidebar-text">Products</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'employee.add_sale' %}active fw-bold{% endif %}" href="{{ url_for('employee.add_sale') }}">
                            <i class="fa fa-plus-circle"></i> <span class="sidebar-text">Record Sale</span>
                        </a>
                    </li>
                    <li class="nav-item mb-2">
                        <a class="nav-link text-white {% if request.endpoint == 'employee.sales' %}active fw-bold{% endif %}" href="{{ url_for('employee.sales') }}">
                            <i class="fa fa-receipt"></i> <span class="sidebar-text">My Sales</span>
                        </a>
                    </li>
                {% endif %}
                <hr class="bg-light">
                <li>
                    <a class="nav-link text-danger" href="{{ url_for('auth.logout') }}">
                        <i class="fa fa-sign-out-alt"></i> <span class="sidebar-text">Logout</span>
                    </a>
                </li>
            {% endif %}
        </ul>
    </nav>

    <!-- MAIN CONTENT -->
    <div class="main-content flex-grow-1" id="mainContent">

        <!-- TOP NAVBAR -->
        <nav class="navbar navbar-light bg-light px-4 shadow-sm d-flex justify-content-between">
            <div class="container-fluid px-4">
                <form class="d-flex" method="GET" action="{{ url_for('admin.search_products') if current_user.is_admin() else url_for('employee.search_products') }}">
                    <div class="input-group">
                        <input type="text" name="query" class="form-control" placeholder="Search products..." value="{{ request.args.get('query', '') }}">
                        <button class="btn btn-outline-secondary" type="submit">
                            <i class="fas fa-search"></i>
                        </button>
                    </div>
                </form>
            </div>
            
            <span class="navbar-text ms-auto">
                {% if current_user.is_authenticated %}
                    <b>CKS BUSINESS MANAGEMENT SYSTEM</b>
                    <div class="small">Logged in as: <strong>{{ current_user.username }}</strong></div>
                {% endif %}
            </span>
        </nav>

        <!-- MOBILE MENU -->
        <div class="offcanvas offcanvas-start" tabindex="-1" id="mobileMenu">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title"><i class="fa fa-box"></i> Inventory Menu</h5>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
            </div>

            <div class="offcanvas-body">
                <ul class="nav flex-column">
                    {% if current_user.is_authenticated %}
                        {% if current_user.is_admin() %}
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'admin.dashboard' %}fw-bold text-primary{% endif %}" href="{{ url_for('admin.dashboard') }}">Dashboard</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'admin.products' %}fw-bold text-primary{% endif %}" href="{{ url_for('admin.products') }}">Products</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'admin.add_product' %}fw-bold text-primary{% endif %}" href="{{ url_for('admin.add_product') }}">Add Product</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'admin.add_stock' %}fw-bold text-primary{% endif %}" href="{{ url_for('admin.add_stock') }}">Add Stock</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'admin.stock_movement' %}fw-bold text-primary{% endif %}" href="{{ url_for('admin.stock_movement') }}">Stock Movement</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'admin.sales' %}fw-bold text-primary{% endif %}" href="{{ url_for('admin.sales') }}">Sales</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'admin.reports' %}fw-bold text-primary{% endif %}" href="{{ url_for('admin.reports') }}">Reports</a>
                            </li>
                        {% else %}
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'employee.dashboard' %}fw-bold text-primary{% endif %}" href="{{ url_for('employee.dashboard') }}">Dashboard</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'employee.products' %}fw-bold text-primary{% endif %}" href="{{ url_for('employee.products') }}">Products</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'employee.add_sale' %}fw-bold text-primary{% endif %}" href="{{ url_for('employee.add_sale') }}">Record Sale</a>
                            </li>
                            <li class="nav-item mb-2">
                                <a class="nav-link {% if request.endpoint == 'employee.sales' %}fw-bold text-primary{% endif %}" href="{{ url_for('employee.sales') }}">My Sales</a>
                            </li>
                        {% endif %}
                        <hr>
                        <li>
                            <a class="nav-link text-danger" href="{{ url_for('auth.logout') }}">Logout</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>

        <!-- PAGE CONTENT -->
        <div class="container-fluid py-4">
            {% block content %}{% endblock %}
        </div>
    </div>

    <!-- JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    <script>
        // Toggle sidebar
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.getElementById('mainContent');
            const sidebarTexts = document.querySelectorAll('.sidebar-text');
            
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
            
            // Hide/show text when sidebar is collapsed
            sidebarTexts.forEach(text => {
                if (sidebar.classList.contains('collapsed')) {
                    text.style.display = 'none';
                } else {
                    text.style.display = 'inline';
                }
            });
        }
        
        // Initialize sidebar state
        document.addEventListener('DOMContentLoaded', function() {
            // Check if we should start with collapsed sidebar on mobile
            if (window.innerWidth < 768) {
                const sidebar = document.getElementById('sidebar');
                const mainContent = document.getElementById('mainContent');
                sidebar.classList.add('collapsed');
                mainContent.classList.add('expanded');
                
                // Hide sidebar text
                document.querySelectorAll('.sidebar-text').forEach(text => {
                    text.style.display = 'none';
                });
            }
        });
    </script>
    
    {% block scripts %}{% endblock %}
</body>
</html>'''
}

# Create all other templates with their content
templates.update({
    'auth/login.html': '''{% extends "base.html" %}

{% block title %}Login - CKS Business Management System{% endblock %}

{% block styles %}
<style>
    .login-container {
        min-height: 100vh;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        max-width: 400px;
        width: 100%;
        animation: slideUp 0.5s ease-out;
    }
    
    .login-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 30px;
        text-align: center;
        color: white;
    }
    
    .login-header .logo {
        width: 60px;
        height: 60px;
        background: white;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        font-size: 24px;
        color: var(--primary-color);
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .password-toggle {
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
        color: #999;
        z-index: 10;
    }
    
    .password-toggle:hover {
        color: var(--primary-color);
    }
    
    .form-floating {
        position: relative;
    }
    
    .remember-forgot {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        font-size: 14px;
    }
    
    .form-check-input:checked {
        background-color: var(--primary-color);
        border-color: var(--primary-color);
    }
    
    .forgot-link {
        color: var(--primary-color);
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .forgot-link:hover {
        color: var(--secondary-color);
        text-decoration: underline;
    }
    
    .social-login {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .social-btn {
        flex: 1;
        padding: 10px;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        background: white;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-decoration: none;
        color: #333;
        font-size: 14px;
    }
    
    .social-btn:hover {
        border-color: var(--primary-color);
        background: #f8f9ff;
        transform: translateY(-2px);
        color: var(--primary-color);
    }
    
    .register-link {
        text-align: center;
        margin-top: 20px;
        color: #666;
    }
    
    .register-link a {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .register-link a:hover {
        color: var(--secondary-color);
        text-decoration: underline;
    }
</style>
{% endblock %}

{% block content %}
<div class="login-container">
    <div class="login-card">
        <div class="login-header">
            <div class="logo">
                <i class="fas fa-warehouse"></i>
            </div>
            <h3 class="mb-0">CKS Business Management</h3>
            <p class="mb-0 mt-2 opacity-75">Sign in to your account</p>
        </div>
        
        <div class="login-body">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                            <i class="fas fa-{% if category == 'danger' %}exclamation-circle{% elif category == 'success' %}check-circle{% else %}info-circle{% endif %} me-2"></i>
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST" id="loginForm">
                {{ form.hidden_tag() }}
                
                <div class="form-floating mb-3">
                    {{ form.username(class="form-control", placeholder="Username", id="floatingUsername") }}
                    <label for="floatingUsername">
                        <i class="fas fa-user me-2"></i>Username
                    </label>
                    {% if form.username.errors %}
                        <div class="text-danger mt-1">
                            {% for error in form.username.errors %}
                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="form-floating mb-3 position-relative">
                    {{ form.password(class="form-control", placeholder="Password", id="floatingPassword") }}
                    <label for="floatingPassword">
                        <i class="fas fa-lock me-2"></i>Password
                    </label>
                    <span class="password-toggle" onclick="togglePassword()">
                        <i class="fas fa-eye" id="toggleIcon"></i>
                    </span>
                    {% if form.password.errors %}
                        <div class="text-danger mt-1">
                            {% for error in form.password.errors %}
                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="remember-forgot">
                    <div class="form-check">
                        {{ form.remember_me(class="form-check-input", id="rememberCheck") }}
                        <label class="form-check-label" for="rememberCheck">
                            Remember me
                        </label>
                    </div>
                    <a href="#" class="forgot-link">Forgot password?</a>
                </div>
                
                <button type="submit" class="btn btn-primary w-100" id="loginBtn">
                    <i class="fas fa-sign-in-alt me-2"></i>
                    <span id="loginBtnText">Sign In</span>
                </button>
            </form>
            
            <div class="text-center my-4">
                <span>OR</span>
            </div>
            
            <div class="social-login">
                <a href="#" class="social-btn">
                    <i class="fab fa-google"></i>
                    <span>Google</span>
                </a>
                <a href="#" class="social-btn">
                    <i class="fab fa-microsoft"></i>
                    <span>Microsoft</span>
                </a>
            </div>
            
            <div class="register-link">
                Don't have an account? 
                <a href="{{ url_for('auth.register') }}">Register here</a>
            </div>
        </div>
    </div>
</div>

<!-- Demo Credentials Card -->
<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
    <div class="card" style="width: 300px;">
        <div class="card-header bg-info text-white">
            <h6 class="mb-0"><i class="fas fa-info-circle me-2"></i>Demo Credentials</h6>
        </div>
        <div class="card-body">
            <p class="mb-2"><strong>Admin:</strong></p>
            <p class="mb-1 small">Username: <code>admin</code></p>
            <p class="mb-3 small">Password: <code>admin123</code></p>
            
            <p class="mb-2"><strong>Employee:</strong></p>
            <p class="mb-1 small">Username: <code>employee</code></p>
            <p class="mb-0 small">Password: <code>emp123</code></p>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Toggle password visibility
    function togglePassword() {
        const passwordInput = document.getElementById('floatingPassword');
        const toggleIcon = document.getElementById('toggleIcon');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        }
    }
    
    // Form submission with loading state
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        const loginBtn = document.getElementById('loginBtn');
        const loginBtnText = document.getElementById('loginBtnText');
        
        // Show loading state
        loginBtn.disabled = true;
        loginBtnText.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Signing in...';
        
        // Simulate loading (remove this in production)
        setTimeout(() => {
            // Form will submit normally
        }, 500);
    });
    
    // Auto-focus on username field
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('floatingUsername').focus();
    });
    
    // Add input validation feedback
    document.getElementById('floatingUsername').addEventListener('input', function() {
        if (this.value.length > 0) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        } else {
            this.classList.remove('is-valid');
        }
    });
    
    document.getElementById('floatingPassword').addEventListener('input', function() {
        if (this.value.length > 0) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        } else {
            this.classList.remove('is-valid');
        }
    });
    
    // Handle forgot password
    document.querySelector('.forgot-link').addEventListener('click', function(e) {
        e.preventDefault();
        alert('Password reset functionality would be implemented here. Please contact administrator.');
    });
    
    // Handle social login
    document.querySelectorAll('.social-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const provider = this.querySelector('span').textContent;
            alert(`${provider} login integration would be implemented here.`);
        });
    });
</script>
{% endblock %}''',
    
    'auth/register.html': '''{% extends "base.html" %}

{% block title %}Register - CKS Business Management System{% endblock %}

{% block styles %}
<style>
    .register-container {
        min-height: 100vh;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .register-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        max-width: 450px;
        width: 100%;
        animation: slideUp 0.5s ease-out;
    }
    
    .register-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 30px;
        text-align: center;
        color: white;
    }
    
    .register-header .logo {
        width: 60px;
        height: 60px;
        background: white;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        font-size: 24px;
        color: var(--primary-color);
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
{% endblock %}

{% block content %}
<div class="register-container">
    <div class="register-card">
        <div class="register-header">
            <div class="logo">
                <i class="fas fa-warehouse"></i>
            </div>
            <h3 class="mb-0">CKS Business Management</h3>
            <p class="mb-0 mt-2 opacity-75">Create a new account</p>
        </div>
        
        <div class="register-body">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                            <i class="fas fa-{% if category == 'danger' %}exclamation-circle{% elif category == 'success' %}check-circle{% else %}info-circle{% endif %} me-2"></i>
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                {{ form.hidden_tag() }}
                
                <div class="form-floating mb-3">
                    {{ form.username(class="form-control", placeholder="Username", id="floatingUsername") }}
                    <label for="floatingUsername">
                        <i class="fas fa-user me-2"></i>Username
                    </label>
                    {% if form.username.errors %}
                        <div class="text-danger mt-1">
                            {% for error in form.username.errors %}
                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="form-floating mb-3">
                    {{ form.email(class="form-control", placeholder="Email", id="floatingEmail") }}
                    <label for="floatingEmail">
                        <i class="fas fa-envelope me-2"></i>Email
                    </label>
                    {% if form.email.errors %}
                        <div class="text-danger mt-1">
                            {% for error in form.email.errors %}
                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="form-floating mb-3">
                    {{ form.password(class="form-control", placeholder="Password", id="floatingPassword") }}
                    <label for="floatingPassword">
                        <i class="fas fa-lock me-2"></i>Password
                    </label>
                    {% if form.password.errors %}
                        <div class="text-danger mt-1">
                            {% for error in form.password.errors %}
                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="form-floating mb-3">
                    {{ form.password2(class="form-control", placeholder="Confirm Password", id="floatingPassword2") }}
                    <label for="floatingPassword2">
                        <i class="fas fa-lock me-2"></i>Confirm Password
                    </label>
                    {% if form.password2.errors %}
                        <div class="text-danger mt-1">
                            {% for error in form.password2.errors %}
                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="d-grid gap-2">
                    {{ form.submit(class="btn btn-primary") }}
                    <a href="{{ url_for('auth.login') }}" class="btn btn-secondary">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Auto-focus on username field
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('floatingUsername').focus();
    });
</script>
{% endblock %}''',
    
    'admin/dashboard.html': '''{% extends "base.html" %}

{% block title %}Admin Dashboard - CKS Business Management System{% endblock %}

{% block styles %}
<style>
    .stat-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
    }
    
    .table-responsive {
        border-radius: 10px;
        overflow: hidden;
    }
    
    .table th {
        background-color: rgba(102, 126, 234, 0.1);
        border-top: none;
        font-weight: 600;
    }
    
    .table-hover tbody tr:hover {
        background-color: rgba(102, 126, 234, 0.05);
    }
    
    .badge {
        font-weight: 500;
        border-radius: 6px;
    }
    
    .low-stock {
        background-color: #fff3cd !important;
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
                <i class="fas fa-layer-group me-2"></i>Add Stock
            </a>
            <a href="{{ url_for('admin.search_products') }}" class="btn btn-info">
                <i class="fas fa-search me-2"></i>Search Products
            </a>
            <a href="{{ url_for('admin.reports') }}" class="btn btn-secondary">
                <i class="fas fa-file-alt me-2"></i>Reports
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
                            <h4 class="card-title mb-0">{{ total_products }}</h4>
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
                            <h4 class="card-title mb-0">${{ "%.2f"|format(total_stock_value) }}</h4>
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
                            <h4 class="card-title mb-0">${{ "%.2f"|format(total_sales) }}</h4>
                            <p class="card-text">Total Sales</p>
                        </div>
                        <div class="align-self-center">
                            <i class="fas fa-chart-line fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        
        <div class="col-md-3 mb-4">
            <div class="card stat-card bg-warning text-white">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h4 class="card-title mb-0">{{ low_stock_products }}</h4>
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
                    <h5 class="card-title mb-0">
                        <i class="fas fa-chart-line me-2"></i>Sales Chart (Last 7 Days)
                    </h5>
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
                    <h5 class="card-title mb-0">
                        <i class="fas fa-trophy me-2"></i>Best Selling Products
                    </h5>
                </div>
                <div class="card-body">
                    {% if best_sellers %}
                        <div class="list-group list-group-flush">
                            {% for product in best_sellers %}
                                <div class="list-group-item d-flex justify-content-between align-items-center">
                                    <div>
                                        <h6 class="mb-1">{{ product.name }}</h6>
                                    <div class="text-muted">Units sold</div>
                                </div>
                                    <span class="badge bg-primary rounded-pill">{{ product.total_sold }} units</span>
                                </div>
                            </li>
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
                    <h5 class="card-title mb-0">
                        <i class="fas fa-exclamation-triangle me-2"></i>Low Stock Products
                    </h5>
                </div>
                <div class="card-body">
                    {% if low_stock %}
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>SKU</th>
                                        <th>Current Stock</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for product in low_stock %}
                                        <tr class="table-warning">
                                            <td>{{ product.name }}</td>
                                            <td>{{ product.sku }}</td>
                                            <td>{{ product.quantity_in_stock }}</td>
                                            <td>
                                                <div class="btn-group" role="group">
                                                    <a href="{{ url_for('admin.add_stock') }}?product_id={{ product.id }}" class="btn btn-sm btn-success" title="Add Stock">
                                                        <i class="fas fa-plus"></i>
                                                    </a>
                                                    <a href="{{ url_for('admin.add_product') }}?product_id={{ product.id }}" class="btn btn-sm btn-primary" title="Edit Product">
                                                        <i class="fas fa-edit"></i>
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
                            <i class="fas fa-check-circle fa-3x text-muted mb-3"></i>
                            <h4 class="text-muted">All products have sufficient stock</h4>
                            <p class="text-muted">No products are running low on stock</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-shopping-cart me-2"></i>Recent Sales Activities
                    </h5>
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
                                        <th>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for sale in recent_activities %}
                                        <tr>
                                            <td>{{ sale.product.name }}</td>
                                            <td>{{ sale.quantity_sold }}</td>
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
                            <h4 class="text-muted">No recent sales activities</h4>
                            <p class="text-muted">No sales have been recorded yet</p>
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
{% endblock %}''',
    
    'admin/products.html': '''{% extends "base.html" %}

{% block title %}Products - CKS Business Management System{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Products</h1>
        <div class="btn-group" role="group">
            <a href="{{ url_for('admin.add_product') }}" class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Add Product
            </a>
            <a href="{{ url_for('admin.search_products') }}" class="btn btn-info">
                <i class="fas fa-search me-2"></i>Search Products
            </a>
            <a href="{{ url_for('admin.add_stock') }}" class="btn btn-success">
                <i class="fas fa-layer-group me-2"></i>Add Stock
            </a>
            <a href="{{ url_for('admin.reports') }}" class="btn btn-secondary">
                <i class="fas fa-file-alt me-2"></i>Reports
            </a>
        </div>
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
                                <th>Category</th>
                                <th>Low Stock Threshold</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for product in products %}
                                <tr class="{% if product.is_low_stock() %}table-warning{% endif %}">
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="me-3">
                                                {% if product.quantity_in_stock == 0 %}
                                                    <i class="fas fa-times-circle text-danger"></i>
                                                {% elif product.quantity_in_stock < product.low_stock_threshold %}
                                                    <i class="fas fa-exclamation-triangle text-warning"></i>
                                                {% else %}
                                                    <i class="fas fa-check-circle text-success"></i>
                                                {% endif %}
                                            </div>
                                            <div>
                                                <strong>{{ product.name }}</strong>
                                                <div class="text-muted small">SKU: {{ product.sku }}</div>
                                            </div>
                                        </td>
                                        <td>{{ product.sku }}</td>
                                        <td>UGX{{ "%.2f"|format(product.cost_price) }}</td>
                                        <td>UGX{{ "%.2f"|format(product.selling_price) }}</td>
                                        <td>{{ product.quantity_in_stock }}</td>
                                        <td>UGX{{ "%.2f"|format(product.total_value) }}</td>
                                        <td>{{ product.category }}</td>
                                        <td>{{ product.low_stock_threshold }}</td>
                                        <td>
                                            <div class="btn-group" role="group'''})