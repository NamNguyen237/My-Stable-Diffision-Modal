import modal
import requests
import io
import zipfile
import hashlib
import os

# Volume bindings
comfy_checkpoints = modal.Volume.from_name("comfy_checkpoints")
comfy_loras = modal.Volume.from_name("comfy_loras")
comfy_custom_nodes = modal.Volume.from_name("comfy_custom_nodes")

# Utility
def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def file_exists_and_same(volume, path, new_data):
    try:
        if path not in volume.list_files():
            return False
        old_data = volume.read(path)
        return sha256_bytes(old_data) == sha256_bytes(new_data)
    except:
        return False

def write_if_new(volume, path, data):
    if file_exists_and_same(volume, path, data):
        print(f"✅ '{path}' đã có và giống nhau, bỏ qua.")
    else:
        volume.write(path, data)
        print(f"✅ Đã ghi '{path}' vào volume.")

# Streaming download
def stream_download_to_volume(url, volume, filename):
    try:
        print(f"⬇️ Đang tải '{filename}' bằng streaming...")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            buffer = bytearray()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    buffer.extend(chunk)
            volume.write(filename, bytes(buffer))
            print(f"✅ Đã ghi '{filename}' vào volume.")
            del buffer
    except Exception as e:
        print(f"❌ Lỗi khi tải '{filename}': {e}")

# Core functions
def download_files_to_volume(urls, names, volume, use_stream=False):
    for url, name in zip(urls, names):
        try:
            if use_stream:
                stream_download_to_volume(url, volume, name)
            else:
                print(f"⬇️ Đang tải '{name}'...")
                response = requests.get(url)
                response.raise_for_status()
                write_if_new(volume, name, response.content)
        except Exception as e:
            print(f"❌ Lỗi tải '{name}': {e}")

def extract_zip_to_volume(zip_bytes, volume, folder_name):
    try:
        with zipfile.ZipFile(zip_bytes) as zip_ref:
            root_folder = zip_ref.namelist()[0].split("/")[0]
            found_init = False
            for zip_info in zip_ref.infolist():
                if zip_info.is_dir():
                    continue
                extracted_path = zip_info.filename
                if not extracted_path.startswith(root_folder + "/"):
                    continue
                relative_path = "/".join(extracted_path.split("/")[1:])
                file_data = zip_ref.read(zip_info.filename)
                full_path = f"{folder_name}/{relative_path}"
                volume.write(full_path, file_data)
                if relative_path.endswith("__init__.py"):
                    found_init = True
            if found_init:
                print(f"✅ Node '{folder_name}' hợp lệ (có __init__.py).")
            else:
                print(f"⚠️ Node '{folder_name}' có thể KHÔNG hợp lệ.")
    except Exception as e:
        print(f"❌ Lỗi giải nén node '{folder_name}': {e}")

def download_and_extract_nodes(urls, folder_names, volume):
    for url, folder_name in zip(urls, folder_names):
        try:
            print(f"⬇️ Tải và giải nén node '{folder_name}'...")
            response = requests.get(url)
            response.raise_for_status()
            zip_bytes = io.BytesIO(response.content)
            extract_zip_to_volume(zip_bytes, volume, folder_name)
        except Exception as e:
            print(f"❌ Lỗi với node '{folder_name}': {e}")

def upload_local_to_volume(local_dir, volume, remote_prefix=""):
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, local_dir)
            remote_path = os.path.join(remote_prefix, rel_path)
            with open(local_path, "rb") as f:
                data = f.read()
                volume.write(remote_path, data)
                print(f"✅ Đã ghi '{remote_path}' từ local vào volume.")
