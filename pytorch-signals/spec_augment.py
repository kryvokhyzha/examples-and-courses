import torch 
import numpy as np 
import random 

from sparse_image_warp import sparse_image_warp 

class TimeMask(object):
    
    def __init__(self, T = 40, num_masks = 1, replace_with_zero = False):
        
        self.T = T
        self.num_masks = num_masks
        self.replace_with_zero = replace_with_zero
        
    def __call__(self,spec):
        
        cloned = spec.clone()
        len_spectro = cloned.shape[2]
        
        for i in range(0, self.num_masks):
            t = random.randrange(0, self.T)
            t_zero = random.randrange(0, len_spectro - t)
            
            if (t_zero == t_zero + t):
                return cloned
            
            mask_end = random.randrange(t_zero, t_zero + t)
            if(self.replace_with_zero):
                cloned[0][:,t_zero:mask_end] = 0
            else:
                cloned[0][:,t_zero:mask_end] = cloned.mean()
                
        return cloned

class FreqMask(object):
    
    def __init__(self, F = 10, num_masks = 1, replace_with_zero = False):
        self.F = F
        self.num_masks = num_masks
        self.replace_with_zero = replace_with_zero
        
    def __call__(self,spec):
        cloned = spec.clone()
        num_mel_channels = cloned.shape[1]

        for i in range(0, self.num_masks):
            f = random.randrange(0,self.F)
            f_zero = random.randrange(0, num_mel_channels - f)

            if f_zero == f_zero + f:
                return cloned

            mask_end = random.randrange(f_zero, f_zero + f)
            if self.replace_with_zero:
                cloned[0][f_zero:mask_end] = 0
            else:
                cloned[0][f_zero:mask_end] = cloned.mean()

        return cloned


class TimeWarp(object):
    
    def __init__(self,W = 5):
        self.W = W
        
    def __call__(self, spec):
        num_rows = spec.shape[1]
        spec_len = spec.shape[2]
        device = spec.device
        y = num_rows//2
        horizontal_line_at_ctr = spec[0][y]
        assert len(horizontal_line_at_ctr) == spec_len

        point_to_warp = horizontal_line_at_ctr[random.randrange(self.W, spec_len - self.W)]
        assert isinstance(point_to_warp, torch.Tensor)

        dist_to_warp = random.randrange(-self.W, self.W)
        src_pts, dest_pts = (torch.tensor([[[y, point_to_warp]]], device=device), 
                             torch.tensor([[[y, point_to_warp + dist_to_warp]]], device=device))
        warped_spectro, dense_flows = sparse_image_warp(spec, src_pts, dest_pts)
        return warped_spectro.squeeze(3)
