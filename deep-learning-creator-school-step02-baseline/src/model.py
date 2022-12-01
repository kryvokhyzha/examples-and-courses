import torch
from torch import nn


class DeepfakeClassifierR3D18(nn.Module):
    def __init__(self, encoder, linear_size=512, num_classes=1):
        super(DeepfakeClassifierR3D18, self).__init__()
        self.encoder = encoder
        
        # Modify output layer.
        num_features = self.encoder.fc.in_features
        self.encoder.fc = nn.Linear(num_features, num_classes)

    def forward(self, x):
        return torch.sigmoid(self.encoder(x))
    
    def freeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = False

    def freeze_middle_layers(self):
        self.freeze_all_layers()
            
        for param in self.encoder.fc.parameters():
            param.requires_grad = True

    def unfreeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = True