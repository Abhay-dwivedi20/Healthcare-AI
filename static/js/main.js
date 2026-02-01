// static/js/main.js

// Global variables
const API_BASE_URL = window.location.origin;

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Healthcare AI loaded');
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize form validations
    initFormValidations();
    
    // Add loading indicators to submit buttons
    addLoadingIndicators();
    
    // Initialize file upload previews
    initFileUploadPreviews();
    
    // Add smooth scrolling for anchor links
    initSmoothScroll();
});

// Initialize Bootstrap tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize form validations
function initFormValidations() {
    const forms = document.querySelectorAll('form.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Add loading indicators to submit buttons
function addLoadingIndicators() {
    document.addEventListener('submit', function(e) {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Processing...
            `;
            submitBtn.disabled = true;
            
            // Store original text to restore later
            submitBtn.dataset.originalText = originalText;
            
            // Restore button after 10 seconds (safety)
            setTimeout(() => {
                if (submitBtn) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            }, 10000);
        }
    });
}

// Initialize file upload previews
function initFileUploadPreviews() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (!file) return;
            
            // Validate file size (5MB max)
            const maxSize = 5 * 1024 * 1024; // 5MB
            if (file.size > maxSize) {
                showToast('File is too large. Maximum size is 5MB.', 'danger');
                this.value = '';
                return;
            }
            
            // Validate file type
            const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
            if (!validTypes.includes(file.type)) {
                showToast('Invalid file type. Please upload an image (JPG, PNG, GIF).', 'danger');
                this.value = '';
                return;
            }
            
            // Show preview for image files
            if (file.type.startsWith('image/')) {
                showImagePreview(file, this);
            }
        });
    });
}

// Show image preview
function showImagePreview(file, inputElement) {
    const reader = new FileReader();
    const container = inputElement.closest('.mb-3');
    
    // Remove existing preview
    const existingPreview = container.querySelector('.image-preview');
    if (existingPreview) existingPreview.remove();
    
    reader.onload = function(e) {
        const previewDiv = document.createElement('div');
        previewDiv.className = 'image-preview mt-2';
        previewDiv.innerHTML = `
            <div class="card">
                <div class="card-body p-2">
                    <div class="d-flex align-items-center">
                        <img src="${e.target.result}" 
                             class="img-thumbnail me-3" 
                             style="width: 80px; height: 80px; object-fit: cover;">
                        <div>
                            <small class="d-block">${file.name}</small>
                            <small class="text-muted">${(file.size / 1024).toFixed(2)} KB</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(previewDiv);
    };
    
    reader.readAsDataURL(file);
}

// Initialize smooth scrolling
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">Healthcare AI</strong>
                <small>Just now</small>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.innerHTML += toastHtml;
    
    // Show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    toast.show();
    
    // Remove toast from DOM after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// API Helper Functions
class HealthcareAPI {
    // Test API connection
    static async testConnection() {
        try {
            const response = await fetch(`${API_BASE_URL}/test`);
            return await response.json();
        } catch (error) {
            console.error('API Connection Error:', error);
            return null;
        }
    }
    
    // Get health status
    static async getHealthStatus() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health Check Error:', error);
            return { status: 'unhealthy', error: error.message };
        }
    }
    
    // Chat with AI
    static async sendChatMessage(message) {
        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            return await response.json();
        } catch (error) {
            console.error('Chat Error:', error);
            return { error: 'Failed to send message' };
        }
    }
    
    // Upload file for prediction
    static async uploadFile(file, endpoint) {
        const formData = new FormData();
        formData.append('image', file);
        
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                body: formData
            });
            return await response.json();
        } catch (error) {
            console.error('Upload Error:', error);
            return { error: 'Failed to upload file' };
        }
    }
}

// Utility Functions
const Utils = {
    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleString();
    },
    
    // Truncate text
    truncateText: function(text, maxLength = 100) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },
    
    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text)
            .then(() => showToast('Copied to clipboard!', 'success'))
            .catch(err => console.error('Copy failed:', err));
    },
    
    // Download as JSON
    downloadJSON: function(data, filename) {
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'healthcare-data.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    },
    
    // Validate email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    // Validate number range
    validateNumberRange: function(number, min, max) {
        return !isNaN(number) && number >= min && number <= max;
    }
};

// Dark mode toggle (optional)
function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (!darkModeToggle) return;
    
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }
    
    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    });
}

// Initialize dark mode
initDarkMode();

// Export for use in other scripts (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { HealthcareAPI, Utils };
}