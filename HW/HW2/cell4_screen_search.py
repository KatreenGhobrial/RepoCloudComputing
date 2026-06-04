from IPython.display import HTML, display
import json

# Ensure you have run cell1_common_styles.py first to load COMMON_CSS and TOAST_JS

HTML_CONTENT = COMMON_CSS + TOAST_JS + """
<style>
/* ========== SEARCH BAR ========== */
.search-container {
    max-width: 800px;
    margin: 0 auto 32px;
}
.search-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background: rgba(15, 26, 10, 0.8);
    border: 2px solid rgba(74,124,46,0.4);
    border-radius: 24px;
    padding: 8px 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.search-input-wrapper.focused {
    border-color: #6bbf4e;
    box-shadow: 0 4px 24px rgba(58,125,42,0.3);
    background: rgba(20, 32, 14, 0.9);
}
.search-icon {
    font-size: 20px;
    color: #6bbf4e;
    margin-right: 12px;
}
.search-input {
    flex: 1;
    background: transparent;
    border: none;
    color: #e8f0e4;
    font-size: 16px;
    font-family: 'Inter', sans-serif;
    outline: none;
    padding: 8px 0;
}
.search-input::placeholder { color: #5a7a52; }
.search-btn {
    background: linear-gradient(135deg, #3a7d2a, #2d5a20);
    color: #fff;
    border: none;
    border-radius: 16px;
    padding: 10px 24px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
}
.search-btn:hover { background: linear-gradient(135deg, #4e9e38, #3a7d2a); }

/* ========== AUTOCOMPLETE ========== */
.autocomplete-dropdown {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background: rgba(26, 38, 20, 0.95);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(74,124,46,0.3);
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    z-index: 100;
    overflow: hidden;
    display: none;
}
.autocomplete-dropdown.active { display: block; animation: fadeIn 0.2s ease; }
.ac-item {
    padding: 12px 20px;
    cursor: pointer;
    color: #c2eaaf;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: background 0.2s;
}
.ac-item:hover, .ac-item.selected { background: rgba(58,125,42,0.2); color: #e8f0e4; }
.ac-item .ac-icon { color: #5a7a52; font-size: 14px; }

/* ========== SEARCH TOGGLES & CHIPS ========== */
.search-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    padding: 0 16px;
}
.operator-toggle {
    display: flex;
    background: rgba(15,26,10,0.6);
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid rgba(74,124,46,0.2);
}
.op-btn {
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    background: transparent;
    color: #9cb896;
    border: none;
    cursor: pointer;
}
.op-btn.active { background: rgba(58,125,42,0.3); color: #e8f0e4; }
.recent-chips {
    display: flex;
    gap: 8px;
    overflow-x: auto;
}
.chip {
    padding: 6px 12px;
    background: rgba(58,125,42,0.1);
    border: 1px solid rgba(74,124,46,0.2);
    border-radius: 16px;
    font-size: 12px;
    color: #c2eaaf;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.chip:hover { background: rgba(58,125,42,0.2); border-color: rgba(74,124,46,0.4); }

/* ========== RAG PANEL ========== */
.rag-panel {
    background: linear-gradient(135deg, rgba(26,38,20,0.8) 0%, rgba(15,26,10,0.9) 100%);
    border: 1px solid rgba(245,158,11,0.3); /* Accent gold border */
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(245,158,11,0.08);
    display: none;
}
.rag-panel.active { display: block; animation: slideIn 0.4s ease; }
.rag-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    color: #fbbf24;
}
.rag-content { color: #e8f0e4; font-size: 15px; line-height: 1.7; }
.rag-source-badge {
    background: rgba(245,158,11,0.15);
    color: #fbbf24;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 16px;
    display: inline-block;
}

/* ========== RESULTS LIST ========== */
.results-meta {
    color: #9cb896;
    font-size: 14px;
    margin-bottom: 20px;
    display: none;
}
.result-card {
    background: rgba(26,38,20,0.4);
    border: 1px solid rgba(74,124,46,0.15);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.2s;
    animation: fadeIn 0.4s ease backwards;
}
.result-card:hover { border-color: rgba(74,124,46,0.4); background: rgba(26,38,20,0.6); }
.res-title { font-size: 18px; font-weight: 600; color: #c2eaaf; margin-bottom: 8px; cursor: pointer; }
.res-title:hover { text-decoration: underline; color: #6bbf4e; }
.res-authors { font-size: 13px; color: #9cb896; margin-bottom: 12px; }
.res-abstract { font-size: 14px; color: #d1d5db; line-height: 1.6; }
.highlight { background: rgba(245,158,11,0.25); color: #fbbf24; padding: 0 4px; border-radius: 4px; font-weight: 500; }
.res-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(74,124,46,0.1); }
.res-score { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #9cb896; }
.score-bar { width: 100px; height: 6px; background: rgba(15,26,10,0.5); border-radius: 3px; overflow: hidden; }
.score-fill { height: 100%; background: #3a7d2a; }
.res-terms { display: flex; gap: 6px; flex-wrap: wrap; }
.term-badge { background: rgba(58,125,42,0.15); color: #6bbf4e; padding: 2px 8px; border-radius: 10px; font-size: 11px; }

/* ========== LAYOUT ========== */
.search-layout { display: grid; grid-template-columns: 240px 1fr; gap: 32px; }
.filters-sidebar { background: rgba(26,38,20,0.3); border-radius: 16px; padding: 20px; height: fit-content; }
.filter-group { margin-bottom: 24px; }
.filter-title { font-size: 13px; font-weight: 600; color: #9cb896; text-transform: uppercase; margin-bottom: 12px; }
.filter-label { display: flex; align-items: center; gap: 8px; font-size: 14px; color: #c2eaaf; margin-bottom: 8px; cursor: pointer; }
.filter-label input[type="checkbox"] { accent-color: #3a7d2a; width: 16px; height: 16px; }

@media (max-width: 768px) {
    .search-layout { grid-template-columns: 1fr; }
    .filters-sidebar { display: none; }
}
</style>

<div class="bg-app" id="searchScreen">
    
    <div class="screen-header">
        <div class="icon">🔍</div>
        <div>
            <h1>Academic Search Engine</h1>
            <div class="subtitle">Query the Basil research inverted index</div>
        </div>
    </div>

    <!-- SEARCH AREA -->
    <div class="search-container">
        <div class="search-input-wrapper" id="search-wrapper">
            <span class="search-icon">🔎</span>
            <input type="text" id="search-input" class="search-input" placeholder="Search basil research papers (e.g. 'fusarium wilt basil')..." autocomplete="off">
            <button class="search-btn" onclick="window.searchApp.executeSearch()">Search</button>
            
            <div class="autocomplete-dropdown" id="ac-dropdown"></div>
        </div>
        
        <div class="search-controls">
            <div class="operator-toggle">
                <button class="op-btn active" id="op-and" onclick="window.searchApp.setOperator('AND')">AND</button>
                <button class="op-btn" id="op-or" onclick="window.searchApp.setOperator('OR')">OR</button>
            </div>
            <div class="recent-chips" id="recent-searches">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>

    <div class="search-layout">
        <!-- SIDEBAR -->
        <div class="filters-sidebar">
            <div class="flex-between mb-md">
                <h3 style="margin:0">Filters</h3>
                <button class="btn btn-sm btn-secondary" onclick="window.searchApp.clearFilters()" style="padding: 2px 8px; font-size:11px;">Clear</button>
            </div>
            
            <div class="filter-group">
                <div class="filter-title">Topic Tags</div>
                <label class="filter-label"><input type="checkbox" class="tag-filter" value="disease" checked> Disease & Pathology</label>
                <label class="filter-label"><input type="checkbox" class="tag-filter" value="chemistry" checked> Chemistry</label>
                <label class="filter-label"><input type="checkbox" class="tag-filter" value="agriculture" checked> Agriculture</label>
                <label class="filter-label"><input type="checkbox" class="tag-filter" value="ai" checked> AI / ML</label>
            </div>
            
            <div class="filter-group">
                <div class="filter-title">Year Range</div>
                <select class="select-field" style="width:100%">
                    <option value="all">All Time</option>
                    <option value="5">Last 5 Years</option>
                    <option value="10">Last 10 Years</option>
                </select>
            </div>
        </div>

        <!-- MAIN RESULTS -->
        <div class="results-area">
            
            <!-- Empty State -->
            <div class="empty-state" id="search-empty">
                <div class="empty-icon" style="font-size: 64px;">📚</div>
                <h3 style="color:#c2eaaf; margin-bottom:12px; font-size:18px;">Ready to explore</h3>
                <p style="margin-bottom:24px;">Search our indexed academic database for basil plant research, diseases, and treatments.</p>
                <div style="display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
                    <span class="chip" onclick="window.searchApp.quickSearch('fusarium biocontrol')">fusarium biocontrol</span>
                    <span class="chip" onclick="window.searchApp.quickSearch('machine learning classification')">machine learning classification</span>
                    <span class="chip" onclick="window.searchApp.quickSearch('downy mildew peronospora')">downy mildew peronospora</span>
                    <span class="chip" onclick="window.searchApp.quickSearch('essential oil antimicrobial')">essential oil antimicrobial</span>
                </div>
            </div>

            <!-- RAG Panel -->
            <div class="rag-panel" id="rag-panel">
                <div class="rag-header">
                    <span style="font-size: 20px;">✨</span>
                    <h3 style="margin:0; color:#fbbf24;">AI-Enhanced Summary</h3>
                </div>
                <div class="rag-content" id="rag-text"></div>
                <div class="rag-source-badge" id="rag-badge">Generated from X papers</div>
            </div>

            <!-- Results Meta -->
            <div class="results-meta" id="results-meta"></div>

            <!-- Results List -->
            <div id="results-list"></div>

        </div>
    </div>

</div>

<script>
(function() {
    
    // --- MOCK DATABASE ---
    const documents = [
        {
            id: "DOC_001",
            title: "Detection and Management of Downy Mildew on Sweet Basil (Ocimum basilicum)",
            authors: "Cohen Y., Vaknin M., Ben-Naim Y.",
            tags: ["disease", "agriculture"],
            abstract: "Peronospora belbahrii is the primary pathogen causing downy mildew in sweet basil. Symptoms include yellowing leaves and gray-purple sporulation on leaf undersides. Effective management relies on resistant cultivars and timely fungicide application."
        },
        {
            id: "DOC_002",
            title: "Fusarium Wilt of Basil: Molecular Identification and Biological Control Strategies",
            authors: "Reis A., Giordano L.B., Lopes C.A.",
            tags: ["disease", "agriculture"],
            abstract: "Fusarium oxysporum f. sp. basilici causes severe wilting and vascular discoloration in basil plants. Recent studies explore biocontrol using Trichoderma harzianum and Bacillus subtilis as alternatives to chemical fungicide treatments."
        },
        {
            id: "DOC_003",
            title: "Chemical Composition and Antimicrobial Activity of Essential Oils from Ocimum basilicum",
            authors: "Suppakul P., Miltz J., Sonneveld K.",
            tags: ["chemistry"],
            abstract: "The essential oil of sweet basil contains linalool, eugenol, and methyl chavicol as major compounds. These exhibit significant antimicrobial properties against E. coli and S. aureus, alongside strong antioxidant activity."
        },
        {
            id: "DOC_004",
            title: "Effects of Temperature and Light on Growth and Essential Oil Content of Sweet Basil",
            authors: "Chang X., Alderson P.G., Wright C.J.",
            tags: ["agriculture", "chemistry"],
            abstract: "Growth of sweet basil is highly sensitive to environmental factors. Optimal temperature is 20-25°C. Variations in light intensity significantly impact both total biomass and the yield of essential oil, with specific photoperiod responses observed."
        },
        {
            id: "DOC_005",
            title: "Machine Learning Approaches for Early Detection of Basil Leaf Diseases Using Image Analysis",
            authors: "Singh V., Misra A.K., Sharma P.",
            tags: ["disease", "ai"],
            abstract: "We propose a CNN-based machine learning architecture for classification of basil leaf diseases. Using transfer learning with ResNet50, the model achieved 96.2% accuracy. This enables real-time disease detection via smartphone applications."
        }
    ];

    // Build Inverted Index
    const stopWords = new Set(["is","the","of","and","in","on","for","with","to","a","an","as","by"]);
    const invertedIndex = {};
    const termFrequency = {};

    documents.forEach(doc => {
        // Tokenize abstract + title
        const text = (doc.title + " " + doc.abstract).toLowerCase();
        const tokens = text.match(/\b[a-z]+\b/g) || [];
        
        const docWordCounts = {};
        tokens.forEach(token => {
            if (!stopWords.has(token) && token.length > 2) {
                docWordCounts[token] = (docWordCounts[token] || 0) + 1;
            }
        });

        for (const [word, count] of Object.entries(docWordCounts)) {
            if (!invertedIndex[word]) {
                invertedIndex[word] = {};
                termFrequency[word] = 0;
            }
            invertedIndex[word][doc.id] = count;
            termFrequency[word] += count;
        }
    });

    // Extract vocabulary for autocomplete
    const vocabulary = Object.keys(invertedIndex).filter(w => termFrequency[w] > 1 || w.length > 5).sort();

    // --- APP STATE ---
    const state = {
        operator: 'AND',
        recentSearches: ["fusarium", "machine learning", "essential oil"],
        currentQuery: ""
    };

    // --- UI ELEMENTS ---
    const elements = {
        input: document.getElementById('search-input'),
        wrapper: document.getElementById('search-wrapper'),
        dropdown: document.getElementById('ac-dropdown'),
        recentContainer: document.getElementById('recent-searches'),
        resultsMeta: document.getElementById('results-meta'),
        resultsList: document.getElementById('results-list'),
        emptyState: document.getElementById('search-empty'),
        ragPanel: document.getElementById('rag-panel'),
        ragText: document.getElementById('rag-text'),
        ragBadge: document.getElementById('rag-badge'),
        opAnd: document.getElementById('op-and'),
        opOr: document.getElementById('op-or')
    };

    // --- INIT ---
    function init() {
        renderRecentSearches();
        
        elements.input.addEventListener('focus', () => elements.wrapper.classList.add('focused'));
        elements.input.addEventListener('blur', () => {
            elements.wrapper.classList.remove('focused');
            setTimeout(() => elements.dropdown.classList.remove('active'), 200);
        });
        
        elements.input.addEventListener('input', handleAutocomplete);
        elements.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') executeSearch();
        });

        // Expose API
        window.searchApp = {
            executeSearch,
            quickSearch,
            setOperator,
            clearFilters
        };
    }

    // --- AUTOCOMPLETE ---
    function handleAutocomplete(e) {
        const query = e.target.value.toLowerCase().split(' ').pop();
        if (query.length < 2) {
            elements.dropdown.classList.remove('active');
            return;
        }

        const matches = vocabulary.filter(w => w.startsWith(query)).slice(0, 5);
        if (matches.length === 0) {
            elements.dropdown.classList.remove('active');
            return;
        }

        elements.dropdown.innerHTML = matches.map(match => `
            <div class="ac-item" onclick="window.searchApp.quickSearch('${match}')">
                <span class="ac-icon">🔎</span> ${match}
                <span style="margin-left:auto; font-size:11px; color:#5a7a52">${termFrequency[match]} occurrences</span>
            </div>
        `).join('');
        elements.dropdown.classList.add('active');
    }

    // --- SEARCH LOGIC ---
    function setOperator(op) {
        state.operator = op;
        elements.opAnd.className = op === 'AND' ? 'op-btn active' : 'op-btn';
        elements.opOr.className = op === 'OR' ? 'op-btn active' : 'op-btn';
        if (state.currentQuery) executeSearch(state.currentQuery);
    }

    function quickSearch(query) {
        elements.input.value = query;
        executeSearch(query);
    }

    function clearFilters() {
        document.querySelectorAll('.tag-filter').forEach(cb => cb.checked = true);
        if (state.currentQuery) executeSearch(state.currentQuery);
        if (typeof showToast === 'function') showToast('Filters cleared', 'info');
    }

    function executeSearch(queryOverride) {
        const query = queryOverride || elements.input.value.trim();
        if (!query) return;

        state.currentQuery = query;
        elements.dropdown.classList.remove('active');
        elements.emptyState.style.display = 'none';
        
        // Add to recent
        if (!state.recentSearches.includes(query)) {
            state.recentSearches.unshift(query);
            if (state.recentSearches.length > 4) state.recentSearches.pop();
            renderRecentSearches();
        }

        const startTime = performance.now();
        const searchTerms = query.toLowerCase().match(/\b[a-z]+\b/g) || [];
        
        // Get active filters
        const activeTags = Array.from(document.querySelectorAll('.tag-filter'))
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        // Score documents
        const scores = {};
        const matchedTermsPerDoc = {};

        documents.forEach(doc => {
            scores[doc.id] = 0;
            matchedTermsPerDoc[doc.id] = [];
        });

        searchTerms.forEach(term => {
            if (invertedIndex[term]) {
                for (const [docId, count] of Object.entries(invertedIndex[term])) {
                    scores[docId] += count; // Simple TF scoring
                    matchedTermsPerDoc[docId].push(term);
                }
            }
        });

        // Filter and Rank
        let results = documents.filter(doc => {
            // Apply tag filter
            if (!doc.tags.some(tag => activeTags.includes(tag))) return false;
            
            const matchedTerms = matchedTermsPerDoc[doc.id];
            if (state.operator === 'AND') {
                return searchTerms.every(term => matchedTerms.includes(term));
            } else {
                return matchedTerms.length > 0;
            }
        });

        results.sort((a, b) => scores[b.id] - scores[a.id]);

        const endTime = performance.now();
        const timeMs = (endTime - startTime).toFixed(1);

        renderResults(results, searchTerms, scores, matchedTermsPerDoc, timeMs);
        
        if (results.length > 0) {
            generateRAGSummary(results, searchTerms);
        } else {
            elements.ragPanel.classList.remove('active');
        }
    }

    function renderRecentSearches() {
        elements.recentContainer.innerHTML = state.recentSearches.map(q => 
            `<span class="chip" onclick="window.searchApp.quickSearch('${q}')">${q}</span>`
        ).join('');
    }

    function renderResults(results, terms, scores, matchedTermsPerDoc, timeMs) {
        elements.resultsMeta.style.display = 'block';
        elements.resultsMeta.textContent = `Found ${results.length} result(s) in ${timeMs}ms using ${state.operator} logic`;

        if (results.length === 0) {
            elements.resultsList.innerHTML = `<div style="text-align:center; padding: 40px; color: #9cb896;">No matching documents found. Try adjusting filters or search terms.</div>`;
            return;
        }

        const maxScore = Math.max(...results.map(r => scores[r.id]));

        elements.resultsList.innerHTML = results.map((doc, index) => {
            const score = scores[doc.id];
            const scorePct = Math.round((score / maxScore) * 100);
            const matchedTerms = matchedTermsPerDoc[doc.id];
            
            // Highlight abstract
            let highlightedAbstract = doc.abstract;
            terms.forEach(term => {
                const regex = new RegExp(`\\b(${term})\\b`, 'gi');
                highlightedAbstract = highlightedAbstract.replace(regex, '<span class="highlight">$1</span>');
            });

            const termBadges = matchedTerms.map(t => `<span class="term-badge">${t}</span>`).join('');

            return `
                <div class="result-card" style="animation-delay: ${index * 0.1}s">
                    <div class="res-title">${doc.title}</div>
                    <div class="res-authors">${doc.authors}</div>
                    <div class="res-abstract">${highlightedAbstract}</div>
                    <div class="res-footer">
                        <div class="res-terms">${termBadges}</div>
                        <div class="res-score">
                            Relevance: 
                            <div class="score-bar"><div class="score-fill" style="width:${scorePct}%"></div></div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    function generateRAGSummary(results, terms) {
        // Simple template-based RAG simulation based on top 2 results
        const topDocs = results.slice(0, 2);
        
        let summaryText = `Based on the retrieved literature, `;
        
        if (terms.includes('fusarium') || terms.includes('wilt') || terms.includes('biocontrol')) {
            summaryText += `Fusarium wilt is a major issue managed via biocontrol agents like Trichoderma harzianum and Bacillus subtilis, which serve as alternatives to chemical fungicides. `;
        } else if (terms.includes('machine') || terms.includes('cnn') || terms.includes('detection')) {
            summaryText += `CNN-based machine learning approaches, specifically utilizing transfer learning with architectures like ResNet50, demonstrate high accuracy (up to 96.2%) for early detection of basil diseases via image analysis. `;
        } else if (terms.includes('downy') || terms.includes('mildew')) {
            summaryText += `Downy mildew, primarily caused by Peronospora belbahrii, manifests as yellowing leaves and requires management through resistant cultivars and fungicide applications. `;
        } else {
            // Generic synthesis
            const combinedSnippets = topDocs.map(d => {
                const sentences = d.abstract.split('. ');
                return sentences[sentences.length > 1 ? 1 : 0].replace('.', '');
            }).join(' Additionally, ');
            summaryText += combinedSnippets + ".";
        }
        
        summaryText += ` <br><br><span style="color:#9cb896; font-size:13px;"><em>Note: This synthesis combines findings from the top-ranked papers in the inverted index.</em></span>`;

        elements.ragText.innerHTML = summaryText;
        elements.ragBadge.textContent = `Synthesized from top ${topDocs.length} source(s)`;
        elements.ragPanel.classList.add('active');
    }

    // Run
    init();
})();
</script>
"""

display(HTML(HTML_CONTENT))
print("✅ Search Engine Query Screen loaded successfully!")
