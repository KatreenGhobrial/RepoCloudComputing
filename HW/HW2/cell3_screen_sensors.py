from IPython.display import HTML, display

# Ensure you have run cell1_common_styles.py first to load COMMON_CSS and TOAST_JS

HTML_CONTENT = COMMON_CSS + TOAST_JS + """
<style>
/* ========== SENSOR GAUGES ========== */
.sensor-gauge-wrapper {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto 16px;
}
.sensor-gauge {
    transform: rotate(-90deg);
    width: 100%;
    height: 100%;
}
.sensor-gauge-bg {
    fill: none;
    stroke: rgba(74,124,46,0.15);
    stroke-width: 10;
}
.sensor-gauge-fill {
    fill: none;
    stroke-width: 10;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.5s ease-out, stroke 0.5s ease;
}
.sensor-gauge-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    width: 100%;
}
.sensor-gauge-text {
    font-size: 20px;
    font-weight: 800;
    color: #e8f0e4;
    line-height: 1;
}
.sensor-gauge-unit {
    font-size: 11px;
    color: #9cb896;
    margin-top: 2px;
}

/* Gauge Gradients */
.gauge-temp { stroke: url(#grad-temp); }
.gauge-humid { stroke: url(#grad-humid); }
.gauge-soil { stroke: url(#grad-soil); }
.gauge-light { stroke: url(#grad-light); }

/* ========== CONTROLS BAR ========== */
.controls-bar {
    background: rgba(26, 38, 20, 0.4);
    border: 1px solid rgba(74,124,46,0.2);
    border-radius: 12px;
    padding: 16px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

/* ========== STATUS INDICATOR ========== */
.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 600;
}
.status-indicator.active .dot { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
.status-indicator.inactive .dot { background: #ef4444; box-shadow: 0 0 8px #ef4444; }

/* ========== CHART CONTAINER ========== */
.chart-container {
    height: 300px;
    width: 100%;
    position: relative;
}

/* ========== SETTINGS PANEL ========== */
.settings-panel {
    background: rgba(15, 26, 10, 0.6);
    border-radius: 12px;
    padding: 20px;
    margin-top: 24px;
    display: none;
    border: 1px solid rgba(74,124,46,0.2);
}
.settings-panel.active { display: block; animation: fadeIn 0.3s ease; }
.threshold-group {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}
.threshold-group label { width: 120px; font-size: 13px; color: #c2eaaf; }
.threshold-input {
    width: 80px;
    background: #0a1205;
    border: 1px solid rgba(74,124,46,0.3);
    color: #e8f0e4;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 13px;
}

/* ========== DATA TABLE ========== */
.table-container {
    max-height: 400px;
    overflow-y: auto;
    border-radius: 12px;
    border: 1px solid rgba(74,124,46,0.15);
    background: rgba(26, 38, 20, 0.3);
}

/* Custom Scrollbar for table */
.table-container::-webkit-scrollbar { width: 6px; }
.table-container::-webkit-scrollbar-track { background: rgba(15,26,10,0.5); }
.table-container::-webkit-scrollbar-thumb { background: rgba(74,124,46,0.4); border-radius: 3px; }

tr.new-row { animation: fadeIn 0.5s ease; background: rgba(58,125,42,0.1); }
</style>

<div class="bg-app" id="sensorsScreen">
    
    <!-- SVG Defs for Gradients -->
    <svg style="width:0;height:0;position:absolute;" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="grad-temp" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#f59e0b" />
          <stop offset="100%" stop-color="#ef4444" />
        </linearGradient>
        <linearGradient id="grad-humid" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#3b82f6" />
          <stop offset="100%" stop-color="#0ea5e9" />
        </linearGradient>
        <linearGradient id="grad-soil" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#22c55e" />
          <stop offset="100%" stop-color="#10b981" />
        </linearGradient>
        <linearGradient id="grad-light" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#eab308" />
          <stop offset="100%" stop-color="#f59e0b" />
        </linearGradient>
      </defs>
    </svg>

    <div class="screen-header">
        <div class="icon">📡</div>
        <div>
            <h1>IoT Sensor Data</h1>
            <div class="subtitle">Real-time telemetry for Basil plant monitoring</div>
        </div>
    </div>

    <!-- SENSOR CARDS -->
    <div class="metrics-grid" style="grid-template-columns: repeat(4, 1fr);">
        <!-- Temp -->
        <div class="metric-card" style="text-align: center;">
            <div class="sensor-gauge-wrapper">
                <svg class="sensor-gauge" viewBox="0 0 100 100">
                    <circle class="sensor-gauge-bg" cx="50" cy="50" r="40"></circle>
                    <circle class="sensor-gauge-fill gauge-temp" cx="50" cy="50" r="40" stroke-dasharray="251.2" stroke-dashoffset="251.2" id="gauge-temp"></circle>
                </svg>
                <div class="sensor-gauge-value">
                    <div class="sensor-gauge-text" id="val-temp">--</div>
                    <div class="sensor-gauge-unit">°C</div>
                </div>
            </div>
            <div class="metric-label">Temperature</div>
            <div class="flex-center mt-2" style="justify-content: center; gap: 8px; margin-top: 8px;">
                <span class="badge badge-success" id="badge-temp">Optimal</span>
                <span id="trend-temp" class="metric-change"></span>
            </div>
        </div>
        
        <!-- Humidity -->
        <div class="metric-card" style="text-align: center;">
            <div class="sensor-gauge-wrapper">
                <svg class="sensor-gauge" viewBox="0 0 100 100">
                    <circle class="sensor-gauge-bg" cx="50" cy="50" r="40"></circle>
                    <circle class="sensor-gauge-fill gauge-humid" cx="50" cy="50" r="40" stroke-dasharray="251.2" stroke-dashoffset="251.2" id="gauge-humid"></circle>
                </svg>
                <div class="sensor-gauge-value">
                    <div class="sensor-gauge-text" id="val-humid">--</div>
                    <div class="sensor-gauge-unit">%</div>
                </div>
            </div>
            <div class="metric-label">Air Humidity</div>
            <div class="flex-center mt-2" style="justify-content: center; gap: 8px; margin-top: 8px;">
                <span class="badge badge-success" id="badge-humid">Optimal</span>
                <span id="trend-humid" class="metric-change"></span>
            </div>
        </div>

        <!-- Soil -->
        <div class="metric-card" style="text-align: center;">
            <div class="sensor-gauge-wrapper">
                <svg class="sensor-gauge" viewBox="0 0 100 100">
                    <circle class="sensor-gauge-bg" cx="50" cy="50" r="40"></circle>
                    <circle class="sensor-gauge-fill gauge-soil" cx="50" cy="50" r="40" stroke-dasharray="251.2" stroke-dashoffset="251.2" id="gauge-soil"></circle>
                </svg>
                <div class="sensor-gauge-value">
                    <div class="sensor-gauge-text" id="val-soil">--</div>
                    <div class="sensor-gauge-unit">%</div>
                </div>
            </div>
            <div class="metric-label">Soil Moisture</div>
            <div class="flex-center mt-2" style="justify-content: center; gap: 8px; margin-top: 8px;">
                <span class="badge badge-warning" id="badge-soil">Low</span>
                <span id="trend-soil" class="metric-change"></span>
            </div>
        </div>

        <!-- Light -->
        <div class="metric-card" style="text-align: center;">
            <div class="sensor-gauge-wrapper">
                <svg class="sensor-gauge" viewBox="0 0 100 100">
                    <circle class="sensor-gauge-bg" cx="50" cy="50" r="40"></circle>
                    <circle class="sensor-gauge-fill gauge-light" cx="50" cy="50" r="40" stroke-dasharray="251.2" stroke-dashoffset="251.2" id="gauge-light"></circle>
                </svg>
                <div class="sensor-gauge-value">
                    <div class="sensor-gauge-text" id="val-light">--</div>
                    <div class="sensor-gauge-unit">lux</div>
                </div>
            </div>
            <div class="metric-label">Light Intensity</div>
            <div class="flex-center mt-2" style="justify-content: center; gap: 8px; margin-top: 8px;">
                <span class="badge badge-success" id="badge-light">Optimal</span>
                <span id="trend-light" class="metric-change"></span>
            </div>
        </div>
    </div>

    <!-- CONTROLS -->
    <div class="controls-bar">
        <div class="flex-row">
            <button id="btn-toggle-sampling" class="btn btn-primary" onclick="window.sensors.toggleSampling()">
                ▶ Start Sampling
            </button>
            <select id="select-interval" class="select-field" onchange="window.sensors.changeInterval()">
                <option value="1000">1s Interval</option>
                <option value="2000" selected>2s Interval</option>
                <option value="5000">5s Interval</option>
            </select>
            <button class="btn btn-secondary" onclick="window.sensors.resetData()">↺ Reset</button>
        </div>
        
        <div class="flex-row">
            <div class="status-indicator inactive" id="connection-status">
                <span class="status-dot dot"></span>
                <span id="connection-text">Disconnected</span>
            </div>
            <div class="divider" style="width:1px; height:24px; margin:0 12px; transform:none;"></div>
            <button class="btn btn-secondary btn-sm" onclick="window.sensors.toggleSettings()">⚙️ Thresholds</button>
            <button class="btn btn-secondary btn-sm" onclick="window.sensors.exportCSV()">📥 Export CSV</button>
        </div>
    </div>

    <!-- SETTINGS PANEL -->
    <div id="settings-panel" class="settings-panel">
        <h3 class="mb-md">Alert Thresholds</h3>
        <div class="grid-2">
            <div>
                <div class="threshold-group">
                    <label>Temperature (°C)</label>
                    <input type="number" id="th-temp-min" class="threshold-input" value="18"> <span style="color:#5a7a52">to</span> 
                    <input type="number" id="th-temp-max" class="threshold-input" value="30">
                </div>
                <div class="threshold-group">
                    <label>Humidity (%)</label>
                    <input type="number" id="th-humid-min" class="threshold-input" value="40"> <span style="color:#5a7a52">to</span> 
                    <input type="number" id="th-humid-max" class="threshold-input" value="80">
                </div>
            </div>
            <div>
                <div class="threshold-group">
                    <label>Soil Moisture (%)</label>
                    <input type="number" id="th-soil-min" class="threshold-input" value="40"> <span style="color:#5a7a52">to</span> 
                    <input type="number" id="th-soil-max" class="threshold-input" value="100">
                </div>
                <div class="threshold-group">
                    <label>Light (lux)</label>
                    <input type="number" id="th-light-min" class="threshold-input" value="300"> <span style="color:#5a7a52">to</span> 
                    <input type="number" id="th-light-max" class="threshold-input" value="1200">
                </div>
            </div>
        </div>
        <div class="mt-2" style="text-align: right; margin-top:16px;">
            <button class="btn btn-primary btn-sm" onclick="window.sensors.saveSettings()">Save Changes</button>
        </div>
    </div>

    <div class="grid-2" style="margin-top: 24px; grid-template-columns: 1fr 1fr;">
        <!-- CHART -->
        <div class="glass-card">
            <h3 class="mb-md">Live Telemetry</h3>
            <div class="chart-container">
                <canvas id="sensorsChart"></canvas>
            </div>
        </div>

        <!-- TABLE -->
        <div class="glass-card">
            <h3 class="mb-md">Recent Readings</h3>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Temp</th>
                            <th>Humid</th>
                            <th>Soil</th>
                            <th>Light</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="readings-tbody">
                        <!-- Data rows here -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<script>
(function() {
    // Make sure Chart.js is loaded
    function init() {
        if (typeof Chart === 'undefined') {
            setTimeout(init, 100);
            return;
        }
        setupApp();
    }

    const app = {
        isSampling: false,
        intervalId: null,
        intervalMs: 2000,
        maxDataPoints: 20,
        data: {
            labels: [],
            temp: [],
            humid: [],
            soil: [],
            light: []
        },
        readingsCount: 0,
        chart: null,
        
        // Base values for simulation
        sim: {
            temp: 23.0,
            humid: 55.0,
            soil: 45.0,
            light: 600.0,
            time: 0
        },

        thresholds: {
            temp: { min: 18, max: 30 },
            humid: { min: 40, max: 80 },
            soil: { min: 40, max: 100 },
            light: { min: 300, max: 1200 }
        }
    };

    function setupApp() {
        initChart();
        updateGauges(app.sim.temp, app.sim.humid, app.sim.soil, app.sim.light);
        
        // Initial empty row
        const tbody = document.getElementById('readings-tbody');
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 24px; color: #5a7a52;">No data yet. Start sampling.</td></tr>';

        // Expose API
        window.sensors = {
            toggleSampling: toggleSampling,
            changeInterval: changeInterval,
            resetData: resetData,
            toggleSettings: toggleSettings,
            saveSettings: saveSettings,
            exportCSV: exportCSV
        };
    }

    function initChart() {
        const ctx = document.getElementById('sensorsChart').getContext('2d');
        
        Chart.defaults.color = '#9cb896';
        Chart.defaults.font.family = "'Inter', sans-serif";

        app.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: app.data.labels,
                datasets: [
                    {
                        label: 'Temp (°C)',
                        data: app.data.temp,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Humid (%)',
                        data: app.data.humid,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Soil (%)',
                        data: app.data.soil,
                        borderColor: '#22c55e',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Light (lux/10)',
                        data: app.data.light,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        yAxisID: 'y1',
                        hidden: true // Hidden by default to reduce clutter
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, boxWidth: 8 } },
                    tooltip: {
                        backgroundColor: 'rgba(26,38,20,0.9)',
                        titleColor: '#e8f0e4',
                        bodyColor: '#c2eaaf',
                        borderColor: 'rgba(74,124,46,0.3)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(74,124,46,0.1)' }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        grid: { color: 'rgba(74,124,46,0.1)' },
                        min: 0,
                        max: 100
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        min: 0,
                        max: 150
                    }
                }
            }
        });
    }

    function toggleSampling() {
        const btn = document.getElementById('btn-toggle-sampling');
        const status = document.getElementById('connection-status');
        const statusText = document.getElementById('connection-text');

        if (app.isSampling) {
            // Stop
            clearInterval(app.intervalId);
            app.isSampling = false;
            btn.innerHTML = '▶ Start Sampling';
            btn.className = 'btn btn-primary';
            status.className = 'status-indicator inactive';
            statusText.textContent = 'Disconnected';
            if (typeof showToast === 'function') showToast('Sampling paused', 'info');
        } else {
            // Start
            app.isSampling = true;
            generateReading(); // immediate
            app.intervalId = setInterval(generateReading, app.intervalMs);
            btn.innerHTML = '⏸ Stop Sampling';
            btn.className = 'btn btn-danger';
            status.className = 'status-indicator active';
            statusText.textContent = 'Connected (Live)';
            
            // clear empty message if needed
            const tbody = document.getElementById('readings-tbody');
            if (app.readingsCount === 0) tbody.innerHTML = '';
            
            if (typeof showToast === 'function') showToast('Sampling started', 'success');
        }
    }

    function changeInterval() {
        const select = document.getElementById('select-interval');
        app.intervalMs = parseInt(select.value);
        if (app.isSampling) {
            clearInterval(app.intervalId);
            app.intervalId = setInterval(generateReading, app.intervalMs);
        }
    }

    function generateReading() {
        app.sim.time += app.intervalMs / 1000;
        
        // Random walk simulation
        app.sim.temp = Math.max(15, Math.min(35, app.sim.temp + (Math.random() - 0.5) * 1.5));
        app.sim.humid = Math.max(20, Math.min(90, app.sim.humid + (Math.random() - 0.5) * 3.0));
        app.sim.soil = Math.max(10, Math.min(90, app.sim.soil - 0.1 + (Math.random() * 0.1))); // Slow drain
        
        // Sine wave for light (day/night) + noise
        const lightBase = 600 + Math.sin(app.sim.time * 0.1) * 400;
        app.sim.light = Math.max(0, lightBase + (Math.random() - 0.5) * 50);

        const rTemp = parseFloat(app.sim.temp.toFixed(1));
        const rHumid = Math.round(app.sim.humid);
        const rSoil = Math.round(app.sim.soil);
        const rLight = Math.round(app.sim.light);
        
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], {hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit'});

        // Update arrays
        app.data.labels.push(timeStr);
        app.data.temp.push(rTemp);
        app.data.humid.push(rHumid);
        app.data.soil.push(rSoil);
        app.data.light.push(rLight / 10); // Scale down for chart

        if (app.data.labels.length > app.maxDataPoints) {
            app.data.labels.shift();
            app.data.temp.shift();
            app.data.humid.shift();
            app.data.soil.shift();
            app.data.light.shift();
        }

        app.chart.update();
        app.readingsCount++;

        updateGauges(rTemp, rHumid, rSoil, rLight);
        addTableRow(timeStr, rTemp, rHumid, rSoil, rLight);
        checkAlerts(rTemp, rHumid, rSoil, rLight);
    }

    function updateGauges(t, h, s, l) {
        // Temp (15-35)
        const tPct = Math.max(0, Math.min(100, ((t - 15) / 20) * 100));
        setGauge('temp', tPct, t);
        updateStatusBadge('temp', t, app.thresholds.temp.min, app.thresholds.temp.max, tPct > 50 ? '↑' : '↓');

        // Humid (20-90)
        const hPct = Math.max(0, Math.min(100, ((h - 20) / 70) * 100));
        setGauge('humid', hPct, h);
        updateStatusBadge('humid', h, app.thresholds.humid.min, app.thresholds.humid.max, hPct > 50 ? '↑' : '↓');

        // Soil (10-90)
        const sPct = Math.max(0, Math.min(100, ((s - 10) / 80) * 100));
        setGauge('soil', sPct, s);
        updateStatusBadge('soil', s, app.thresholds.soil.min, app.thresholds.soil.max, '↓');

        // Light (0-1500)
        const lPct = Math.max(0, Math.min(100, (l / 1500) * 100));
        setGauge('light', lPct, l);
        updateStatusBadge('light', l, app.thresholds.light.min, app.thresholds.light.max, '≈');
    }

    function setGauge(id, pct, val) {
        const circle = document.getElementById('gauge-' + id);
        const text = document.getElementById('val-' + id);
        if (circle && text) {
            const circumference = 2 * Math.PI * 40; // 251.2
            const offset = circumference - (pct / 100) * circumference;
            circle.style.strokeDashoffset = offset;
            text.textContent = val;
        }
    }

    function updateStatusBadge(id, val, min, max, trend) {
        const badge = document.getElementById('badge-' + id);
        const trendEl = document.getElementById('trend-' + id);
        if (!badge || !trendEl) return;

        if (val < min) {
            badge.className = 'badge badge-warning';
            badge.textContent = 'Low';
        } else if (val > max) {
            badge.className = 'badge badge-danger';
            badge.textContent = 'High';
        } else {
            badge.className = 'badge badge-success';
            badge.textContent = 'Optimal';
        }
        
        trendEl.textContent = trend;
        if (trend === '↑') trendEl.className = 'metric-change up';
        else if (trend === '↓') trendEl.className = 'metric-change down';
        else trendEl.className = 'metric-change neutral';
    }

    function checkAlerts(t, h, s, l) {
        let alerts = [];
        if (t > app.thresholds.temp.max) alerts.push('High Temp');
        if (t < app.thresholds.temp.min) alerts.push('Low Temp');
        if (s < app.thresholds.soil.min) alerts.push('Low Soil Moisture');
        
        if (alerts.length > 0 && Math.random() > 0.8) { // Only occasionally show toast to avoid spam
            if (typeof showToast === 'function') {
                showToast('Alert: ' + alerts.join(', '), 'warning');
            }
        }
    }

    function addTableRow(time, t, h, s, l) {
        const tbody = document.getElementById('readings-tbody');
        
        let statusHtml = '<span class="badge badge-success">Normal</span>';
        if (t > app.thresholds.temp.max || s < app.thresholds.soil.min) {
            statusHtml = '<span class="badge badge-warning">Warning</span>';
        }

        const tr = document.createElement('tr');
        tr.className = 'new-row';
        tr.innerHTML = `
            <td>${time}</td>
            <td><strong style="color:#e8f0e4">${t}</strong> °C</td>
            <td><strong style="color:#e8f0e4">${h}</strong> %</td>
            <td><strong style="color:#e8f0e4">${s}</strong> %</td>
            <td><strong style="color:#e8f0e4">${l}</strong> lux</td>
            <td>${statusHtml}</td>
        `;
        
        tbody.insertBefore(tr, tbody.firstChild);
        
        // Remove animation class after it plays
        setTimeout(() => tr.classList.remove('new-row'), 600);

        // Keep table small
        while (tbody.children.length > 15) {
            tbody.removeChild(tbody.lastChild);
        }
    }

    function resetData() {
        app.data.labels = [];
        app.data.temp = [];
        app.data.humid = [];
        app.data.soil = [];
        app.data.light = [];
        app.chart.update();
        app.readingsCount = 0;
        
        const tbody = document.getElementById('readings-tbody');
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 24px; color: #5a7a52;">Data reset. Start sampling.</td></tr>';
        
        if (app.isSampling) toggleSampling();
        
        setGauge('temp', 0, '--');
        setGauge('humid', 0, '--');
        setGauge('soil', 0, '--');
        setGauge('light', 0, '--');
        
        if (typeof showToast === 'function') showToast('Telemetry data reset', 'info');
    }

    function toggleSettings() {
        const panel = document.getElementById('settings-panel');
        if (panel.classList.contains('active')) {
            panel.classList.remove('active');
        } else {
            panel.classList.add('active');
        }
    }

    function saveSettings() {
        app.thresholds.temp.min = parseFloat(document.getElementById('th-temp-min').value);
        app.thresholds.temp.max = parseFloat(document.getElementById('th-temp-max').value);
        app.thresholds.humid.min = parseFloat(document.getElementById('th-humid-min').value);
        app.thresholds.humid.max = parseFloat(document.getElementById('th-humid-max').value);
        app.thresholds.soil.min = parseFloat(document.getElementById('th-soil-min').value);
        app.thresholds.soil.max = parseFloat(document.getElementById('th-soil-max').value);
        app.thresholds.light.min = parseFloat(document.getElementById('th-light-min').value);
        app.thresholds.light.max = parseFloat(document.getElementById('th-light-max').value);
        
        toggleSettings();
        if (typeof showToast === 'function') showToast('Thresholds updated successfully', 'success');
    }

    function exportCSV() {
        if (app.readingsCount === 0) {
            if (typeof showToast === 'function') showToast('No data to export', 'error');
            return;
        }
        
        let csv = 'Timestamp,Temperature(C),Humidity(%),SoilMoisture(%),Light(lux)\\n';
        for (let i = 0; i < app.data.labels.length; i++) {
            csv += `${app.data.labels[i]},${app.data.temp[i]},${app.data.humid[i]},${app.data.soil[i]},${app.data.light[i] * 10}\\n`;
        }
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.setAttribute('hidden', '');
        a.setAttribute('href', url);
        a.setAttribute('download', 'basil_telemetry_data.csv');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        if (typeof showToast === 'function') showToast('CSV Export generated', 'success');
    }

    // Start
    init();

})();
</script>
"""

display(HTML(HTML_CONTENT))
print("✅ IoT Sensor Data Screen loaded successfully!")
