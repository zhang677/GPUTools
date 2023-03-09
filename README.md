# GPUTools
Useful scripts to monitor NVIDIA GPU

## GPUMemoryRecorder
Modify this [repo](https://github.com/ppalasek/gpu_memory_recorder). 
```bash
cd gpu_memory_recorder
python measure.py
```

## TorchTensorRecorder
Modify this [repo](https://github.com/Oldpan/Pytorch-Memory-Utils).
 ```python
 from GPUTools.torch_tensor_recorder.gpu_mem_track import MemTracker
 gpu_tracker = MemTracker()
 gpu_tracker.track() 
 ```