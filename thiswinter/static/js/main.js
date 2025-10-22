// Main JavaScript for KioskHelp Web Portal

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add fade-in animation to cards
    $('.card').addClass('fade-in');
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Confirm before destructive actions
    $('[data-confirm]').on('click', function(e) {
        if (!confirm($(this).data('confirm'))) {
            e.preventDefault();
        }
    });
    
    // Show loading spinner on form submit
    $('form').on('submit', function() {
        $(this).find('button[type="submit"]').prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-2"></span>Processing...');
    });
});

// Theme Management Functions
function changeTheme(themeId) {
    $.ajax({
        url: '/api/themes/apply',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ theme_id: themeId }),
        success: function(response) {
            location.reload();
        },
        error: function(xhr) {
            alert('Failed to change theme');
        }
    });
}

// Widget Management Functions
function toggleWidget(widgetId, enabled) {
    $.ajax({
        url: '/admin/widgets/toggle',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ widget_id: widgetId, enabled: enabled }),
        success: function(response) {
            if (response.success) {
                showNotification('success', response.message);
            } else {
                showNotification('error', response.message);
            }
        },
        error: function(xhr) {
            showNotification('error', 'Failed to toggle widget');
        }
    });
}

// Feature Management Functions
function toggleFeature(featureId, enabled) {
    $.ajax({
        url: '/admin/features/toggle',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ feature_id: featureId, enabled: enabled }),
        success: function(response) {
            if (response.success) {
                showNotification('success', response.message);
            } else {
                showNotification('error', response.message);
            }
        },
        error: function(xhr) {
            showNotification('error', 'Failed to toggle feature');
        }
    });
}

// System Check Functions
function runSystemCheck() {
    $('#systemCheckResults').html('<div class="spinner-border"></div> Running system check...');
    
    $.ajax({
        url: '/admin/troubleshoot/system-check',
        method: 'POST',
        success: function(response) {
            displaySystemCheckResults(response);
        },
        error: function(xhr) {
            $('#systemCheckResults').html('<div class="alert alert-danger">System check failed</div>');
        }
    });
}

function displaySystemCheckResults(results) {
    var html = '<div class="list-group">';
    
    for (var category in results) {
        var check = results[category];
        var statusClass = check.status === 'healthy' ? 'success' : 'danger';
        var icon = check.status === 'healthy' ? 'check-circle' : 'times-circle';
        
        html += `
            <div class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="mb-0">
                        <i class="fas fa-${icon} text-${statusClass}"></i>
                        ${category.replace('_', ' ').toUpperCase()}
                    </h6>
                    <span class="badge bg-${statusClass}">${check.status}</span>
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    $('#systemCheckResults').html(html);
}

// Notification Helper
function showNotification(type, message) {
    var alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    var alert = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('main').prepend(alert);
    
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
}

// Analytics Chart Helpers
function createPieChart(canvasId, data) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function createBarChart(canvasId, data) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createLineChart(canvasId, data) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Export Functions
function exportToCSV(tableId, filename) {
    var csv = [];
    var rows = document.querySelectorAll('#' + tableId + ' tr');
    
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (var j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }
        
        csv.push(row.join(','));
    }
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;
    
    csvFile = new Blob([csv], {type: 'text/csv'});
    downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
}

// Search and Filter Functions
function filterTable(inputId, tableId) {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById(inputId);
    filter = input.value.toUpperCase();
    table = document.getElementById(tableId);
    tr = table.getElementsByTagName('tr');
    
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName('td')[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = '';
            } else {
                tr[i].style.display = 'none';
            }
        }
    }
}
