// API接口文件
const API_BASE_URL = window.location.origin + '/api';

// API接口函数
const api = {
    // 分析上传的文件
    async analyzeFile(files, patientInfo) {
        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });
        if (patientInfo) {
            formData.append('patient_info', JSON.stringify(patientInfo));
        }

        try {
            const response = await fetch(`${API_BASE_URL}/analyze`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            return {
                success: false,
                error: '网络请求失败，请检查服务器连接'
            };
        }
    },

    // 使用示例数据
    async useDemo() {
        try {
            const response = await fetch(`${API_BASE_URL}/demo`);

            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            return {
                success: false,
                error: '网络请求失败，请检查服务器连接'
            };
        }
    },

    // 生成PDF报告
    async generatePDF(results, patientInfo) {
        try {
            const response = await fetch(`${API_BASE_URL}/generate-pdf`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    results: results,
                    patient_info: patientInfo
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            return {
                success: false,
                error: '网络请求失败，请检查服务器连接'
            };
        }
    },

    // 获取报告列表
    async getReports() {
        try {
            const response = await fetch(`${API_BASE_URL}/reports`);

            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            return {
                success: false,
                error: '网络请求失败，请检查服务器连接'
            };
        }
    },

    // 获取系统统计
    async getStats() {
        try {
            const response = await fetch(`${API_BASE_URL}/stats`);

            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            return {
                success: false,
                error: '网络请求失败，请检查服务器连接'
            };
        }
    },

    // 清理临时文件
    async clearTemp() {
        try {
            const response = await fetch(`${API_BASE_URL}/clear-temp`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            return {
                success: false,
                error: '网络请求失败，请检查服务器连接'
            };
        }
    }
};

// 全局导出
window.API = api;

// 模拟数据生成（备用）
function generateMockResults() {
    const labels = ['CN', 'EMCI', 'LMCI', 'MCI', 'AD'];
    const pred_label = labels[Math.floor(Math.random() * labels.length)];

    const labelChinese = {
        'CN': '认知正常',
        'EMCI': '早期轻度认知障碍',
        'LMCI': '晚期轻度认知障碍',
        'MCI': '轻度认知障碍',
        'AD': '阿尔兹海默病'
    };

    const medicalAdvice = {
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
        'MCI': [
            "轻度认知障碍，需要定期随访",
            "每3-6个月评估一次认知状态",
            "加强认知康复训练",
            "控制阿尔兹海默病风险因素",
            "建立健康档案，记录认知变化"
        ],
        'AD': [
            "高度怀疑阿尔兹海默病，立即就医",
            "尽快进行PET-CT或脑脊液检查确诊",
            "开始药物治疗（胆碱酯酶抑制剂等）",
            "制定全面的护理和支持计划",
            "参与临床试验和新治疗方案"
        ]
    };

    // 生成置信度分布
    const probabilities = {};
    let baseConfidence = 0.85 + Math.random() * 0.14;
    probabilities[pred_label] = baseConfidence;

    // 其他类别的置信度
    const otherLabels = labels.filter(l => l !== pred_label);
    let remaining = 1 - baseConfidence;

    otherLabels.forEach((label, index) => {
        if (index === otherLabels.length - 1) {
            probabilities[label] = remaining;
        } else {
            const prob = remaining * 0.3 * Math.random();
            probabilities[label] = prob;
            remaining -= prob;
        }
    });

    // 确保总和为1
    const sum = Object.values(probabilities).reduce((a, b) => a + b, 0);
    Object.keys(probabilities).forEach(key => {
        probabilities[key] = probabilities[key] / sum;
    });

    // 风险指标详情配置
    const indicatorDetails = {
        '海马体萎缩': {
            description: '海马体是记忆形成的关键脑区，其萎缩程度是阿尔兹海默症早期诊断的重要标志物',
            normal_range: '正常: <30%',
            unit: '%'
        },
        'p-tau217浓度': {
            description: '磷酸化tau蛋白217位点，是阿尔兹海默症病理过程的核心生物标志物',
            normal_range: '正常: <60 pg/mL',
            unit: 'pg/mL'
        },
        'Aβ42/Aβ40比率': {
            description: 'β淀粉样蛋白42与40的比率，降低表明大脑中存在淀粉样斑块沉积',
            normal_range: '正常: >0.8',
            unit: ''
        },
        '脑葡萄糖代谢率': {
            description: '大脑利用葡萄糖的效率，后部脑区代谢降低是阿尔兹海默症的典型特征',
            normal_range: '正常: >95%',
            unit: '%'
        },
        '白质高信号': {
            description: 'MRI影像中显示的白质病变程度，与认知功能下降和血管性认知障碍相关',
            normal_range: '正常: <20%',
            unit: '%'
        },
        '脑体积减少率': {
            description: '全脑或特定区域体积随时间减少的速度，阿尔兹海默症患者脑萎缩加速',
            normal_range: '正常: <0.5%/年',
            unit: '%/年'
        }
    };

    // 生成风险指标
    const riskIndicators = {
        '海马体萎缩': { 
            value: pred_label === 'AD' ? 85 + Math.random() * 15 : 
                   pred_label === 'LMCI' ? 60 + Math.random() * 25 :
                   pred_label === 'EMCI' ? 40 + Math.random() * 20 : 
                   20 + Math.random() * 20,
            risk_level: pred_label === 'AD' ? 'high' : 
                       pred_label === 'LMCI' ? 'high' :
                       pred_label === 'EMCI' ? 'medium' : 'low',
            ...indicatorDetails['海马体萎缩']
        },
        'p-tau217浓度': { 
            value: pred_label === 'AD' ? 140 + Math.random() * 20 :
                   pred_label === 'LMCI' ? 100 + Math.random() * 40 :
                   pred_label === 'EMCI' ? 60 + Math.random() * 40 :
                   40 + Math.random() * 20,
            risk_level: pred_label === 'AD' ? 'high' : 
                       pred_label === 'LMCI' ? 'high' :
                       pred_label === 'EMCI' ? 'medium' : 'low',
            ...indicatorDetails['p-tau217浓度']
        },
        'Aβ42/Aβ40比率': { 
            value: pred_label === 'AD' ? 0.7 + Math.random() * 0.2 :
                   pred_label === 'LMCI' ? 0.5 + Math.random() * 0.2 :
                   pred_label === 'EMCI' ? 0.3 + Math.random() * 0.2 :
                   0.1 + Math.random() * 0.2,
            risk_level: pred_label === 'AD' ? 'high' : 
                       pred_label === 'LMCI' ? 'high' :
                       pred_label === 'EMCI' ? 'medium' : 'low',
            ...indicatorDetails['Aβ42/Aβ40比率']
        },
        '脑葡萄糖代谢率': { 
            value: pred_label === 'AD' ? 70 + Math.random() * 15 :
                   pred_label === 'LMCI' ? 80 + Math.random() * 15 :
                   pred_label === 'EMCI' ? 90 + Math.random() * 15 :
                   95 + Math.random() * 5,
            risk_level: pred_label === 'AD' ? 'high' : 
                       pred_label === 'LMCI' ? 'medium' :
                       pred_label === 'EMCI' ? 'low' : 'low',
            ...indicatorDetails['脑葡萄糖代谢率']
        },
        '白质高信号': { 
            value: pred_label === 'AD' ? 80 + Math.random() * 20 :
                   pred_label === 'LMCI' ? 60 + Math.random() * 20 :
                   pred_label === 'EMCI' ? 40 + Math.random() * 20 :
                   20 + Math.random() * 20,
            risk_level: pred_label === 'AD' ? 'high' : 
                       pred_label === 'LMCI' ? 'medium' :
                       pred_label === 'EMCI' ? 'low' : 'low',
            ...indicatorDetails['白质高信号']
        },
        '脑体积减少率': { 
            value: pred_label === 'AD' ? 75 + Math.random() * 25 :
                   pred_label === 'LMCI' ? 55 + Math.random() * 20 :
                   pred_label === 'EMCI' ? 35 + Math.random() * 20 :
                   15 + Math.random() * 15,
            risk_level: pred_label === 'AD' ? 'high' : 
                       pred_label === 'LMCI' ? 'medium' :
                       pred_label === 'EMCI' ? 'low' : 'low',
            ...indicatorDetails['脑体积减少率']
        }
    };

    // 风险评分
    const riskScoreMap = {
        'CN': 0.05 + Math.random() * 0.1,
        'EMCI': 0.2 + Math.random() * 0.2,
        'LMCI': 0.4 + Math.random() * 0.3,
        'MCI': 0.4 + Math.random() * 0.3,
        'AD': 0.7 + Math.random() * 0.25
    };

    return {
        success: true,
        results: {
            pred_label: pred_label,
            chinese_label: labelChinese[pred_label],
            confidence: probabilities[pred_label],
            probabilities: probabilities,
            risk_score: riskScoreMap[pred_label],
            risk_indicators: riskIndicators,
            medical_advice: medicalAdvice[pred_label],
            heatmap_image: null,
            analysis_time: new Date().toLocaleString('zh-CN')
        },
        modalities_used: ['MRI', '临床数据', '分子数据', '生活方式数据'],
        modality_weights: {
            'MRI': 0.4,
            '临床数据': 0.25,
            '分子数据': 0.2,
            '生活方式数据': 0.15
        }
    };
}

// 备用函数：当API不可用时使用模拟数据
function getFallbackResults() {
    return generateMockResults();
}
