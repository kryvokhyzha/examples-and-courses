import torch
from torch import nn


class Encoder(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(Encoder, self).__init__()
        
        self.encoder = nn.Sequential(
            self.make_encoder_block(in_channels, hidden_channels),
            self.make_encoder_block(hidden_channels, hidden_channels * 2),
            self.make_encoder_block(hidden_channels * 2, hidden_channels * 4),
            self.make_encoder_block(hidden_channels * 4, out_channels, final_layer=True),
        )
        
    def forward(self, x):
        return self.encoder(x)
    
    def make_encoder_block(self, input_channels, output_channels, kernel_size=4, stride=2, padding=1, final_layer=False):
        if not final_layer:
            return nn.Sequential(
                nn.Conv2d(
                    in_channels=input_channels, out_channels=output_channels,
                    kernel_size=kernel_size, stride=stride, padding=padding,
                ),
                nn.BatchNorm2d(output_channels),
                nn.LeakyReLU(negative_slope=0.2),
            )
        else:
            return nn.Sequential(
                nn.Conv2d(
                    in_channels=input_channels, out_channels=output_channels,
                    kernel_size=kernel_size, stride=stride, padding=padding,
                ),
            )
        
        
class Decoder(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(Decoder, self).__init__()
        
        self.decoder = nn.Sequential(
            self.make_decoder_block(in_channels, hidden_channels * 4, output_padding=1),
            self.make_decoder_block(hidden_channels * 4, hidden_channels * 2, output_padding=1),
            self.make_decoder_block(hidden_channels * 2, hidden_channels, output_padding=0),
            self.make_decoder_block(hidden_channels, out_channels, output_padding=0, final_layer=True),
        )
        
    def forward(self, x):
        return self.decoder(x)
    
    def make_decoder_block(self, input_channels, output_channels, kernel_size=4, stride=2, padding=1, output_padding=1, final_layer=False):
        if not final_layer:
            return nn.Sequential(
                nn.ConvTranspose2d(
                    in_channels=input_channels, out_channels=output_channels,
                    kernel_size=kernel_size, stride=stride, padding=padding,
                    output_padding=output_padding,
                ),
                nn.BatchNorm2d(output_channels),
                nn.LeakyReLU(negative_slope=0.2),
            )
        else:
            return nn.Sequential(
                nn.ConvTranspose2d(
                    in_channels=input_channels, out_channels=output_channels,
                    kernel_size=kernel_size, stride=stride, padding=padding,
                    output_padding=output_padding,
                ),
                nn.Sigmoid(),
            )


class DenoiserMNISTModel(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(DenoiserMNISTModel, self).__init__()
        self.encodee = Encoder(in_channels=in_channels, hidden_channels=hidden_channels, out_channels=out_channels)
        self.decoder = Decoder(in_channels=out_channels, hidden_channels=hidden_channels, out_channels=in_channels)
        
    def forward(self, x):
        latent_representation = self.encodee(x)
        return self.decoder(latent_representation)
