/**
 * Database marquee functionality
 * Efficient infinite scroll carousel for database icons
 */
class DatabaseMarquee {
    constructor() {
        this.dbConfig = {
            postgres: { name: 'Postgres', extra: 'postgres' },
            mysql: { name: 'MySQL', extra: 'mysql' },
            sqlite: { name: 'SQLite', extra: 'sqlite' },
            snowflake: { name: 'Snowflake', extra: 'snowflake' },
            bigquery: { name: 'BigQuery', extra: 'bigquery' },
            databricks: { name: 'Databricks', extra: 'databricks' },
            duckdb: { name: 'DuckDB', extra: 'duckdb' }
        };
        
        this.currentDb = 'postgres';
        this.highlightTimeout = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupMarqueeClickHandlers();
        this.setupModelsClickHandlers();
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
    
    // Initialize marquees with bulletproof infinite scroll
    function initializeMarquees() {
        const dbTrack = document.querySelector('.db-marquee-track');
        const modelsTrack = document.querySelector('.models-marquee-track');
        
        // Proven infinite scroll marquee setup
        function setupInfiniteMarquee(track, direction = 'left', speed = 5) {
            if (!track) return;
            
            // Clone all items multiple times for seamless loop
            const originalItems = Array.from(track.children);
            const cloneCount = 3; // Clone 3 times for safety
            
            for (let i = 0; i < cloneCount; i++) {
                originalItems.forEach(item => {
                    const clone = item.cloneNode(true);
                    track.appendChild(clone);
                });
            }
            
            // Re-setup click handlers for all items (including clones)
            const allItems = Array.from(track.children);
            allItems.forEach(item => {
                // Remove any existing listeners to avoid duplicates
                item.replaceWith(item.cloneNode(true));
            });
            
            // Get fresh references after cloning
            const freshItems = Array.from(track.children);
            freshItems.forEach(item => {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    const dbType = item.dataset.db;
                    const modelType = item.dataset.model;
                    
                    if (dbType) {
                        const url = `documentation/databases/${dbType}/`;
                        window.location.href = url;
                    } else if (modelType) {
                        const url = `documentation/ai_models/${modelType}/`;
                        window.location.href = url;
                    }
                });
                
                // Add keyboard navigation
                item.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        const dbType = item.dataset.db;
                        const modelType = item.dataset.model;
                        
                        if (dbType) {
                            const url = `documentation/databases/${dbType}/`;
                            window.location.href = url;
                        } else if (modelType) {
                            const url = `documentation/ai_models/${modelType}/`;
                            window.location.href = url;
                        }
                    }
                });
                
                // Make items focusable for accessibility
                item.setAttribute('tabindex', '0');
                item.setAttribute('role', 'button');
                const img = item.querySelector('img');
                if (img) {
                    item.setAttribute('aria-label', `Learn more about ${img.alt}`);
                }
            });
            
            // Use transform animation with JavaScript for perfect control
            let position = 0;
            const itemWidth = 108; // 48px icon + 60px gap
            const totalOriginalWidth = originalItems.length * itemWidth;
            
            function animate() {
                if (direction === 'left') {
                    position -= speed;
                    if (position <= -totalOriginalWidth) {
                        position = 0; // Reset to start
                    }
                } else {
                    position += speed;
                    if (position >= totalOriginalWidth) {
                        position = 0; // Reset to start
                    }
                }
                
                track.style.transform = `translateX(${position}px)`;
                requestAnimationFrame(animate);
            }
            
            // Start animation
            requestAnimationFrame(animate);
            
            // Pause on hover
            const marqueeContainer = track.parentElement;
            marqueeContainer.addEventListener('mouseenter', () => {
                track.style.animationPlayState = 'paused';
            });
            marqueeContainer.addEventListener('mouseleave', () => {
                track.style.animationPlayState = 'running';
            });
        }
        
        setupInfiniteMarquee(dbTrack, 'left', 0.5);
        setupInfiniteMarquee(modelsTrack, 'right', 0.5);
    }
    
    // Call initialization
    setTimeout(initializeMarquees, 100);
    
    // Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-quad',
            once: false,
            mirror: true,
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
        
        window.addEventListener('resize', () => {
            AOS.refresh();
        });
        
        setTimeout(() => {
            AOS.refresh();
        }, 100);
    }
    
    // Expose to global scope for potential external control
    window.DatabaseMarquee = marquee;
});