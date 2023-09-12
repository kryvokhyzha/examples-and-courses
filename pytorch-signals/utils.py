import torch 
import numpy as np 
import matplotlib.pyplot as plt 


def multiclass_accuracy(y_pred,y_true):
    top_p,top_class = y_pred.topk(1,dim = 1)
    equals = top_class == y_true.view(*top_class.shape)
    return torch.mean(equals.type(torch.FloatTensor))
    
    
def view_classify(img, ps, true_label = None):
    classes = ["squiggle", "narrowband",  "narrowbanddrd", "noise"]

    ps = ps.data.cpu().numpy().squeeze()
    img = img.numpy()
   
    fig, (ax1, ax2) = plt.subplots(figsize=(12,8), ncols=2)
    ax1.imshow(img)
    ax1.axis('off')
    if true_label != None:
        ax1.set_title(f'Ground-Truth : {true_label}')
    ax2.barh(classes, ps)
    ax2.set_aspect(0.1)
    ax2.set_yticks(classes)
    ax2.set_yticklabels(classes)
    ax2.set_title('Class Probability')
    ax2.set_xlim(0, 1.1)

    plt.tight_layout()

    return None
