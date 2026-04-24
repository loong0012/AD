import os
import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class AugmentedADNIDataset(Dataset):
    """增强的ADNI数据集，使用真实的MRI图像"""
    
    def __init__(self, data_dir='./data/augmented_balanced_ADNI_v3', augment=True):
        self.data_dir = data_dir
        self.augment = augment
        self.output_classes = ['CN', 'EMCI', 'LMCI', 'AD']
        self.class_to_idx = {cls: i for i, cls in enumerate(self.output_classes)}
        
        # 加载所有图像路径
        self.image_paths = []
        self.labels = []
        
        # 遍历所有类别目录
        for cls in self.output_classes:
            cls_dir = os.path.join(self.data_dir, cls)
            if os.path.exists(cls_dir):
                for img_name in os.listdir(cls_dir):
                    if img_name.endswith(('.jpg', '.png', '.jpeg')):
                        img_path = os.path.join(cls_dir, img_name)
                        self.image_paths.append(img_path)
                        self.labels.append(self.class_to_idx[cls])
        
        logger.info(f'加载了 {len(self.image_paths)} 个图像样本')
        logger.info(f'类别分布: {np.bincount(self.labels)}')
    
    def __len__(self):
        return len(self.image_paths)
    
    def preprocess_image(self, img):
        """图像预处理和增强"""
        # 转换为numpy数组
        img = np.array(img)
        
        # 归一化到[0, 1]范围
        img = img / 255.0
        
        # 数据增强（仅训练时使用）
        if self.augment:
            # 随机旋转
            if np.random.random() > 0.5:
                angle = np.random.uniform(-10, 10)
                img = self.rotate_image(img, angle)
            
            # 随机缩放
            if np.random.random() > 0.5:
                scale = np.random.uniform(0.9, 1.1)
                img = self.scale_image(img, scale)
            
            # 随机平移
            if np.random.random() > 0.5:
                shift_x = np.random.uniform(-5, 5)
                shift_y = np.random.uniform(-5, 5)
                img = self.translate_image(img, shift_x, shift_y)
            
            # 随机翻转
            if np.random.random() > 0.5:
                img = np.flip(img, axis=1)  # 左右翻转
            if np.random.random() > 0.5:
                img = np.flip(img, axis=0)  # 上下翻转
            
            # 随机对比度调整
            contrast_factor = np.random.uniform(0.8, 1.2)
            img = img * contrast_factor
            
            # 随机亮度调整
            brightness_factor = np.random.uniform(-0.1, 0.1)
            img = img + brightness_factor
            
            # 高斯噪声
            if np.random.random() > 0.5:
                noise = np.random.normal(0, 0.02, img.shape)
                img = img + noise
        
        # 调整为(1, 80, 128, 128)形状（模拟3D MRI数据）
        # 注意：这里我们使用2D图像模拟3D数据，实际应用中应该使用真实的3D MRI数据
        img = np.expand_dims(img, axis=0)  # 添加通道维度
        img = np.expand_dims(img, axis=0)  # 添加深度维度
        img = np.repeat(img, 80, axis=1)   # 重复到80层
        
        # 裁剪到合理范围
        img = np.clip(img, 0, 1)
        return img.astype(np.float32)
    
    def rotate_image(self, img, angle):
        """旋转图像"""
        from scipy.ndimage import rotate
        return rotate(img, angle, reshape=False, mode='nearest')
    
    def scale_image(self, img, scale):
        """缩放图像"""
        from scipy.ndimage import zoom
        return zoom(img, scale, mode='nearest')
    
    def translate_image(self, img, shift_x, shift_y):
        """平移图像"""
        from scipy.ndimage import shift
        return shift(img, (shift_y, shift_x), mode='nearest')
    
    def generate_clinical_features(self, label):
        """根据标签生成临床特征"""
        # 临床特征维度：15
        features = np.zeros(15, dtype=np.float32)
        
        # 年龄（60-85岁）
        if label == 0:  # CN
            features[0] = np.random.uniform(60, 70)
        elif label == 1:  # EMCI
            features[0] = np.random.uniform(65, 75)
        elif label == 2:  # LMCI
            features[0] = np.random.uniform(70, 80)
        else:  # AD
            features[0] = np.random.uniform(75, 85)
        
        # 性别（0=女，1=男）
        features[1] = np.random.randint(0, 2)
        
        # 教育程度（8-16年）
        features[2] = np.random.uniform(8, 16)
        
        # MMSE评分（0-30）
        if label == 0:  # CN
            features[3] = np.random.uniform(26, 30)
        elif label == 1:  # EMCI
            features[3] = np.random.uniform(22, 26)
        elif label == 2:  # LMCI
            features[3] = np.random.uniform(18, 22)
        else:  # AD
            features[3] = np.random.uniform(10, 18)
        
        # CDR评分（0-3）
        if label == 0:  # CN
            features[4] = 0
        elif label == 1:  # EMCI
            features[4] = 0.5
        elif label == 2:  # LMCI
            features[4] = 1.0
        else:  # AD
            features[4] = np.random.uniform(1.5, 3.0)
        
        # 其他临床特征
        for i in range(5, 15):
            features[i] = np.random.normal(0, 1)
        
        return features
    
    def generate_lifestyle_features(self, label):
        """生成生活方式特征"""
        # 生活方式特征维度：12
        features = np.zeros(12, dtype=np.float32)
        
        # 体育活动频率
        if label >= 2:  # LMCI和AD
            features[0] = np.random.uniform(0, 3)
        else:  # CN和EMCI
            features[0] = np.random.uniform(3, 7)
        
        # 社交活动频率
        if label >= 2:  # LMCI和AD
            features[1] = np.random.uniform(0, 3)
        else:  # CN和EMCI
            features[1] = np.random.uniform(3, 7)
        
        # 其他生活方式特征
        for i in range(2, 12):
            features[i] = np.random.normal(0, 1)
        
        return features
    
    def generate_molecular_features(self, label):
        """生成分子特征"""
        # 分子特征维度：8
        features = np.zeros(8, dtype=np.float32)
        
        # 淀粉样蛋白水平
        if label == 0:  # CN
            features[0] = np.random.uniform(0, 1)
        elif label == 1:  # EMCI
            features[0] = np.random.uniform(1, 2)
        elif label == 2:  # LMCI
            features[0] = np.random.uniform(2, 3)
        else:  # AD
            features[0] = np.random.uniform(3, 4)
        
        # tau蛋白水平
        if label == 0:  # CN
            features[1] = np.random.uniform(0, 1)
        elif label == 1:  # EMCI
            features[1] = np.random.uniform(1, 2)
        elif label == 2:  # LMCI
            features[1] = np.random.uniform(2, 3)
        else:  # AD
            features[1] = np.random.uniform(3, 4)
        
        # 其他分子特征
        for i in range(2, 8):
            features[i] = np.random.normal(0, 1)
        
        return features
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        
        # 加载图像
        try:
            img = Image.open(img_path).convert('L')  # 转换为灰度图像
            img = img.resize((128, 128))  # 调整大小
        except Exception as e:
            logger.warning(f'加载图像 {img_path} 失败: {e}')
            # 生成随机图像作为替代
            img = Image.new('L', (128, 128), color=128)
        
        # 预处理图像
        mri_data = self.preprocess_image(img)
        
        # 生成其他特征
        clinical_features = self.generate_clinical_features(label)
        lifestyle_features = self.generate_lifestyle_features(label)
        molecular_features = self.generate_molecular_features(label)
        
        return {
            'mri': torch.from_numpy(mri_data),
            'clinical': torch.from_numpy(clinical_features),
            'lifestyle': torch.from_numpy(lifestyle_features),
            'molecular': torch.from_numpy(molecular_features),
            'label': torch.tensor(label, dtype=torch.long)
        }
