/**
 * Database marquee functionality
 * Efficient infinite scroll carousel for database icons
 */
class DatabaseMarquee {
    constructor() {
        this.dbConfig = {
            postgresql: { name: 'PostgreSQL', extra: 'postgresql' },
            mysql: { name: 'MySQL', extra: 'mysql' },
            sqlite: { name: 'SQLite', extra: 'sqlite' },
            snowflake: { name: 'Snowflake', extra: 'snowflake' },
            bigquery: { name: 'BigQuery', extra: 'bigquery' },
            databricks: { name: 'Databricks', extra: 'databricks' },
            duckdb: { name: 'DuckDB', extra: 'duckdb' }
        };
        
        this.currentDb = 'postgresql';
        this.highlightTimeout = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupMarqueeClickHandlers();
        this.setupModelsClickHandlers();
        this.duplicateIcons();
        this.duplicateModels();
    }
    
    setupEventListeners() {
        const icons = document.querySelectorAll('.db-icon');
        const dbName = document.getElementById('db-name');
        const installCommand = document.getElementById('install-command');
        const installSection = document.getElementById('install-section');
        
        if (!dbName || !installCommand || !installSection) return;
        
        icons.forEach(icon => {
            icon.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleIconClick(icon, dbName, installCommand, installSection);
            });
            
            // Add keyboard navigation
            icon.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.handleIconClick(icon, dbName, installCommand, installSection);
                }
            });
            
            // Make icons focusable
            icon.setAttribute('tabindex', '0');
            icon.setAttribute('role', 'button');
        });
    }
    
    handleIconClick(icon, dbName, installCommand, installSection) {
        const extra = icon.dataset.extra;
        const config = this.dbConfig[extra];
        
        if (!config) return;
        
        // Update active state
        document.querySelectorAll('.db-icon').forEach(i => i.classList.remove('active'));
        icon.classList.add('active');
        
        // Update content
        dbName.textContent = config.name;
        installCommand.textContent = `pip install toolfront[${config.extra}]`;
        
        // Highlight install section
        this.highlightInstallSection(installSection);
        
        // Store current selection
        this.currentDb = extra;
    }
    
    highlightInstallSection(installSection) {
        // Clear previous timeout
        if (this.highlightTimeout) {
            clearTimeout(this.highlightTimeout);
        }
        
        installSection.classList.add('highlight');
        
        this.highlightTimeout = setTimeout(() => {
            installSection.classList.remove('highlight');
        }, 300);
    }
    
    setupMarqueeClickHandlers() {
        const marqueeItems = document.querySelectorAll('.db-marquee-item');
        
        marqueeItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const dbType = item.dataset.db;
                if (dbType) {
                    const url = `documentation/databases/${dbType}/`;
                    window.location.href = url;
                }
            });
            
            // Add keyboard navigation
            item.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const dbType = item.dataset.db;
                    if (dbType) {
                        const url = `documentation/databases/${dbType}/`;
                        window.location.href = url;
                    }
                }
            });
            
            // Make items focusable for accessibility
            item.setAttribute('tabindex', '0');
            item.setAttribute('role', 'button');
            item.setAttribute('aria-label', `Learn more about ${item.querySelector('img').alt}`);
        });
    }
    
    setupModelsClickHandlers() {
        const modelsItems = document.querySelectorAll('.models-marquee-item');
        
        modelsItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const modelType = item.dataset.model;
                if (modelType) {
                    const url = `documentation/ai_models/${modelType}/`;
                    window.location.href = url;
                }
            });
            
            // Add keyboard navigation
            item.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const modelType = item.dataset.model;
                    if (modelType) {
                        const url = `documentation/ai_models/${modelType}/`;
                        window.location.href = url;
                    }
                }
            });
            
            // Make items focusable for accessibility
            item.setAttribute('tabindex', '0');
            item.setAttribute('role', 'button');
            item.setAttribute('aria-label', `Learn more about ${item.querySelector('img').alt}`);
        });
    }
    
    duplicateIcons() {
        const marqueeTrack = document.querySelector('.db-marquee-track');
        if (!marqueeTrack) return;
        
        // Clone all items to create seamless loop
        const items = marqueeTrack.querySelectorAll('.db-marquee-item');
        items.forEach(item => {
            const clone = item.cloneNode(true);
            marqueeTrack.appendChild(clone);
        });
        
        // Re-setup click handlers for cloned items
        this.setupMarqueeClickHandlers();
    }
    
    duplicateModels() {
        const modelsTrack = document.querySelector('.models-marquee-track');
        if (!modelsTrack) return;
        
        // Clone all items to create seamless loop
        const items = modelsTrack.querySelectorAll('.models-marquee-item');
        items.forEach(item => {
            const clone = item.cloneNode(true);
            modelsTrack.appendChild(clone);
        });
        
        // Re-setup click handlers for cloned items
        this.setupModelsClickHandlers();
    }
    
    // Method to programmatically select a database
    selectDatabase(dbKey) {
        const icon = document.querySelector(`[data-extra="${dbKey}"]`);
        if (icon) {
            const dbName = document.getElementById('db-name');
            const installCommand = document.getElementById('install-command');
            const installSection = document.getElementById('install-section');
            
            if (dbName && installCommand && installSection) {
                this.handleIconClick(icon, dbName, installCommand, installSection);
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const marquee = new DatabaseMarquee();
    
    // Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-quad',
            once: false, // Allow animations to repeat
            mirror: true, // Animate out when scrolling past
            offset: 120,
            delay: 0,
            anchorPlacement: 'top-bottom',
            disable: false,
            startEvent: 'DOMContentLoaded',
            initClassName: 'aos-init',
            animatedClassName: 'aos-animate',
            useClassNames: false,
            disableMutationObserver: false,
            debounceDelay: 50,
            throttleDelay: 99
        });
        
        // Refresh AOS when window is resized
        window.addEventListener('resize', () => {
            AOS.refresh();
        });
        
        // Force refresh after a short delay to ensure proper initialization
        setTimeout(() => {
            AOS.refresh();
        }, 100);
    }
    
    // Expose to global scope for potential external control
    window.DatabaseMarquee = marquee;
});