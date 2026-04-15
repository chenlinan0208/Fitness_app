document.addEventListener('DOMContentLoaded', function () {
    setTimeout(() => {
        renderWorkoutsChart();
        renderCategoryChart();
    }, 200);
});

function getWeekRange(weekNo) {
    const year = 2026;
    try {
        const d = new Date(year, 0, 1 + (weekNo * 7));
        const day = d.getDay();
        const diff = d.getDate() - day + (day === 0 ? -6 : 1);
        const monday = new Date(d.setDate(diff));
        const sunday = new Date(monday);
        sunday.setDate(monday.getDate() + 6);
        return `${monday.toLocaleDateString('en-US', {month:'short', day:'numeric'})}`;
    } catch (e) { return "Week " + weekNo; }
}

function renderWorkoutsChart() {
    const canvas = document.getElementById('workoutsChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Create a beautiful gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(78, 115, 223, 0.2)');
    gradient.addColorStop(1, 'rgba(78, 115, 223, 0)');

    const rawWeeks = JSON.parse(canvas.getAttribute('data-weeks') || "[]");
    const rawCounts = JSON.parse(canvas.getAttribute('data-counts') || "[]");

    let combined = rawWeeks.map((w, i) => ({ week: parseInt(w), count: rawCounts[i] }));
    combined.sort((a, b) => a.week - b.week);

    new Chart(canvas, {
        type: 'line',
        data: {
            labels: combined.map(item => getWeekRange(item.week)),
            datasets: [{
                data: combined.map(item => item.count),
                borderColor: '#4e73df',
                borderWidth: 3,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointRadius: 0, // Hidden until hover
                pointHitRadius: 20,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#4e73df',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1a202c',
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: (ctx) => `🔥 ${ctx.raw} Workouts`
                    }
                }
            },
            scales: {
                y: { 
                    beginAtZero: true, 
                    border: { display: false },
                    grid: { color: '#f1f3f9' },
                    ticks: { color: '#a0aec0', font: { size: 11 } }
                },
                x: { 
                    border: { display: false },
                    grid: { display: false },
                    ticks: { color: '#a0aec0', font: { size: 11 } }
                }
            }
        }
    });
}

function renderCategoryChart() {
    const canvas = document.getElementById('categoryChart');
    if (!canvas) return;

    const labels = JSON.parse(canvas.getAttribute('data-labels') || "[]");
    const data = JSON.parse(canvas.getAttribute('data-counts') || "[]");

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '80%',
            plugins: {
                legend: { 
                    position: 'bottom', 
                    labels: { usePointStyle: true, padding: 20, font: { size: 10, weight: 'bold' } } 
                }
            }
        }
    });
}