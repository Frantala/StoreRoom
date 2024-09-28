import torch
import numpy as np


array = np.array([[1,2,3,4,5], [6,7,8,9,10]])

tensor = torch.tensor((array))

print(tensor.ndim)