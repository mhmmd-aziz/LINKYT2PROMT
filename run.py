import os
import sys
import webbrowser
import threading
import time
import subprocess

def print_banner():
    banner = """
========================================================================
   __  __  ______  __  __     ___    _____ _____ ___ _     ___    _  _____ _____ 
  |  \/  |/_  /\ \/ / / /    / _ \  |  ___|  ___|_ _| |   |_ _|  / \|_   _| ____|
  | |\/| | / /  \  / / /    / /_\ \ | |_  | |_   | || |    | |  / _ \ | | |  _|  
  | |  | |/ /__ / / / /___ / /   \ \|  _| |  _|  | || |___ | | / ___ \| | | |___ 
  |_|  |_/_____/_/ |_____//_/     \_|_|   |_|   |___|_____|___/_/   \_\_| |_____|
                                                                                 
     Google Flow Edition: YouTube Copas Link -> 10s Consistent Video Prompts
========================================================================
"""
    print(banner)

def open_browser(port):
    time.sleep(1.5)
    url = f"http://127.0.0.1:{port}"
    print(f"\n[Browser] Membuka antarmuka web imzy affilate di: {url}")
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
    print(f"[*] Menjalankan server aplikasi di http://127.0.0.1:{port} ...")

    # Launch browser in a separate thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    # Start Uvicorn server
    import uvicorn
    uvicorn.run("server.main:app", host="127.0.0.1", port=port, reload=False)

if __name__ == "__main__":
    main()

