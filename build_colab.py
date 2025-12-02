#!/usr/bin/env python3
"""
Build script for Google Colab A100 environment.
Builds the block_sparse_attn wheel and saves it to Google Drive.

Usage in Colab:
    # Mount Google Drive
    from google.colab import drive
    drive.mount('/content/drive')
    
    # Run the build script
    !python build_colab.py /content/drive/MyDrive/path/to/wheels
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_colab_environment():
    """Check if we're in a Colab environment and verify dependencies."""
    print("=" * 60)
    print("Checking Colab Environment")
    print("=" * 60)
    
    # Check if in Colab
    try:
        import google.colab
        print("✓ Running in Google Colab")
    except ImportError:
        print("⚠ Warning: Not running in Google Colab")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check PyTorch
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"✓ CUDA available: {torch.version.cuda}")
            print(f"✓ CUDA device: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠ CUDA not available")
    except ImportError:
        print("✗ PyTorch not installed")
        sys.exit(1)
    
    # Check CUDA_HOME
    cuda_home = os.environ.get('CUDA_HOME')
    if cuda_home:
        print(f"✓ CUDA_HOME: {cuda_home}")
    else:
        print("⚠ CUDA_HOME not set")
    
    print()


def install_build_dependencies():
    """Install required build dependencies."""
    print("=" * 60)
    print("Installing Build Dependencies")
    print("=" * 60)
    
    dependencies = [
        "setuptools>=68.0.0",
        "wheel",
        "ninja",
        "packaging",
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", dep])
    
    print("✓ Build dependencies installed\n")


def build_wheel(output_dir):
    """Build the wheel and save it to the output directory."""
    print("=" * 60)
    print("Building Wheel")
    print("=" * 60)
    
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_path.absolute()}")
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for dir_name in ['build', 'dist', '*.egg-info']:
        for path in Path('.').glob(dir_name):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed {path}")
            elif path.is_file():
                path.unlink()
                print(f"  Removed {path}")
    
    # Build the wheel
    print("\nBuilding wheel...")
    try:
        # Set environment variable to force build
        env = os.environ.copy()
        env['FLASH_ATTENTION_FORCE_BUILD'] = 'TRUE'
        
        subprocess.check_call(
            [sys.executable, "setup.py", "bdist_wheel"],
            env=env
        )
        
        # Find the built wheel
        dist_dir = Path('dist')
        wheels = list(dist_dir.glob('*.whl'))
        
        if not wheels:
            print("✗ No wheel file found in dist/")
            sys.exit(1)
        
        # Copy wheel to output directory
        for wheel in wheels:
            dest = output_path / wheel.name
            shutil.copy2(wheel, dest)
            print(f"✓ Built and saved: {dest}")
            print(f"  Size: {dest.stat().st_size / (1024*1024):.2f} MB")
        
        return wheels[0].name
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed with exit code {e.returncode}")
        sys.exit(1)


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: Output directory not specified")
        print("Usage: python build_colab.py <output_directory>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    
    print("\n" + "=" * 60)
    print("Block Sparse Attention - Colab Build Script")
    print("=" * 60 + "\n")
    
    # Check environment
    check_colab_environment()
    
    # Install dependencies
    install_build_dependencies()
    
    # Build wheel
    wheel_name = build_wheel(output_dir)
    
    print("\n" + "=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print(f"\nWheel saved to: {Path(output_dir).absolute()}/{wheel_name}")
    print("\nTo install the wheel:")
    print(f"  !pip install {Path(output_dir).absolute()}/{wheel_name}")
    print()


if __name__ == "__main__":
    main()

