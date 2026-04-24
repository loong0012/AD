// 主JavaScript文件
console.log('=== JavaScript文件开始加载 ===');

// 性能优化工具函数

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 图片懒加载（如果将来添加图片）
function initImageLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

// 显示通知函数
window.showNotification = function(message, type = 'info') {
    if (typeof loadingManager !== 'undefined') {
        loadingManager.showToast(message, type);
    } else {
        console.log('loadingManager not available:', message);
    }
};

// 显示加载
window.showLoading = function(message = '加载中...') {
    // 创建一个临时的加载容器
    const loadingContainer = document.createElement('div');
    loadingContainer.id = 'temp-loading';
    loadingContainer.style.position = 'fixed';
    loadingContainer.style.top = '0';
    loadingContainer.style.left = '0';
    loadingContainer.style.width = '100%';
    loadingContainer.style.height = '100%';
    loadingContainer.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
    loadingContainer.style.display = 'flex';
    loadingContainer.style.alignItems = 'center';
    loadingContainer.style.justifyContent = 'center';
    loadingContainer.style.zIndex = '9999';
    loadingContainer.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-message">${message}</div>
        </div>
    `;
    document.body.appendChild(loadingContainer);
};

// 隐藏加载
window.hideLoading = function() {
    const loadingContainer = document.getElementById('temp-loading');
    if (loadingContainer) {
        loadingContainer.remove();
    }
};

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOMContentLoaded事件触发 ===');
    console.log('AD-CPredSys系统初始化...'); // 修改系统名称
    
    // 检查loadingManager是否存在
    console.log('loadingManager存在:', typeof loadingManager !== 'undefined');
    
    // 初始化认证系统
    console.log('开始初始化认证系统...');
    initAuthSystem();
    
    // 初始化组件
    console.log('开始初始化导航...');
    initNavigation();
    console.log('开始初始化按钮...');
    initButtons();
    console.log('开始初始化文件上传...');
    initFileUpload();
    console.log('开始初始化表单验证...');
    initFormValidation();
    console.log('开始初始化模态框...');
    initModal();
    console.log('开始初始化数据管理...');
    initDataManagement();
    console.log('开始初始化报告设置模态框...');
    initReportSettingsModal();
    
    // 初始化图片懒加载
    console.log('开始初始化图片懒加载...');
    initImageLazyLoading();
    
    // 初始化报告搜索防抖
    console.log('开始初始化报告搜索防抖...');
    const searchInput = document.getElementById('report-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            if (this.value.trim()) {
                searchReports();
            } else {
                clearReportSearch();
            }
        }, 300));
    }
    
    // 加载统计数据
    console.log('开始加载统计数据...');
    loadSystemStats();
    
    // 检查登录状态
    console.log('检查登录状态...');
    checkLoginStatus();
    
    // 显示欢迎消息
    console.log('显示欢迎消息...');
    if (typeof loadingManager !== 'undefined') {
        loadingManager.showSuccess('AD-CPredSys多模态分析系统已就绪');
    } else {
        console.error('loadingManager未定义');
    }
    
    // 添加粒子背景
    console.log('添加粒子背景...');
    createParticles();
    
    console.log('=== 系统初始化完成 ===');
});

// 认证系统初始化
function initAuthSystem() {
    console.log('初始化认证系统...');
    
    // 角色选择事件
    const roleCards = document.querySelectorAll('.role-card');
    if (roleCards.length > 0) {
        console.log('找到角色卡片:', roleCards.length);
        roleCards.forEach(card => {
            card.addEventListener('click', function() {
                // 移除其他卡片的选中状态
                roleCards.forEach(c => c.classList.remove('selected'));
                // 添加当前卡片的选中状态
                this.classList.add('selected');
                console.log('选择角色:', this.dataset.role);
            });
        });
    }
    
    // 登录表单提交
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        console.log('找到登录表单');
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('登录表单提交');
            await handleLogin();
        });
    }
    
    // 注册表单提交
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        console.log('找到注册表单');
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('注册表单提交');
            await handleRegister();
        });
    }
    
    // 页面切换
    const switchToRegisterBtn = document.getElementById('switch-to-register');
    if (switchToRegisterBtn) {
        console.log('找到切换到注册按钮');
        switchToRegisterBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('切换到注册页面');
            switchToRegister();
        });
    }
    
    const switchToLoginBtn = document.getElementById('switch-to-login');
    if (switchToLoginBtn) {
        console.log('找到切换到登录按钮');
        switchToLoginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('切换到登录页面');
            switchToLogin();
        });
    }
    
    // 登录/注册按钮
    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        console.log('找到登录按钮');
        loginBtn.addEventListener('click', function() {
            console.log('点击登录按钮');
            showLoginPage();
        });
    }
    
    const registerBtn = document.getElementById('register-btn');
    if (registerBtn) {
        console.log('找到注册按钮');
        registerBtn.addEventListener('click', function() {
            console.log('点击注册按钮');
            showRegisterPage();
        });
    }
    
    // 登出按钮
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        console.log('找到登出按钮');
        logoutBtn.addEventListener('click', function() {
            console.log('点击登出按钮');
            logout();
        });
    }
    
    // 个人中心标签切换
    const profileTabs = document.querySelectorAll('.profile-tabs .tab');
    if (profileTabs.length > 0) {
        console.log('找到个人中心标签:', profileTabs.length);
        profileTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const tabName = this.dataset.tab;
                
                // 移除所有标签的active状态
                profileTabs.forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
                
                // 添加当前标签的active状态
                this.classList.add('active');
                document.getElementById(`${tabName}-tab`).classList.add('active');
                console.log('切换到标签:', tabName);
            });
        });
    }
    
    // 个人中心退出登录按钮
    const profileLogoutBtn = document.getElementById('profile-logout-btn');
    if (profileLogoutBtn) {
        console.log('找到个人中心退出登录按钮');
        profileLogoutBtn.addEventListener('click', function() {
            console.log('点击个人中心退出登录按钮');
            logout();
        });
    }
    
    // 个人中心返回首页按钮
    const backToHomeBtn = document.getElementById('back-to-home-btn');
    if (backToHomeBtn) {
        console.log('找到个人中心返回首页按钮');
        backToHomeBtn.addEventListener('click', function() {
            console.log('点击个人中心返回首页按钮');
            showHomePage();
        });
    }
    
    // 保存资料按钮
    const saveProfileBtn = document.getElementById('save-profile-btn');
    if (saveProfileBtn) {
        console.log('找到保存资料按钮');
        saveProfileBtn.addEventListener('click', async function() {
            console.log('点击保存资料按钮');
            const userInfo = getUserInfo();
            if (userInfo && userInfo.role === 'patient') {
                await savePatientInfo();
            } else {
                window.showNotification('保存成功', 'success');
            }
        });
    }
    
    // 同步到诊断表单按钮
    const loadDiagnosisFormBtn = document.getElementById('load-diagnosis-form-btn');
    if (loadDiagnosisFormBtn) {
        console.log('找到同步到诊断表单按钮');
        loadDiagnosisFormBtn.addEventListener('click', function() {
            console.log('点击同步到诊断表单按钮');
            syncToDiagnosisForm();
        });
    }
    
    console.log('认证系统初始化完成');
}

// 获取选中的角色
function getSelectedRole() {
    const selectedCard = document.querySelector('.role-card.selected');
    return selectedCard ? selectedCard.dataset.role : null;
}

// 处理登录
async function handleLogin() {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value.trim();
    const role = getSelectedRole();
    
    if (!username || !password || !role) {
        window.showNotification('请填写所有字段并选择角色', 'error');
        return;
    }
    
    try {
        window.showLoading('登录中...');
        
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password, role })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('登录成功，用户数据:', data.data);
            // 保存用户信息
            saveUserInfo({
                username: data.data.username,
                role: data.data.role,
                displayName: data.data.display_name,
                token: data.token,
                user_id: data.data.user_id
            });
            
            // 更新UI
            console.log('开始更新导航栏');
            updateNavigationForLoggedInUser(data.data);
            
            // 根据角色显示对应的界面
            showDashboardForRole(data.data.role);
            
            // 显示欢迎消息，格式为"欢迎患者张三"
            const roleDisplayName = getRoleDisplayName(data.data.role);
            window.showNotification(`欢迎${roleDisplayName}${data.data.username}`, 'success');
            
            // 如果是患者角色，自动填充诊断表单
            if (data.data.role === 'patient' && data.data.patient_info) {
                console.log('填充患者信息到诊断表单');
                const patientInfo = data.data.patient_info;
                
                // 填充基本信息
                document.getElementById('patient-age').value = patientInfo.age || '';
                document.getElementById('patient-gender').value = patientInfo.gender || '';
                document.getElementById('patient-education').value = patientInfo.education_years || '';
                document.getElementById('patient-history').value = patientInfo.medical_history || '';
                
                // 填充生活方式信息
                if (data.data.lifestyle_data) {
                    const lifestyleData = data.data.lifestyle_data;
                    document.getElementById('exercise-frequency').value = lifestyleData.exercise_frequency || '';
                    document.getElementById('sleep-duration').value = lifestyleData.sleep_duration || '';
                    document.getElementById('diet-health').value = lifestyleData.diet_health || '';
                    document.getElementById('social-activities').value = lifestyleData.social_activities || '';
                    document.getElementById('smoking-status').value = lifestyleData.smoking_status || '';
                    document.getElementById('alcohol-consumption').value = lifestyleData.alcohol_consumption || '';
                }
                
                // 保存到本地存储
                saveFormData();
            }
            
            // 返回首页
            showHomePage();
        } else {
            window.showNotification(data.message || '登录失败', 'error');
        }
    } catch (error) {
        console.error('登录错误:', error);
        window.showNotification('登录失败，请重试', 'error');
    } finally {
        window.hideLoading();
    }
}

// 处理注册
async function handleRegister() {
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value.trim();
    const confirmPassword = document.getElementById('register-confirm-password').value.trim();
    const role = getSelectedRole();
    
    if (!username || !email || !password || !confirmPassword || !role) {
        window.showNotification('请填写所有字段并选择角色', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        window.showNotification('两次输入的密码不一致', 'error');
        return;
    }
    
    try {
        window.showLoading('注册中...');
        
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password, role })
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.showNotification('注册成功，请登录', 'success');
            switchToLogin();
        } else {
            window.showNotification(data.message || '注册失败', 'error');
        }
    } catch (error) {
        console.error('注册错误:', error);
        window.showNotification('注册失败，请重试', 'error');
    } finally {
        window.hideLoading();
    }
}

// 保存用户信息
function saveUserInfo(userInfo) {
    localStorage.setItem('userInfo', JSON.stringify(userInfo));
}

// 获取用户信息
function getUserInfo() {
    const userInfo = localStorage.getItem('userInfo');
    return userInfo ? JSON.parse(userInfo) : null;
}

// 检查登录状态
function checkLoginStatus() {
    const userInfo = getUserInfo();
    if (userInfo) {
        updateNavigationForLoggedInUser(userInfo);
    }
}

// 获取角色显示名称
function getRoleDisplayName(role) {
    const roleMap = {
        'patient': '患者',
        'doctor': '医生',
        'admin': '管理员'
    };
    return roleMap[role] || role;
}

// 更新导航栏为登录状态
function updateNavigationForLoggedInUser(userInfo) {
    console.log('更新导航栏，用户信息:', userInfo);
    const navAuth = document.querySelector('.nav-auth');
    if (!navAuth) {
        console.error('找不到导航栏认证区域');
        return;
    }
    
    console.log('找到导航栏认证区域:', navAuth);
    
    // 清空现有内容
    const roleDisplayName = getRoleDisplayName(userInfo.role);
    navAuth.innerHTML = `
        <div class="user-profile" onclick="showProfilePage()">
            <span class="welcome-text">欢迎${roleDisplayName}${userInfo.username}</span>
        </div>
        <button id="logout-btn" class="btn btn-outline">
            <i class="fas fa-sign-out-alt"></i> 退出
        </button>
    `;
    
    console.log('导航栏HTML已更新');
    
    // 确保用户信息区域是可点击的
    const userProfile = document.querySelector('.user-profile');
    if (userProfile) {
        userProfile.style.pointerEvents = 'auto';
        userProfile.style.position = 'relative';
        userProfile.style.zIndex = '9999';
        console.log('用户信息区域已设置为可点击');
    }
    
    // 重新绑定登出事件
    document.getElementById('logout-btn').addEventListener('click', logout);
    
    // 根据角色显示对应的导航菜单
    updateNavigationByRole(userInfo.role);
    console.log('导航栏更新完成');
}

// 根据角色更新导航菜单
function updateNavigationByRole(role) {
    const navLinks = document.querySelectorAll('.nav-links .nav-link');
    
    // 基础菜单（所有角色都可见）
    const baseLinks = ['#home', '#about'];
    
    // 角色特定菜单
    const roleLinks = {
        'patient': ['#prediction', '#reports'],
        'doctor': ['#prediction', '#reports', '#patients'],
        'admin': ['#prediction', '#reports', '#patients', '#system']
    };
    
    // 显示/隐藏导航链接
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        const shouldShow = baseLinks.includes(href) || (roleLinks[role] && roleLinks[role].includes(href));
        link.style.display = shouldShow ? 'block' : 'none';
    });
}

// 根据角色显示对应的仪表盘
function showDashboardForRole(role) {
    // 这里可以根据角色跳转到不同的页面
    console.log(`用户角色: ${role}，显示对应的仪表盘`);
    
    // 示例：根据角色显示不同的统计数据或功能
    if (role === 'patient') {
        // 患者：显示个人诊断历史和健康建议
        console.log('显示患者仪表盘');
    } else if (role === 'doctor') {
        // 医生：显示患者管理和诊断工具
        console.log('显示医生仪表盘');
    } else if (role === 'admin') {
        // 管理员：显示系统管理和用户管理
        console.log('显示管理员仪表盘');
    }
}

// 登出
function logout() {
    if (confirm('确定要登出吗？')) {
        localStorage.removeItem('userInfo');
        
        // 更新导航栏
        const navAuth = document.querySelector('.nav-auth');
        if (navAuth) {
            navAuth.innerHTML = `
                <button id="login-btn" class="btn btn-outline">
                    <i class="fas fa-user-circle"></i> 登录
                </button>
                <button id="register-btn" class="btn btn-primary">
                    <i class="fas fa-user-plus"></i> 注册
                </button>
            `;
            
            // 重新绑定登录/注册事件
            document.getElementById('login-btn').addEventListener('click', showLoginPage);
            document.getElementById('register-btn').addEventListener('click', showRegisterPage);
        }
        
        // 重置导航菜单
        resetNavigation();
        
        showNotification('已成功登出', 'success');
        showHomePage();
    }
}

// 重置导航菜单
function resetNavigation() {
    const navLinks = document.querySelectorAll('.nav-links .nav-link');
    navLinks.forEach(link => {
        link.style.display = 'block';
    });
}

// 隐藏所有页面
function hideAllSections() {
    const sections = document.querySelectorAll('.page-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
}

// 页面切换函数
function switchToRegister() {
    hideAllSections();
    document.getElementById('register').classList.add('active');
}

function switchToLogin() {
    hideAllSections();
    document.getElementById('login').classList.add('active');
}

function showLoginPage() {
    hideAllSections();
    document.getElementById('login').classList.add('active');
}

function showRegisterPage() {
    hideAllSections();
    document.getElementById('register').classList.add('active');
}

// 显示个人中心页面（全局函数）
window.showProfilePage = function() {
    console.log('显示个人中心页面');
    hideAllSections();
    const profileSection = document.getElementById('profile');
    if (profileSection) {
        profileSection.classList.add('active');
        console.log('个人中心页面已显示');
        loadProfileData();
    } else {
        console.error('找不到个人中心页面元素');
    }
}

// 获取用户信息
function getUserInfo() {
    const userInfoStr = localStorage.getItem('userInfo');
    return userInfoStr ? JSON.parse(userInfoStr) : null;
}

// 加载个人资料数据
async function loadProfileData() {
    const userInfo = getUserInfo();
    if (!userInfo) return;
    
    // 获取角色中文名称
    const roleDisplayName = getRoleDisplayName(userInfo.role);
    
    // 设置个人信息
    document.getElementById('profile-name').textContent = `${roleDisplayName}${userInfo.username}`;
    document.getElementById('profile-role').textContent = roleDisplayName;
    document.getElementById('profile-username').value = userInfo.username;
    document.getElementById('profile-email').value = userInfo.email || '未设置';
    document.getElementById('profile-role-display').value = roleDisplayName;
    
    // 设置时间信息（模拟数据）
    document.getElementById('profile-registration-time').value = '2024-01-01 00:00:00';
    document.getElementById('profile-last-login').value = new Date().toLocaleString();
    
    // 如果是患者角色，显示患者基本信息和生活方式信息表单
    if (userInfo.role === 'patient') {
        document.getElementById('patient-info-section').style.display = 'block';
        document.getElementById('lifestyle-info-section').style.display = 'block';
        
        // 加载患者信息
        await loadPatientInfo(userInfo.user_id);
    }
}

// 加载患者信息
async function loadPatientInfo(userId) {
    try {
        const response = await fetch(`/api/patients/by-user/${userId}`, {
            headers: {
                'Authorization': `Bearer ${getUserInfo().token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.data) {
            const patientInfo = data.data;
            
            // 填充患者基本信息
            document.getElementById('profile-patient-name').value = patientInfo.name || '';
            document.getElementById('profile-patient-age').value = patientInfo.age || '';
            document.getElementById('profile-patient-gender').value = patientInfo.gender || '';
            document.getElementById('profile-patient-education').value = patientInfo.education_years || '';
            document.getElementById('profile-patient-contact').value = patientInfo.contact_info || '';
            document.getElementById('profile-patient-history').value = patientInfo.medical_history || '';
            
            // 填充生活方式信息
            if (patientInfo.lifestyle_data) {
                const lifestyleData = patientInfo.lifestyle_data;
                document.getElementById('profile-exercise-frequency').value = lifestyleData.exercise_frequency || '';
                document.getElementById('profile-sleep-duration').value = lifestyleData.sleep_duration || '';
                document.getElementById('profile-diet-health').value = lifestyleData.diet_health || '';
                document.getElementById('profile-social-activities').value = lifestyleData.social_activities || '';
                document.getElementById('profile-smoking-status').value = lifestyleData.smoking_status || '';
                document.getElementById('profile-alcohol-consumption').value = lifestyleData.alcohol_consumption || '';
            }
        }
    } catch (error) {
        console.error('加载患者信息失败:', error);
    }
}

// 保存患者信息
async function savePatientInfo() {
    const userInfo = getUserInfo();
    if (!userInfo || userInfo.role !== 'patient') return;
    
    try {
        // 首先获取患者ID
        const response = await fetch(`/api/patients/by-user/${userInfo.user_id}`, {
            headers: {
                'Authorization': `Bearer ${userInfo.token}`
            }
        });
        
        const data = await response.json();
        let patientId;
        
        if (data.success && data.data) {
            patientId = data.data.id;
        } else {
            // 如果患者不存在，创建新患者
            const createResponse = await fetch('/api/patients', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${userInfo.token}`
                },
                body: JSON.stringify({
                    user_id: userInfo.user_id,
                    name: document.getElementById('profile-patient-name').value,
                    age: parseInt(document.getElementById('profile-patient-age').value) || null,
                    gender: document.getElementById('profile-patient-gender').value,
                    education_years: parseInt(document.getElementById('profile-patient-education').value) || null,
                    contact_info: document.getElementById('profile-patient-contact').value,
                    medical_history: document.getElementById('profile-patient-history').value
                })
            });
            
            const createData = await createResponse.json();
            if (createData.success && createData.data) {
                patientId = createData.data.id;
            } else {
                throw new Error('创建患者失败');
            }
        }
        
        // 更新患者基本信息
        await fetch(`/api/patients/${patientId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userInfo.token}`
            },
            body: JSON.stringify({
                name: document.getElementById('profile-patient-name').value,
                age: parseInt(document.getElementById('profile-patient-age').value) || null,
                gender: document.getElementById('profile-patient-gender').value,
                education_years: parseInt(document.getElementById('profile-patient-education').value) || null,
                contact_info: document.getElementById('profile-patient-contact').value,
                medical_history: document.getElementById('profile-patient-history').value
            })
        });
        
        // 更新生活方式信息
        await fetch(`/api/patients/${patientId}/lifestyle`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userInfo.token}`
            },
            body: JSON.stringify({
                exercise_frequency: parseInt(document.getElementById('profile-exercise-frequency').value) || null,
                sleep_duration: parseFloat(document.getElementById('profile-sleep-duration').value) || null,
                diet_health: document.getElementById('profile-diet-health').value,
                social_activities: parseInt(document.getElementById('profile-social-activities').value) || null,
                smoking_status: document.getElementById('profile-smoking-status').value,
                alcohol_consumption: document.getElementById('profile-alcohol-consumption').value
            })
        });
        
        window.showNotification('患者信息保存成功', 'success');
    } catch (error) {
        console.error('保存患者信息失败:', error);
        window.showNotification('保存患者信息失败，请重试', 'error');
    }
}

// 同步患者信息到诊断表单
function syncToDiagnosisForm() {
    // 同步基本信息
    document.getElementById('patient-age').value = document.getElementById('profile-patient-age').value;
    document.getElementById('patient-gender').value = document.getElementById('profile-patient-gender').value;
    document.getElementById('patient-education').value = document.getElementById('profile-patient-education').value;
    document.getElementById('patient-history').value = document.getElementById('profile-patient-history').value;
    
    // 同步生活方式信息
    document.getElementById('exercise-frequency').value = document.getElementById('profile-exercise-frequency').value;
    document.getElementById('sleep-duration').value = document.getElementById('profile-sleep-duration').value;
    document.getElementById('diet-health').value = document.getElementById('profile-diet-health').value;
    document.getElementById('social-activities').value = document.getElementById('profile-social-activities').value;
    document.getElementById('smoking-status').value = document.getElementById('profile-smoking-status').value;
    document.getElementById('alcohol-consumption').value = document.getElementById('profile-alcohol-consumption').value;
    
    // 保存到本地存储
    saveFormData();
    
    window.showNotification('已同步到诊断表单', 'success');
}

function showHomePage() {
    hideAllSections();
    document.getElementById('home').classList.add('active');
}

// 创建粒子背景
function createParticles() {
    const heroSection = document.querySelector('.hero-background');
    if (!heroSection) return;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // 随机大小
        const size = Math.random() * 5 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // 随机位置
        particle.style.left = `${Math.random() * 100}%`;
        
        // 随机动画延迟
        particle.style.animationDelay = `${Math.random() * 15}s`;
        
        // 随机颜色
        const colors = [
            'rgba(255, 255, 255, 0.5)',
            'rgba(59, 130, 246, 0.3)',
            'rgba(16, 185, 129, 0.3)',
            'rgba(245, 158, 11, 0.3)'
        ];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        heroSection.appendChild(particle);
    }
}

// 初始化导航
function initNavigation() {
    try {
        console.log('开始初始化导航...');
        const navLinks = document.querySelectorAll('.nav-link');
        const pageSections = document.querySelectorAll('.page-section');
        const navbar = document.querySelector('.navbar');
        
        console.log('找到导航链接:', navLinks.length);
        console.log('找到页面部分:', pageSections.length);

        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                try {
                    e.preventDefault();
                    const targetId = this.getAttribute('href').substring(1);
                    console.log('点击导航:', targetId);

                    // 更新活动链接
                    navLinks.forEach(l => {
                        l.classList.remove('active');
                        l.style.transform = 'translateY(0)';
                    });
                    this.classList.add('active');
                    this.style.transform = 'translateY(-2px)';

                    // 平滑过渡效果
                    pageSections.forEach(section => {
                        if (section.classList.contains('active') && section.id !== targetId) {
                            section.classList.add('closing');
                            setTimeout(() => {
                                section.classList.remove('active', 'closing');
                            }, 400);
                        }
                    });
                    
                    // 延迟显示目标页面，等待关闭动画完成
                    setTimeout(() => {
                        pageSections.forEach(section => {
                            if (section.id === targetId) {
                                section.classList.add('active');
                            }
                        });
                    }, 200);

                    // 滚动到顶部
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                    
                    // 如果是报告页面，加载报告列表
                    if (targetId === 'reports') {
                        if (typeof loadReportsList === 'function') {
                            loadReportsList();
                        } else {
                            console.warn('loadReportsList函数未定义');
                        }
                    }
                    
                    // 如果是首页，添加粒子动画
                    if (targetId === 'home') {
                        if (typeof createParticles === 'function') {
                            createParticles();
                        } else {
                            console.warn('createParticles函数未定义');
                        }
                    }
                } catch (error) {
                    console.error('导航点击事件出错:', error);
                }
            });
        });
        
        // 添加导航栏滚动效果
        if (navbar) {
            window.addEventListener('scroll', throttle(function() {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }, 100));
        }
        
        console.log('导航初始化完成');
    } catch (error) {
        console.error('导航初始化出错:', error);
    }
}

// 初始化按钮事件
function initButtons() {
    // 首页按钮
    document.getElementById('start-demo').addEventListener('click', function() {
        // 先跳转到诊断页面
        document.querySelector('[href="#diagnosis"]').click();
        // 延迟加载演示数据，确保页面已经切换
        setTimeout(() => {
            loadingManager.showInfo('正在加载多模态演示数据...');
            startDemoAnalysis();
        }, 500);
    });

    document.getElementById('start-diagnosis').addEventListener('click', function() {
        document.querySelector('[href="#diagnosis"]').click();
        setTimeout(() => {
            document.getElementById('browse-files').click();
        }, 100);
    });

    document.getElementById('view-reports').addEventListener('click', function() {
        document.querySelector('[href="#reports"]').click();
    });
    
    // PDF报告相关按钮
    document.getElementById('generate-new-report').addEventListener('click', generateNewPDFReport);
    document.getElementById('view-history-reports').addEventListener('click', function() {
        // 先跳转到报告页面
        document.querySelector('[href="#reports"]').click();
        // 延迟加载报告列表，确保页面已经切换
        setTimeout(() => {
            loadReportsList();
        }, 500);
    });
    document.getElementById('report-settings').addEventListener('click', openReportSettingsModal);
    
    // 报告搜索功能
    document.getElementById('search-reports').addEventListener('click', searchReports);
    document.getElementById('clear-report-search').addEventListener('click', clearReportSearch);
    
    // 表单清空按钮
    document.getElementById('clear-form').addEventListener('click', clearForm);
}

// 初始化文件上传
let selectedFiles = [];

function initFileUpload() {
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-files');
    const fileInfo = document.getElementById('file-info');
    const useDemoBtn = document.getElementById('use-demo');
    const startAnalysisBtn = document.getElementById('start-analysis');

    browseBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function(e) {
        const newFiles = Array.from(e.target.files);
        if (newFiles.length > 0) {
            // 添加新文件到已选择的文件列表
            selectedFiles = [...selectedFiles, ...newFiles];
            showFileInfo(selectedFiles);
            startAnalysisBtn.disabled = false;
        }
    });

    startAnalysisBtn.addEventListener('click', function() {
        if (selectedFiles.length > 0) {
            startFileAnalysis(selectedFiles);
        }
    });

    useDemoBtn.addEventListener('click', function() {
        const category = document.getElementById('demo-category').value;
        loadingManager.showInfo('正在使用多模态演示数据...');
        startDemoAnalysis(category);
    });
}

// 初始化表单验证
function initFormValidation() {
    const formInputs = document.querySelectorAll('.form-input');
    
    formInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
            saveFormData();
        });
        
        input.addEventListener('blur', function() {
            validateField(this);
            saveFormData();
        });
    });
    
    // 加载保存的表单数据
    loadFormData();
}

// 保存表单数据到localStorage
function saveFormData() {
    const formData = {
        patient_id: document.getElementById('patient-id').value,
        age: document.getElementById('patient-age').value,
        gender: document.getElementById('patient-gender').value,
        education: document.getElementById('patient-education').value,
        clinical_history: document.getElementById('patient-history').value,
        family_history: document.getElementById('patient-family').value,
        lifestyle: {
            exercise_frequency: document.getElementById('exercise-frequency').value,
            sleep_duration: document.getElementById('sleep-duration').value,
            diet_health: document.getElementById('diet-health').value,
            social_activities: document.getElementById('social-activities').value,
            smoking_status: document.getElementById('smoking-status').value,
            alcohol_consumption: document.getElementById('alcohol-consumption').value,
            cognitive_activities: document.getElementById('cognitive-activities').value
        },
        lastSaved: new Date().toISOString()
    };
    
    localStorage.setItem('adDiagnosisFormData', JSON.stringify(formData));
    
    // 更新保存状态
    updateSaveStatus();
}

// 更新保存状态
function updateSaveStatus() {
    const saveStatus = document.getElementById('save-status');
    if (saveStatus) {
        saveStatus.innerHTML = '<i class="fas fa-check-circle" style="color: var(--secondary-color);"></i> 已保存';
        saveStatus.style.color = 'var(--secondary-color)';
        
        setTimeout(() => {
            saveStatus.innerHTML = '<i class="fas fa-save"></i> 自动保存中...';
            saveStatus.style.color = 'var(--gray-color)';
        }, 2000);
    }
}

// 清空表单
function clearForm() {
    if (confirm('确定要清空所有表单数据吗？此操作无法撤销。')) {
        // 清空所有表单字段
        document.getElementById('patient-id').value = '';
        document.getElementById('patient-age').value = '';
        document.getElementById('patient-gender').value = '';
        document.getElementById('patient-education').value = '';
        document.getElementById('patient-history').value = '';
        document.getElementById('patient-family').value = '';
        
        document.getElementById('exercise-frequency').value = '';
        document.getElementById('sleep-duration').value = '';
        document.getElementById('diet-health').value = '';
        document.getElementById('social-activities').value = '';
        document.getElementById('smoking-status').value = '';
        document.getElementById('alcohol-consumption').value = '';
        document.getElementById('cognitive-activities').value = '';
        
        // 清除localStorage
        localStorage.removeItem('adDiagnosisFormData');
        
        // 清除所有验证状态
        const formInputs = document.querySelectorAll('.form-input');
        formInputs.forEach(input => {
            input.classList.remove('error', 'success');
            removeErrorMessage(input);
        });
        
        showToast('表单已清空', 'success');
    }
}

// 从localStorage加载表单数据
function loadFormData() {
    const savedData = localStorage.getItem('adDiagnosisFormData');
    if (savedData) {
        try {
            const formData = JSON.parse(savedData);
            
            document.getElementById('patient-id').value = formData.patient_id || '';
            document.getElementById('patient-age').value = formData.age || '';
            document.getElementById('patient-gender').value = formData.gender || '';
            document.getElementById('patient-education').value = formData.education || '';
            document.getElementById('patient-history').value = formData.clinical_history || '';
            document.getElementById('patient-family').value = formData.family_history || '';
            
            if (formData.lifestyle) {
                document.getElementById('exercise-frequency').value = formData.lifestyle.exercise_frequency || '';
                document.getElementById('sleep-duration').value = formData.lifestyle.sleep_duration || '';
                document.getElementById('diet-health').value = formData.lifestyle.diet_health || '';
                document.getElementById('social-activities').value = formData.lifestyle.social_activities || '';
                document.getElementById('smoking-status').value = formData.lifestyle.smoking_status || '';
                document.getElementById('alcohol-consumption').value = formData.lifestyle.alcohol_consumption || '';
                document.getElementById('cognitive-activities').value = formData.lifestyle.cognitive_activities || '';
            }
            
            // 验证加载的数据
            validateForm();
        } catch (error) {
            console.error('加载表单数据失败:', error);
        }
    }
}

// 验证单个字段
function validateField(field) {
    const fieldId = field.id;
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // 移除之前的错误状态
    field.classList.remove('error', 'success');
    removeErrorMessage(field);
    
    switch(fieldId) {
        case 'patient-age':
            if (!value) {
                isValid = false;
                errorMessage = '请输入年龄';
            } else if (value< 18 || value >120) {
                isValid = false;
                errorMessage = '年龄应在18-120岁之间';
            } else {
                isValid = true;
            }
            break;
            
        case 'patient-gender':
            if (!value) {
                isValid = false;
                errorMessage = '请选择性别';
            } else {
                isValid = true;
            }
            break;
            
        case 'patient-education':
            if (!value) {
                isValid = false;
                errorMessage = '请输入教育程度';
            } else if (value.length > 50) {
                isValid = false;
                errorMessage = '教育程度不能超过50个字符';
            } else {
                isValid = true;
            }
            break;
            
        case 'patient-history':
            if (value.length > 200) {
                isValid = false;
                errorMessage = '病史描述不能超过200个字符';
            } else {
                isValid = true;
            }
            break;
            
        case 'patient-family':
            if (value.length > 200) {
                isValid = false;
                errorMessage = '家族史描述不能超过200个字符';
            } else {
                isValid = true;
            }
            break;
            
        case 'exercise-frequency':
            if (value !== '' && (value< 0 || value >7)) {
                isValid = false;
                errorMessage = '运动频率应在0-7之间';
            } else {
                isValid = true;
            }
            break;
            
        case 'sleep-duration':
            if (value !== '' && (value< 4 || value >12)) {
                isValid = false;
                errorMessage = '睡眠时长应在4-12小时之间';
            } else {
                isValid = true;
            }
            break;
            
        case 'social-activities':
            if (value !== '' && (value< 0 || value >10)) {
                isValid = false;
                errorMessage = '社交活动次数应在0-10之间';
            } else {
                isValid = true;
            }
            break;
            
        case 'cognitive-activities':
            if (value.length > 100) {
                isValid = false;
                errorMessage = '认知活动描述不能超过100个字符';
            } else {
                isValid = true;
            }
            break;
    }
    
    if (!isValid) {
        field.classList.add('error');
        field.classList.remove('success');
        showErrorMessage(field, errorMessage);
    } else if (value) {
        field.classList.add('success');
        field.classList.remove('error');
        showSuccessMessage(field);
    } else {
        field.classList.remove('error', 'success');
        removeErrorMessage(field);
    }
    
    return isValid;
}

// 显示错误信息
function showErrorMessage(field, message) {
    // 移除现有的错误信息
    removeErrorMessage(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i>${message}`;
    
    field.parentNode.appendChild(errorDiv);
}

// 显示成功信息
function showSuccessMessage(field, message = '输入有效') {
    // 移除现有的错误信息
    removeErrorMessage(field);
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `<i class="fas fa-check-circle"></i>${message}`;
    
    field.parentNode.appendChild(successDiv);
}

// 移除错误信息
function removeErrorMessage(field) {
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const existingSuccess = field.parentNode.querySelector('.success-message');
    if (existingSuccess) {
        existingSuccess.remove();
    }
}

// 表单验证函数
function validateForm() {
    let isValid = true;
    const formInputs = document.querySelectorAll('.form-input');
    
    formInputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        showToast('请修正表单中的错误', 'error');
    }
    
    return isValid;
}

// 初始化模态框
function initModal() {
    const modal = document.getElementById('results-modal');
    const pdfModal = document.getElementById('pdf-preview-modal');
    const closeModalBtn = document.querySelector('.modal-close');
    const closeModalBtn2 = document.getElementById('close-modal');
    const closePdfModalBtn = document.getElementById('close-pdf-modal');

    function openModal(modalElement, content) {
        if (content) {
            document.getElementById('modal-body').innerHTML = content;
        }
        modalElement.classList.add('active');
    }

    closeModalBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        modal.classList.add('closing');
        setTimeout(() => modal.classList.remove('closing'), 300);
    });
    
    closeModalBtn2.addEventListener('click', () => {
        modal.classList.remove('active');
        modal.classList.add('closing');
        setTimeout(() => modal.classList.remove('closing'), 300);
    });
    
    closePdfModalBtn.addEventListener('click', () => {
        pdfModal.classList.remove('active');
        pdfModal.classList.add('closing');
        setTimeout(() => pdfModal.classList.remove('closing'), 300);
    });
    
    // PDF生成按钮
    document.getElementById('generate-pdf').addEventListener('click', function() {
        const results = window.currentResults;
        if (results) {
            generatePDFReportFromResults(results);
        }
    });
    
    // PDF下载按钮
    document.getElementById('download-pdf').addEventListener('click', function() {
        const iframe = document.getElementById('pdf-preview-frame');
        const pdfUrl = iframe.src;
        if (pdfUrl) {
            const a = document.createElement('a');
            a.href = pdfUrl;
            a.download = pdfUrl.split('/').pop();
            a.click();
        }
    });

    // 点击模态框外部关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            modal.classList.add('closing');
            setTimeout(() => modal.classList.remove('closing'), 300);
        }
    });
    
    pdfModal.addEventListener('click', (e) => {
        if (e.target === pdfModal) {
            pdfModal.classList.remove('active');
            pdfModal.classList.add('closing');
            setTimeout(() => pdfModal.classList.remove('closing'), 300);
        }
    });
}

// 全屏图像查看模态框
function openImageModal(imageSrc, imageTitle, imageType) {
    const existingModal = document.querySelector('.image-zoom-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.className = 'image-zoom-modal';
    modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.95);z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center;animation:fadeIn 0.3s ease;';
    
    let imageInfo = '';
    if (imageType === 'brain') {
        imageInfo = `
            <div style="position:absolute;top:20px;left:20px;background:linear-gradient(135deg,#1e40af,#3b82f6);padding:15px 25px;border-radius:10px;color:white;font-size:14px;max-width:400px;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="font-size:18px;font-weight:bold;margin-bottom:10px;"><i class="fas fa-brain"></i> ${imageTitle}</div>
                <div style="margin-bottom:8px;"><strong style="color:#ef4444;">●</strong> 红色区域：海马体/前额叶 - 严重萎缩</div>
                <div style="margin-bottom:8px;"><strong style="color:#f59e0b;">●</strong> 橙色区域：颞叶/顶叶 - 中度病变</div>
                <div style="margin-bottom:0;"><strong style="color:#10b981;">●</strong> 绿色区域：相对正常脑组织</div>
            </div>
        `;
    } else if (imageType === 'heatmap') {
        imageInfo = `
            <div style="position:absolute;top:20px;left:20px;background:linear-gradient(135deg,#dc2626,#f59e0b);padding:15px 25px;border-radius:10px;color:white;font-size:14px;max-width:400px;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="font-size:18px;font-weight:bold;margin-bottom:10px;"><i class="fas fa-map"></i> ${imageTitle}</div>
                <div style="margin-bottom:8px;"><strong style="color:#ef4444;">●</strong> 高风险区域：红色/橙色 - 需重点关注</div>
                <div style="margin-bottom:8px;"><strong style="color:#f59e0b;">●</strong> 中风险区域：黄色 - 建议监测</div>
                <div style="margin-bottom:0;"><strong style="color:#10b981;">●</strong> 低风险区域：绿色 - 相对正常</div>
            </div>
        `;
    }
    
    modal.innerHTML = `
        ${imageInfo}
        <div style="position:absolute;top:20px;right:20px;display:flex;gap:10px;">
            <button onclick="adjustZoom(this)" data-action="zoom-in" style="background:#3b82f6;border:none;color:white;padding:12px 18px;border-radius:8px;cursor:pointer;font-size:16px;box-shadow:0 4px 15px rgba(0,0,0,0.3);transition:all 0.3s;" title="放大">
                <i class="fas fa-search-plus"></i>
            </button>
            <button onclick="adjustZoom(this)" data-action="zoom-out" style="background:#6b7280;border:none;color:white;padding:12px 18px;border-radius:8px;cursor:pointer;font-size:16px;box-shadow:0 4px 15px rgba(0,0,0,0.3);transition:all 0.3s;" title="缩小">
                <i class="fas fa-search-minus"></i>
            </button>
            <button onclick="adjustZoom(this)" data-action="reset" style="background:#10b981;border:none;color:white;padding:12px 18px;border-radius:8px;cursor:pointer;font-size:16px;box-shadow:0 4px 15px rgba(0,0,0,0.3);transition:all 0.3s;" title="重置">
                <i class="fas fa-redo"></i>
            </button>
            <button onclick="this.closest('.image-zoom-modal').remove()" style="background:#ef4444;border:none;color:white;padding:12px 18px;border-radius:8px;cursor:pointer;font-size:16px;box-shadow:0 4px 15px rgba(0,0,0,0.3);transition:all 0.3s;" title="关闭">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div style="position:absolute;bottom:30px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.7);padding:12px 25px;border-radius:30px;color:white;font-size:13px;display:flex;gap:20px;align-items:center;">
            <span><i class="fas fa-info-circle"></i> 提示：双击图像可拖动 | 滚轮缩放 | 按ESC关闭</span>
        </div>
        <img id="zoomable-image" src="${imageSrc}" style="max-width:95%;max-height:85vh;object-fit:contain;border-radius:10px;box-shadow:0 0 50px rgba(255,255,255,0.1);transition:transform 0.3s ease;cursor:grab;"
             onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22400%22><rect fill=%22%23f3f4f6%22 width=%22400%22 height=%22400%22/><text x=%2250%%22 y=%2250%%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%239ca3af%22 font-size=%2216%22>图像加载失败</text></svg>'">
    `;
    
    document.body.appendChild(modal);
    
    const img = document.getElementById('zoomable-image');
    let scale = 1;
    let isDragging = false;
    let startX, startY, translateX = 0, translateY = 0;
    
    img.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        scale = Math.min(Math.max(scale * delta, 0.5), 5);
        img.style.transform = `scale(${scale}) translate(${translateX}px, ${translateY}px)`;
    });
    
    img.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.clientX - translateX;
        startY = e.clientY - translateY;
        img.style.cursor = 'grabbing';
    });
    
    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        translateX = e.clientX - startX;
        translateY = e.clientY - startY;
        img.style.transform = `scale(${scale}) translate(${translateX}px, ${translateY}px)`;
    });
    
    document.addEventListener('mouseup', () => {
        isDragging = false;
        img.style.cursor = 'grab';
    });
    
    img.addEventListener('dblclick', () => {
        scale = 1;
        translateX = 0;
        translateY = 0;
        img.style.transform = 'scale(1)';
    });
    
    modal.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            modal.remove();
        }
    });
    
    modal.style.display = 'flex';
}

function adjustZoom(btn) {
    const img = document.getElementById('zoomable-image');
    if (!img) return;
    
    const action = btn.dataset.action;
    let currentTransform = img.style.transform;
    let scale = 1;
    let match = currentTransform.match(/scale\(([^)]+)\)/);
    if (match) {
        scale = parseFloat(match[1]);
    }
    
    if (action === 'zoom-in') {
        scale = Math.min(scale * 1.2, 5);
    } else if (action === 'zoom-out') {
        scale = Math.max(scale / 1.2, 0.5);
    } else if (action === 'reset') {
        scale = 1;
        img.style.transform = 'scale(1)';
        return;
    }
    
    img.style.transform = `scale(${scale})`;
}

// 初始化数据管理
function initDataManagement() {
    // 刷新统计按钮
    document.getElementById('refresh-stats').addEventListener('click', loadSystemStats);
    
    // 数据操作按钮
    document.getElementById('export-data').addEventListener('click', exportData);
    
    document.getElementById('clear-temp').addEventListener('click', function() {
        if (confirm('确定要清理临时文件吗？')) {
            clearTempFiles();
        }
    });
    
    document.getElementById('backup-data').addEventListener('click', backupData);
    
    // 添加导入数据按钮事件
    const importButton = document.querySelector('#import-data');
    if (importButton) {
        importButton.addEventListener('click', importData);
    }
    
    // 患者搜索功能
    document.getElementById('search-patients').addEventListener('click', searchPatients);
    document.getElementById('clear-search').addEventListener('click', clearSearch);
    
    // 实时搜索功能
    const searchInput = document.getElementById('patient-search');
    const filterSelect = document.getElementById('patient-filter');
    
    const debouncedSearch = debounce(() => {
        const searchTerm = searchInput.value;
        const diagnosisFilter = filterSelect.value;
        loadPatientList(searchTerm, diagnosisFilter);
    }, 300);
    
    searchInput.addEventListener('input', debouncedSearch);
    filterSelect.addEventListener('change', debouncedSearch);
    
    // 加载患者列表
    loadPatientList();
}

// 保存患者数据到localStorage
function savePatientData(patientInfo, results) {
    const patientData = {
        patient_id: patientInfo.patient_id,
        age: patientInfo.age,
        gender: patientInfo.gender,
        education: patientInfo.education,
        clinical_history: patientInfo.clinical_history,
        family_history: patientInfo.family_history,
        lifestyle: patientInfo.lifestyle,
        diagnosis: {
            label: results.pred_label,
            chinese_label: results.chinese_label || results.pred_label,
            confidence: results.confidence,
            risk_score: results.risk_score
        },
        analysis_time: new Date().toISOString(),
        modalities_used: results.modalities_used || []
    };
    
    // 获取现有患者数据
    let patients = JSON.parse(localStorage.getItem('adPatients') || '[]');
    
    // 检查是否已存在相同患者ID
    const existingIndex = patients.findIndex(p => p.patient_id === patientData.patient_id);
    if (existingIndex >= 0) {
        patients[existingIndex] = patientData;
    } else {
        patients.push(patientData);
    }
    
    localStorage.setItem('adPatients', JSON.stringify(patients));
}

// 分页相关变量
let currentPage = 1;
const itemsPerPage = 10;
let filteredPatients = [];

// 加载患者列表
function loadPatientList(filter = '', diagnosisFilter = '') {
    const patients = JSON.parse(localStorage.getItem('adPatients') || '[]');
    const listBody = document.getElementById('patient-list-body');
    
    // 过滤患者数据
    filteredPatients = patients;
    if (filter) {
        filteredPatients = patients.filter(patient => 
            patient.patient_id.toLowerCase().includes(filter.toLowerCase()) ||
            patient.diagnosis.chinese_label.toLowerCase().includes(filter.toLowerCase()) ||
            patient.diagnosis.label.toLowerCase().includes(filter.toLowerCase())
        );
    }
    
    if (diagnosisFilter) {
        filteredPatients = filteredPatients.filter(patient => 
            patient.diagnosis.label === diagnosisFilter
        );
    }
    
    // 重置分页
    currentPage = 1;
    
    if (filteredPatients.length === 0) {
        listBody.innerHTML = `
            <div class="no-patients">
                <i class="fas fa-user-md"></i>
                <p>暂无患者数据</p>
                <p>请先进行诊断分析</p>
            </div>
        `;
        updatePagination();
        return;
    }
    
    // 显示当前页的数据
    displayCurrentPage();
}

// 显示当前页的数据
function displayCurrentPage() {
    const listBody = document.getElementById('patient-list-body');
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentPatients = filteredPatients.slice(startIndex, endIndex);
    
    let html = '';
    currentPatients.forEach(patient => {
        const genderText = patient.gender === 'male' ? '男' : '女';
        const analysisTime = new Date(patient.analysis_time).toLocaleString('zh-CN');
        
        html += `
            <div class="list-item">
                <div><i class="fas fa-id-card"></i> ${patient.patient_id}</div>
                <div>${patient.age}岁</div>
                <div>${genderText}</div>
                <div>
                    <span class="patient-status ${patient.diagnosis.label}">
                        ${patient.diagnosis.label} - ${patient.diagnosis.chinese_label}
                    </span>
                </div>
                <div>${analysisTime}</div>
                <div class="list-actions">
                    <button class="btn btn-sm btn-primary" onclick="viewPatientDetails('${patient.patient_id}')">
                        <i class="fas fa-eye"></i> 查看
                    </button>
                    <button class="btn btn-sm btn-outline" onclick="editPatientData('${patient.patient_id}')">
                        <i class="fas fa-edit"></i> 编辑
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deletePatientData('${patient.patient_id}')">
                        <i class="fas fa-trash-alt"></i> 删除
                    </button>
                </div>
            </div>
        `;
    });
    
    listBody.innerHTML = html;
    updatePagination();
}

// 更新分页控件
function updatePagination() {
    // 检查是否存在分页控件
    let pagination = document.getElementById('patient-pagination');
    if (!pagination) {
        // 创建分页控件
        const patientList = document.querySelector('.patient-list');
        pagination = document.createElement('div');
        pagination.id = 'patient-pagination';
        pagination.className = 'pagination';
        patientList.appendChild(pagination);
    }
    
    const totalPages = Math.ceil(filteredPatients.length / itemsPerPage);
    
    if (totalPages<= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    let paginationHTML = `
        <button class="btn btn-sm btn-outline" ${currentPage === 1 ? 'disabled' : ''} onclick="changePage(${currentPage - 1})">
            <i class="fas fa-chevron-left"></i> 上一页
        </button>
        <span class="page-info">第 ${currentPage} 页，共 ${totalPages} 页</span>
        <button class="btn btn-sm btn-outline" ${currentPage === totalPages ? 'disabled' : ''} onclick="changePage(${currentPage + 1})">
            下一页 <i class="fas fa-chevron-right"></i>
        </button>
    `;
    
    pagination.innerHTML = paginationHTML;
}

// 切换页码
function changePage(page) {
    if (page > 0 && page<= Math.ceil(filteredPatients.length / itemsPerPage)) {
        currentPage = page;
        displayCurrentPage();
    }
}

// 搜索患者
function searchPatients() {
    const searchTerm = document.getElementById('patient-search').value;
    const diagnosisFilter = document.getElementById('patient-filter').value;
    loadPatientList(searchTerm, diagnosisFilter);
}

// 清除搜索
function clearSearch() {
    document.getElementById('patient-search').value = '';
    document.getElementById('patient-filter').value = '';
    loadPatientList();
}

// 查看患者详情
function viewPatientDetails(patientId) {
    const patients = JSON.parse(localStorage.getItem('adPatients') || '[]');
    const patient = patients.find(p => p.patient_id === patientId);
    
    if (patient) {
        const modal = document.getElementById('results-modal');
        const modalBody = document.getElementById('modal-body');
        
        let lifestyleHtml = '';
        if (patient.lifestyle) {
            lifestyleHtml = `
                <div class="report-section">
                    <h4><i class="fas fa-heartbeat"></i> 生活方式信息</h4>
                    <div class="lifestyle-details">
                        <div class="detail-item">
                            <span class="label">每周运动次数：</span>
                            <span class="value">${patient.lifestyle.exercise_frequency || '未提供'}次</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">每晚睡眠时长：</span>
                            <span class="value">${patient.lifestyle.sleep_duration || '未提供'}小时</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">健康饮食频率：</span>
                            <span class="value">${patient.lifestyle.diet_health ? 
                                (patient.lifestyle.diet_health === 'high' ? '高' : 
                                 patient.lifestyle.diet_health === 'medium' ? '中' : '低') : '未提供'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">每周社交活动次数：</span>
                            <span class="value">${patient.lifestyle.social_activities || '未提供'}次</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">吸烟状况：</span>
                            <span class="value">${patient.lifestyle.smoking_status ? 
                                (patient.lifestyle.smoking_status === 'never' ? '从不吸烟' : 
                                 patient.lifestyle.smoking_status === 'past' ? '曾经吸烟' : '当前吸烟') : '未提供'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">饮酒频率：</span>
                            <span class="value">${patient.lifestyle.alcohol_consumption ? 
                                (patient.lifestyle.alcohol_consumption === 'never' ? '从不饮酒' : 
                                 patient.lifestyle.alcohol_consumption === 'occasional' ? '偶尔饮酒' : '经常饮酒') : '未提供'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">认知活动：</span>
                            <span class="value">${patient.lifestyle.cognitive_activities || '未提供'}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        modalBody.innerHTML = `
            <div class="detailed-report">
                <div class="report-header">
                    <h3><i class="fas fa-file-medical-alt"></i> 患者详细信息</h3>
                    <div class="report-meta">
                        <div>患者ID：${patient.patient_id}</div>
                        <div>分析时间：${new Date(patient.analysis_time).toLocaleString('zh-CN')}</div>
                    </div>
                </div>
                
                <div class="report-section">
                    <h4><i class="fas fa-user"></i> 基本信息</h4>
                    <div class="patient-details">
                        <div class="detail-item">
                            <span class="label">年龄：</span>
                            <span class="value">${patient.age}岁</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">性别：</span>
                            <span class="value">${patient.gender === 'male' ? '男' : '女'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">教育程度：</span>
                            <span class="value">${patient.education || '未提供'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">主要病史：</span>
                            <span class="value">${patient.clinical_history || '无'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">家族史：</span>
                            <span class="value">${patient.family_history || '无'}</span>
                        </div>
                    </div>
                </div>
                
                ${lifestyleHtml}
                
                <div class="report-section">
                    <h4><i class="fas fa-diagnoses"></i> 诊断结果</h4>
                    <div class="diagnosis-details">
                        <div class="detail-item">
                            <span class="label">诊断类别：</span>
                            <span class="value highlight">${patient.diagnosis.label} - ${patient.diagnosis.chinese_label}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">诊断置信度：</span>
                            <span class="value">${(patient.diagnosis.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">12个月进展风险：</span>
                            <span class="value ${patient.diagnosis.risk_score > 0.5 ? 'danger' : patient.diagnosis.risk_score > 0.2 ? 'warning' : 'safe'}">
                                ${(patient.diagnosis.risk_score * 100).toFixed(1)}%
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        modal.classList.add('active');
    }
}

// 编辑患者数据
function editPatientData(patientId) {
    showToast('编辑功能开发中', 'info');
}

// 删除患者数据
function deletePatientData(patientId) {
    if (confirm(`确定要删除患者 ${patientId} 的所有数据吗？此操作无法撤销。`)) {
        let patients = JSON.parse(localStorage.getItem('adPatients') || '[]');
        patients = patients.filter(p => p.patient_id !== patientId);
        localStorage.setItem('adPatients', JSON.stringify(patients));
        loadPatientList();
        showToast('患者数据已删除', 'success');
    }
}

// 格式化文件大小
function formatFileSize(sizeInBytes) {
    if (sizeInBytes < 1024) {
        return `${sizeInBytes} B`;
    } else if (sizeInBytes < 1024 * 1024) {
        return `${(sizeInBytes / 1024).toFixed(2)} KB`;
    } else {
        return `${(sizeInBytes / 1024 / 1024).toFixed(2)} MB`;
    }
}

// 显示文件信息
function showFileInfo(files) {
    const fileInfo = document.getElementById('file-info');
    fileInfo.style.display = 'block';
    fileInfo.classList.add('active');
    
    let html = '<div><strong>已选择文件：</strong></div>';
    files.forEach((file, index) => {
        const fileType = file.name.split('.').pop().toUpperCase();
        const icon = getFileIcon(fileType);
        
        html += `
            <div style="margin-top: 0.5rem; padding: 0.75rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="font-size: 1.5rem;">${icon}</div>
                    <div style="flex: 1;">
                        <div><strong>文件 ${index + 1}:</strong> ${file.name}</div>
                        <div style="margin-top: 0.25rem; color: #64748b; font-size: 0.9rem;">
                            <span class="badge badge-primary">${fileType}</span>
                            <span style="margin-left: 1rem;">大小: ${formatFileSize(file.size)}</span>
                        </div>
                    </div>
                    <button onclick="removeFile(${index})" style="background: #ef4444; color: white; border: none; border-radius: 4px; padding: 0.5rem; cursor: pointer; font-size: 0.8rem;">
                        <i class="fas fa-trash-alt"></i> 删除
                    </button>
                </div>
            </div>
        `;
    });
    
    fileInfo.innerHTML = html;
}

// 删除文件
function removeFile(index) {
    // 从选中文件数组中移除指定索引的文件
    selectedFiles.splice(index, 1);
    
    // 更新文件信息显示
    if (selectedFiles.length > 0) {
        showFileInfo(selectedFiles);
        document.getElementById('start-analysis').disabled = false;
    } else {
        document.getElementById('file-info').style.display = 'none';
        document.getElementById('start-analysis').disabled = true;
        document.getElementById('file-input').value = '';
    }
}

// 获取文件图标
function getFileIcon(fileType) {
    const iconMap = {
        'NII': '',
        'NII.GZ': '',
        'NPY': '',
        'JSON': '',
        'CSV': '',
        'PDF': '',
        'TXT': '',
        'JPG': '',
        'JPEG': '',
        'PNG': '',
        'DICOM': '',
        'DCM': ''
    };
    
    return iconMap[fileType.toUpperCase()] || '';
}

// 表单验证函数
function validateForm() {
    let isValid = true;
    const errors = [];
    
    // 验证必填字段
    const age = document.getElementById('patient-age').value;
    if (!age || age < 18 || age > 120) {
        errors.push('请输入有效的年龄（18-120岁）');
        document.getElementById('patient-age').style.borderColor = 'var(--danger-color)';
        isValid = false;
    } else {
        document.getElementById('patient-age').style.borderColor = '';
    }
    
    const gender = document.getElementById('patient-gender').value;
    if (!gender) {
        errors.push('请选择性别');
        document.getElementById('patient-gender').style.borderColor = 'var(--danger-color)';
        isValid = false;
    } else {
        document.getElementById('patient-gender').style.borderColor = '';
    }
    
    const education = document.getElementById('patient-education').value;
    if (!education) {
        errors.push('请输入教育程度');
        document.getElementById('patient-education').style.borderColor = 'var(--danger-color)';
        isValid = false;
    } else {
        document.getElementById('patient-education').style.borderColor = '';
    }
    
    const exerciseFrequency = document.getElementById('exercise-frequency').value;
    if (exerciseFrequency !== '' && (exerciseFrequency < 0 || exerciseFrequency > 7)) {
        errors.push('运动频率应在0-7之间');
        document.getElementById('exercise-frequency').style.borderColor = 'var(--danger-color)';
        isValid = false;
    } else {
        document.getElementById('exercise-frequency').style.borderColor = '';
    }
    
    const sleepDuration = document.getElementById('sleep-duration').value;
    if (sleepDuration !== '' && (sleepDuration < 4 || sleepDuration > 12)) {
        errors.push('睡眠时长应在4-12小时之间');
        document.getElementById('sleep-duration').style.borderColor = 'var(--danger-color)';
        isValid = false;
    } else {
        document.getElementById('sleep-duration').style.borderColor = '';
    }
    
    const socialActivities = document.getElementById('social-activities').value;
    if (socialActivities !== '' && (socialActivities < 0 || socialActivities > 10)) {
        errors.push('社交活动次数应在0-10之间');
        document.getElementById('social-activities').style.borderColor = 'var(--danger-color)';
        isValid = false;
    } else {
        document.getElementById('social-activities').style.borderColor = '';
    }
    
    if (!isValid) {
        showToast('请修正以下错误：' + errors.join('、'), 'error');
    }
    
    return isValid;
}

// 开始文件分析
function startFileAnalysis(files) {
    // 先验证表单
    if (!validateForm()) {
        return;
    }
    
    // 检查用户是否登录
    const userInfo = getUserInfo();
    if (!userInfo || !userInfo.token) {
        loadingManager.showError('请先登录后再进行分析');
        showLoginPage();
        return;
    }
    
    const progressDiv = document.getElementById('analysis-progress');
    const resultsDiv = document.getElementById('results-container');
    const placeholder = document.getElementById('results-placeholder');

    progressDiv.style.display = 'block';
    placeholder.style.display = 'none';
    resultsDiv.style.display = 'none';

    // 模拟进度
    simulateProgress(100, 0);

    // 收集患者信息
    const patientInfo = {
        patient_id: document.getElementById('patient-id').value || `PAT_${Date.now().toString().slice(-6)}`,
        age: document.getElementById('patient-age').value,
        gender: document.getElementById('patient-gender').value,
        education: document.getElementById('patient-education').value,
        clinical_history: document.getElementById('patient-history').value,
        family_history: document.getElementById('patient-family').value,
        lifestyle: {
            exercise_frequency: document.getElementById('exercise-frequency').value,
            sleep_duration: document.getElementById('sleep-duration').value,
            diet_health: document.getElementById('diet-health').value,
            social_activities: document.getElementById('social-activities').value,
            smoking_status: document.getElementById('smoking-status').value,
            alcohol_consumption: document.getElementById('alcohol-consumption').value,
            cognitive_activities: document.getElementById('cognitive-activities').value
        }
    };

    // 创建FormData
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });
    formData.append('patient_info', JSON.stringify(patientInfo));

    // 发送到后端API
    setTimeout(() => {
        const headers = {
            'Authorization': `Bearer ${userInfo.token}`
        };
        
        fetch('/api/analyze', {
            method: 'POST',
            headers: headers,
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                simulateProgress(100, 100);
                setTimeout(() => {
                    progressDiv.style.display = 'none';
                    showResults(data);
                }, 500);
            } else {
                throw new Error(data.error || '分析失败');
            }
        })
        .catch(error => {
            console.error('分析失败:', error);
            loadingManager.showError('分析失败: ' + error.message);
            progressDiv.style.display = 'none';
            placeholder.style.display = 'flex';
            const fileInfo = document.getElementById('file-info');
            if (fileInfo) {
                fileInfo.style.display = 'none';
            }
        });
    }, 2000);
}

// 开始示例分析
function startDemoAnalysis(category = null) {
    const progressDiv = document.getElementById('analysis-progress');
    const resultsDiv = document.getElementById('results-container');
    const placeholder = document.getElementById('results-placeholder');
    const fileInfo = document.getElementById('file-info');

    progressDiv.style.display = 'block';
    placeholder.style.display = 'none';
    resultsDiv.style.display = 'none';
    fileInfo.style.display = 'none';

    // 模拟进度
    simulateProgress(100, 0);

    // 使用示例数据
    setTimeout(() => {
        let url = '/api/demo';
        if (category) {
            url += `?category=${category}`;
        }
        
        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('演示数据API返回:', data);
            // 检查是否有诊断结果
            if (data.results && data.results.pred_label) {
                simulateProgress(100, 100);
                setTimeout(() => {
                    progressDiv.style.display = 'none';
                    showResults(data);
                }, 500);
            } else {
                throw new Error('返回的数据格式不正确');
            }
        })
        .catch(error => {
            console.error('示例分析失败:', error);
            loadingManager.showError('示例分析失败: ' + error.message);
            progressDiv.style.display = 'none';
            placeholder.style.display = 'flex';
        });
    }, 2000);
}

// 模拟进度
function simulateProgress(totalSteps, currentStep = 0) {
    if (currentStep <= totalSteps) {
        const percentage = (currentStep / totalSteps) * 100;
        
        // 使用加载管理器更新进度
        loadingManager.updateProgress('progress-fill', percentage);
        
        // 计算当前步骤索引
        const steps = document.querySelectorAll('.progress-steps .step');
        const activeStepIndex = Math.floor((currentStep / totalSteps) * steps.length);
        
        // 更新步骤状态
        steps.forEach((step, index) => {
            if (index< activeStepIndex) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (index === activeStepIndex) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });

        if (currentStep < totalSteps) {
            setTimeout(() =>{
                simulateProgress(totalSteps, currentStep + 2);
            }, 100);
        }
    }
}

// 显示结果
function showResults(data) {
    const resultsContainer = document.getElementById('results-container');
    const resultsPlaceholder = document.getElementById('results-placeholder');
    const results = data.results || data.data || data;

    // 显示结果容器，隐藏占位符
    if (resultsPlaceholder) {
        resultsPlaceholder.style.display = 'none';
    }
    if (resultsContainer) {
        resultsContainer.style.display = 'block';
    }

    // 保存结果和患者信息到全局变量，供PDF生成使用
    window.currentResults = results;
    window.currentPatientInfo = {
        patient_id: document.getElementById('patient-id').value || `PAT_${Date.now().toString().slice(-6)}`,
        age: document.getElementById('patient-age').value,
        gender: document.getElementById('patient-gender').value,
        education: document.getElementById('patient-education').value,
        clinical_history: document.getElementById('patient-history').value,
        family_history: document.getElementById('patient-family').value,
        lifestyle: {
            exercise_frequency: document.getElementById('exercise-frequency').value,
            sleep_duration: document.getElementById('sleep-duration').value,
            diet_health: document.getElementById('diet-health').value,
            social_activities: document.getElementById('social-activities').value,
            smoking_status: document.getElementById('smoking-status').value,
            alcohol_consumption: document.getElementById('alcohol-consumption').value,
            cognitive_activities: document.getElementById('cognitive-activities').value
        }
    };
    
    // 颜色映射
    const colorMap = {
        'CN': '#10b981',
        'EMCI': '#f59e0b',
        'LMCI': '#f97316',
        'AD': '#ef4444'
    };

    const iconMap = {
        'CN': '<div class="diagnosis-icon cn"></div>',
        'EMCI': '<div class="diagnosis-icon emci"></div>',
        'LMCI': '<div class="diagnosis-icon lmci"></div>',
        'AD': '<div class="diagnosis-icon ad"></div>'
    };
    
    // 标签中文映射
    const labelChinese = {
        'CN': '认知正常',
        'EMCI': '早期轻度认知障碍',
        'LMCI': '晚期轻度认知障碍',
        'AD': '阿尔兹海默病'
    };

    // 如果没有提供医学建议，使用默认
    if (!results.medical_advice && results.pred_label) {
        const adviceMap = {
            'CN': [
                "认知功能正常，继续保持健康生活方式",
                "建议每年进行一次认知功能筛查",
                "保持地中海式饮食，多摄入Omega-3脂肪酸",
                "每周至少150分钟中等强度运动",
                "参与社交和认知训练活动"
            ],
            'EMCI': [
                "发现早期认知变化，建议密切监测",
                "每6个月进行一次神经心理学评估",
                "开始认知训练，特别是记忆和执行功能",
                "控制血管危险因素（血压、血糖、血脂）",
                "考虑进行ApoE基因检测"
            ],
            'LMCI': [
                "认知功能明显下降，需要积极干预",
                "建议神经科专科就诊",
                "进行全面的生物标志物检测",
                "开始药物和非药物治疗方案",
                "制定长期护理计划"
            ],
            'AD': [
                "高度怀疑阿尔兹海默病，立即就医",
                "尽快进行PET-CT或脑脊液检查确诊",
                "开始药物治疗（胆碱酯酶抑制剂等）",
                "制定全面的护理和支持计划",
                "参与临床试验和新治疗方案"
            ]
        };
        results.medical_advice = adviceMap[results.pred_label] || [];
    }

    // 如果没有中文标签，添加
    if (!results.chinese_label && results.pred_label) {
        results.chinese_label = labelChinese[results.pred_label] || results.pred_label;
    }

    // 生成置信度分布（如果不存在）
    if (!results.probabilities && results.pred_label) {
        results.probabilities = {};
        const labels = ['CN', 'EMCI', 'LMCI', 'AD'];
        const baseConfidence = results.confidence || 0.85;
        
        labels.forEach(label => {
            if (label === results.pred_label) {
                results.probabilities[label] = baseConfidence;
            } else {
                results.probabilities[label] = (1 - baseConfidence) / (labels.length - 1) * Math.random();
            }
        });
    }

    // 生成结果HTML - 优化布局结构
    let html = `
        <div class="results-header">
            <h3><i class="fas fa-diagnoses"></i> 多模态诊断结果</h3>
            <div class="results-meta">
                <span><i class="far fa-clock"></i> ${results.analysis_time || new Date().toLocaleString('zh-CN')}</span>
                <span><i class="fas fa-database"></i> ${data.modalities_used ? data.modalities_used.length : 4}模态融合</span>
            </div>
        </div>

        <div class="diagnosis-summary-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1.5rem;">
            <div class="summary-card" style="border-left: 4px solid ${colorMap[results.pred_label] || '#1e40af'}; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 0 12px 12px 0; padding: 2rem; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);">
                <div class="summary-title" style="font-size: 2.5rem; font-weight: 800; color: ${colorMap[results.pred_label] || '#1e40af'}">
                    ${results.pred_label}
                </div>
                <div class="summary-desc" style="color: #666; font-size: 1.2rem; margin-top: 0.5rem;">
                    ${results.chinese_label || ''}
                </div>
                <div class="summary-subtitle" style="color: #888; font-size: 1rem; margin-top: 0.5rem;">
                    <i class="fas fa-cogs"></i> 多模态融合分析完成
                </div>
                <div class="summary-stats" style="display: flex; gap: 2rem; margin-top: 1.5rem;">
                    <div class="stat">
                        <div class="stat-value" style="font-size: 1.8rem; font-weight: 700; color: #3b82f6;">${((results.confidence || 0.85) * 100).toFixed(1)}%</div>
                        <div class="stat-label" style="color: #6b7280; font-size: 0.9rem;">模型置信度</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" style="font-size: 1.8rem; font-weight: 700; color: #ef4444;">${((results.risk_score || 0.18) * 100).toFixed(1)}%</div>
                        <div class="stat-label" style="color: #6b7280; font-size: 0.9rem;">12个月进展风险</div>
                    </div>
                </div>
            </div>

            ${results.probabilities ? `
            <div class="confidence-section" style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <h4 style="font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;"><i class="fas fa-chart-bar"></i> 诊断置信度分布</h4>
                <div class="confidence-bars">
                    ${Object.entries(results.probabilities).map(([label, value]) => {
                        const isPredicted = label === results.pred_label;
                        const width = Math.min(value * 100, 100);
                        return `
                            <div class="confidence-bar" style="margin-bottom: 0.75rem;">
                                <div class="bar-label" style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                    <span class="label-text" style="font-weight: ${isPredicted ? '600' : '400'}; color: #374151; font-size: 0.9rem;">${label} - ${labelChinese[label] || label}</span>
                                    <span class="label-value" style="font-weight: 600; color: ${colorMap[label] || '#1e40af'}; font-size: 0.9rem;">${(value * 100).toFixed(1)}%</span>
                                </div>
                                <div class="bar-container" style="background: #e5e7eb; height: 10px; border-radius: 5px; overflow: hidden;">
                                    <div class="bar-fill" style="width: ${width}%; background: linear-gradient(90deg, ${colorMap[label] || '#1e40af'} 0%, ${colorMap[label] ? colorMap[label] + 'cc' : '#3b82f6'} 100%); ${isPredicted ? 'box-shadow: 0 2px 6px rgba(0,0,0,0.2);' : ''}"></div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
            ` : ''}
        </div>

        <div class="diagnosis-content" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem;">
            ${results.brain_image ? `
            <div class="brain-image-section" style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <div class="section-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="font-size: 1.1rem; font-weight: 600; color: #1f2937;"><i class="fas fa-brain"></i> 脑部图像分析</h4>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="btn btn-sm btn-outline" id="toggle-image" data-state="analyzed" title="切换到原始MRI影像">
                            <i class="fas fa-image"></i> 查看原始MRI
                        </button>
                        <button class="btn btn-sm btn-primary" id="brain-zoom" title="全屏放大查看">
                            <i class="fas fa-search-plus"></i> 全屏查看
                        </button>
                    </div>
                </div>
                <div class="brain-image-container" style="text-align: center; margin-bottom: 1rem;">
                    <img id="brain-img" src="data:image/png;base64,${results.brain_image}" 
                         alt="脑部图像分析"
                         class="brain-image clickable-image"
                         data-image-type="brain"
                         style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); border: 2px solid #e2e8f0; cursor: zoom-in; transition: all 0.3s ease;">
                    <img id="original-mri-img" src="data:image/png;base64,${results.original_mri_image || results.brain_image}" 
                         alt="原始MRI影像"
                         class="brain-image clickable-image"
                         data-image-type="brain"
                         style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); border: 2px solid #e2e8f0; cursor: zoom-in; display: none; transition: all 0.3s ease;">
                </div>
                <div class="brain-image-info" style="font-size: 0.85rem; color: #64748b; background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <p><strong><i class="fas fa-info-circle"></i> 图像说明：</strong></p>
                    <p id="image-description">此图像显示了基于诊断结果的脑部分析，<strong style="color: #ef4444;">红色标注区域</strong>表示病变位置，<strong style="color: #f59e0b;">橙色标注区域</strong>表示中度风险区域。用户可点击图像使用鼠标滚轮或双击进行放大查看。</p>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem; flex-wrap: wrap;">
                        <span><span style="color: #10b981;">●</span> 绿色：低风险/正常</span>
                        <span><span style="color: #f59e0b;">●</span> 黄色/橙色：中风险</span>
                        <span><span style="color: #ef4444;">●</span> 红色：高风险/病变</span>
                    </div>
                </div>
            </div>
            ` : ''}

            ${results.monthly_risk ? `
            <div class="monthly-risk-section" style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <h4 style="font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;"><i class="fas fa-chart-line"></i> 12个月进展风险趋势</h4>
                <div id="risk-trend-chart" style="width: 100%; height: 280px;"></div>
                <div class="risk-legend" style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; padding: 0.75rem; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <div class="legend-item" style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="legend-color" style="width: 20px; height: 12px; background: linear-gradient(90deg, rgba(16, 185, 129, 0.5), rgba(16, 185, 129, 0.3)); border: 1px solid rgba(16, 185, 129, 0.6); border-radius: 2px;"></span>
                        <span style="font-size: 0.85rem; color: #374151;">低风险 <span style="color: #10b981; font-weight: 600;">0-30%</span></span>
                    </div>
                    <div class="legend-item" style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="legend-color" style="width: 20px; height: 12px; background: linear-gradient(90deg, rgba(245, 158, 11, 0.5), rgba(245, 158, 11, 0.3)); border: 1px solid rgba(245, 158, 11, 0.6); border-radius: 2px;"></span>
                        <span style="font-size: 0.85rem; color: #374151;">中风险 <span style="color: #f59e0b; font-weight: 600;">30-60%</span></span>
                    </div>
                    <div class="legend-item" style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="legend-color" style="width: 20px; height: 12px; background: linear-gradient(90deg, rgba(239, 68, 68, 0.5), rgba(239, 68, 68, 0.3)); border: 1px solid rgba(239, 68, 68, 0.6); border-radius: 2px;"></span>
                        <span style="font-size: 0.85rem; color: #374151;">高风险 <span style="color: #ef4444; font-weight: 600;">60-100%</span></span>
                    </div>
                </div>
                <div class="risk-warning" style="margin-top: 0.75rem; padding: 0.5rem 1rem; background: linear-gradient(135deg, #fef3c7, #fde68a); border-left: 3px solid #f59e0b; border-radius: 4px; font-size: 0.8rem; color: #92400e;">
                    <i class="fas fa-exclamation-triangle" style="margin-right: 0.5rem;"></i>
                    <strong>注意：</strong>风险概率 > 60% 时建议密切监测并考虑临床干预
                </div>
            </div>
            ` : ''}
        </div>

        ${results.heatmap_image ? `
        <div class="heatmap-section" style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-top: 2rem;">
            <div class="section-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="font-size: 1.1rem; font-weight: 600; color: #1f2937;"><i class="fas fa-map"></i> 脑区风险热力图</h4>
                <div class="heatmap-controls" style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-sm btn-outline" id="heatmap-toggle" title="切换视图">
                        <i class="fas fa-exchange-alt"></i> 切换视图
                    </button>
                    <button class="btn btn-sm btn-outline" id="heatmap-download" title="下载热力图">
                        <i class="fas fa-download"></i> 下载
                    </button>
                    <button class="btn btn-sm btn-primary" id="heatmap-fullscreen" title="全屏放大查看">
                        <i class="fas fa-expand-arrows-alt"></i> 全屏查看
                    </button>
                </div>
            </div>
            <div class="heatmap-container" style="text-align: center; margin-bottom: 1rem; position: relative;">
                <img id="heatmap-img" src="data:image/png;base64,${results.heatmap_image}"
                     alt="风险热力图"
                     class="heatmap-image clickable-image"
                     data-image-type="heatmap"
                     style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); border: 2px solid #e2e8f0; cursor: zoom-in; transition: all 0.3s ease;">
            </div>
            <div class="heatmap-legend" style="display: flex; justify-content: center; gap: 1.5rem; padding: 0.75rem; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                <div class="legend-item"><span class="legend-color" style="background: linear-gradient(90deg, #ef4444 0%, #f87171 100%); width: 18px; height: 18px; display: inline-block; margin-right: 0.5rem; border-radius: 4px;"></span>高风险</div>
                <div class="legend-item"><span class="legend-color" style="background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%); width: 18px; height: 18px; display: inline-block; margin-right: 0.5rem; border-radius: 4px;"></span>中风险</div>
                <div class="legend-item"><span class="legend-color" style="background: linear-gradient(90deg, #10b981 0%, #34d399 100%); width: 18px; height: 18px; display: inline-block; margin-right: 0.5rem; border-radius: 4px;"></span>低风险</div>
            </div>
            <div class="heatmap-info-panel" style="margin-top: 1rem; padding: 1rem; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 8px; border: 1px solid #93c5fd;">
                <h5 style="font-size: 0.95rem; font-weight: 600; color: #1e40af; margin-bottom: 0.75rem;"><i class="fas fa-info-circle"></i> 如何理解脑区风险热力图</h5>
                <div style="font-size: 0.85rem; color: #1e3a8a; line-height: 1.6;">
                    <p style="margin-bottom: 0.5rem;"><strong>热力图原理：</strong>热力图叠加在原始MRI影像上，通过颜色差异展示不同脑区的风险程度。红色/橙色区域表示与阿尔兹海默症相关的病理变化高发区，绿色区域表示相对正常的脑组织。</p>
                    <p style="margin-bottom: 0.5rem;"><strong>视图说明：</strong>系统从三个正交平面展示脑部结构：横断面（水平切面）、矢状面（侧面）、冠状面（前后切面），便于全面观察脑区异常。</p>
                    <p style="margin-bottom: 0;"><strong>关键区域：</strong>海马体（记忆形成核心）、颞叶（语言与记忆）、前额叶（决策与执行功能）是阿尔兹海默症最早影响的脑区，请重点关注这些区域的颜色变化。</p>
                </div>
            </div>
        </div>
        ` : ''}

        ${results.risk_indicators ? `
        <div class="risk-indicators" style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-top: 2rem;">
            <h4 style="font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;"><i class="fas fa-exclamation-triangle"></i> 关键风险指标</h4>
            <div class="indicators-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                ${Object.entries(results.risk_indicators).slice(0, 6).map(([indicator, data]) => {
                    const riskClass = data.risk_level || 'low';
                    const indicatorColor = {'high': '#ef4444', 'medium': '#f59e0b', 'low': '#10b981'}[riskClass] || '#64748b';
                    const value = data.value || 50;
                    const riskText = {'high': '高风险', 'medium': '中风险', 'low': '低风险'}[riskClass] || '未知';
                    const description = data.description || {
                        '海马体萎缩': '海马体是记忆形成的关键脑区，其萎缩程度是阿尔兹海默症早期诊断的重要标志物',
                        'p-tau217浓度': '磷酸化tau蛋白217位点，是阿尔兹海默症病理过程的核心生物标志物',
                        'Aβ42/Aβ40比率': 'β淀粉样蛋白42与40的比率，降低表明大脑中存在淀粉样斑块沉积',
                        '脑葡萄糖代谢率': '大脑利用葡萄糖的效率，后部脑区代谢降低是阿尔兹海默症的典型特征',
                        '白质高信号': 'MRI影像中显示的白质病变程度，与认知功能下降和血管性认知障碍相关',
                        '脑体积减少率': '全脑或特定区域体积随时间减少的速度，阿尔兹海默症患者脑萎缩加速'
                    }[indicator] || '该指标反映了您的健康状况';
                    const normalRange = data.normal_range || {
                        '海马体萎缩': '正常: <30%',
                        'p-tau217浓度': '正常: <60 pg/mL',
                        'Aβ42/Aβ40比率': '正常: >0.8',
                        '脑葡萄糖代谢率': '正常: >95%',
                        '白质高信号': '正常: <20%',
                        '脑体积减少率': '正常: <0.5%/年'
                    }[indicator] || '';
                    const unit = data.unit || '';
                    return `
                        <div class="indicator-card" style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-left: 3px solid ${indicatorColor}; border-radius: 0 6px 6px 0; padding: 1rem; border: 1px solid #e2e8f0;">
                            <div class="indicator-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <span class="indicator-name" style="font-weight: 600; font-size: 0.9rem; color: #374151;">${indicator}</span>
                                <span class="indicator-risk" style="color: ${indicatorColor}; font-weight: 600; font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 10px; background: ${indicatorColor}15;">${riskText}</span>
                            </div>
                            <div class="indicator-description" style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; line-height: 1.4;">${description}</div>
                            <div class="indicator-progress" style="margin-top: 0.5rem;">
                                <div class="progress-bar" style="background: ${indicatorColor}20; height: 6px; border-radius: 3px; overflow: hidden;">
                                    <div class="progress-fill" style="width: ${Math.min(value, 100)}%; background: linear-gradient(90deg, ${indicatorColor} 0%, ${indicatorColor}cc 100%); height: 100%;"></div>
                                </div>
                                <div class="indicator-value" style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.25rem;">
                                    <span style="color: ${indicatorColor}; font-weight: 600; font-size: 0.9rem;">${value.toFixed(1)}${unit}</span>
                                    <span class="indicator-normal" style="font-size: 0.7rem; color: #10b981; background: #d1fae5; padding: 0.1rem 0.4rem; border-radius: 4px;">${normalRange}</span>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
        ` : ''}

        ${results.medical_advice ? `
        <div class="advice-section" style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-top: 2rem;">
            <h4 style="font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;"><i class="fas fa-user-md"></i> 个性化医学建议</h4>
            <div class="advice-list" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
                ${results.medical_advice.map((advice, index) => `
                    <div class="advice-item" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 3px solid #3b82f6; border-radius: 0 6px 6px 0; padding: 1rem; display: flex; gap: 0.75rem; border: 1px solid #dbeafe;">
                        <div class="advice-number" style="background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%); color: white; min-width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 600; flex-shrink: 0;">${index + 1}</div>
                        <div class="advice-text" style="flex: 1; line-height: 1.5; color: #374151; font-size: 0.9rem;">${advice}</div>
                    </div>
                `).join('')}
            </div>
        </div>
        ` : ''}

        <div class="results-actions" style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem; padding: 1.5rem; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0;">
            <button class="btn btn-primary" id="view-detailed-report">
                <i class="fas fa-file-medical-alt"></i> 查看详细报告
            </button>
            <button class="btn btn-success" id="generate-pdf-from-results">
                <i class="fas fa-file-pdf"></i> 生成PDF报告
            </button>
            <button class="btn btn-outline" onclick="startNewDiagnosis()">
                <i class="fas fa-redo"></i> 新的诊断
            </button>
        </div>
    `;

    // 添加CSS样式
    const style = document.createElement('style');
    style.textContent = `
        /* 诊断结果容器 */
        .results-header {
            margin-bottom: 2rem;
        }
        
        .results-meta {
            display: flex;
            gap: 1.5rem;
            margin-top: 0.75rem;
            color: #6b7280;
            font-size: 0.9rem;
        }
        
        .results-meta i {
            margin-right: 0.5rem;
        }
        
        /* 诊断摘要 */
        .diagnosis-summary {
            margin-bottom: 2rem;
        }
        
        .summary-card {
            transition: all 0.3s ease;
        }
        
        .summary-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.15);
        }
        
        /* 主要内容布局 */
        .diagnosis-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .visualization-column,
        .metrics-column {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }
        
        /* 各模块通用样式 */
        .brain-image-section,
        .heatmap-section,
        .confidence-section,
        .monthly-risk-section,
        .risk-indicators,
        .advice-section {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
        }
        
        .brain-image-section:hover,
        .heatmap-section:hover,
        .confidence-section:hover,
        .monthly-risk-section:hover,
        .risk-indicators:hover,
        .advice-section:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* 图像容器 */
        .brain-image-container,
        .heatmap-container {
            text-align: center;
            margin-bottom: 1.5rem;
        }
        
        .brain-image,
        .heatmap-image {
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .brain-image:hover,
        .heatmap-image:hover {
            transform: scale(1.02);
            box-shadow: 0 15px 35px rgba(0,0,0,0.25);
        }
        
        /* 热力图控制 */
        .heatmap-controls {
            display: flex;
            gap: 0.75rem;
            justify-content: center;
            margin-top: 1rem;
        }
        
        /* 指标网格 */
        .indicators-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.25rem;
        }
        
        /* 操作按钮 */
        .results-actions {
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            margin-top: 2.5rem;
            margin-bottom: 2rem;
        }
        
        /* 按钮样式 */
        .btn {
            padding: 0.75rem 1.5rem;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: white;
            color: #4b5563;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn:hover {
            background: #f3f4f6;
            transform: translateY(-1px);
        }
        
        .btn-sm {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
        
        .btn-outline {
            border-color: #e5e7eb;
        }
        
        .btn-primary {
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }
        
        .btn-primary:hover {
            background: #2563eb;
            transform: translateY(-1px);
        }
        
        .btn-success {
            background: #10b981;
            color: white;
            border-color: #10b981;
        }
        
        .btn-success:hover {
            background: #059669;
            transform: translateY(-1px);
        }
        
        /* 响应式设计 */
        @media (max-width: 1024px) {
            .diagnosis-content {
                grid-template-columns: 1fr;
            }
            
            .indicators-grid {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 640px) {
            .results-actions {
                flex-direction: column;
                align-items: center;
            }
            
            .results-actions button {
                width: 100%;
                max-width: 300px;
                justify-content: center;
            }
            
            .indicators-grid {
                grid-template-columns: 1fr;
            }
            
            .diagnosis-summary {
                padding: 1.5rem;
            }
            
            .brain-image-section,
            .heatmap-section,
            .confidence-section,
            .monthly-risk-section,
            .risk-indicators,
            .advice-section {
                padding: 1.5rem;
            }
        }
        
        /* 部分标题 */
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .section-header h4 {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1f2937;
            margin: 0;
        }
        
        /* 医学建议 */
        .advice-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
        }
        
        .advice-item {
            transition: all 0.3s ease;
        }
        
        .advice-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* 置信度条 */
        .confidence-bar {
            margin-bottom: 1rem;
        }
        
        .bar-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }
        
        .bar-container {
            background: #e5e7eb;
            height: 12px;
            border-radius: 6px;
            overflow: hidden;
        }
        
        .bar-fill {
            transition: width 0.5s ease;
        }
        
        /* 指标卡片 */
        .indicator-card {
            transition: all 0.3s ease;
        }
        
        .indicator-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* 统计数据 */
        .summary-stats {
            display: flex;
            gap: 2rem;
            margin-top: 1rem;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        
        .stat-label {
            color: #6b7280;
            font-size: 0.9rem;
        }
    `;
    document.head.appendChild(style);

    // 热力图交互功能将在HTML渲染完成后绑定
    let bindHeatmapEvents = function() {
        setTimeout(function() {
            const heatmapImg = document.getElementById('heatmap-img');
            const heatmapDownload = document.getElementById('heatmap-download');
            const heatmapZoom = document.getElementById('heatmap-zoom');
            const heatmapToggle = document.getElementById('heatmap-toggle');
            const heatmapInfo = document.getElementById('heatmap-info');
            const heatmapInfoPanel = document.getElementById('heatmap-info-panel');

            let currentViewIndex = 0;
            const viewTypes = ['热力图视图', 'MRI原始视图', '叠加视图'];
            let isOverlaid = false;

            // 切换视图功能
            if (heatmapToggle && heatmapImg) {
                heatmapToggle.addEventListener('click', function() {
                    currentViewIndex = (currentViewIndex + 1) % viewTypes.length;
                    const currentView = viewTypes[currentViewIndex];
                    heatmapToggle.innerHTML = '<i class="fas fa-exchange-alt"></i> ' + currentView;
                    heatmapToggle.title = currentView;

                    if (currentViewIndex === 0) {
                        // 热力图视图
                        heatmapImg.style.opacity = '1';
                    } else if (currentViewIndex === 1) {
                        // MRI原始视图 - 降低热力图透明度
                        heatmapImg.style.opacity = '0.3';
                    } else {
                        // 叠加视图 - 半透明
                        heatmapImg.style.opacity = '0.7';
                    }
                });
            }

            // 下载热力图
            if (heatmapDownload) {
                heatmapDownload.addEventListener('click', function() {
                    // 获取base64数据
                    let base64Data = heatmapImg.src;
                    if (base64Data.startsWith('data:image/png;base64,')) {
                        base64Data = base64Data.split(',')[1];
                    }
                    
                    // 使用POST请求下载热力图
                    fetch('/api/download-heatmap', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ data: base64Data })
                    })
                        .then(response => {
                            if (response.ok) {
                                return response.json();
                            }
                            throw new Error('下载失败');
                        })
                        .then(data => {
                            if (data.success) {
                                // 显示下载成功提示
                                loadingManager.showSuccess('热力图下载成功，已保存到项目results/grad_cam文件夹');
                            } else {
                                throw new Error(data.error || '下载失败');
                            }
                        })
                        .catch(error => {
                            console.error('下载失败:', error);
                            loadingManager.showError('热力图下载失败');
                        });
                });
            }
            
            // 放大热力图和拖动功能
            if (heatmapZoom && heatmapImg) {
                let isDragging = false;
                let startX, startY;
                let translateX = 0, translateY = 0;
                let scale = 1;
                let startDistance, startScale;
                const minScale = 0.5;
                const maxScale = 3;
                
                // 设置图片容器样式
                const container = heatmapImg.parentElement;
                container.style.position = 'relative';
                container.style.cursor = 'zoom-in';
                container.style.overflow = 'hidden';
                container.style.borderRadius = '12px';
                
                heatmapImg.style.transformOrigin = 'center center';
                heatmapImg.style.transition = 'transform 0.1s ease';
                heatmapImg.style.maxWidth = '100%';
                heatmapImg.style.height = 'auto';
                
                // 添加缩放级别指示器
                const zoomIndicator = document.createElement('div');
                zoomIndicator.className = 'zoom-indicator';
                zoomIndicator.style.position = 'absolute';
                zoomIndicator.style.bottom = '10px';
                zoomIndicator.style.right = '10px';
                zoomIndicator.style.background = 'rgba(0, 0, 0, 0.7)';
                zoomIndicator.style.color = 'white';
                zoomIndicator.style.padding = '4px 8px';
                zoomIndicator.style.borderRadius = '4px';
                zoomIndicator.style.fontSize = '0.8rem';
                zoomIndicator.style.zIndex = '10';
                zoomIndicator.innerHTML = '100%';
                container.appendChild(zoomIndicator);
                
                // 更新缩放指示器
                function updateZoomIndicator() {
                    zoomIndicator.innerHTML = `${Math.round(scale * 100)}%`;
                }
                
                // 缩放函数
                function zoom(factor, centerX, centerY) {
                    const newScale = Math.max(minScale, Math.min(maxScale, scale * factor));
                    if (newScale !== scale) {
                        const relativeX = centerX - container.getBoundingClientRect().left - translateX;
                        const relativeY = centerY - container.getBoundingClientRect().top - translateY;
                        translateX += relativeX * (1 - newScale / scale);
                        translateY += relativeY * (1 - newScale / scale);
                        scale = newScale;
                        heatmapImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                        updateZoomIndicator();
                        
                        // 更新光标和按钮状态
                        if (scale > 1) {
                            heatmapImg.style.cursor = 'grab';
                            heatmapZoom.innerHTML = '<i class="fas fa-search-minus"></i> 缩小查看';
                            heatmapZoom.title = '缩小热力图';
                        } else {
                            heatmapImg.style.cursor = 'zoom-in';
                            heatmapZoom.innerHTML = '<i class="fas fa-search-plus"></i> 放大查看';
                            heatmapZoom.title = '放大热力图';
                        }
                    }
                }
                
                // 重置视图
                function resetView() {
                    scale = 1;
                    translateX = 0;
                    translateY = 0;
                    heatmapImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                    heatmapImg.style.cursor = 'zoom-in';
                    heatmapZoom.innerHTML = '<i class="fas fa-search-plus"></i> 放大查看';
                    heatmapZoom.title = '放大热力图';
                    updateZoomIndicator();
                }
                
                // 放大/缩小按钮
                heatmapZoom.addEventListener('click', function() {
                    if (scale === 1) {
                        zoom(1.5, container.getBoundingClientRect().left + container.offsetWidth / 2, container.getBoundingClientRect().top + container.offsetHeight / 2);
                    } else {
                        resetView();
                    }
                });
                
                // 鼠标滚轮缩放
                container.addEventListener('wheel', function(e) {
                    e.preventDefault();
                    const rect = container.getBoundingClientRect();
                    const centerX = e.clientX;
                    const centerY = e.clientY;
                    const delta = e.deltaY > 0 ? 0.9 : 1.1;
                    zoom(delta, centerX, centerY);
                });
                
                // 点击图片放大
                heatmapImg.addEventListener('click', function(e) {
                    if (scale === 1) {
                        zoom(1.5, e.clientX, e.clientY);
                    }
                });
                
                // 拖动功能
                heatmapImg.addEventListener('mousedown', function(e) {
                    if (scale > 1) {
                        isDragging = true;
                        startX = e.clientX - translateX;
                        startY = e.clientY - translateY;
                        heatmapImg.style.cursor = 'grabbing';
                        e.preventDefault();
                    }
                });
                
                document.addEventListener('mousemove', function(e) {
                    if (isDragging && scale > 1) {
                        translateX = e.clientX - startX;
                        translateY = e.clientY - startY;
                        heatmapImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                    }
                });
                
                document.addEventListener('mouseup', function() {
                    if (isDragging) {
                        isDragging = false;
                        heatmapImg.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
                    }
                });
                
                // 触摸设备支持
                heatmapImg.addEventListener('touchstart', function(e) {
                    if (scale > 1 && e.touches.length === 1) {
                        isDragging = true;
                        startX = e.touches[0].clientX - translateX;
                        startY = e.touches[0].clientY - translateY;
                        e.preventDefault();
                    } else if (e.touches.length === 2) {
                        // 双指缩放
                        const touch1 = e.touches[0];
                        const touch2 = e.touches[1];
                        const distance = Math.sqrt(
                            Math.pow(touch2.clientX - touch1.clientX, 2) +
                            Math.pow(touch2.clientY - touch1.clientY, 2)
                        );
                        startDistance = distance;
                        startScale = scale;
                    }
                });
                
                document.addEventListener('touchmove', function(e) {
                    if (isDragging && scale > 1 && e.touches.length === 1) {
                        translateX = e.touches[0].clientX - startX;
                        translateY = e.touches[0].clientY - startY;
                        heatmapImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                        e.preventDefault();
                    } else if (e.touches.length === 2) {
                        const touch1 = e.touches[0];
                        const touch2 = e.touches[1];
                        const distance = Math.sqrt(
                            Math.pow(touch2.clientX - touch1.clientX, 2) +
                            Math.pow(touch2.clientY - touch1.clientY, 2)
                        );
                        const scaleFactor = distance / startDistance;
                        const newScale = Math.max(minScale, Math.min(maxScale, startScale * scaleFactor));
                        if (newScale !== scale) {
                            scale = newScale;
                            heatmapImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                            updateZoomIndicator();
                        }
                    }
                });
                
                document.addEventListener('touchend', function() {
                    isDragging = false;
                    heatmapImg.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
                });
            }
            
            // 显示/隐藏热力图说明
            if (heatmapInfo && heatmapInfoPanel) {
                heatmapInfo.addEventListener('click', function() {
                    if (heatmapInfoPanel.style.display === 'none') {
                        heatmapInfoPanel.style.display = 'block';
                        heatmapInfo.innerHTML = '<i class="fas fa-times"></i> 关闭说明';
                        heatmapInfo.title = '关闭说明';
                    } else {
                        heatmapInfoPanel.style.display = 'none';
                        heatmapInfo.innerHTML = '<i class="fas fa-info-circle"></i> 热力图说明';
                        heatmapInfo.title = '热力图说明';
                    }
                });
            }
        }, 100);
    };
    
    // 添加操作按钮 - 已在showResults中提供，此处不再重复
    // 保持与快速视图一致的UI

    resultsContainer.innerHTML = html;
    resultsContainer.style.display = 'block';
    
    // 隐藏placeholder
    const placeholder = document.getElementById('results-placeholder');
    if (placeholder) {
        placeholder.style.display = 'none';
    }

    // 为按钮添加事件监听器
    setTimeout(() => {
        const reportBtn = document.getElementById('view-detailed-report');
        if (reportBtn) {
            reportBtn.addEventListener('click', () => {
                openDetailedReport(results, data);
            });
        }
        
        const pdfBtn = document.getElementById('generate-pdf-from-results');
        if (pdfBtn) {
            pdfBtn.addEventListener('click', () => {
                generatePDFReportFromResults(results);
            });
        }
        
        // 绑定热力图事件
        bindHeatmapEvents();
        
        // 保存诊断结果到全局变量，供ECharts加载完成后使用
        window.currentDiagnosisResults = results;
        
        // 渲染每月进展风险折线图
        function renderRiskTrendChart(monthlyRiskData) {
            console.log('开始渲染风险趋势图，数据:', monthlyRiskData);
            
            // 等待DOM完全渲染
            setTimeout(() => {
                console.log('等待DOM渲染完成...');
                
                // 再次检查容器
                const chartDom = document.getElementById('risk-trend-chart');
                console.log('图表容器:', chartDom);
                console.log('图表容器是否存在:', !!chartDom);
                
                if (!chartDom) {
                    console.error('图表容器未找到，重试中...');
                    setTimeout(() => renderRiskTrendChart(monthlyRiskData), 200);
                    return;
                }
                
                console.log('图表容器已找到');
                console.log('图表容器尺寸:', chartDom.offsetWidth, 'x', chartDom.offsetHeight);
                
                // 确保容器有足够的尺寸
                if (chartDom.offsetWidth === 0 || chartDom.offsetHeight === 0) {
                    console.error('图表容器尺寸为0，等待尺寸更新...');
                    setTimeout(() => renderRiskTrendChart(monthlyRiskData), 200);
                    return;
                }
                
                // 检查ECharts是否已加载
                if (typeof echarts === 'undefined') {
                    console.log('ECharts 尚未加载，等待中...');
                    setTimeout(() => renderRiskTrendChart(monthlyRiskData), 100);
                    return;
                }
                console.log('ECharts已加载');
                console.log('ECharts版本:', echarts.version);
            
                try {
                    const myChart = echarts.init(chartDom);
                    console.log('图表初始化成功');
            
                    // 准备数据
                    console.log('原始数据:', monthlyRiskData);
                    const months = monthlyRiskData.map(item => item.month + '月');
                    console.log('月份数据:', months);
            
                    // 检查数据是否已经是百分比格式
                    const riskData = monthlyRiskData.map(item => {
                        const riskValue = parseFloat(item.risk);
                        // 如果值在0-1之间，说明是小数概率，需要转换为百分比
                        if (riskValue >= 0 && riskValue <= 1) {
                            return parseFloat((riskValue * 100).toFixed(1));
                        }
                        // 否则直接使用（可能已经是百分比）
                        return parseFloat(riskValue.toFixed(1));
                    });
                    console.log('风险数据:', riskData);
            
                    // 检查数据有效性
                    if (!riskData || riskData.length === 0) {
                        console.error('风险数据为空');
                        return;
                    }
            
                    // 图表配置，添加风险区域背景和区域填充
                    const option = {
                        tooltip: {
                            trigger: 'axis',
                            formatter: function(params) {
                                const value = params[0].data;
                                let riskLevel = '';
                                let riskColor = '';
                                if (value < 30) {
                                    riskLevel = '低风险';
                                    riskColor = '#10b981';
                                } else if (value < 60) {
                                    riskLevel = '中风险';
                                    riskColor = '#f59e0b';
                                } else {
                                    riskLevel = '高风险';
                                    riskColor = '#ef4444';
                                }
                                return params[0].axisValue + '<br/>风险概率: <span style="color:' + riskColor + '; font-weight:bold;">' + value + '%</span><br/>风险等级: <span style="color:' + riskColor + '; font-weight:bold;">' + riskLevel + '</span>';
                            }
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            top: '15%',
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: months
                        },
                        yAxis: {
                            type: 'value',
                            min: 0,
                            max: 100,
                            axisLabel: {
                                formatter: '{value}%'
                            }
                        },
                        series: [
                            {
                                name: '进展风险',
                                type: 'line',
                                smooth: true,
                                data: riskData,
                                lineStyle: {
                                    width: 3,
                                    color: '#3b82f6'
                                },
                                itemStyle: {
                                    color: '#3b82f6'
                                },
                                showSymbol: true,
                                symbolSize: 6,
                                areaStyle: {
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                        { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
                                        { offset: 1, color: 'rgba(59, 130, 246, 0.1)' }
                                    ])
                                },
                                // 添加风险区域背景
                                markArea: {
                                    silent: true,
                                    data: [
                                        // 低风险区域（0-30%）
                                        [
                                            {
                                                yAxis: 0,
                                                itemStyle: {
                                                    color: 'rgba(16, 185, 129, 0.3)',
                                                    borderColor: 'rgba(16, 185, 129, 0.6)',
                                                    borderWidth: 1
                                                }
                                            },
                                            {
                                                yAxis: 30
                                            }
                                        ],
                                        // 中风险区域（30-60%）
                                        [
                                            {
                                                yAxis: 30,
                                                itemStyle: {
                                                    color: 'rgba(245, 158, 11, 0.3)',
                                                    borderColor: 'rgba(245, 158, 11, 0.6)',
                                                    borderWidth: 1
                                                }
                                            },
                                            {
                                                yAxis: 60
                                            }
                                        ],
                                        // 高风险区域（60-100%）
                                        [
                                            {
                                                yAxis: 60,
                                                itemStyle: {
                                                    color: 'rgba(239, 68, 68, 0.3)',
                                                    borderColor: 'rgba(239, 68, 68, 0.6)',
                                                    borderWidth: 1
                                                }
                                            },
                                            {
                                                yAxis: 100
                                            }
                                        ]
                                    ]
                                },
                                // 添加风险等级标签
                                markLine: {
                                    silent: true,
                                    label: {
                                        position: 'end',
                                        formatter: '{b}'
                                    },
                                    lineStyle: {
                                        type: 'dashed',
                                        color: '#999'
                                    },
                                    data: [
                                        { yAxis: 30, name: '低风险 (< 30%)' },
                                        { yAxis: 60, name: '中风险 (30-60%)' },
                                        { yAxis: 100, name: '高风险 (> 60%)' }
                                    ]
                                }
                            }
                        ]
                    };
            
                    console.log('图表配置:', option);
                    console.log('设置图表选项');
                    myChart.setOption(option);
            
                    console.log('图表渲染完成');
                    console.log('图表实例:', myChart);
                    console.log('图表容器尺寸:', chartDom.offsetWidth, 'x', chartDom.offsetHeight);
            
                    // 响应式调整
                    window.addEventListener('resize', () => {
                        myChart.resize();
                    });
                    
                    // 手动触发一次resize确保图表正确显示
                    setTimeout(() => {
                        myChart.resize();
                        console.log('手动触发resize');
                    }, 500);
                    
                } catch (error) {
                    console.error('图表渲染出错:', error);
                }
            }, 300); // 增加延迟时间确保DOM完全渲染
        }
        
        // 如果ECharts已加载，立即渲染；否则等待ECharts加载完成后自动渲染
        if (results.monthly_risk) {
            console.log('准备渲染风险趋势图，数据:', results.monthly_risk);
            console.log('ECharts是否可用:', typeof echarts !== 'undefined');
            
            if (typeof echarts !== 'undefined') {
                renderRiskTrendChart(results.monthly_risk);
            } else {
                console.log('ECharts 尚未加载，将在加载完成后自动渲染风险趋势图');
                // 设置一个定时器，定期检查ECharts是否加载完成
                const checkEChartsInterval = setInterval(() => {
                    if (typeof echarts !== 'undefined') {
                        console.log('ECharts加载完成，开始渲染风险趋势图');
                        renderRiskTrendChart(results.monthly_risk);
                        clearInterval(checkEChartsInterval);
                    }
                }, 500);
                
                // 最多等待10秒
                setTimeout(() => {
                    clearInterval(checkEChartsInterval);
                    console.log('ECharts加载超时');
                }, 10000);
            }
        }
    }, 100);

    // 保存患者数据
    savePatientData(window.currentPatientInfo, results);
    
    // 绑定图像切换按钮事件
    setTimeout(() => {
        const toggleButton = document.getElementById('toggle-image');
        if (toggleButton) {
            toggleButton.addEventListener('click', function() {
                const brainImg = document.getElementById('brain-img');
                const originalImg = document.getElementById('original-mri-img');
                const imageDescription = document.getElementById('image-description');
                const riskLevels = document.getElementById('risk-levels');
                
                if (brainImg && originalImg) {
                    if (this.dataset.state === 'analyzed') {
                        // 切换到原始MRI影像
                        brainImg.style.display = 'none';
                        originalImg.style.display = 'block';
                        this.dataset.state = 'original';
                        this.innerHTML = '<i class="fas fa-brain"></i> 查看分析图像';
                        this.title = '切换到分析图像';
                        
                        if (imageDescription) {
                            imageDescription.textContent = '此图像显示了原始MRI扫描结果，未添加任何分析标记。';
                        }
                        if (riskLevels) {
                            riskLevels.style.display = 'none';
                        }
                    } else {
                        // 切换到分析图像
                        brainImg.style.display = 'block';
                        originalImg.style.display = 'none';
                        this.dataset.state = 'analyzed';
                        this.innerHTML = '<i class="fas fa-image"></i> 查看原始MRI';
                        this.title = '切换到原始MRI影像';
                        
                        if (imageDescription) {
                            imageDescription.textContent = '此图像显示了基于诊断结果的脑部分析，标记了可能存在异常的区域。不同颜色表示不同的风险级别：';
                        }
                        if (riskLevels) {
                            riskLevels.style.display = 'block';
                        }
                    }
                }
            });
        }
    }, 100);
    
    setTimeout(() => {
        const brainZoomBtn = document.getElementById('brain-zoom');
        const heatmapFullscreenBtn = document.getElementById('heatmap-fullscreen');
        
        if (brainZoomBtn) {
            brainZoomBtn.addEventListener('click', function() {
                const currentImg = document.getElementById('brain-img');
                const originalImg = document.getElementById('original-mri-img');
                const activeImg = currentImg && currentImg.style.display !== 'none' ? currentImg : originalImg;
                if (activeImg && activeImg.style.display !== 'none') {
                    openImageModal(activeImg.src, '脑部图像分析', 'brain');
                }
            });
        }
        
        if (heatmapFullscreenBtn) {
            heatmapFullscreenBtn.addEventListener('click', function() {
                const heatmapImg = document.getElementById('heatmap-img');
                if (heatmapImg) {
                    openImageModal(heatmapImg.src, '脑区风险热力图', 'heatmap');
                }
            });
        }
        
        document.querySelectorAll('.clickable-image').forEach(img => {
            img.addEventListener('click', function() {
                openImageModal(this.src, this.alt || '图像预览', this.dataset.imageType || 'unknown');
            });
            
            img.addEventListener('dblclick', function() {
                openImageModal(this.src, this.alt || '图像预览', this.dataset.imageType || 'unknown');
            });
        });
    }, 150);
    
    showToast('多模态分析完成！', 'success');
}

// 查看详细报告
function openDetailedReport(results, fullData) {
    console.log("正在生成详细报告...");
    
    const modal = document.getElementById('results-modal');
    const modalBody = document.getElementById('modal-body');
    
    // 生成报告HTML
    let html = `
        <div class="detailed-report">
            <div class="report-header">
                <h3><i class="fas fa-file-medical-alt"></i> 详细诊断报告</h3>
                <div class="report-meta">
                    <div>报告编号：RPT-${Date.now().toString().slice(-8)}</div>
                    <div>生成时间：${new Date().toLocaleString('zh-CN')}</div>
                </div>
            </div>
            
            <div class="report-section">
                <h4><i class="fas fa-diagnoses"></i> 诊断摘要</h4>
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="label">诊断类别：</span>
                        <span class="value highlight">${results.pred_label} - ${results.chinese_label || results.pred_label}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">诊断置信度：</span>
                        <span class="value">${(results.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">12个月进展概率：</span>
                        <span class="value ${results.risk_score > 0.5 ? 'danger' : results.risk_score > 0.2 ? 'warning' : 'safe'}">
                            ${(results.risk_score * 100).toFixed(1)}%
                        </span>
                    </div>
                    <div class="summary-item">
                        <span class="label">综合风险等级：</span>
                        <span class="value ${results.risk_score > 0.5 ? 'danger' : results.risk_score > 0.2 ? 'warning' : 'safe'}">
                            ${results.risk_score > 0.5 ? '高风险' : results.risk_score > 0.2 ? '中风险' : '低风险'}
                        </span>
                    </div>
                </div>
            </div>
    `;
    
    // 模态信息
    if (fullData.modalities_used) {
        html += `
            <div class="report-section">
                <h4><i class="fas fa-database"></i> 多模态数据</h4>
                <div class="modality-info">
                    <p><strong>使用的数据模态：</strong> ${fullData.modalities_used.join(', ')}</p>
        `;
        
        if (fullData.modality_weights) {
            html += `<p><strong>模态融合权重：</strong></p><ul>`;
            Object.entries(fullData.modality_weights).forEach(([modality, weight]) => {
                html += `<li>${modality}: ${(weight * 100).toFixed(1)}%</li>`;
            });
            html += `</ul>`;
        }
        
        html += `</div></div>`;
    }
    
    // 风险指标表格
    if (results.risk_indicators) {
        html += `
            <div class="report-section">
                <h4><i class="fas fa-chart-bar"></i> 风险指标分析</h4>
                <div class="risk-indicators-table">
                    <table>
                        <thead>
                            <tr>
                                <th>指标名称</th>
                                <th>指标描述</th>
                                <th>当前值</th>
                                <th>参考范围</th>
                                <th>风险等级</th>
                            </tr>
                        </thead>
                        <tbody>
        `;
        
        // 指标描述映射
        const indicatorDescriptions = {
            'MRI脑萎缩程度': '通过脑部核磁共振(MRI)扫描测量大脑总体积与正常值的差异。脑萎缩是神经元丢失的标志，萎缩程度越高，认知功能衰退的速度越快，尤其是记忆、思维和行为能力会受到明显影响。正常老年人每年脑体积减少约0.5-1%，超过这个范围提示异常。',
            '脑脊液Aβ42水平': '通过腰椎穿刺采集脑脊液检测淀粉样蛋白Aβ42的浓度。Aβ42是阿尔茨海默病特征性病理蛋白，低水平(<500 pg/mL)提示大脑中已有大量淀粉样蛋白沉积，这是疾病早期阶段的重要生物标志物，比症状出现早5-10年。',
            '脑脊液Tau蛋白': '脑脊液中磷酸化tau蛋白的浓度检测。Tau蛋白是神经元内维持细胞结构的重要蛋白，异常磷酸化的tau蛋白会形成神经纤维缠结，高水平(>200 pg/mL)直接反映神经元损伤和死亡程度，是神经退行性病变的核心标志。',
            '海马体积': '通过MRI测量大脑海马区域的体积。海马是学习记忆的中枢，位于大脑内侧颞叶，体积缩小与记忆障碍高度相关。正常老年人海马体积每年减少约1-2%，阿尔茨海默病患者减少速度可达3-5%。',
            '前额叶皮层厚度': '前额叶皮层负责注意力、执行功能、决策和情绪调节。厚度变薄会影响工作记忆、计划能力和自我控制。通过MRI测量皮层厚度，厚度低于同年龄段正常范围提示认知功能下降风险增加。',
            '认知评分': '通过标准化神经心理测试评估多个认知领域：记忆力(情景记忆、工作记忆)、注意力、语言功能、执行功能和视空间能力。常用测试包括MMSE(简易精神状态检查)、MoCA(蒙特利尔认知评估)等，分数低于正常值提示认知功能受损。',
            'APOE基因风险': 'APOE基因编码载脂蛋白E，有ε2、ε3、ε4三种等位基因。携带ε4等位基因会增加患病风险：ε4/ε4基因型风险增加10-15倍，ε3/ε4增加2-3倍。但基因只是风险因素，不是决定性因素，还需结合其他临床指标综合评估。',
            '年龄风险因子': '年龄是阿尔茨海默病最强的风险因素。65岁以后每增加5岁，患病风险约增加一倍。65-74岁患病率约3%，75-84岁约17%，85岁以上可达32%。但年龄只是风险因素，并非必然发病，早期干预可延缓疾病进展。',
            '生活方式风险': '综合评估体育活动、饮食模式、认知刺激、社交互动和睡眠质量。每周150分钟中等强度运动可降低风险30%；地中海饮食富含抗氧化剂和抗炎成分；持续学习和社交活动可维持大脑可塑性；睡眠障碍与认知衰退密切相关。',
            '血管风险因素': '高血压、糖尿病、高血脂、房颤、卒中史等血管疾病会损害脑血流和微循环。高血压可导致小血管病变和脑白质损伤；糖尿病增加血管并发症和胰岛素抵抗；这些因素共同影响神经元代谢和功能，是可干预的重要风险因素。',
            '海马体萎缩': '记忆中枢海马区域的萎缩程度。海马位于大脑内侧颞叶，是记忆形成和提取的关键区域，萎缩程度与记忆功能下降呈高度相关。正常老年人每年萎缩约1-2%，病理状态下可达3-5%。',
            'p-tau217浓度': '血液中磷酸化tau蛋白217的浓度。这是近年来发现的新型血液生物标志物，具有很高的诊断准确性，能在症状出现前预测阿尔茨海默病风险，浓度>3.8 pg/mL提示风险增加。',
            'Aβ42/Aβ40比率': '脑脊液中Aβ42与Aβ40的比值。正常比值为0.2-0.4，降低(<0.2)提示淀粉样蛋白沉积增加，是早期阿尔茨海默病的重要标志，比临床症状早5-10年出现异常。',
            '脑葡萄糖代谢率': '通过PET扫描测量大脑葡萄糖摄取水平。大脑神经元活动依赖葡萄糖代谢，代谢率降低反映神经元功能减退，尤其是在顶叶和颞叶区域的代谢降低与认知障碍密切相关。',
            '白质高信号': 'MRI上显示的脑部白质病变程度，反映小血管疾病和缺血性损伤。高信号体积增加与血管性认知障碍风险相关，常见于高血压、糖尿病患者，可影响信息传递效率。',
            '脑体积减少率': '通过系列MRI扫描测量脑体积减少的年速率。正常衰老为0.5-1%/年，病理性萎缩可达2-3%/年，快速萎缩提示疾病进展较快，需要密切监测和干预。'
        };
        
        const referenceRanges = {
            '海马体萎缩': '0-30%',
            'p-tau217浓度': '<40 pg/mL',
            'Aβ42/Aβ40比率': '0.2-0.4',
            '脑葡萄糖代谢率': '>85%',
            '白质高信号': '<20%',
            '脑体积减少率': '0-25%'
        };
        
        Object.entries(results.risk_indicators).forEach(([indicator, data]) => {
            const riskClass = data.risk_level || 'medium';
            const riskText = {
                'high': '高风险',
                'medium': '中等风险',
                'low': '低风险'
            }[riskClass] || '未知';

            // 获取单位信息
            const unit = data.unit || '';

            // 获取正常范围值 - 优先使用data中的值，否则使用本地映射
            let normalRange = data.normal_range || referenceRanges[indicator] || 'N/A';

            // 获取描述 - 优先使用data中的值，否则使用本地映射
            const description = data.description || indicatorDescriptions[indicator] || '该指标反映了您的健康状况，数值越高表示风险越大';

            html += `
                <tr class="risk-${riskClass}">
                    <td><strong>${indicator}</strong></td>
                    <td>${description}</td>
                    <td>${data.value.toFixed(1)} ${unit}</td>
                    <td>${normalRange}</td>
                    <td>
                        <span class="risk-badge ${riskClass}">${riskText}</span>
                    </td>
                </tr>
            `;
        });
        
        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }
    
    // 医学建议
    if (results.medical_advice) {
        html += `
            <div class="report-section">
                <h4><i class="fas fa-user-md"></i> 医学建议</h4>
                <div class="advice-list">
        `;
        
        results.medical_advice.forEach((item, index) => {
            html += `
                <div class="advice-item">
                    <div class="advice-number">${index + 1}</div>
                    <div class="advice-content">${item}</div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    // 免责声明
    html += `
            <div class="report-section disclaimer">
                <h4><i class="fas fa-exclamation-triangle"></i> 重要声明</h4>
                <div class="disclaimer-content">
                    <p><strong>本报告为AI辅助诊断结果，仅供临床参考：</strong></p>
                    <ul>
                        <li>诊断结果不能替代执业医师的专业判断</li>
                        <li>紧急情况请立即就医，不要依赖本报告延迟治疗</li>
                        <li>所有医疗决策应在医生指导下进行</li>
                        <li>报告生成时间：${new Date().toLocaleString('zh-CN')}</li>
                        <li>系统版本：AD-CPredSys v4.0.0</li> <!-- 修改系统名称和版本 -->
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    modalBody.innerHTML = html;
    modal.classList.add('active');
    console.log("详细报告已生成并显示");
}

// 生成PDF报告
function generatePDFReportFromResults(results) {
    showToast('正在生成PDF报告...', 'info');
    
    fetch('/api/generate-pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            results: results,
            patient_info: window.currentPatientInfo || {},
            timestamp: new Date().toISOString()
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('PDF报告生成成功！', 'success');
            
            // 预览PDF
            previewPDF(data.pdf_url);
            
            // 刷新报告列表
            loadReportsList();
        } else {
            throw new Error(data.error || '生成PDF失败');
        }
    })
    .catch(error => {
        console.error('PDF生成失败:', error);
        showToast('PDF生成失败: ' + error.message, 'error');
    });
}

// 预览PDF
function previewPDF(pdfUrl) {
    const modal = document.getElementById('pdf-preview-modal');
    const iframe = document.getElementById('pdf-preview-frame');
    
    iframe.src = pdfUrl;
    modal.classList.add('active');
}

// 生成新PDF报告
function generateNewPDFReport() {
    if (window.currentResults) {
        generatePDFReportFromResults(window.currentResults);
    } else {
        showToast('请先进行诊断分析', 'warning');
        document.querySelector('[href="#diagnosis"]').click();
    }
}

// 加载报告列表
function loadReportsList() {
    const tableBody = document.getElementById('reports-table-body');
    
    fetch('/api/reports')
    .then(response => response.json())
    .then(data => {
        if (data.success && data.reports.length > 0) {
            let html = '';
            
            data.reports.forEach((report, index) => {
                const date = new Date(report.timestamp || report.modified);
                const formattedDate = date.toLocaleString('zh-CN');
                const fileSize = report.size ? (report.size / 1024 / 1024).toFixed(2) + ' MB' : '未知';
                
                html += `
                    <div class="report-item">
                        <div class="report-cell">${report.name}</div>
                        <div class="report-cell">${report.patient_id || '未知'}</div>
                        <div class="report-cell">${formattedDate}</div>
                        <div class="report-cell">${fileSize}</div>
                        <div class="report-cell">
                            <div class="report-actions">
                                <button class="btn btn-sm btn-outline" onclick="previewReport('${report.path}')">
                                    <i class="fas fa-eye"></i> 浏览
                                </button>
                                <button class="btn btn-sm btn-outline" onclick="downloadReport('${report.path}', '${report.name}')">
                                    <i class="fas fa-download"></i> 下载
                                </button>
                                <button class="btn btn-sm btn-outline" onclick="renameReport('${report.path}', '${report.name}')">
                                    <i class="fas fa-edit"></i> 重命名
                                </button>
                                <button class="btn btn-sm btn-danger" onclick="deleteReport('${report.path}', '${report.name}')">
                                    <i class="fas fa-trash-alt"></i> 删除
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            tableBody.innerHTML = html;
        } else {
            tableBody.innerHTML = `
                <div class="no-reports">
                    <i class="fas fa-file-pdf"></i>
                    <p>暂无PDF报告</p>
                    <p>请先生成报告</p>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('加载报告列表失败:', error);
        tableBody.innerHTML = `
            <div class="no-reports">
                <i class="fas fa-exclamation-triangle"></i>
                <p>加载失败</p>
                <p>${error.message}</p>
            </div>
        `;
    });
}

// 预览报告
function previewReport(path) {
    previewPDF(path);
}

// 下载报告
function downloadReport(path, filename) {
    const a = document.createElement('a');
    a.href = path;
    a.download = filename;
    a.click();
}

// 搜索报告
function searchReports() {
    const searchTerm = document.getElementById('report-search').value.toLowerCase();
    const tableBody = document.getElementById('reports-table-body');
    
    fetch('/api/reports')
    .then(response => response.json())
    .then(data => {
        if (data.success && data.reports.length > 0) {
            const filteredReports = data.reports.filter(report => 
                report.name.toLowerCase().includes(searchTerm) ||
                (report.patient_id && report.patient_id.toLowerCase().includes(searchTerm))
            );
            
            if (filteredReports.length > 0) {
                let html = '';
                filteredReports.forEach((report, index) => {
                    const date = new Date(report.timestamp || report.modified);
                    const formattedDate = date.toLocaleString('zh-CN');
                    const fileSize = report.size ? (report.size / 1024 / 1024).toFixed(2) + ' MB' : '未知';
                    
                    html += `
                        <div class="report-item">
                            <div class="report-cell">${report.name}</div>
                            <div class="report-cell">${report.patient_id || '未知'}</div>
                            <div class="report-cell">${formattedDate}</div>
                            <div class="report-cell">${fileSize}</div>
                            <div class="report-cell">
                                <div class="report-actions">
                                    <button class="btn btn-sm btn-outline" onclick="previewReport('${report.path}')">
                                        <i class="fas fa-eye"></i> 浏览
                                    </button>
                                    <button class="btn btn-sm btn-outline" onclick="downloadReport('${report.path}', '${report.name}')">
                                        <i class="fas fa-download"></i> 下载
                                    </button>
                                    <button class="btn btn-sm btn-outline" onclick="renameReport('${report.path}', '${report.name}')">
                                        <i class="fas fa-edit"></i> 重命名
                                    </button>
                                    <button class="btn btn-sm btn-danger" onclick="deleteReport('${report.path}', '${report.name}')">
                                        <i class="fas fa-trash-alt"></i> 删除
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                tableBody.innerHTML = html;
            } else {
                tableBody.innerHTML = `
                    <div class="no-reports">
                        <i class="fas fa-search"></i>
                        <p>未找到匹配的报告</p>
                        <p>请尝试其他搜索关键词</p>
                    </div>
                `;
            }
        }
    })
    .catch(error => {
        console.error('搜索报告失败:', error);
        showToast('搜索报告失败: ' + error.message, 'error');
    });
}

// 清除搜索
function clearReportSearch() {
    document.getElementById('report-search').value = '';
    loadReportsList();
}

// 删除报告
function deleteReport(path, filename) {
    if (confirm(`确定要删除报告 "${filename}" 吗？此操作无法撤销。`)) {
        fetch('/api/delete-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                report_path: path
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('报告删除成功！', 'success');
                loadReportsList();
            } else {
                throw new Error(data.error || '删除报告失败');
            }
        })
        .catch(error => {
            console.error('删除报告失败:', error);
            showToast('删除报告失败: ' + error.message, 'error');
        });
    }
}

// 重命名报告
function renameReport(path, currentName) {
    const newName = prompt('请输入新的报告名称:', currentName.replace('.pdf', ''));
    if (newName && newName.trim() !== '') {
        const newFilename = newName.trim() + '.pdf';
        
        fetch('/api/rename-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                report_path: path,
                new_name: newFilename
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('报告重命名成功！', 'success');
                loadReportsList();
            } else {
                throw new Error(data.error || '重命名报告失败');
            }
        })
        .catch(error => {
            console.error('重命名报告失败:', error);
            showToast('重命名报告失败: ' + error.message, 'error');
        });
    }
}

// 诊断类别分布图表
let diagnosisChart = null;

// 初始化诊断类别分布图表
function initDiagnosisChart(data) {
    console.log('开始初始化诊断类别分布图表...');
    
    const ctx = document.getElementById('diagnosisChart');
    if (!ctx) {
        console.error('图表容器未找到');
        return;
    }
    console.log('图表容器找到:', ctx);
    
    // 检查Chart对象是否已加载
    if (typeof Chart === 'undefined') {
        console.log('Chart.js 尚未加载，等待中...');
        // 延迟重试
        setTimeout(() => initDiagnosisChart(data), 100);
        return;
    }
    console.log('Chart.js 已加载');
    
    // 销毁现有图表
    if (diagnosisChart) {
        console.log('销毁现有图表');
        diagnosisChart.destroy();
    }
    
    // 诊断类别数据
    const labels = ['CN - 认知正常', 'EMCI - 早期轻度认知障碍', 'LMCI - 晚期轻度认知障碍', 'AD - 阿尔兹海默病'];
    const colors = [
        'rgba(16, 185, 129, 0.8)',   // CN - 绿色
        'rgba(245, 158, 11, 0.8)',   // EMCI - 黄色
        'rgba(249, 115, 22, 0.8)',   // LMCI - 橙色
        'rgba(239, 68, 68, 0.8)'     // AD - 红色
    ];
    
    // 首先尝试从服务器数据获取诊断分布
    let diagnosisCounts = {
        'CN': data.cn_count || 0,
        'EMCI': data.emci_count || 0,
        'LMCI': data.lmci_count || 0,
        'AD': data.ad_count || 0
    };
    
    console.log('服务器诊断计数:', diagnosisCounts);
    
    // 如果服务器没有提供数据，从localStorage获取患者数据
    if (diagnosisCounts.CN === 0 && diagnosisCounts.EMCI === 0 && diagnosisCounts.LMCI === 0 && diagnosisCounts.AD === 0) {
        console.log('服务器没有提供诊断数据，从localStorage获取');
        const patients = JSON.parse(localStorage.getItem('adPatients') || '[]');
        console.log('患者数据:', patients);
        console.log('患者数量:', patients.length);
        
        diagnosisCounts = {
            'CN': 0,
            'EMCI': 0,
            'LMCI': 0,
            'AD': 0
        };
        
        patients.forEach(patient => {
            if (patient.diagnosis && patient.diagnosis.label) {
                const label = patient.diagnosis.label;
                if (diagnosisCounts.hasOwnProperty(label)) {
                    diagnosisCounts[label]++;
                } else {
                    console.warn('未知的诊断标签:', label);
                }
            } else {
                console.warn('患者数据缺少诊断信息:', patient);
            }
        });
    }
    
    console.log('最终诊断计数:', diagnosisCounts);
    
    const values = [
        diagnosisCounts.CN,
        diagnosisCounts.EMCI,
        diagnosisCounts.LMCI,
        diagnosisCounts.AD
    ];
    
    console.log('图表数据:', labels, values);
    
    // 如果没有数据，使用测试数据
    if (values.every(v => v === 0)) {
        console.log('没有真实数据，使用测试数据');
        values[0] = 15; // CN
        values[1] = 8;  // EMCI
        values[2] = 5;  // LMCI
        values[3] = 3;  // AD
    }
    
    diagnosisChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: colors.map(color => color.replace('0.8', '1')),
                borderWidth: 2,
                hoverOffset: 8,
                hoverBackgroundColor: colors.map(color => color.replace('0.8', '1')),
                hoverBorderColor: '#ffffff',
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 25,
                        font: {
                            size: 14,
                            weight: '600',
                            family: 'Inter, sans-serif'
                        },
                        color: '#374151',
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#4b5563',
                    borderWidth: 1,
                    padding: 15,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        title: function(context) {
                            return context[0].label;
                        },
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                            return `数量: ${value} | 占比: ${percentage}%`;
                        },
                        afterLabel: function(context) {
                            const value = context.raw || 0;
                            let status = '';
                            if (value === 0) {
                                status = '暂无数据';
                            } else if (value < 3) {
                                status = '数据较少';
                            } else if (value < 10) {
                                status = '数据良好';
                            } else {
                                status = '数据充足';
                            }
                            return `状态: ${status}`;
                        }
                    }
                },
                title: {
                    display: true,
                    text: '诊断类别分布',
                    font: {
                        size: 18,
                        weight: '700',
                        family: 'Inter, sans-serif'
                    },
                    color: '#111827',
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            },
            cutout: '65%',
            animation: {
                animateScale: true,
                animateRotate: true,
                duration: 2000,
                easing: 'easeOutQuart'
            },
            onClick: (event, elements) => {
                if (elements.length > 0) {
                    const index = elements[0].index;
                    const label = labels[index];
                    const value = values[index];
                    const diagnosisType = label.split(' - ')[0];
                    
                    // 根据诊断类型筛选患者列表
                    document.getElementById('patient-filter').value = diagnosisType;
                    loadPatientList('', diagnosisType);
                    
                    showToast(`已筛选 ${label}: ${value} 例`, 'success');
                }
            },
            interaction: {
                mode: 'nearest',
                intersect: false
            },
            elements: {
                arc: {
                    borderWidth: 2
                }
            }
        }
    });
    
    console.log('诊断类别分布图表创建完成');
}

// 加载系统统计
function loadSystemStats() {
    fetch('/api/stats')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('total-patients').textContent = data.total_patients || '0';
            document.getElementById('total-reports').textContent = data.total_reports || '0';
            document.getElementById('analysis-count').textContent = data.analysis_count || '0';
            document.getElementById('data-size').textContent = data.data_size || '0 GB';
            
            // 初始化诊断类别分布图表
            initDiagnosisChart(data);
        }
    })
    .catch(error => {
        console.error('加载统计失败:', error);
    });
}

// 清理临时文件
function clearTempFiles() {
    const button = document.getElementById('clear-temp');
    const originalText = button.innerHTML;
    
    // 显示加载状态
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 清理中...';
    
    fetch('/api/clear-temp', {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showToast('临时文件清理完成', 'success');
            // 重新加载系统统计
            loadSystemStats();
        } else {
            throw new Error(data.error || '清理失败');
        }
    })
    .catch(error => {
        console.error('清理失败:', error);
        showToast('清理失败: ' + error.message, 'error');
    })
    .finally(() => {
        // 恢复按钮状态
        button.disabled = false;
        button.innerHTML = originalText;
    });
}

// 数据备份功能
function backupData() {
    if (confirm('确定要创建数据备份吗？这将备份所有系统数据。')) {
        const button = document.getElementById('backup-data');
        const originalText = button.innerHTML;
        
        // 显示加载状态
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 备份中...';
        showToast('正在创建数据备份...', 'info');
        
        // 获取系统统计数据
        fetch('/api/stats')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(statsData => {
            // 获取报告列表
            return fetch('/api/reports')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(reportsData => {
                return { stats: statsData, reports: reportsData };
            });
        })
        .then(data => {
            // 获取患者数据
            const patients = JSON.parse(localStorage.getItem('adPatients') || '[]');
            
            // 创建备份数据对象
            const backupData = {
                backup_info: {
                    name: 'AD-CPredSys Backup',
                    version: '4.0.0',
                    backup_date: new Date().toISOString(),
                    backup_type: 'full',
                    system_version: '4.0.0',
                    data_size: (new Blob([JSON.stringify({
                        patients: patients,
                        reports: data.reports.reports || []
                    })]).size / 1024).toFixed(2) + ' KB'
                },
                statistics: data.stats,
                patients: patients,
                reports: data.reports.reports || [],
                settings: {
                    report_settings: JSON.parse(localStorage.getItem('reportSettings') || '{}'),
                    user_preferences: JSON.parse(localStorage.getItem('userPreferences') || '{}')
                }
            };
            
            // 转换为JSON字符串
            const jsonString = JSON.stringify(backupData, null, 2);
            const blob = new Blob([jsonString], { type: 'application/json' });
            
            // 创建下载链接
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ad_cpredsys_backup_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showToast('数据备份创建成功', 'success');
        })
        .catch(error => {
            console.error('数据备份失败:', error);
            showToast('数据备份失败: ' + error.message, 'error');
        })
        .finally(() => {
            // 恢复按钮状态
            button.disabled = false;
            button.innerHTML = originalText;
        });
    }
}

// 导出数据功能
function exportData() {
    const button = document.getElementById('export-data');
    const originalText = button.innerHTML;
    
    // 显示加载状态
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 保存中...';
    showToast('正在准备导出数据...', 'info');
    
    // 获取系统统计数据
    fetch('/api/stats')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(statsData => {
        // 获取报告列表
        return fetch('/api/reports')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(reportsData => {
            return { stats: statsData, reports: reportsData };
        });
    })
    .then(data => {
        // 获取患者数据
        const patients = JSON.parse(localStorage.getItem('adPatients') || '[]');
        
        // 创建导出数据对象
        const exportData = {
            system_info: {
                name: 'AD-CPredSys',
                version: '4.0.0',
                export_date: new Date().toISOString(),
                export_by: 'System',
                export_type: 'comprehensive',
                data_size: (new Blob([JSON.stringify({
                    patients: patients,
                    reports: data.reports.reports || []
                })]).size / 1024).toFixed(2) + ' KB'
            },
            statistics: data.stats,
            patients: patients,
            reports: data.reports.reports || [],
            summary: {
                total_patients: patients.length,
                total_reports: (data.reports.reports || []).length,
                diagnosis_distribution: {
                    CN: patients.filter(p => p.diagnosis && p.diagnosis.label === 'CN').length,
                    EMCI: patients.filter(p => p.diagnosis && p.diagnosis.label === 'EMCI').length,
                    LMCI: patients.filter(p => p.diagnosis && p.diagnosis.label === 'LMCI').length,
                    AD: patients.filter(p => p.diagnosis && p.diagnosis.label === 'AD').length
                }
            }
        };
        
        // 将数据发送到服务器保存
        return fetch('/api/save-export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(exportData)
        });
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        if (result.success) {
            showToast(`数据已成功保存到项目目录: ${result.filename}`, 'success');
        } else {
            throw new Error(result.error || '保存失败');
        }
    })
    .catch(error => {
        console.error('数据导出失败:', error);
        showToast('数据导出失败: ' + error.message, 'error');
    })
    .finally(() => {
        // 恢复按钮状态
        button.disabled = false;
        button.innerHTML = originalText;
    });
}

// 导入数据功能
function importData() {
    const button = document.getElementById('import-data');
    const originalText = button.innerHTML;
    
    // 创建文件选择器
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (!file) {
            button.disabled = false;
            button.innerHTML = originalText;
            return;
        }
        
        // 显示加载状态
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 导入中...';
        showToast('正在导入数据...', 'info');
        
        const reader = new FileReader();
        reader.onload = function(event) {
            try {
                const importData = JSON.parse(event.target.result);
                
                // 验证数据格式
                if (!importData.system_info || !importData.system_info.name) {
                    throw new Error('无效的数据格式：缺少系统信息');
                }
                
                let importedCount = 0;
                
                // 处理导入的患者数据
                if (importData.patients && importData.patients.length > 0) {
                    // 合并患者数据
                    const existingPatients = JSON.parse(localStorage.getItem('adPatients') || '[]');
                    const importedPatients = importData.patients;
                    
                    // 合并数据（避免重复）
                    const mergedPatients = [...existingPatients];
                    importedPatients.forEach(patient => {
                        const existingIndex = mergedPatients.findIndex(p => p.patient_id === patient.patient_id);
                        if (existingIndex === -1) {
                            mergedPatients.push(patient);
                            importedCount++;
                        } else {
                            // 更新现有患者数据
                            mergedPatients[existingIndex] = patient;
                            importedCount++;
                        }
                    });
                    
                    localStorage.setItem('adPatients', JSON.stringify(mergedPatients));
                }
                
                // 处理导入的报告数据（如果有）
                if (importData.reports && importData.reports.length > 0) {
                    importedCount += importData.reports.length;
                }
                
                // 重新加载数据
                loadPatientList();
                loadSystemStats();
                
                showToast(`成功导入 ${importedCount} 条数据`, 'success');
                
            } catch (error) {
                console.error('数据导入失败:', error);
                showToast('数据导入失败: ' + error.message, 'error');
            } finally {
                // 恢复按钮状态
                button.disabled = false;
                button.innerHTML = originalText;
            }
        };
        
        reader.onerror = function() {
            showToast('文件读取失败', 'error');
            button.disabled = false;
            button.innerHTML = originalText;
        };
        
        reader.onabort = function() {
            showToast('文件读取被取消', 'warning');
            button.disabled = false;
            button.innerHTML = originalText;
        };
        
        reader.readAsText(file);
    };
    
    input.click();
}

// 开始新的诊断
function startNewDiagnosis() {
    const fileInput = document.getElementById('file-input');
    fileInput.value = '';
    selectedFiles = [];
    document.getElementById('file-info').style.display = 'none';
    document.getElementById('start-analysis').disabled = true;
    document.getElementById('results-container').style.display = 'none';
    document.getElementById('results-placeholder').style.display = 'flex';
    document.getElementById('analysis-progress').style.display = 'none';
    
    // 清空表单
    document.getElementById('patient-id').value = '';
    document.getElementById('patient-age').value = '';
    document.getElementById('patient-gender').value = '';
    document.getElementById('patient-education').value = '';
    document.getElementById('patient-history').value = '';
    document.getElementById('patient-family').value = '';
    document.getElementById('exercise-frequency').value = '';
    document.getElementById('sleep-duration').value = '';
    document.getElementById('diet-health').value = '';
    document.getElementById('social-activities').value = '';
    document.getElementById('smoking-status').value = '';
    document.getElementById('alcohol-consumption').value = '';
    document.getElementById('cognitive-activities').value = '';
    
    // 清除全局变量
    window.currentResults = null;
    window.currentPatientInfo = null;
}

// 显示消息提示
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = 'fas fa-info-circle';
    if (type === 'success') icon = 'fas fa-check-circle';
    if (type === 'error') icon = 'fas fa-exclamation-circle';
    if (type === 'warning') icon = 'fas fa-exclamation-triangle';

    toast.innerHTML = `
        <span class="toast-icon">
            <i class="${icon}"></i>
        </span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    container.appendChild(toast);

    // 添加脉冲动画效果
    setTimeout(() => {
        toast.style.transform = 'translateY(-3px)';
        setTimeout(() => {
            toast.style.transform = 'translateY(0)';
        }, 100);
    }, 50);

    // 自动移除
    const timeout = setTimeout(() => {
        toast.style.animation = 'slideOut 0.4s cubic-bezier(0.6, -0.05, 0.01, 0.99)';
        setTimeout(() => toast.remove(), 400);
    }, 5000);

    // 鼠标悬停时暂停自动关闭
    toast.addEventListener('mouseenter', () => {
        clearTimeout(timeout);
        toast.style.animationPlayState = 'paused';
    });

    toast.addEventListener('mouseleave', () => {
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.4s cubic-bezier(0.6, -0.05, 0.01, 0.99)';
            setTimeout(() => toast.remove(), 400);
        }, 1000);
    });
}

// 报告设置模态框功能
function openReportSettingsModal() {
    const modal = document.getElementById('report-settings-modal');
    modal.style.display = 'block';
    setTimeout(() => {
        modal.classList.add('active');
    }, 10);
    loadSavedReportSettings();
}

function closeReportSettingsModal() {
    const modal = document.getElementById('report-settings-modal');
    modal.classList.remove('active');
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

function loadSavedReportSettings() {
    const savedSettings = localStorage.getItem('reportSettings');
    if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        document.getElementById('report-template').value = settings.template || 'standard';
        document.getElementById('report-language').value = settings.language || 'zh';
        document.getElementById('report-font').value = settings.font || 'SimHei';
        document.getElementById('report-font-size').value = settings.fontSize || 12;
        document.getElementById('include-patient-info').checked = settings.includePatientInfo !== false;
        document.getElementById('include-risk-analysis').checked = settings.includeRiskAnalysis !== false;
        document.getElementById('include-recommendations').checked = settings.includeRecommendations !== false;
        document.getElementById('include-visualizations').checked = settings.includeVisualizations !== false;
        document.getElementById('hospital-name').value = settings.hospitalName || '';
        document.getElementById('department-name').value = settings.departmentName || '';
        document.getElementById('doctor-name').value = settings.doctorName || '';
    }
}

function saveReportSettings() {
    const settings = {
        template: document.getElementById('report-template').value,
        language: document.getElementById('report-language').value,
        font: document.getElementById('report-font').value,
        fontSize: parseInt(document.getElementById('report-font-size').value),
        includePatientInfo: document.getElementById('include-patient-info').checked,
        includeRiskAnalysis: document.getElementById('include-risk-analysis').checked,
        includeRecommendations: document.getElementById('include-recommendations').checked,
        includeVisualizations: document.getElementById('include-visualizations').checked,
        hospitalName: document.getElementById('hospital-name').value,
        departmentName: document.getElementById('department-name').value,
        doctorName: document.getElementById('doctor-name').value
    };
    localStorage.setItem('reportSettings', JSON.stringify(settings));
    showToast('报告设置已保存', 'success');
    closeReportSettingsModal();
}

// 初始化报告设置模态框事件
function initReportSettingsModal() {
    const modal = document.getElementById('report-settings-modal');
    const closeBtn = modal.querySelector('.modal-close');
    const saveBtn = document.getElementById('save-settings');
    const cancelBtn = document.getElementById('cancel-settings');

    closeBtn.addEventListener('click', closeReportSettingsModal);
    saveBtn.addEventListener('click', saveReportSettings);
    cancelBtn.addEventListener('click', closeReportSettingsModal);

    // 点击模态框外部关闭
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeReportSettingsModal();
        }
    });
}

// 添加CSS动画
const navigationStyle = document.createElement('style');
navigationStyle.textContent = `
    .slideOut {
        animation: slideOut 0.3s ease forwards;
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    /* 模态融合权重样式 */
    .modality-weights-section {
        margin: 2rem 0;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .weights-container {
        margin-top: 1rem;
    }
    
    .weight-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.75rem;
        padding: 0.75rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .weight-label {
        width: 100px;
        font-weight: 600;
        color: #1e293b;
    }
    
    .weight-bar-container {
        flex: 1;
        height: 20px;
        background: #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .weight-bar {
        height: 100%;
        transition: width 0.5s ease;
        position: relative;
        overflow: hidden;
    }
    
    .weight-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.3) 50%, 
            transparent 100%);
        animation: shimmer 2s infinite;
    }
    
    .weight-value {
        width: 60px;
        text-align: right;
        font-weight: 600;
        color: #1e40af;
    }
    
    /* 置信度条样式 */
    .confidence-bars {
        margin-top: 1rem;
    }
    
    .confidence-bar {
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .bar-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .label-text {
        font-weight: 500;
        color: #1e293b;
    }
    
    .label-value {
        font-weight: 600;
        color: #2563eb;
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .bar-container {
        height: 20px;
        background: #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .bar-fill {
        height: 100%;
        transition: width 0.5s ease;
        position: relative;
        overflow: hidden;
    }
    
    .bar-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.3) 50%, 
            transparent 100%);
        animation: shimmer 2s infinite;
    }
    
    /* 每月进展风险区域 */
    .monthly-risk-section {
        margin-top: 1.5rem;
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .risk-trend-container {
        display: grid;
        grid-template-rows: auto auto;
        gap: 1.5rem;
        align-items: start;
    }
    
    .risk-trend-explanation {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .brain-image-section {
        margin-top: 1.5rem;
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .brain-image-container {
        position: relative;
        margin-bottom: 1rem;
    }
    
    .brain-image {
        display: block;
        margin: 0 auto;
    }
    
    .brain-image-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0);
        border-radius: 12px;
        transition: background 0.3s ease;
    }
    
    .brain-image-container:hover .brain-image-overlay {
        background: rgba(0,0,0,0.1);
    }
    
    .brain-image-info {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .brain-image-info p {
        margin-bottom: 1rem;
        line-height: 1.6;
        color: #475569;
    }
    
    .brain-image-info ul {
        margin-bottom: 1rem;
        padding-left: 1.5rem;
    }
    
    .brain-image-info li {
        margin-bottom: 0.5rem;
        line-height: 1.6;
        color: #475569;
    }
    
    .risk-trend-explanation p {
        margin-bottom: 1rem;
        line-height: 1.6;
        color: #475569;
    }
    
    .risk-trend-explanation ul {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .risk-trend-explanation li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
        color: #475569;
    }
    
    /* 风险指标网格 */
    .risk-indicators {
        margin-top: 1.5rem;
        overflow: visible;
    }
    
    .indicators-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.25rem;
        margin-top: 1rem;
        align-items: stretch;
    }
    
    .indicator-card {
        padding: 1.25rem;
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        min-height: 180px;
        display: flex;
        flex-direction: column;
    }

    .indicator-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    .indicator-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .indicator-name {
        font-weight: 600;
        color: #1e293b;
    }

    .indicator-description {
        font-size: 0.75rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
        line-height: 1.4;
        flex-grow: 1;
    }

    .indicator-normal {
        font-size: 0.7rem;
        color: #10b981;
        background: #d1fae5;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
    }

    .indicator-progress {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* 医学建议样式 */
    .advice-item {
        display: flex;
        gap: 1rem;
        padding: 1rem;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 8px;
        margin-bottom: 0.75rem;
        border-left: 4px solid #2563eb;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .advice-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .advice-number {
        width: 30px;
        height: 30px;
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
        box-shadow: 0 2px 5px rgba(37, 99, 235, 0.3);
    }
    
    .advice-text {
        flex: 1;
        color: #1e293b;
        line-height: 1.5;
    }
    
    /* 热力图图例 */
    .heatmap-legend {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: white;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
    }
    
    .legend-color {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 4px;
    }
    
    /* 详细报告样式 */
    .detailed-report {
        padding: 1rem;
    }
    
    .report-header {
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .report-section {
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .summary-item {
        padding: 1rem;
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .risk-indicators-table {
        overflow-x: auto;
    }
    
    .risk-indicators-table table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .risk-indicators-table th {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 1rem;
        text-align: left;
    }
    
    .risk-indicators-table td {
        padding: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .risk-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .risk-badge.high {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        color: #991b1b;
        border: 1px solid #fecaca;
    }
    
    .risk-badge.medium {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 1px solid #fde68a;
    }
    
    .risk-badge.low {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #047857;
        border: 1px solid #a7f3d0;
    }
`;
document.head.appendChild(navigationStyle);
