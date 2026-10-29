import platform
import psutil
import torch

def get_system_hardware():
    """
    Detects GPU (CUDA) and CPU hardware specifications in real-time.
    """
    has_cuda = torch.cuda.is_available()
    gpu_info = None
    
    if has_cuda:
        try:
            device_count = torch.cuda.device_count()
            current_device = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(current_device)
            total_vram = torch.cuda.get_device_properties(current_device).total_memory
            total_vram_mb = round(total_vram / (1024 * 1024), 2)
            total_vram_gb = round(total_vram / (1024 * 1024 * 1024), 2)
            
            allocated_vram = round(torch.cuda.memory_allocated(current_device) / (1024 * 1024), 2)
            reserved_vram = round(torch.cuda.memory_reserved(current_device) / (1024 * 1024), 2)
            
            gpu_info = {
                "available": True,
                "device_name": gpu_name,
                "device_count": device_count,
                "total_vram_mb": total_vram_mb,
                "total_vram_gb": total_vram_gb,
                "allocated_vram_mb": allocated_vram,
                "reserved_vram_mb": reserved_vram,
                "cuda_version": torch.version.cuda,
                "compute_capability": torch.cuda.get_device_capability(current_device) if hasattr(torch.cuda, "get_device_capability") else None,
                "status": "Active (CUDA High Performance)"
            }
        except Exception as e:
            gpu_info = {
                "available": False,
                "error": str(e),
                "status": "Detection Warning"
            }
    else:
        gpu_info = {
            "available": False,
            "status": "No CUDA GPU Detected (Using CPU Mode)"
        }
        
    cpu_info = {
        "processor": platform.processor() or platform.machine(),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "ram_percent": psutil.virtual_memory().percent
    }
    
    return {
        "gpu": gpu_info,
        "cpu": cpu_info,
        "recommended_device": "cuda" if has_cuda else "cpu",
        "system": platform.system(),
        "platform": platform.platform()
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_system_hardware(), indent=2))

