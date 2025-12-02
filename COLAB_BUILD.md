# Building Block Sparse Attention for Google Colab A100

This guide explains how to build the `block_sparse_attn` wheel on Google Colab A100 and save it to Google Drive for reuse.

## Quick Start

1. **Open the Colab notebook**: `colab_build.ipynb`
2. **Run all cells** - The notebook will:
   - Mount Google Drive
   - Clone the repository
   - Build the wheel
   - Save it to your specified Google Drive location

## Manual Build Script

Alternatively, you can use the build script directly:

### Step 1: Mount Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/cliffpyles/Block-Sparse-Attention.git /content/Block-Sparse-Attention
cd /content/Block-Sparse-Attention
```

### Step 3: Run the Build Script

```bash
python build_colab.py /content/drive/MyDrive/path/to/wheels
```

Replace `/content/drive/MyDrive/path/to/wheels` with your desired Google Drive path.

### Step 4: Install the Built Wheel

```bash
pip install /content/drive/MyDrive/path/to/wheels/block_sparse_attn-*.whl
```

## What the Build Script Does

1. **Environment Check**: Verifies Python version, PyTorch, and CUDA availability
2. **Dependency Installation**: Installs required build tools (setuptools, wheel, ninja, packaging)
3. **Clean Build**: Removes previous build artifacts
4. **Wheel Building**: Compiles the CUDA extensions and creates a wheel file
5. **Save to Drive**: Copies the wheel to your specified Google Drive location

## Environment Requirements

- **Python**: 3.12 (Colab default)
- **PyTorch**: 2.9.0+cu126 (Colab A100 default)
- **CUDA**: 12.6 (Colab A100 default)
- **GPU**: A100 (required for CUDA compilation)

## Troubleshooting

### Build Fails with CUDA Errors

- Ensure you're using an A100 runtime: Runtime → Change runtime type → Hardware accelerator: GPU → GPU type: A100
- Check CUDA availability: `torch.cuda.is_available()` should return `True`

### Out of Memory

- The build process requires significant memory. If you encounter OOM errors:
  - Restart the runtime
  - Ensure no other memory-intensive processes are running
  - Try building in a fresh Colab session

### Import Errors After Installation

- Make sure you're installing the correct wheel for your Python version
- Verify the wheel was built for the correct CUDA version (12.6)
- Try reinstalling: `pip install --force-reinstall /path/to/wheel.whl`

## Reusing Built Wheels

Once you've built a wheel and saved it to Google Drive, you can reuse it in future Colab sessions:

```python
from google.colab import drive
drive.mount('/content/drive')

# Install from your saved wheel
!pip install /content/drive/MyDrive/path/to/wheels/block_sparse_attn-*.whl
```

This saves time since you don't need to rebuild every time!

## Notes

- **Build Time**: The build process typically takes **45-60 minutes** on Colab A100, depending on server load.
- Built wheels are specific to the Python version and CUDA version used during build
- Wheels built on Colab A100 should work on other A100 environments with matching Python/CUDA versions
