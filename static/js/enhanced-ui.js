// 增强UI交互效果
document.addEventListener('DOMContentLoaded', function() {
    // 添加粒子动画效果
    createHeroParticles();
    
    // 添加滚动动画
    initScrollAnimations();
    
    // 添加悬停效果
    initHoverEffects();
    
    // 添加动态背景
    initDynamicBackground();
});

// 创建英雄区域粒子动画
function createHeroParticles() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;
    
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    particleContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    `;
    
    heroSection.appendChild(particleContainer);
    
    // 创建粒子
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 10 + 2}px;
            height: ${Math.random() * 10 + 2}px;
            background: rgba(${Math.random() > 0.5 ? '255,255,255' : '167,243,208'}, ${Math.random() * 0.4 + 0.1});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float-${Math.floor(Math.random() * 3)} 6s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        
        // 添加不同的浮动动画
        const keyframes = `
            @keyframes float-0 {
                0%, 100% { transform: translate(0, 0) rotate(0deg); opacity: 0.6; }
                50% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(180deg); opacity: 1; }
            }
            @keyframes float-1 {
                0%, 100% { transform: translate(0, 0) scale(1); }
                50% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(1.2); }
            }
            @keyframes float-2 {
                0%, 100% { transform: translate(0, 0) rotate(0deg) scale(1); }
                25% { transform: translate(${Math.random() * 80 - 40}px, ${Math.random() * 80 - 40}px) rotate(90deg) scale(1.1); }
                50% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(180deg) scale(0.9); }
                75% { transform: translate(${Math.random() * 80 - 40}px, ${Math.random() * 80 - 40}px) rotate(270deg) scale(1.05); }
            }
        `;
        
        const style = document.createElement('style');
        style.textContent = keyframes;
        document.head.appendChild(style);
        
        particleContainer.appendChild(particle);
    }
}

// 初始化滚动动画
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(30px)';
                
                // 延迟一点开始动画，创造交错效果
                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, Math.random() * 300);
            }
        });
    }, observerOptions);
    
    // 观察所有卡片元素
    document.querySelectorAll('.modality-card, .category-card, .stat-card, .card').forEach(card => {
        observer.observe(card);
    });
}

// 初始化悬停效果
function initHoverEffects() {
    // 为所有可悬停元素添加波纹效果
    document.querySelectorAll('.btn, .modality-card, .category-card, .stat-card, .card, .nav-link').forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            // 添加波纹效果
            const ripple = document.createElement('span');
            const rect = element.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
                z-index: 1000;
            `;
            
            element.style.position = 'relative';
            element.appendChild(ripple);
            
            // 移除波纹元素
            setTimeout(() => {
                if (ripple.parentNode) {
                    ripple.parentNode.removeChild(ripple);
                }
            }, 600);
        });
    });
    
    // 添加涟漪动画
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
}

// 初始化动态背景
function initDynamicBackground() {
    // 为整个页面添加微妙的动态背景
    const dynamicBgStyle = document.createElement('style');
    dynamicBgStyle.textContent = `
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.05) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.05) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.05) 0%, transparent 70%);
            z-index: -1;
            animation: bgMove 20s ease-in-out infinite alternate;
            pointer-events: none;
        }
        
        @keyframes bgMove {
            0% { transform: scale(1) rotate(0deg); }
            100% { transform: scale(1.1) rotate(1deg); }
        }
    `;
    document.head.appendChild(dynamicBgStyle);
}

// 添加进度条动画
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const targetWidth = bar.dataset.target || 100;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 2s ease-in-out';
            bar.style.width = targetWidth + '%';
        }, 300);
    });
}

// 页面加载完成后执行
window.addEventListener('load', function() {
    // 延迟执行动画，确保页面完全加载
    setTimeout(() => {
        animateProgressBars();
    }, 500);
});

// 添加视差滚动效果
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.hero-background, .brain-animation');
    
    parallaxElements.forEach(element => {
        const speed = element.dataset.speed || 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});