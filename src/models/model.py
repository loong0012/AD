import torch
import torch.nn as nn
import torch.nn.functional as F


class MultiModalADModel(nn.Module):

    def __init__(self, dropout=0.3):
        super(MultiModalADModel, self).__init__()

        self.mri_encoder = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)),
        )

        self.clinical_encoder = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 32),
            nn.ReLU(),
        )

        self.lifestyle_encoder = nn.Sequential(
            nn.Linear(6, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 16),
            nn.ReLU(),
        )

        self.molecular_encoder = nn.Sequential(
            nn.Linear(5, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 16),
            nn.ReLU(),
        )

        mri_feature_dim = 128 * 4 * 4
        fused_dim = mri_feature_dim + 32 + 16 + 16

        self.fusion = nn.Sequential(
            nn.Linear(fused_dim, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
        )

        self.classifier = nn.Linear(128, 4)
        self.risk_head = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, mri_data, clinical_features, lifestyle_features, molecular_features):
        mri_features = self.mri_encoder(mri_data)
        mri_features = mri_features.view(mri_features.size(0), -1)

        clinical_features = self.clinical_encoder(clinical_features)
        lifestyle_features = self.lifestyle_encoder(lifestyle_features)
        molecular_features = self.molecular_encoder(molecular_features)

        fused = torch.cat([mri_features, clinical_features, lifestyle_features, molecular_features], dim=1)
        fused = self.fusion(fused)

        class_logits = self.classifier(fused)
        risk_score = self.risk_head(fused)

        return class_logits, risk_score, fused