# ============================================================
# Cell 1: Common Styles & Utilities
# Run this cell FIRST before running any screen cells.
# ============================================================

COMMON_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ========== RESET & BASE ========== */
.bg-app * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
.bg-app {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(145deg, #0a0f07 0%, #0d1a08 50%, #0a1205 100%);
    color: #e8f0e4;
    min-height: 600px;
    border-radius: 16px;
    padding: 32px;
    position: relative;
    overflow: hidden;
}
.bg-app::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 20%, rgba(58,125,42,0.06) 0%, transparent 50%),
                radial-gradient(circle at 70% 80%, rgba(245,158,11,0.03) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}
.bg-app > * {
    position: relative;
    z-index: 1;
}

/* ========== TYPOGRAPHY ========== */
.bg-app h1 {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #6bbf4e 0%, #3a7d2a 50%, #f59e0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
}
.bg-app h2 {
    font-size: 20px;
    font-weight: 700;
    color: #e8f0e4;
    margin-bottom: 6px;
}
.bg-app h3 {
    font-size: 16px;
    font-weight: 600;
    color: #c2eaaf;
    margin-bottom: 4px;
}
.bg-app p, .bg-app span, .bg-app label, .bg-app td, .bg-app th {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
}
.bg-app .subtitle {
    color: #9cb896;
    font-size: 14px;
    font-weight: 400;
    margin-bottom: 24px;
}

/* ========== HEADER ========== */
.screen-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(74,124,46,0.15);
}
.screen-header .icon {
    font-size: 36px;
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(58,125,42,0.15);
    border-radius: 14px;
    border: 1px solid rgba(58,125,42,0.25);
}

/* ========== CARDS ========== */
.glass-card {
    background: rgba(26, 38, 20, 0.55);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(74, 124, 46, 0.18);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.glass-card:hover {
    border-color: rgba(74, 124, 46, 0.35);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 20px rgba(58,125,42,0.08);
    transform: translateY(-2px);
}

/* ========== METRIC CARDS ========== */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.metric-card {
    background: rgba(26, 38, 20, 0.55);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(74,124,46,0.18);
    border-radius: 14px;
    padding: 20px;
    transition: all 0.3s ease;
}
.metric-card:hover {
    border-color: rgba(74,124,46,0.35);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.metric-card .metric-icon {
    font-size: 24px;
    margin-bottom: 12px;
}
.metric-card .metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #e8f0e4;
    margin-bottom: 4px;
}
.metric-card .metric-label {
    font-size: 12px;
    color: #9cb896;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}
.metric-card .metric-change {
    font-size: 12px;
    margin-top: 8px;
    font-weight: 600;
}
.metric-change.up { color: #22c55e; }
.metric-change.down { color: #ef4444; }
.metric-change.neutral { color: #9cb896; }

/* ========== BUTTONS ========== */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border: none;
    border-radius: 10px;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
    outline: none;
}
.btn-primary {
    background: linear-gradient(135deg, #3a7d2a, #2d5a20);
    color: #e8f0e4;
    box-shadow: 0 4px 12px rgba(58,125,42,0.3);
}
.btn-primary:hover {
    background: linear-gradient(135deg, #4e9e38, #3a7d2a);
    box-shadow: 0 6px 20px rgba(58,125,42,0.4);
    transform: translateY(-1px);
}
.btn-secondary {
    background: rgba(74,124,46,0.15);
    color: #c2eaaf;
    border: 1px solid rgba(74,124,46,0.3);
}
.btn-secondary:hover {
    background: rgba(74,124,46,0.25);
    border-color: rgba(74,124,46,0.5);
}
.btn-accent {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: #1a1a00;
    box-shadow: 0 4px 12px rgba(245,158,11,0.3);
}
.btn-accent:hover {
    box-shadow: 0 6px 20px rgba(245,158,11,0.4);
    transform: translateY(-1px);
}
.btn-danger {
    background: rgba(239,68,68,0.15);
    color: #fca5a5;
    border: 1px solid rgba(239,68,68,0.3);
}
.btn-danger:hover {
    background: rgba(239,68,68,0.25);
}
.btn-sm { padding: 6px 14px; font-size: 12px; border-radius: 8px; }
.btn-lg { padding: 14px 28px; font-size: 16px; border-radius: 12px; }

/* ========== INPUTS ========== */
.input-field {
    width: 100%;
    padding: 12px 16px;
    background: rgba(15, 26, 10, 0.7);
    border: 1px solid rgba(74,124,46,0.2);
    border-radius: 10px;
    color: #e8f0e4;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    transition: all 0.25s ease;
    outline: none;
}
.input-field:focus {
    border-color: #3a7d2a;
    box-shadow: 0 0 0 3px rgba(58,125,42,0.15);
}
.input-field::placeholder {
    color: #5a7a52;
}

/* ========== SELECT ========== */
.select-field {
    padding: 10px 14px;
    background: rgba(15, 26, 10, 0.7);
    border: 1px solid rgba(74,124,46,0.2);
    border-radius: 10px;
    color: #e8f0e4;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    cursor: pointer;
    outline: none;
    transition: all 0.25s ease;
}
.select-field:focus {
    border-color: #3a7d2a;
}
.select-field option {
    background: #1a2614;
    color: #e8f0e4;
}

/* ========== TABLES ========== */
.data-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 13px;
}
.data-table thead th {
    background: rgba(58,125,42,0.12);
    color: #9cb896;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 11px;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid rgba(74,124,46,0.15);
    position: sticky;
    top: 0;
}
.data-table thead th:first-child { border-radius: 10px 0 0 0; }
.data-table thead th:last-child { border-radius: 0 10px 0 0; }
.data-table tbody td {
    padding: 10px 16px;
    border-bottom: 1px solid rgba(74,124,46,0.08);
    color: #c2eaaf;
}
.data-table tbody tr {
    transition: background 0.2s ease;
}
.data-table tbody tr:hover {
    background: rgba(58,125,42,0.08);
}

/* ========== BADGES & PILLS ========== */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-success { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }
.badge-warning { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.25); }
.badge-danger { background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid rgba(239,68,68,0.25); }
.badge-info { background: rgba(59,130,246,0.15); color: #93c5fd; border: 1px solid rgba(59,130,246,0.25); }
.badge-neutral { background: rgba(148,163,184,0.15); color: #cbd5e1; border: 1px solid rgba(148,163,184,0.2); }

/* ========== PROGRESS BAR ========== */
.progress-bar-container {
    width: 100%;
    height: 8px;
    background: rgba(74,124,46,0.1);
    border-radius: 4px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #3a7d2a, #6bbf4e);
    border-radius: 4px;
    transition: width 0.6s ease;
}

/* ========== GAUGE (Circular) ========== */
.gauge-container {
    position: relative;
    width: 120px;
    height: 120px;
}
.gauge-container svg {
    transform: rotate(-90deg);
}
.gauge-bg {
    fill: none;
    stroke: rgba(74,124,46,0.12);
    stroke-width: 8;
}
.gauge-fill {
    fill: none;
    stroke-width: 8;
    stroke-linecap: round;
    transition: stroke-dashoffset 1s ease;
}
.gauge-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}
.gauge-value .value {
    font-size: 24px;
    font-weight: 800;
    color: #e8f0e4;
}
.gauge-value .unit {
    font-size: 11px;
    color: #9cb896;
}

/* ========== TOAST / NOTIFICATIONS ========== */
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.toast {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 20px;
    border-radius: 12px;
    background: rgba(26,38,20,0.95);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(74,124,46,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    animation: slideIn 0.4s ease forwards;
    font-size: 13px;
    color: #e8f0e4;
    min-width: 280px;
}
.toast.success { border-left: 3px solid #22c55e; }
.toast.warning { border-left: 3px solid #f59e0b; }
.toast.error { border-left: 3px solid #ef4444; }
.toast.info { border-left: 3px solid #3b82f6; }

/* ========== TABS ========== */
.tabs {
    display: flex;
    gap: 4px;
    background: rgba(15,26,10,0.5);
    padding: 4px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid rgba(74,124,46,0.1);
}
.tab {
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    color: #9cb896;
    cursor: pointer;
    transition: all 0.25s ease;
    border: none;
    background: transparent;
    font-family: 'Inter', sans-serif;
}
.tab:hover {
    color: #c2eaaf;
    background: rgba(58,125,42,0.1);
}
.tab.active {
    background: rgba(58,125,42,0.2);
    color: #6bbf4e;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(58,125,42,0.15);
}

/* ========== GRID LAYOUTS ========== */
.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.flex-row { display: flex; align-items: center; gap: 12px; }
.flex-between { display: flex; align-items: center; justify-content: space-between; }
.flex-col { display: flex; flex-direction: column; gap: 8px; }
.gap-sm { gap: 8px; }
.gap-md { gap: 16px; }
.gap-lg { gap: 24px; }
.mb-sm { margin-bottom: 8px; }
.mb-md { margin-bottom: 16px; }
.mb-lg { margin-bottom: 24px; }

/* ========== SCROLLBAR ========== */
.bg-app ::-webkit-scrollbar { width: 6px; height: 6px; }
.bg-app ::-webkit-scrollbar-track { background: rgba(15,26,10,0.3); border-radius: 3px; }
.bg-app ::-webkit-scrollbar-thumb { background: rgba(74,124,46,0.3); border-radius: 3px; }
.bg-app ::-webkit-scrollbar-thumb:hover { background: rgba(74,124,46,0.5); }

/* ========== ANIMATIONS ========== */
@keyframes slideIn {
    from { opacity: 0; transform: translateX(40px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(58,125,42,0.3); }
    50% { box-shadow: 0 0 20px rgba(58,125,42,0.5); }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.animate-fade-in {
    animation: fadeIn 0.5s ease forwards;
}
.animate-pulse {
    animation: pulse 2s ease infinite;
}

/* ========== EMPTY / LOADING STATES ========== */
.loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(74,124,46,0.2);
    border-top-color: #3a7d2a;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 20px auto;
}
.empty-state {
    text-align: center;
    padding: 48px 24px;
    color: #5a7a52;
}
.empty-state .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}
.empty-state p {
    font-size: 14px;
    max-width: 300px;
    margin: 0 auto;
}

/* ========== STATUS DOT ========== */
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}
.status-dot.online { background: #22c55e; box-shadow: 0 0 6px rgba(34,197,94,0.5); }
.status-dot.warning { background: #f59e0b; box-shadow: 0 0 6px rgba(245,158,11,0.5); }
.status-dot.offline { background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,0.5); }

/* ========== DIVIDER ========== */
.divider {
    height: 1px;
    background: rgba(74,124,46,0.12);
    margin: 20px 0;
}

/* ========== TOOLTIP ========== */
.tooltip-wrap {
    position: relative;
    cursor: help;
}
.tooltip-wrap::after {
    content: attr(data-tip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(-4px);
    background: rgba(26,38,20,0.95);
    border: 1px solid rgba(74,124,46,0.3);
    color: #e8f0e4;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
}
.tooltip-wrap:hover::after {
    opacity: 1;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
    .bg-app { padding: 16px; }
    .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
    .metrics-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
"""

# Toast utility function (reusable JS)
TOAST_JS = """
<script>
function showToast(message, type='info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML = (type==='success'?'✅':type==='warning'?'⚠️':type==='error'?'❌':'ℹ️') + ' ' + message;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity='0'; toast.style.transform='translateX(40px)'; setTimeout(()=>toast.remove(),400); }, 3500);
}
</script>
"""

print("✅ Common styles and utilities loaded!")
print("   COMMON_CSS variable is now available for all screens.")
print("   TOAST_JS variable provides toast notification function.")
