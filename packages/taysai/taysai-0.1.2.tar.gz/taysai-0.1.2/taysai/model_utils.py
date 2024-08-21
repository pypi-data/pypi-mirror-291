# taysai/model_utils.py
import torch
import dill
import inspect
import torch.nn.functional as F

# List of allowed imports
allowed_imports = [
    "import torch",
    "import torch.nn as nn",
    "import torch.optim as optim",
    "import torch.nn.functional as F",
    "import torch.utils.data as data",
    "import numpy as np",
    "import os",
    "import time",
    "import random",
    "import torchvision.transforms as transforms",
]

# Function to extract and filter imports used in a module or class
def extract_imports(module, allowed_imports=allowed_imports):
    source = inspect.getsource(module)
    lines = source.splitlines()
    imports = []
    for line in lines:
        if any(allowed_imp in line for allowed_imp in allowed_imports):
            imports.append(line.strip())
    return imports

# Function to save the entire model instance along with detected imports
def save_model_instance(model, save_path="model_instance.pkl"):
    # Detect imports used in the module where the model class is defined
    module = inspect.getmodule(model.__class__)
    imports = extract_imports(module)

    # Store imports and model
    save_data = {
        'imports': imports,
        'model': model
    }
    with open(save_path, 'wb') as f:
        dill.dump(save_data, f)
