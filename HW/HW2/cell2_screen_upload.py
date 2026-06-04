# ============================================================
# Cell 2: Plant Image Upload Screen (העלאת תמונות צמחים)
# Requires: Cell 1 (COMMON_CSS, TOAST_JS) to be run first.
# ============================================================

from IPython.display import HTML, display

display(HTML(COMMON_CSS + """
<style>
/* ========== UPLOAD ZONE ========== */
#uploadScreen .upload-zone {
    border: 2px dashed rgba(74,124,46,0.35);
    border-radius: 20px;
    padding: 56px 32px;
    text-align: center;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(.4,0,.2,1);
    background: rgba(15,26,10,0.35);
    position: relative;
    overflow: hidden;
    margin-bottom: 28px;
}
#uploadScreen .upload-zone::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    background: radial-gradient(circle at 50% 50%, rgba(58,125,42,0.06) 0%, transparent 70%);
    transition: opacity 0.4s ease;
    opacity: 0;
}
#uploadScreen .upload-zone:hover,
#uploadScreen .upload-zone.drag-over {
    border-color: #4e9e38;
    background: rgba(58,125,42,0.08);
    box-shadow: 0 0 40px rgba(58,125,42,0.12), inset 0 0 60px rgba(58,125,42,0.04);
    transform: scale(1.005);
}
#uploadScreen .upload-zone:hover::before,
#uploadScreen .upload-zone.drag-over::before {
    opacity: 1;
}
#uploadScreen .upload-zone.drag-over {
    border-color: #6bbf4e;
    border-style: solid;
    animation: uploadGlow 1.2s ease-in-out infinite;
}
@keyframes uploadGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(58,125,42,0.12); }
    50% { box-shadow: 0 0 50px rgba(58,125,42,0.25), inset 0 0 30px rgba(58,125,42,0.06); }
}
#uploadScreen .upload-zone .zone-icon {
    font-size: 64px;
    display: block;
    margin-bottom: 16px;
    animation: floatBasil 3s ease-in-out infinite;
    filter: drop-shadow(0 4px 12px rgba(58,125,42,0.3));
}
@keyframes floatBasil {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-6px) rotate(2deg); }
    75% { transform: translateY(-3px) rotate(-1deg); }
}
#uploadScreen .upload-zone .zone-title {
    font-size: 18px;
    font-weight: 700;
    color: #c2eaaf;
    margin-bottom: 8px;
}
#uploadScreen .upload-zone .zone-subtitle {
    font-size: 13px;
    color: #5a7a52;
    margin-bottom: 20px;
}
#uploadScreen .upload-zone .zone-formats {
    font-size: 11px;
    color: #5a7a52;
    letter-spacing: 0.5px;
}
#uploadScreen .upload-zone .browse-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 28px;
    background: linear-gradient(135deg, #3a7d2a, #2d5a20);
    color: #e8f0e4;
    border: none;
    border-radius: 12px;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(58,125,42,0.35);
    margin-bottom: 16px;
}
#uploadScreen .upload-zone .browse-btn:hover {
    background: linear-gradient(135deg, #4e9e38, #3a7d2a);
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(58,125,42,0.45);
}

/* ========== PROGRESS BAR (upload simulation) ========== */
#uploadScreen .upload-progress-wrap {
    margin: 20px 0;
    display: none;
}
#uploadScreen .upload-progress-wrap .progress-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 13px;
}
#uploadScreen .upload-progress-wrap .progress-info .filename {
    color: #c2eaaf;
    font-weight: 600;
}
#uploadScreen .upload-progress-wrap .progress-info .percent {
    color: #6bbf4e;
    font-weight: 700;
}
#uploadScreen .upload-progress-bar {
    height: 6px;
    background: rgba(74,124,46,0.12);
    border-radius: 3px;
    overflow: hidden;
}
#uploadScreen .upload-progress-bar .fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #3a7d2a, #6bbf4e, #4e9e38);
    background-size: 200% 100%;
    border-radius: 3px;
    transition: width 0.15s linear;
    animation: shimmer 1.5s ease infinite;
}

/* ========== GALLERY GRID ========== */
#uploadScreen .gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 20px;
}
#uploadScreen .image-card {
    background: rgba(26, 38, 20, 0.55);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(74,124,46,0.15);
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(.4,0,.2,1);
    animation: cardAppear 0.45s ease forwards;
    opacity: 0;
}
@keyframes cardAppear {
    from { opacity: 0; transform: translateY(20px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
#uploadScreen .image-card:hover {
    border-color: rgba(74,124,46,0.4);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px rgba(58,125,42,0.08);
    transform: translateY(-4px);
}
#uploadScreen .image-card .card-thumb {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
    border-bottom: 1px solid rgba(74,124,46,0.1);
    background: rgba(10,15,7,0.6);
    transition: transform 0.4s ease;
}
#uploadScreen .image-card:hover .card-thumb {
    transform: scale(1.03);
}
#uploadScreen .image-card .card-thumb-wrap {
    overflow: hidden;
    position: relative;
}
#uploadScreen .image-card .card-thumb-wrap .card-delete-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(239,68,68,0.75);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(239,68,68,0.4);
    color: #fff;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: all 0.25s ease;
    transform: scale(0.8);
}
#uploadScreen .image-card:hover .card-delete-btn {
    opacity: 1;
    transform: scale(1);
}
#uploadScreen .image-card .card-delete-btn:hover {
    background: rgba(239,68,68,0.95);
    box-shadow: 0 4px 12px rgba(239,68,68,0.4);
}
#uploadScreen .image-card .card-body {
    padding: 16px;
}
#uploadScreen .image-card .card-filename {
    font-size: 14px;
    font-weight: 600;
    color: #e8f0e4;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
#uploadScreen .image-card .card-meta {
    display: flex;
    gap: 12px;
    font-size: 11px;
    color: #5a7a52;
    margin-bottom: 14px;
}
#uploadScreen .image-card .card-meta span {
    display: flex;
    align-items: center;
    gap: 4px;
}
/* Metadata form within each card */
#uploadScreen .image-card .card-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
#uploadScreen .image-card .card-form label {
    font-size: 11px;
    color: #9cb896;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 2px;
}
#uploadScreen .image-card .card-form select {
    padding: 8px 12px;
    background: rgba(15, 26, 10, 0.7);
    border: 1px solid rgba(74,124,46,0.2);
    border-radius: 8px;
    color: #e8f0e4;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    cursor: pointer;
    outline: none;
    transition: all 0.25s ease;
    width: 100%;
}
#uploadScreen .image-card .card-form select:focus {
    border-color: #3a7d2a;
    box-shadow: 0 0 0 2px rgba(58,125,42,0.12);
}
#uploadScreen .image-card .card-form select option {
    background: #1a2614;
    color: #e8f0e4;
}
#uploadScreen .image-card .card-form textarea {
    padding: 8px 12px;
    background: rgba(15, 26, 10, 0.7);
    border: 1px solid rgba(74,124,46,0.2);
    border-radius: 8px;
    color: #e8f0e4;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    resize: vertical;
    min-height: 48px;
    outline: none;
    transition: all 0.25s ease;
    width: 100%;
}
#uploadScreen .image-card .card-form textarea::placeholder {
    color: #5a7a52;
}
#uploadScreen .image-card .card-form textarea:focus {
    border-color: #3a7d2a;
    box-shadow: 0 0 0 2px rgba(58,125,42,0.12);
}

/* ========== FILTER TABS ROW ========== */
#uploadScreen .gallery-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 8px;
}

/* ========== EMPTY STATE ========== */
#uploadScreen .upload-empty {
    text-align: center;
    padding: 60px 24px;
    color: #5a7a52;
}
#uploadScreen .upload-empty .empty-leaf {
    font-size: 72px;
    display: block;
    margin-bottom: 20px;
    animation: floatBasil 3.5s ease-in-out infinite;
    filter: drop-shadow(0 4px 18px rgba(58,125,42,0.2));
    opacity: 0.55;
}
#uploadScreen .upload-empty .empty-title {
    font-size: 18px;
    font-weight: 600;
    color: #9cb896;
    margin-bottom: 8px;
}
#uploadScreen .upload-empty .empty-sub {
    font-size: 13px;
    color: #5a7a52;
    max-width: 340px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ========== SECTION TITLES ========== */
#uploadScreen .section-title {
    font-size: 16px;
    font-weight: 700;
    color: #e8f0e4;
    display: flex;
    align-items: center;
    gap: 8px;
}
#uploadScreen .section-title .count {
    background: rgba(58,125,42,0.2);
    color: #6bbf4e;
    font-size: 12px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    border: 1px solid rgba(74,124,46,0.2);
}

/* ========== MISC UTILITIES ========== */
#uploadScreen .hidden-input {
    display: none;
}
</style>

<div class="bg-app" id="uploadScreen">

    <!-- ===== HEADER ===== -->
    <div class="screen-header">
        <div class="icon">📸</div>
        <div>
            <h1>העלאת תמונות צמחים</h1>
            <p class="subtitle">Upload and manage images of your basil plants for health analysis</p>
        </div>
    </div>

    <!-- ===== STATS METRICS ===== -->
    <div class="metrics-grid" id="uploadMetrics">
        <div class="metric-card">
            <div class="metric-icon">🖼️</div>
            <div class="metric-value" id="uploadStatCount">0</div>
            <div class="metric-label">Images Uploaded</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">💾</div>
            <div class="metric-value" id="uploadStatStorage">0 KB</div>
            <div class="metric-label">Storage Used</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">✅</div>
            <div class="metric-value" id="uploadStatHealthy">0</div>
            <div class="metric-label">Healthy</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">⚠️</div>
            <div class="metric-value" id="uploadStatIssues">0</div>
            <div class="metric-label">Issues Detected</div>
        </div>
    </div>

    <!-- ===== DRAG & DROP ZONE ===== -->
    <div class="upload-zone" id="uploadDropZone">
        <span class="zone-icon">🌿</span>
        <div class="zone-title">Drag & drop your basil plant images here</div>
        <div class="zone-subtitle">or click the button below to browse your files</div>
        <button class="browse-btn" id="uploadBrowseBtn" onclick="document.getElementById('uploadFileInput').click()">
            📂 Browse Files
        </button>
        <div class="zone-formats">Supports JPG, PNG, WEBP • Max 10MB per file</div>
        <input type="file" id="uploadFileInput" class="hidden-input" multiple accept="image/jpeg,image/png,image/webp">
    </div>

    <!-- ===== UPLOAD PROGRESS ===== -->
    <div class="upload-progress-wrap" id="uploadProgressWrap">
        <div class="progress-info">
            <span class="filename" id="uploadProgressName">Uploading...</span>
            <span class="percent" id="uploadProgressPct">0%</span>
        </div>
        <div class="upload-progress-bar">
            <div class="fill" id="uploadProgressFill"></div>
        </div>
    </div>

    <!-- ===== GALLERY SECTION ===== -->
    <div class="glass-card" id="uploadGallerySection" style="display:none; margin-top:8px;">
        <div class="gallery-header">
            <div class="section-title">
                🌱 Plant Gallery <span class="count" id="uploadGalleryCount">0</span>
            </div>
            <div class="tabs" id="uploadFilterTabs">
                <button class="tab active" data-filter="all" onclick="uploadFilterImages('all', this)">All</button>
                <button class="tab" data-filter="healthy" onclick="uploadFilterImages('healthy', this)">🟢 Healthy</button>
                <button class="tab" data-filter="issues" onclick="uploadFilterImages('issues', this)">🟠 Issues</button>
            </div>
        </div>
        <div class="gallery-grid" id="uploadGalleryGrid">
            <!-- Image cards injected here -->
        </div>
    </div>

    <!-- ===== EMPTY STATE ===== -->
    <div class="upload-empty" id="uploadEmptyState">
        <span class="empty-leaf">🍃</span>
        <div class="empty-title">Upload your first basil plant image</div>
        <div class="empty-sub">
            Drag and drop or browse to add images of your basil plants.
            Track their health over time with our analysis tools.
        </div>
    </div>

</div>

""" + TOAST_JS + """
<script>
// ========================================================
// UPLOAD SCREEN - State & Logic
// ========================================================
(function() {
    'use strict';

    // --- State ---
    const state = {
        images: [],       // { id, name, size, dataUrl, timestamp, status, notes }
        nextId: 1,
        activeFilter: 'all',
        totalBytes: 0
    };

    // --- DOM references ---
    const dropZone       = document.getElementById('uploadDropZone');
    const fileInput      = document.getElementById('uploadFileInput');
    const progressWrap   = document.getElementById('uploadProgressWrap');
    const progressName   = document.getElementById('uploadProgressName');
    const progressPct    = document.getElementById('uploadProgressPct');
    const progressFill   = document.getElementById('uploadProgressFill');
    const gallerySection = document.getElementById('uploadGallerySection');
    const galleryGrid    = document.getElementById('uploadGalleryGrid');
    const galleryCount   = document.getElementById('uploadGalleryCount');
    const emptyState     = document.getElementById('uploadEmptyState');
    const statCount      = document.getElementById('uploadStatCount');
    const statStorage    = document.getElementById('uploadStatStorage');
    const statHealthy    = document.getElementById('uploadStatHealthy');
    const statIssues     = document.getElementById('uploadStatIssues');

    // ===== DRAG & DROP EVENTS =====
    ['dragenter', 'dragover'].forEach(evt => {
        dropZone.addEventListener(evt, e => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-over');
        });
    });
    ['dragleave', 'drop'].forEach(evt => {
        dropZone.addEventListener(evt, e => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-over');
        });
    });
    dropZone.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        if (files.length) handleFiles(files);
    });
    // Click anywhere on the zone (except the button itself)
    dropZone.addEventListener('click', e => {
        if (e.target.id !== 'uploadBrowseBtn' && !e.target.closest('#uploadBrowseBtn')) {
            fileInput.click();
        }
    });
    fileInput.addEventListener('change', e => {
        if (e.target.files.length) handleFiles(e.target.files);
        e.target.value = '';  // reset so re-selecting the same file works
    });

    // ===== FILE HANDLING =====
    function handleFiles(fileList) {
        const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
        const maxSize = 10 * 1024 * 1024; // 10 MB
        const files = Array.from(fileList).filter(f => {
            if (!validTypes.includes(f.type)) {
                showToast('Unsupported format: ' + f.name, 'warning');
                return false;
            }
            if (f.size > maxSize) {
                showToast('File too large (>10MB): ' + f.name, 'warning');
                return false;
            }
            return true;
        });
        if (!files.length) return;
        processFileQueue(files, 0);
    }

    // Process files one-by-one with progress simulation
    function processFileQueue(files, idx) {
        if (idx >= files.length) {
            progressWrap.style.display = 'none';
            return;
        }
        const file = files[idx];
        progressWrap.style.display = 'block';
        progressName.textContent = file.name;
        progressPct.textContent = '0%';
        progressFill.style.width = '0%';

        // Read file
        const reader = new FileReader();
        reader.onload = function(ev) {
            // Simulate upload progress
            simulateProgress(0, () => {
                const img = {
                    id: state.nextId++,
                    name: file.name,
                    size: file.size,
                    dataUrl: ev.target.result,
                    timestamp: new Date().toLocaleString(),
                    status: 'unknown',   // default
                    notes: ''
                };
                state.images.push(img);
                state.totalBytes += file.size;
                updateStats();
                renderGallery();
                showToast('✨ "' + file.name + '" uploaded successfully!', 'success');
                // Process next file
                setTimeout(() => processFileQueue(files, idx + 1), 200);
            });
        };
        reader.readAsDataURL(file);
    }

    function simulateProgress(pct, done) {
        if (pct > 100) { done(); return; }
        progressFill.style.width = pct + '%';
        progressPct.textContent = Math.min(pct, 100) + '%';
        const increment = pct < 60 ? randomInt(8, 18) : pct < 90 ? randomInt(4, 10) : randomInt(2, 5);
        const delay = pct < 60 ? randomInt(30, 60) : randomInt(50, 100);
        setTimeout(() => simulateProgress(pct + increment, done), delay);
    }

    function randomInt(a, b) { return Math.floor(Math.random() * (b - a + 1)) + a; }

    // ===== STATS UPDATE =====
    function updateStats() {
        statCount.textContent = state.images.length;
        statStorage.textContent = formatBytes(state.totalBytes);
        const healthy = state.images.filter(i => i.status === 'healthy').length;
        const issues  = state.images.filter(i => i.status === 'mild' || i.status === 'severe').length;
        statHealthy.textContent = healthy;
        statIssues.textContent = issues;
    }

    function formatBytes(bytes) {
        if (bytes === 0) return '0 KB';
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }

    // ===== RENDER GALLERY =====
    function renderGallery() {
        const filter = state.activeFilter;
        let filtered = state.images;
        if (filter === 'healthy') {
            filtered = state.images.filter(i => i.status === 'healthy');
        } else if (filter === 'issues') {
            filtered = state.images.filter(i => i.status === 'mild' || i.status === 'severe');
        }

        if (state.images.length === 0) {
            gallerySection.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }
        emptyState.style.display = 'none';
        gallerySection.style.display = 'block';
        galleryCount.textContent = filtered.length;

        galleryGrid.innerHTML = '';
        if (filtered.length === 0) {
            galleryGrid.innerHTML = `
                <div style="grid-column:1/-1; text-align:center; padding:40px 0; color:#5a7a52;">
                    <div style="font-size:36px; margin-bottom:12px; opacity:.5;">🔍</div>
                    <div style="font-size:14px;">No images match the selected filter.</div>
                </div>`;
            return;
        }

        filtered.forEach((img, i) => {
            const card = document.createElement('div');
            card.className = 'image-card';
            card.style.animationDelay = (i * 0.07) + 's';
            card.dataset.imgId = img.id;

            const statusBadge = getStatusBadge(img.status);

            card.innerHTML = `
                <div class="card-thumb-wrap">
                    <img class="card-thumb" src="${img.dataUrl}" alt="${img.name}" loading="lazy">
                    <button class="card-delete-btn" title="Delete image" onclick="window._uploadDeleteImage(${img.id})">✕</button>
                </div>
                <div class="card-body">
                    <div class="card-filename" title="${img.name}">${img.name}</div>
                    <div class="card-meta">
                        <span>📏 ${formatBytes(img.size)}</span>
                        <span>🕒 ${img.timestamp}</span>
                    </div>
                    <div style="margin-bottom:12px;">${statusBadge}</div>
                    <div class="card-form">
                        <label>Health Status</label>
                        <select onchange="window._uploadSetStatus(${img.id}, this.value)">
                            <option value="unknown" ${img.status==='unknown'?'selected':''}>❓ Unknown</option>
                            <option value="healthy" ${img.status==='healthy'?'selected':''}>🟢 Healthy</option>
                            <option value="mild" ${img.status==='mild'?'selected':''}>🟡 Mild Issue</option>
                            <option value="severe" ${img.status==='severe'?'selected':''}>🔴 Severe Issue</option>
                        </select>
                        <label>Notes</label>
                        <textarea placeholder="Add observations…" onchange="window._uploadSetNotes(${img.id}, this.value)">${img.notes}</textarea>
                    </div>
                </div>`;
            galleryGrid.appendChild(card);
        });
    }

    function getStatusBadge(status) {
        switch (status) {
            case 'healthy': return '<span class="badge badge-success">🟢 Healthy</span>';
            case 'mild':    return '<span class="badge badge-warning">🟡 Mild Issue</span>';
            case 'severe':  return '<span class="badge badge-danger">🔴 Severe Issue</span>';
            default:        return '<span class="badge badge-neutral">❓ Unknown</span>';
        }
    }

    // ===== FILTER TABS =====
    window.uploadFilterImages = function(filter, tabEl) {
        state.activeFilter = filter;
        // Update active tab style
        document.querySelectorAll('#uploadFilterTabs .tab').forEach(t => t.classList.remove('active'));
        tabEl.classList.add('active');
        renderGallery();
    };

    // ===== IMAGE ACTIONS (global handlers) =====
    window._uploadDeleteImage = function(id) {
        const idx = state.images.findIndex(i => i.id === id);
        if (idx === -1) return;
        const img = state.images[idx];
        state.totalBytes -= img.size;
        state.images.splice(idx, 1);
        updateStats();
        renderGallery();
        showToast('"' + img.name + '" deleted.', 'info');
    };

    window._uploadSetStatus = function(id, value) {
        const img = state.images.find(i => i.id === id);
        if (!img) return;
        img.status = value;
        updateStats();
        renderGallery();
    };

    window._uploadSetNotes = function(id, value) {
        const img = state.images.find(i => i.id === id);
        if (img) img.notes = value;
    };

    // ===== INITIAL RENDER =====
    updateStats();
    renderGallery();

})();
</script>
"""))
