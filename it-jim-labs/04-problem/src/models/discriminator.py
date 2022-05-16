import torch
from torch import nn

import functools
import operator


class DiscMNISTModel(nn.Module):
    
    def __init__(self, input_dim, num_classes, hidden_channels, dropout_rate=0.4):
        super(DiscMNISTModel, self).__init__()
        
        in_channels = input_dim[0]
        self.num_classes = num_classes
        self.feature_extractor = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=hidden_channels, kernel_size=5, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout2d(p=dropout_rate),
            nn.Conv2d(in_channels=hidden_channels, out_channels=hidden_channels*2, kernel_size=5, stride=1, padding=0),
            nn.ReLU(),
            nn.Dropout2d(p=dropout_rate),
            nn.MaxPool2d(kernel_size=2),
        )
        
        with torch.no_grad():
            self.num_features = functools.reduce(operator.mul, list(self.feature_extractor(torch.rand(1, *input_dim)).shape))
        
        self.classifier = nn.Sequential(
            nn.Linear(in_features=self.num_features, out_features=self.num_features // 5),
            nn.ReLU(),
            nn.Dropout(p=dropout_rate),
            nn.Linear(in_features=self.num_features // 5, out_features=num_classes),
        )
        
    def forward(self, x):
        features = self.feature_extractor(x)
        features = torch.flatten(features, start_dim=1)
        prediction = self.classifier(features)
        return prediction
