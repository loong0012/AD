/**
 * AD-CPredSys 可视化增强脚本
 * 用于增强数据可视化和界面视觉效果
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('📊 可视化增强模块已加载');
    
    // 初始化可视化增强功能
    initVisualizationEnhancements();
    
    // 监听结果加载事件
    window.addEventListener('resultsLoaded', function(e) {
        enhanceResultVisualizations(e.detail.results);
    });
});

/**
 * 初始化可视化增强功能
 */
function initVisualizationEnhancements() {
    // 添加动画效果到风险指标
    animateRiskIndicators();
    
    // 初始化图表动画
    initChartAnimations();
    
    // 添加交互式视觉反馈
    addInteractiveEffects();
    
    console.log('🎨 可视化增强功能初始化完成');
}

/**
 * 动画化风险指标
 */
function animateRiskIndicators() {
    // 监听风险指标卡片的出现并添加动画
    const observerOptions = {
        threshold: 0.1
    };
    
    const riskObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const indicators = entry.target.querySelectorAll('.risk-indicator');
                indicators.forEach((indicator, index) => {
                    setTimeout(() => {
                        indicator.style.opacity = '0';
                        indicator.style.transform = 'translateY(20px)';
                        indicator.style.transition = 'all 0.6s ease';
                        
                        setTimeout(() => {
                            indicator.style.opacity = '1';
                            indicator.style.transform = 'translateY(0)';
                        }, index * 100);
                    }, 100);
                });
                
                riskObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // 观察风险指标区域
    const riskSections = document.querySelectorAll('.risk-indicators');
    riskSections.forEach(section => riskObserver.observe(section));
}

/**
 * 初始化图表动画
 */
function initChartAnimations() {
    // 动画化概率条
    const probabilityObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateProbabilityBars(entry.target);
                probabilityObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    // 观察概率分布区域
    const probabilitySections = document.querySelectorAll('.probabilities');
    probabilitySections.forEach(section => probabilityObserver.observe(section));
}

/**
 * 动画化概率条
 */
function animateProbabilityBars(container) {
    const probabilityItems = container.querySelectorAll('.probability-item');
    probabilityItems.forEach((item, index) => {
        const fillElement = item.querySelector('.probability-fill');
        if (fillElement) {
            const targetWidth = fillElement.style.width;
            
            // 重置宽度为0
            fillElement.style.width = '0%';
            
            // 动画展开
            setTimeout(() => {
                fillElement.style.width = targetWidth;
            }, index * 200);
        }
    });
}

/**
 * 添加交互式视觉效果
 */
function addInteractiveEffects() {
    // 为热力图容器添加悬停效果
    const heatmapContainers = document.querySelectorAll('.heatmap-container');
    heatmapContainers.forEach(container => {
        container.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0,0,0,0.3)';
        });
        
        container.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'var(--shadow-lg)';
        });
    });
    
    // 为建议项目添加点击效果
    const adviceItems = document.querySelectorAll('.advice-list li');
    adviceItems.forEach(item => {
        item.addEventListener('click', function() {
            this.style.transform = 'scale(1.02)';
            this.style.backgroundColor = 'rgba(15, 118, 110, 0.1)';
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
                this.style.backgroundColor = '';
            }, 200);
        });
    });
}

/**
 * 增强结果可视化
 */
function enhanceResultVisualizations(results) {
    console.log('🔍 增强结果可视化');
    
    // 如果结果包含热力图，优化显示
    if (results.results && results.results.heatmap_image) {
        optimizeHeatmapDisplay();
    }
    
    // 增强风险指标可视化
    enhanceRiskIndicators(results.results);
    
    // 增强概率分布可视化
    enhanceProbabilityDistribution(results.results);
    
    // 应用渐进式显示效果
    applyProgressiveReveal();
}

/**
 * 优化热力图显示
 */
function optimizeHeatmapDisplay() {
    const heatmapImages = document.querySelectorAll('.heatmap-image');
    heatmapImages.forEach(img => {
        // 添加加载动画
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.5s ease';
        
        img.onload = function() {
            this.style.opacity = '1';
        };
    });
}

/**
 * 增强风险指标显示
 */
function enhanceRiskIndicators(resultData) {
    if (!resultData || !resultData.risk_indicators) return;
    
    const riskIndicators = document.querySelectorAll('.risk-indicator');
    riskIndicators.forEach((indicator, index) => {
        // 添加数值动画
        const valueElement = indicator.querySelector('.risk-value');
        if (valueElement) {
            const finalValue = parseFloat(valueElement.textContent);
            animateNumber(valueElement, 0, finalValue, 2000);
        }
    });
}

/**
 * 增强概率分布显示
 */
function enhanceProbabilityDistribution(resultData) {
    if (!resultData || !resultData.probabilities) return;
    
    const probabilityItems = document.querySelectorAll('.probability-item');
    probabilityItems.forEach(item => {
        const fillElement = item.querySelector('.probability-fill');
        const valueElement = item.querySelector('.probability-value');
        
        if (fillElement && valueElement) {
            // 添加百分比动画
            const finalValue = parseFloat(valueElement.textContent);
            animatePercentage(valueElement, 0, finalValue, 2500);
        }
    });
}

/**
 * 数值动画
 */
function animateNumber(element, start, end, duration) {
    let startTime = null;
    
    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        
        const currentValue = start + (end - start) * progress;
        element.textContent = currentValue.toFixed(1);
        
        if (progress < 1) {
            requestAnimationFrame(animation);
        } else {
            element.textContent = end.toFixed(1);
        }
    }
    
    requestAnimationFrame(animation);
}

/**
 * 百分比动画
 */
function animatePercentage(element, start, end, duration) {
    let startTime = null;
    
    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        
        const currentValue = start + (end - start) * progress;
        element.textContent = currentValue.toFixed(1) + '%';
        
        if (progress < 1) {
            requestAnimationFrame(animation);
        } else {
            element.textContent = end.toFixed(1) + '%';
        }
    }
    
    requestAnimationFrame(animation);
}

/**
 * 应用渐进式显示效果
 */
function applyProgressiveReveal() {
    const resultSections = document.querySelectorAll('.diagnosis-result, .risk-indicators, .probabilities, .advice-list, .heatmap-section');
    resultSections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

/**
 * 创建可视化图表
 */
function createVisualizations(data) {
    // 如果浏览器支持Canvas，则创建更高级的可视化
    if (typeof Chart !== 'undefined') {
        createAdvancedCharts(data);
    } else {
        createSimpleVisualizations(data);
    }
}

/**
 * 创建简单可视化
 */
function createSimpleVisualizations(data) {
    console.log('📈 创建简单可视化图表');
    
    // 创建环形进度指示器（如果需要）
    const indicators = document.querySelectorAll('.risk-indicator');
    indicators.forEach(indicator => {
        const value = parseFloat(indicator.querySelector('.risk-value')?.textContent || 0);
        const level = indicator.className.includes('high') ? 'high' : 
                     indicator.className.includes('medium') ? 'medium' : 'low';
        
        // 添加视觉增强
        const enhancedIndicator = document.createElement('div');
        enhancedIndicator.className = `risk-visualizer ${level}`;
        enhancedIndicator.innerHTML = `
            <svg width="60" height="60" viewBox="0 0 60 60">
                <circle cx="30" cy="30" r="25" fill="none" stroke="#e2e8f0" stroke-width="4"/>
                <circle cx="30" cy="30" r="25" fill="none" stroke="currentColor" stroke-width="4" 
                        stroke-dasharray="${2 * Math.PI * 25}" 
                        stroke-dashoffset="${2 * Math.PI * 25 * (1 - value/100)}" 
                        transform="rotate(-90 30 30)" 
                        class="${level}-stroke"/>
            </svg>
            <span class="risk-percent">${value}%</span>
        `;
        
        indicator.appendChild(enhancedIndicator);
    });
}

// 全局函数，供其他脚本调用
window.VisualizationEnhancer = {
    init: initVisualizationEnhancements,
    enhanceResults: enhanceResultVisualizations,
    createVisualizations: createVisualizations
};