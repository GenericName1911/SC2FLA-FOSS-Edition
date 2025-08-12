import subprocess
import sys
import requests

modules = ['requests', 'sc-compression==0.6.1', 'Pillow', 'numpy', 'affine6p', 'colorama', 'lxml', 'ujson']

for module in modules:
    try:
        print(f"Installing: {module}")
        result = subprocess.run([sys.executable, "-m", "pip", "install", module], capture_output=True, text=True)
        
        if "Requirement already satisfied" in result.stdout:
            print(f"{module} is already installed.")
            
        elif result.returncode == 0:
            print(f"Successfully installed: {module}")
            
        else:
            print(f"Failed to install {module}:\n{result.stderr}")
            
    except Exception as e:
        print(f"Error installing {module}: {e}")

urls = [
    "https://api.github.com/repos/Daniil-SV/ScDowngrade/releases/latest",
    "https://api.github.com/repos/Daniil-SV/SCTX-Converter/releases/latest"
]

for api_url in urls:
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        release_data = response.json()
        assets = release_data.get("assets", [])
        
        if not assets:
            print(f"No assets found in release: {api_url}")
            continue
            
        for asset in assets:
            url = asset["browser_download_url"]
            filename = asset["name"]
            
            try:
                with requests.get(url, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open(filename, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Downloaded {filename}")
                
            except Exception as e:
                print(f"Failed to download {filename}:{e}")
                
    except Exception as e:
        print(f"Failed to fetch release data from {api_url}:\n{e}")

input("Press Enter to exit...")
