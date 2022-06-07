import onnx
import torch.onnx
from torchvision import models

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

batch_size = 4
dummy_input = torch.rand(batch_size, 3, 224, 224).to(device)
# Obtain your model, it can be also constructed in your script explicitly
net = models.resnet18(pretrained=True).to(device)
# Invoke export
torch.onnx.export(net, dummy_input, "resnet18.onnx", output_names=['final'])

# Load the ONNX model
model = onnx.load("resnet18.onnx")

# Check that the IR is well formed
onnx.checker.check_model(model)

# Print a human readable representation of the graph
print(onnx.helper.printable_graph(model.graph))
