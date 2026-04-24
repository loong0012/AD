/**
 * 加载状态管理器
 * 提供增强的加载状态指示和消息提示功能
 */

class LoadingManager {
    constructor() {
        this.loadingElements = new Map();
        this.toastQueue = [];
        this.isShowingToast = false;
    }

    /**
     * 显示加载指示器
     * @param {string} elementId - 元素ID
     * @param {string} message - 加载消息
     * @param {boolean} showOverlay - 是否显示遮罩层
     */
    showLoading(elementId, message = '加载中...', showOverlay = false) {
        const element = document.getElementById(elementId);
        if (!element) return;

        // 保存原始内容
        const originalContent = element.innerHTML;
        this.loadingElements.set(elementId, { originalContent });

        // 创建加载指示器
        const loadingHTML = `
            <div class="loading-container ${showOverlay ? 'loading-overlay' : ''}">
                <div class="loading-spinner"></div>
                <div class="loading-message">${message}</div>
            </div>
        `;

        element.innerHTML = loadingHTML;
        element.classList.add('loading-active');
    }

    /**
     * 隐藏加载指示器
     * @param {string} elementId - 元素ID
     */
    hideLoading(elementId) {
        const element = document.getElementById(elementId);
        if (!element || !this.loadingElements.has(elementId)) return;

        const savedData = this.loadingElements.get(elementId);
        element.innerHTML = savedData.originalContent;
        element.classList.remove('loading-active');
        this.loadingElements.delete(elementId);
    }

    /**
     * 更新进度条
     * @param {string} elementId - 进度条元素ID
     * @param {number} percentage - 进度百分比 (0-100)
     */
    updateProgress(elementId, percentage) {
        const progressFill = document.getElementById(elementId);
        if (!progressFill) return;

        percentage = Math.max(0, Math.min(100, percentage));
        progressFill.style.width = `${percentage}%`;
        progressFill.setAttribute('aria-valuenow', percentage);
    }

    /**
     * 显示进度步骤
     * @param {number} currentStep - 当前步骤索引
     */
    updateProgressSteps(currentStep) {
        const steps = document.querySelectorAll('.progress-steps .step');
        steps.forEach((step, index) => {
            if (index< currentStep) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (index === currentStep) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });
    }

    /**
     * 显示消息提示
     * @param {string} message - 消息内容
     * @param {string} type - 消息类型: success, error, info, warning
     * @param {number} duration - 显示时长(毫秒)
     */
    showToast(message, type = 'info', duration = 5000) {
        const toastData = { message, type, duration };
        
        // 如果已有toast在显示，加入队列
        if (this.isShowingToast) {
            this.toastQueue.push(toastData);
            return;
        }

        this._showToastNow(toastData);
    }

    /**
     * 立即显示toast消息
     * @private
     */
    _showToastNow(toastData) {
        this.isShowingToast = true;
        const { message, type, duration } = toastData;

        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        // 根据类型设置图标和样式
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            info: 'fas fa-info-circle',
            warning: 'fas fa-exclamation-triangle'
        };

        const colors = {
            success: '#10b981',
            error: '#ef4444',
            info: '#3b82f6',
            warning: '#f59e0b'
        };

        toast.innerHTML = `
            <div class="toast-icon" style="color: ${colors[type]};">
                <i class="${icons[type]}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;

        container.appendChild(toast);

        // 添加显示动画
        setTimeout(() => {
            toast.classList.add('toast-show');
        }, 10);

        // 自动移除
        setTimeout(() => {
            toast.classList.remove('toast-show');
            setTimeout(() => {
                toast.remove();
                this.isShowingToast = false;
                
                // 显示队列中的下一个toast
                if (this.toastQueue.length > 0) {
                    const nextToast = this.toastQueue.shift();
                    this._showToastNow(nextToast);
                }
            }, 300);
        }, duration);
    }

    /**
     * 显示成功消息
     * @param {string} message - 消息内容
     * @param {number} duration - 显示时长
     */
    showSuccess(message, duration = 4000) {
        this.showToast(message, 'success', duration);
    }

    /**
     * 显示错误消息
     * @param {string} message - 消息内容
     * @param {number} duration - 显示时长
     */
    showError(message, duration = 6000) {
        this.showToast(message, 'error', duration);
    }

    /**
     * 显示信息消息
     * @param {string} message - 消息内容
     * @param {number} duration - 显示时长
     */
    showInfo(message, duration = 5000) {
        this.showToast(message, 'info', duration);
    }

    /**
     * 显示警告消息
     * @param {string} message - 消息内容
     * @param {number} duration - 显示时长
     */
    showWarning(message, duration = 5000) {
        this.showToast(message, 'warning', duration);
    }
}

// 创建全局加载管理器实例
const loadingManager = new LoadingManager();

// 兼容旧的showToast函数
function showToast(message, type = 'info') {
    loadingManager.showToast(message, type);
}

// 添加CSS样式
const style = document.createElement('style');
style.textContent = `
    /* 加载指示器样式 */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        min-height: 200px;
    }

    .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.9);
        z-index: 1000;
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .loading-message {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
    }

    /* Toast消息样式 */
    #toast-container {
        position: fixed;
        top: 2rem;
        right: 2rem;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .toast {
        display: flex;
        align-items: center;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        padding: 1rem 1.5rem;
        min-width: 300px;
        max-width: 400px;
        transform: translateX(100%);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 4px solid #3b82f6;
    }

    .toast-success {
        border-left-color: #10b981;
    }

    .toast-error {
        border-left-color: #ef4444;
    }

    .toast-warning {
        border-left-color: #f59e0b;
    }

    .toast-show {
        transform: translateX(0);
        opacity: 1;
    }

    .toast-icon {
        margin-right: 1rem;
        font-size: 1.25rem;
        flex-shrink: 0;
    }

    .toast-content {
        flex: 1;
    }

    .toast-message {
        font-size: 0.875rem;
        line-height: 1.5;
        color: #374151;
    }

    .toast-close {
        background: none;
        border: none;
        color: #6b7280;
        cursor: pointer;
        padding: 0.25rem;
        margin-left: 1rem;
        border-radius: 0.25rem;
        transition: all 0.2s;
    }

    .toast-close:hover {
        background: #f3f4f6;
        color: #374151;
    }

    /* 进度条增强样式 */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e5e7eb;
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #10b981);
        border-radius: 4px;
        transition: width 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: progress-shine 2s infinite;
    }

    @keyframes progress-shine {
        100% { left: 100%; }
    }

    .progress-steps {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }

    .progress-steps .step {
        flex: 1;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.75rem;
        color: #9ca3af;
        border-bottom: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }

    .progress-steps .step.active {
        color: #3b82f6;
        border-bottom-color: #3b82f6;
        font-weight: 600;
    }

    .progress-steps .step.completed {
        color: #10b981;
        border-bottom-color: #10b981;
    }
`;
document.head.appendChild(style);
