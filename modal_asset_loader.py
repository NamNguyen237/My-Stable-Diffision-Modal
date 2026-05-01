import modal
import requests
import io
import zipfile
import hashlib
import os

# Create an App for the downloader
app = modal.App("comfyui-downloader")

# Define Image for the downloader (needs requests)
downloader_image = modal.Image.debian_slim(python_version="3.11").pip_install("requests")

# Volume bindings (must be consistent with comfyapp.py)
vol_checkpoints = modal.Volume.from_name("comfy_checkpoints", create_if_missing=True)
vol_loras = modal.Volume.from_name("comfy_loras", create_if_missing=True)
vol_controlnet = modal.Volume.from_name("comfy_controlnet", create_if_missing=True)
vol_custom_nodes = modal.Volume.from_name("comfy_custom_nodes", create_if_missing=True)

# Path constants used inside the Modal Function
MOUNT_PATH = "/root/vol_models"

def get_remote_file_size(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return int(response.headers.get('content-length', 0))
    except:
        return 0

def download_file_to_path(url, filepath):
    # This runs inside the Modal container
    try:
        remote_size = get_remote_file_size(url)
        
        if os.path.exists(filepath):
            local_size = os.path.getsize(filepath)
            if remote_size > 0 and local_size == remote_size:
                print(f"⏩ '{os.path.basename(filepath)}' đã tồn tại và khớp kích thước ({local_size/(1024*1024):.2f} MB). Bỏ qua.")
                return
            else:
                 print(f"⚠️ '{os.path.basename(filepath)}' sai kích thước (Local: {local_size}, Remote: {remote_size}). Tải lại...")
        
        print(f"⬇️ Đang tải '{os.path.basename(filepath)}'...")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            # Write to a temp file first to avoid corruption
            temp_filepath = filepath + ".tmp"
            with open(temp_filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0 and downloaded % (100 * 1024 * 1024) == 0:
                             print(f"   ...đã tải {downloaded / (1024*1024):.1f} MB")
            
            # Rename temp file to actual file
            os.rename(temp_filepath, filepath)
            print(f"✅ Đã tải xong '{os.path.basename(filepath)}'")
            
    except Exception as e:
        print(f"❌ Lỗi tải '{os.path.basename(filepath)}': {e}")
        if os.path.exists(filepath + ".tmp"):
             os.remove(filepath + ".tmp")

def extract_zip_to_path(url, extract_to_path, folder_name):
    # Runs inside Modal container
    try:
        print(f"⬇️ Tải và giải nén node '{folder_name}'...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Check if folder exists
        target_dir = os.path.join(extract_to_path, folder_name)
        if os.path.exists(target_dir):
             print(f"⏩ Node '{folder_name}' đã tồn tại. Bỏ qua.")
             return

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # Simple extraction logic: extract all, but try to handle root folder
            # For simplicity, we extract directly to the target path structure
            # But safe extraction usually checks for common prefix
            
            # Create a temp dir for extraction
            temp_extract_dir = os.path.join(extract_to_path, f"temp_{folder_name}")
            os.makedirs(temp_extract_dir, exist_ok=True)
            zip_ref.extractall(temp_extract_dir)
            
            # Find the actual root folder inside the zip
            items = os.listdir(temp_extract_dir)
            if len(items) == 1 and os.path.isdir(os.path.join(temp_extract_dir, items[0])):
                # If zip contains a single folder, move its content or rename it
                src = os.path.join(temp_extract_dir, items[0])
                # We want the folder name to be consistent with 'folder_name' arg
                # So we rename src to target_dir
                os.rename(src, target_dir)
            else:
                 # If zip has loose files or multiple folders, move temp dir to target
                 os.rename(temp_extract_dir, target_dir)
                 
            # Cleanup empty temp dir if it still exists (os.rename works like move)
            if os.path.exists(temp_extract_dir):
                os.rmdir(temp_extract_dir)
                
            print(f"✅ Đã cài đặt node '{folder_name}'")
            
    except Exception as e:
        print(f"❌ Lỗi xử lý node '{folder_name}': {e}")


# The main function that runs on Modal
@app.function(
    image=downloader_image,
    volumes={
        f"{MOUNT_PATH}/checkpoints": vol_checkpoints,
        f"{MOUNT_PATH}/loras": vol_loras,
        f"{MOUNT_PATH}/controlnet": vol_controlnet,
        f"{MOUNT_PATH}/custom_nodes": vol_custom_nodes,
    },
    timeout=3600 # 1 hour timeout for large downloads
)
def download_assets(checkpoint_urls=[], checkpoint_names=[], 
                    lora_urls=[], lora_names=[],
                    controlnet_urls=[], controlnet_names=[],
                    node_urls=[], node_dirs=[]):
    
    print("🚀 Bắt đầu quá trình tải assets trên Modal Cloud...")
    
    # 1. Checkpoints
    for url, name in zip(checkpoint_urls, checkpoint_names):
        # Auto-append token
        if "civitai.com" in url and "token=" not in url:
             url += "&token=403d7e6612cfb89e27559bedd1bb2dbb"
        download_file_to_path(url, os.path.join(MOUNT_PATH, "checkpoints", name))

    # 2. Loras
    for url, name in zip(lora_urls, lora_names):
        if "civitai.com" in url and "token=" not in url:
             url += "&token=403d7e6612cfb89e27559bedd1bb2dbb"
        download_file_to_path(url, os.path.join(MOUNT_PATH, "loras", name))

    # 3. ControlNet
    for url, name in zip(controlnet_urls, controlnet_names):
        if "civitai.com" in url and "token=" not in url:
             url += "&token=403d7e6612cfb89e27559bedd1bb2dbb"
        download_file_to_path(url, os.path.join(MOUNT_PATH, "controlnet", name))

    # 4. Custom Nodes
    for url, folder in zip(node_urls, node_dirs):
        extract_zip_to_path(url, os.path.join(MOUNT_PATH, "custom_nodes"), folder)
        
    print("✨ Hoàn tất tải assets!")

# Helper to be called from local script
def run_download(checkpoint_urls=[], checkpoint_names=[], 
                 lora_urls=[], lora_names=[],
                 controlnet_urls=[], controlnet_names=[],
                 node_urls=[], node_dirs=[]):
    
    # Call the remote function
    with app.run():
        download_assets.remote(
            checkpoint_urls=checkpoint_urls, checkpoint_names=checkpoint_names,
            lora_urls=lora_urls, lora_names=lora_names,
            controlnet_urls=controlnet_urls, controlnet_names=controlnet_names,
            node_urls=node_urls, node_dirs=node_dirs
        )
