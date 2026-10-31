import os
import sys
import webbrowser
import threading
import time
import subprocess

def print_banner():
    banner = """
========================================================================
   ___ __  __ ______   __  _____ ___   ___  _     ____    __   _______ 
  |_ _|  \/  |__  / \ / / |_   _/ _ \ / _ \| |   / ___|   \ \ / /_   _|
   | || |\/| | / / \ V /    | || | | | | | | |   \___ \    \ V /  | |  
   | || |  | |/ /_  | |     | || |_| | |_| | |___ ___) |    | |   | |  
  |___|_|  |_/____| |_|     |_| \___/ \___/|_____|____/     |_|   |_|  
                                                                        
  Google Flow Edition: Kids YouTube Remake -> 20 Consistent Scene Prompts
========================================================================
"""
    print(banner)

def open_browser(port):
    time.sleep(1.5)
    url = f"http://127.0.0.1:{port}"
    print(f"\n[Browser] Membuka antarmuka web imzy tools yt di: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass

def main():
    print_banner()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(root_dir, "dist")
    server_dir = os.path.join(root_dir, "server")

    # Add server dir to sys.path
    if server_dir not in sys.path:
        sys.path.insert(0, server_dir)

    try:
        from hardware import get_system_hardware
        hw = get_system_hardware()
        gpu = hw.get("gpu", {})
        if gpu.get("available"):
            print(f"[*] Hardware Terdeteksi: ⚡ GPU {gpu.get('device_name')} ({gpu.get('total_vram_gb')} GB VRAM - CUDA)")
        else:
            print(f"[*] Hardware Terdeteksi: ⚙️ Mode CPU ({hw.get('cpu', {}).get('cpu_count_logical')} Threads)")
    except Exception as e:
        print(f"[!] Warning hardware check: {e}")

    # Verify dist folder exists
    if not os.path.exists(dist_dir) or not os.path.exists(os.path.join(dist_dir, "index.html")):
        print("[*] Melakukan build frontend React TSX terlebih dahulu...")
        subprocess.run(["npm", "run", "build"], cwd=root_dir, shell=True)

    port = 8000
    print(f"[*] Menjalankan server imzy tools yt di http://127.0.0.1:{port} ...")

    # Launch browser in a separate thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    # Start Uvicorn server with auto-reload
    import uvicorn
    uvicorn.run("server.main:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    main()
