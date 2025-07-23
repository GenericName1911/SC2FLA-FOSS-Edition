import subprocess, sys, os
modules = ['sc-compression==0.6.1','Pillow','numpy','affine6p','colorama','lxml','ujson']
for module in modules:
    try:
        print(f"Installing: {module}")
        result = subprocess.run([sys.executable, "-m", "pip", "install", module], capture_output=True, text=True)
        if "Requirement already satisfied" in result.stdout:
            print(f"{module} is already installed.")
        else:
            print(f"Successfully installed: {module}")
    except Exception as e:
        print(f"Error installing {module}: {e}")
input("Press Enter to exit...")