# Cartesia MLX

This package contains implementations for fast on-device SSM inference on Apple silicon. 

## Installation
This package requires the `cartesia-metal` package.
To install this package, first install Xcode which can be downloaded from https://developer.apple.com/xcode/.
Accept the license agreement with:

```shell 
sudo xcodebuild -license
```

Install metal extension:
```shell 
pip install cartesia-metal
```

Install the package:
```shell 
pip install cartesia-mlx
```

## Models

### Language Models
- `cartesia-ai/Rene-v0.1-1.3b-4bit-mlx` 
- `cartesia-ai/mamba2-130m-8bit-mlx` 
- `cartesia-ai/mamba2-130m-mlx` 
- `cartesia-ai/mamba2-370m-8bit-mlx` 
- `cartesia-ai/mamba2-780m-8bit-mlx` 
- `cartesia-ai/mamba2-1.3b-4bit-mlx` 
- `cartesia-ai/mamba2-2.7b-4bit-mlx` 


## Usage:
```python 
import mlx.core as mx
import cartesia_mlx as cmx

model = cmx.from_pretrained('cartesia-ai/mamba2-130m-8bit-mlx')
model.set_dtype(mx.float32)   

prompt = "Rene Descartes was"

print(prompt, end="", flush=True)
for text in model.generate(
    prompt,
    max_tokens=500,
    eval_every_n=5,
    verbose=True,
    top_p=0.99,
    temperature=0.85,
):
    print(text, end="", flush=True)
```
