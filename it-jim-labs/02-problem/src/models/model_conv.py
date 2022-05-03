import torch
import torchvision.models as models


class FlowersConvModel(torch.nn.Module):
    def __init__(
        self, encoder_name='resnet18', pretrained=True, num_classes=1
    ):
        super(FlowersConvModel, self).__init__()
        self.encoder = getattr(models, encoder_name)(pretrained=pretrained)
        self.encoder.fc = torch.nn.Linear(in_features=512, out_features=num_classes)
        
    def forward(self, x):
        return self.encoder(x)
    
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
