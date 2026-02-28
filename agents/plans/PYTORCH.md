https://docs.astral.sh/uv/guides/integration/pytorch/#using-a-pytorch-index

Pytorch install documentation could add uv.

nvidia-smi

uv pip install torch --torch-backend=auto

uv pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu126

uv pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu128

uv pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu130

pip3 install torch torchvision --index-url https://download.pytorch.org/whl/rocm7.1

 export UV_TORCH_BACKEND=auto

[project]
name = "project"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [
 "torch>=2.9.1",
 "torchvision>=0.24.1",
]
[tool.uv.sources]
torch = [ { index = "pytorch-cpu" } ]
torchvision = [ { index = "pytorch-cpu" } ]
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = [
 { index = "pytorch-cpu", marker = "sys_platform != 'linux'" },
 { index = "pytorch-cu128", marker = "sys_platform == 'linux'" }
]