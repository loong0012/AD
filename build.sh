#!/bin/bash
set -e

echo "=== Upgrading pip ==="
pip install --upgrade pip setuptools wheel

echo "=== Installing requirements ==="
pip install -r requirements.txt

echo "=== Installing PyTorch CPU ==="
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo "=== Verifying torch ==="
python -c "import torch; print('Torch version:', torch.__version__)"

echo "=== Creating directories ==="
mkdir -p data results reports uploaded_img temp demodata logs

echo "=== Build complete ==="