// Main JavaScript file for CKS Business Management System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Format currency values
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Confirm before deletion
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

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