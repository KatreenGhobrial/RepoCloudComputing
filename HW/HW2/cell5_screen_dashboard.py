# ============================================================
# Cell 5: Screen 4 – Visual Dashboard (דשבורד ויזואלי של מצב הצמח)
# Prerequisites: Run Cell 1 (COMMON_CSS, TOAST_JS) first.
# ============================================================

from IPython.display import HTML, display

display(HTML(COMMON_CSS + """
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
/* ========== DASHBOARD-SPECIFIC STYLES ========== */

/* ---- Welcome header ---- */
#dash .dash-welcome {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
#dash .dash-welcome .datetime {
    font-size: 13px;
    color: #9cb896;
    display: flex;
    align-items: center;
    gap: 8px;
}
#dash .dash-welcome .datetime .status-dot {
    width: 10px; height: 10px;
}

/* ---- Health Gauge (large, SVG-based) ---- */
#dash .health-gauge-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 32px 0 28px;
    animation: fadeIn 0.8s ease forwards;
}
#dash .health-gauge-wrap {
    position: relative;
    width: 220px;
    height: 220px;
}
#dash .health-gauge-wrap svg {
    width: 100%;
    height: 100%;
    transform: rotate(-90deg);
    filter: drop-shadow(0 0 18px rgba(58,125,42,0.25));
}
#dash .health-gauge-wrap .gauge-ring-bg {
    fill: none;
    stroke: rgba(74,124,46,0.10);
    stroke-width: 14;
}
#dash .health-gauge-wrap .gauge-ring-fill {
    fill: none;
    stroke-width: 14;
    stroke-linecap: round;
    transition: stroke-dashoffset 1.8s cubic-bezier(.4,0,.2,1);
}
#dash .health-gauge-center {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}
#dash .health-gauge-center .score-num {
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1;
}
#dash .health-gauge-center .score-label {
    font-size: 14px;
    font-weight: 600;
    margin-top: 4px;
}
#dash .health-gauge-center .score-max {
    font-size: 13px;
    color: #5a7a52;
    margin-top: 2px;
}
#dash .health-updated {
    font-size: 12px;
    color: #5a7a52;
    margin-top: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Pulsing glow keyframe for the gauge */
@keyframes gaugeGlow {
    0%,100% { filter: drop-shadow(0 0 12px rgba(78,158,56,0.20)); }
    50%     { filter: drop-shadow(0 0 28px rgba(78,158,56,0.45)); }
}
#dash .health-gauge-wrap svg.glowing {
    animation: gaugeGlow 2.5s ease-in-out infinite;
}

/* ---- Metric summary cards ---- */
#dash .dash-metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
@media (max-width: 900px) {
    #dash .dash-metrics { grid-template-columns: repeat(2,1fr); }
}
@media (max-width: 500px) {
    #dash .dash-metrics { grid-template-columns: 1fr; }
}
#dash .dash-metric-card {
    background: rgba(26,38,20,0.55);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(74,124,46,0.18);
    border-radius: 14px;
    padding: 20px;
    transition: all 0.3s ease;
    animation: fadeIn 0.6s ease forwards;
    opacity: 0;
}
#dash .dash-metric-card:hover {
    border-color: rgba(74,124,46,0.40);
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.35);
}
#dash .dash-metric-card .dm-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
#dash .dash-metric-card .dm-icon {
    font-size: 22px;
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(58,125,42,0.12);
    border-radius: 10px;
}
#dash .dash-metric-card .dm-value {
    font-size: 28px;
    font-weight: 800;
    color: #e8f0e4;
    margin-bottom: 2px;
}
#dash .dash-metric-card .dm-label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #9cb896;
    font-weight: 500;
}
#dash .dash-metric-card .dm-change {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 8px;
    padding: 3px 8px;
    border-radius: 6px;
}
#dash .dm-change.up   { color:#22c55e; background:rgba(34,197,94,0.10); }
#dash .dm-change.down-warn { color:#f59e0b; background:rgba(245,158,11,0.10); }
#dash .dm-change.down-ok   { color:#ef4444; background:rgba(239,68,68,0.10); }
#dash .dm-change.stable    { color:#9cb896; background:rgba(148,163,184,0.08); }

/* ---- Two-column layout ---- */
#dash .dash-columns {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 20px;
    margin-bottom: 28px;
}
@media (max-width: 820px) {
    #dash .dash-columns { grid-template-columns: 1fr; }
}

/* Chart card */
#dash .chart-card {
    animation: fadeIn 0.7s ease 0.2s forwards;
    opacity: 0;
}
#dash .chart-card canvas {
    max-height: 240px;
}

/* Alerts feed */
#dash .alerts-card {
    animation: fadeIn 0.7s ease 0.35s forwards;
    opacity: 0;
    max-height: 360px;
    overflow-y: auto;
}
#dash .alert-item {
    display: flex;
    gap: 12px;
    padding: 12px 14px;
    border-radius: 10px;
    border-left: 3px solid transparent;
    transition: background 0.2s ease;
    margin-bottom: 6px;
}
#dash .alert-item:hover {
    background: rgba(58,125,42,0.06);
}
#dash .alert-item.alert-warning  { border-left-color: #f59e0b; }
#dash .alert-item.alert-success  { border-left-color: #22c55e; }
#dash .alert-item.alert-info     { border-left-color: #3b82f6; }
#dash .alert-item.alert-danger   { border-left-color: #ef4444; }

#dash .alert-icon {
    font-size: 18px;
    flex-shrink: 0;
    margin-top: 2px;
}
#dash .alert-body {
    flex: 1;
}
#dash .alert-body .alert-type {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 2px;
}
#dash .alert-body .alert-msg {
    font-size: 13px;
    color: #c2eaaf;
    line-height: 1.4;
}
#dash .alert-body .alert-time {
    font-size: 11px;
    color: #5a7a52;
    margin-top: 3px;
}

/* ---- Quick actions ---- */
#dash .quick-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 28px;
    animation: fadeIn 0.7s ease 0.5s forwards;
    opacity: 0;
}
#dash .quick-actions .btn {
    flex: 1 1 140px;
    justify-content: center;
    padding: 14px 20px;
    font-size: 14px;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
}
#dash .quick-actions .btn::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.06), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
#dash .quick-actions .btn:hover::after {
    opacity: 1;
}

/* ---- Care Tips card ---- */
#dash .tips-card {
    animation: fadeIn 0.7s ease 0.6s forwards;
    opacity: 0;
    position: relative;
    overflow: hidden;
}
#dash .tips-card .tip-item {
    position: absolute;
    inset: 0;
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.6s ease;
    pointer-events: none;
}
#dash .tips-card .tip-item.active {
    position: relative;
    opacity: 1;
    pointer-events: auto;
}
#dash .tips-card .tip-num {
    font-size: 11px;
    color: #5a7a52;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
#dash .tips-card .tip-text {
    font-size: 15px;
    color: #c2eaaf;
    line-height: 1.6;
    font-style: italic;
}
#dash .tips-dots {
    display: flex;
    gap: 6px;
    justify-content: center;
    margin-top: 12px;
}
#dash .tips-dots .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: rgba(74,124,46,0.25);
    cursor: pointer;
    transition: all 0.3s ease;
}
#dash .tips-dots .dot.active {
    background: #4e9e38;
    box-shadow: 0 0 8px rgba(78,158,56,0.4);
    width: 20px;
    border-radius: 4px;
}

/* ---- Card section titles ---- */
#dash .card-title {
    font-size: 15px;
    font-weight: 700;
    color: #e8f0e4;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ---- Bottom row layout ---- */
#dash .dash-bottom {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}
@media (max-width: 700px) {
    #dash .dash-bottom { grid-template-columns: 1fr; }
}
</style>

<div class="bg-app" id="dash">

    <!-- ======== WELCOME HEADER ======== -->
    <div class="screen-header">
        <div class="icon">🌱</div>
        <div style="flex:1">
            <h1>My Basil Garden</h1>
            <p class="subtitle" style="margin-bottom:0">Visual Plant Health Dashboard</p>
        </div>
        <div class="dash-welcome">
            <div class="datetime">
                <span class="status-dot online"></span>
                <span id="dashDateTime">Loading…</span>
            </div>
        </div>
    </div>

    <!-- ======== HEALTH GAUGE ======== -->
    <div class="health-gauge-section">
        <div class="health-gauge-wrap">
            <svg viewBox="0 0 220 220" class="glowing">
                <defs>
                    <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%"   stop-color="#ef4444"/>
                        <stop offset="35%"  stop-color="#f59e0b"/>
                        <stop offset="65%"  stop-color="#4e9e38"/>
                        <stop offset="100%" stop-color="#22c55e"/>
                    </linearGradient>
                </defs>
                <circle class="gauge-ring-bg" cx="110" cy="110" r="96"/>
                <circle class="gauge-ring-fill" id="dashGaugeFill"
                        cx="110" cy="110" r="96"
                        stroke="url(#gaugeGrad)"
                        stroke-dasharray="603.19"
                        stroke-dashoffset="603.19"/>
            </svg>
            <div class="health-gauge-center">
                <div class="score-num" id="dashScoreNum">0</div>
                <div class="score-label" id="dashScoreLabel" style="color:#4ade80">Good</div>
                <div class="score-max">/ 100</div>
            </div>
        </div>
        <div class="health-updated">
            🕒 Last updated: <span id="dashLastUpdated">3 minutes ago</span>
        </div>
    </div>

    <!-- ======== 4 METRIC CARDS ======== -->
    <div class="dash-metrics">
        <!-- Temperature -->
        <div class="dash-metric-card" style="animation-delay:0.15s">
            <div class="dm-header">
                <div class="dm-icon">🌡️</div>
                <span class="badge badge-success">Optimal</span>
            </div>
            <div class="dm-value">23.5°C</div>
            <div class="dm-label">Temperature</div>
            <div class="dm-change up">↑ +0.3°C</div>
        </div>
        <!-- Humidity -->
        <div class="dash-metric-card" style="animation-delay:0.25s">
            <div class="dm-header">
                <div class="dm-icon">💧</div>
                <span class="badge badge-success">Good</span>
            </div>
            <div class="dm-value">58%</div>
            <div class="dm-label">Humidity</div>
            <div class="dm-change down-ok">↓ -2%</div>
        </div>
        <!-- Soil Moisture -->
        <div class="dash-metric-card" style="animation-delay:0.35s">
            <div class="dm-header">
                <div class="dm-icon">🪴</div>
                <span class="badge badge-warning">Low</span>
            </div>
            <div class="dm-value">45%</div>
            <div class="dm-label">Soil Moisture</div>
            <div class="dm-change down-warn">↓ -5%</div>
        </div>
        <!-- Light -->
        <div class="dash-metric-card" style="animation-delay:0.45s">
            <div class="dm-header">
                <div class="dm-icon">☀️</div>
                <span class="badge badge-success">Optimal</span>
            </div>
            <div class="dm-value">650 lux</div>
            <div class="dm-label">Light Intensity</div>
            <div class="dm-change stable">→ Stable</div>
        </div>
    </div>

    <!-- ======== TWO-COLUMN: CHART + ALERTS ======== -->
    <div class="dash-columns">
        <!-- Left: Trend Chart -->
        <div class="glass-card chart-card">
            <div class="card-title">📈 Health Score – Last 7 Days</div>
            <canvas id="dashTrendChart"></canvas>
        </div>

        <!-- Right: Alerts Feed -->
        <div class="glass-card alerts-card">
            <div class="card-title">🔔 Recent Alerts</div>

            <div class="alert-item alert-warning">
                <span class="alert-icon">⚠️</span>
                <div class="alert-body">
                    <div class="alert-type" style="color:#fbbf24">Warning</div>
                    <div class="alert-msg">Soil moisture dropping below optimal level</div>
                    <div class="alert-time">15 minutes ago</div>
                </div>
            </div>

            <div class="alert-item alert-success">
                <span class="alert-icon">✅</span>
                <div class="alert-body">
                    <div class="alert-type" style="color:#4ade80">Resolved</div>
                    <div class="alert-msg">Temperature returned to normal range</div>
                    <div class="alert-time">1 hour ago</div>
                </div>
            </div>

            <div class="alert-item alert-info">
                <span class="alert-icon">💧</span>
                <div class="alert-body">
                    <div class="alert-type" style="color:#93c5fd">Info</div>
                    <div class="alert-msg">Watering schedule reminder for tomorrow</div>
                    <div class="alert-time">2 hours ago</div>
                </div>
            </div>

            <div class="alert-item alert-danger">
                <span class="alert-icon">🔴</span>
                <div class="alert-body">
                    <div class="alert-type" style="color:#fca5a5">Critical</div>
                    <div class="alert-msg">Light sensor detected unusual darkness</div>
                    <div class="alert-time">5 hours ago</div>
                </div>
            </div>

            <div class="alert-item alert-success">
                <span class="alert-icon">✅</span>
                <div class="alert-body">
                    <div class="alert-type" style="color:#4ade80">Resolved</div>
                    <div class="alert-msg">Humidity level stabilized</div>
                    <div class="alert-time">1 day ago</div>
                </div>
            </div>
        </div>
    </div>

    <!-- ======== BOTTOM: QUICK ACTIONS + CARE TIPS ======== -->
    <div class="dash-bottom">
        <!-- Quick Actions -->
        <div class="glass-card" style="animation: fadeIn 0.7s ease 0.5s forwards; opacity:0;">
            <div class="card-title">⚡ Quick Actions</div>
            <div class="quick-actions" style="animation:none; opacity:1;">
                <button class="btn btn-primary" onclick="dashAction('water')">
                    💧 Water Now
                </button>
                <button class="btn btn-secondary" onclick="dashAction('alert')">
                    🔔 Set Alert
                </button>
                <button class="btn btn-secondary" onclick="dashAction('report')">
                    📊 View Report
                </button>
                <button class="btn btn-accent" onclick="dashAction('photo')">
                    📷 Take Photo
                </button>
            </div>
        </div>

        <!-- Care Tips -->
        <div class="glass-card tips-card" id="dashTipsCard">
            <div class="card-title">🌿 Basil Care Tips</div>
            <div style="position:relative; min-height: 80px;">
                <div class="tip-item active" data-tip-idx="0">
                    <div class="tip-num">Tip 1 of 3</div>
                    <div class="tip-text">"Water basil when the top inch of soil feels dry."</div>
                </div>
                <div class="tip-item" data-tip-idx="1">
                    <div class="tip-num">Tip 2 of 3</div>
                    <div class="tip-text">"Basil thrives in 6-8 hours of direct sunlight."</div>
                </div>
                <div class="tip-item" data-tip-idx="2">
                    <div class="tip-num">Tip 3 of 3</div>
                    <div class="tip-text">"Pinch off flower buds to encourage leaf growth."</div>
                </div>
            </div>
            <div class="tips-dots">
                <div class="dot active" data-dot="0"></div>
                <div class="dot" data-dot="1"></div>
                <div class="dot" data-dot="2"></div>
            </div>
        </div>
    </div>

</div>

<script>
(function() {
    /* ---------- Date/Time ---------- */
    function updateDateTime() {
        const now = new Date();
        const opts = { weekday:'long', year:'numeric', month:'long', day:'numeric',
                       hour:'2-digit', minute:'2-digit' };
        const el = document.getElementById('dashDateTime');
        if (el) el.textContent = now.toLocaleDateString('en-US', opts);
    }
    updateDateTime();
    setInterval(updateDateTime, 30000);

    /* ---------- Health Gauge count-up animation ---------- */
    const TARGET_SCORE = 78;
    const circumference = 2 * Math.PI * 96; // ≈ 603.19
    const gaugeFill = document.getElementById('dashGaugeFill');
    const scoreNum  = document.getElementById('dashScoreNum');

    // Animate score number counting up
    let currentScore = 0;
    const duration = 1800; // ms
    const startTime = performance.now();

    function animateScore(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        currentScore = Math.round(eased * TARGET_SCORE);
        scoreNum.textContent = currentScore;

        // Gauge arc
        const offset = circumference - (eased * TARGET_SCORE / 100) * circumference;
        gaugeFill.style.strokeDashoffset = offset;

        if (progress < 1) requestAnimationFrame(animateScore);
    }
    // Small delay so user sees the animation start
    setTimeout(() => requestAnimationFrame(animateScore), 400);

    /* ---------- Chart.js – 7-day trend ---------- */
    function initDashChart() {
        const ctx = document.getElementById('dashTrendChart');
        if (!ctx) return;

        const labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
        const data   = [72, 75, 78, 74, 76, 80, 78];

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Health Score',
                    data: data,
                    borderColor: '#4e9e38',
                    backgroundColor: function(context) {
                        const chart = context.chart;
                        const {ctx: c, chartArea} = chart;
                        if (!chartArea) return 'rgba(78,158,56,0.15)';
                        const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                        gradient.addColorStop(0, 'rgba(78,158,56,0.35)');
                        gradient.addColorStop(1, 'rgba(78,158,56,0.02)');
                        return gradient;
                    },
                    borderWidth: 3,
                    pointBackgroundColor: '#4e9e38',
                    pointBorderColor: '#1a2614',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointHoverBackgroundColor: '#6bbf4e',
                    pointHoverBorderColor: '#e8f0e4',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { intersect: false, mode: 'index' },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(26,38,20,0.95)',
                        borderColor: 'rgba(74,124,46,0.3)',
                        borderWidth: 1,
                        titleColor: '#e8f0e4',
                        bodyColor: '#c2eaaf',
                        padding: 12,
                        cornerRadius: 10,
                        titleFont: { family: 'Inter', weight: '600' },
                        bodyFont: { family: 'Inter' },
                        callbacks: {
                            label: function(ctx) { return 'Score: ' + ctx.parsed.y + '/100'; }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(74,124,46,0.08)', drawBorder: false },
                        ticks: { color: '#5a7a52', font: { family: 'Inter', size: 12 } },
                        border: { display: false }
                    },
                    y: {
                        min: 50, max: 100,
                        grid: { color: 'rgba(74,124,46,0.08)', drawBorder: false },
                        ticks: {
                            color: '#5a7a52',
                            font: { family: 'Inter', size: 12 },
                            stepSize: 10,
                            callback: function(v) { return v; }
                        },
                        border: { display: false }
                    }
                },
                layout: { padding: { top: 4, bottom: 4 } }
            }
        });
    }

    // Wait for Chart.js to load then render
    function waitForChart() {
        if (typeof Chart !== 'undefined') {
            initDashChart();
        } else {
            setTimeout(waitForChart, 150);
        }
    }
    waitForChart();

    /* ---------- Rotating tips ---------- */
    let tipIdx = 0;
    const tips = document.querySelectorAll('#dashTipsCard .tip-item');
    const dots = document.querySelectorAll('#dashTipsCard .dot');

    function showTip(idx) {
        tips.forEach(t => t.classList.remove('active'));
        dots.forEach(d => d.classList.remove('active'));
        tips[idx].classList.add('active');
        dots[idx].classList.add('active');
        tipIdx = idx;
    }

    // Auto-rotate every 5 seconds
    setInterval(() => {
        showTip((tipIdx + 1) % tips.length);
    }, 5000);

    // Click on dots
    dots.forEach(d => {
        d.addEventListener('click', () => showTip(parseInt(d.dataset.dot)));
    });

    /* ---------- Quick action handler ---------- */
    window.dashAction = function(action) {
        const msgs = {
            water:  { text: 'Watering cycle initiated! 💧',         type: 'success' },
            alert:  { text: 'Alert configuration opened.',          type: 'info'    },
            report: { text: 'Generating weekly health report…',     type: 'info'    },
            photo:  { text: 'Camera module activated! 📷',           type: 'success' }
        };
        const m = msgs[action] || { text: 'Action triggered.', type: 'info' };

        /* --- inline toast (no dependency on TOAST_JS runtime) --- */
        let container = document.getElementById('dashToastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'dashToastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        toast.className = 'toast ' + m.type;
        const icons = { success:'✅', warning:'⚠️', error:'❌', info:'ℹ️' };
        toast.innerHTML = (icons[m.type]||'ℹ️') + ' ' + m.text;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(40px)';
            setTimeout(() => toast.remove(), 400);
        }, 3500);
    };
})();
</script>
"""))
