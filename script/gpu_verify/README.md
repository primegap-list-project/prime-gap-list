# GPU Verify for prime gap list

## Setup

```bash
mkdir -p build
cd build
cmake .. -Dpybind11_DIR=$(pybind11-config --cmakedir)
make
```

## Run

```bash
python verify_gpu.py
```
