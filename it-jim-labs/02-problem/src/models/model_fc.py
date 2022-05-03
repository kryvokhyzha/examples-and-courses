from torch import nn


class FlowersFcModel(nn.Module):
    def __init__(
        self, in_features, hidden_dim, num_classes, dropout_rate=0.3
    ):
        super(FlowersFcModel, self).__init__()
        self.encoder = nn.Sequential(
            self._make_disc_block(in_features, hidden_dim),
            nn.Dropout(p=dropout_rate, inplace=True),
            self._make_disc_block(hidden_dim, hidden_dim // 8),
            nn.Dropout(p=dropout_rate, inplace=True),
            self._make_disc_block(hidden_dim // 8, hidden_dim // 16),
            nn.Dropout(p=dropout_rate, inplace=True),
            self._make_disc_block(hidden_dim // 16, hidden_dim // 32),
            self._make_disc_block(hidden_dim // 32, num_classes, final_layer=True),
        )
        
    def forward(self, x):
        return self.encoder(x)
    
    def freeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = False

    def unfreeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = True
            
    def _make_disc_block(self, in_features, output_features, final_layer=False):
        if not final_layer:
            return nn.Sequential(
                nn.Linear(in_features, output_features),
                nn.LeakyReLU(negative_slope=0.2, inplace=True),
                nn.BatchNorm1d(output_features),
            )
        else:
            return nn.Sequential(
                nn.Linear(in_features, output_features),
            )
