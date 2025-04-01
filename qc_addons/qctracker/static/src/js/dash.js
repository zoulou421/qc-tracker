// dashboard.js

document.addEventListener("DOMContentLoaded", function () {
    // Example of initializing a chart with Chart.js for tasks distribution

    const ctx = document.getElementById('tasksChart').getContext('2d');
    const tasksChart = new Chart(ctx, {
        type: 'pie', // Pie chart for tasks distribution
        data: {
            labels: ['Completed', 'Ongoing', 'Pending'],
            datasets: [{
                label: 'Task Distribution',
                data: [40, 30, 30], // Sample data; replace with dynamic data
                backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
                borderColor: '#fff',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw + '%';
                        }
                    }
                }
            }
        }
    });

    // Example of handling hover animation for the cards
    const cards = document.querySelectorAll('.o_dashboard_card');
    cards.forEach(card => {
        card.addEventListener('mouseover', function () {
            card.classList.add('animated', 'fadeInUp');
        });
        card.addEventListener('mouseout', function () {
            card.classList.remove('animated', 'fadeInUp');
        });
    });
});


