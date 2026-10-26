import modal
import requests
import io
import zipfile
import os
import time
from collections import Counter
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# Create an App for the downloader
app = modal.App("comfyui-downloader")

# Define Image for the downloader (needs requests)
downloader_image = modal.Image.debian_slim(python_version="3.11").pip_install("requests")

# Volume bindings (must be consistent with comfyapp.py)
vol_checkpoints = modal.Volume.from_name("comfy_checkpoints", create_if_missing=True)
vol_loras = modal.Volume.from_name("comfy_loras", create_if_missing=True)
vol_controlnet = modal.Volume.from_name("comfy_controlnet", create_if_missing=True)
vol_custom_nodes = modal.Volume.from_name("comfy_custom_nodes", create_if_missing=True)
vol_vae = modal.Volume.from_name("comfy_vae", create_if_missing=True)

# Path constants used inside the Modal Function
MOUNT_PATH = "/root/vol_models"

def add_civitai_token(url, token):
    if "civitai.com" not in url or not token:
        return url

    parts = urlsplit(url)
    query = [(key, value) for key, value in parse_qsl(parts.query) if key != "token"]
    query.append(("token", token))
    return urlunsplit(parts._replace(query=urlencode(query)))


def get_remote_file_size(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=(15, 60))
        response.raise_for_status()
        size = int(response.headers.get("content-length", 0))
        return size if size > 0 else None
    except (requests.RequestException, ValueError) as exc:
        print(
            f"⚠️ Không xác minh được kích thước từ xa ({type(exc).__name__}).",
            flush=True,
        )
        return None

def download_file_to_path(url, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    remote_size = get_remote_file_size(url)

    if os.path.exists(filepath) and remote_size is not None:
        local_size = os.path.getsize(filepath)
        if local_size == remote_size:
            print(
                f"⏩ '{os.path.basename(filepath)}' đã có đủ "
                f"({local_size / (1024 * 1024):.2f} MB). Bỏ qua.",
                flush=True,
            )
            return
        print(
            f"⚠️ '{os.path.basename(filepath)}' không khớp kích thước. Tải lại...",
            flush=True,
        )

    temp_filepath = filepath + ".part"
    offset = os.path.getsize(temp_filepath) if os.path.exists(temp_filepath) else 0
    if remote_size is not None and offset == remote_size:
        os.replace(temp_filepath, filepath)
        print(f"✅ Khôi phục file đã tải đủ '{os.path.basename(filepath)}'", flush=True)
        return
    if remote_size is not None and offset > remote_size:
        os.remove(temp_filepath)
        offset = 0
    headers = {"Range": f"bytes={offset}-"} if offset else {}
    filename = os.path.basename(filepath)
    print(f"⬇️ Đang tải '{filename}'...", flush=True)

    started_at = time.monotonic()
    progress_interval = 16 * 1024 * 1024
    next_progress_time = started_at + 5
    try:
        with requests.get(
            url, headers=headers, stream=True, timeout=(15, 120)
        ) as response:
            response.raise_for_status()
            append = offset > 0 and response.status_code == 206
            if offset and not append:
                offset = 0
            next_progress_at = offset + progress_interval
            expected_size = remote_size
            content_range = response.headers.get("content-range", "")
            if "/" in content_range and content_range.rsplit("/", 1)[1].isdigit():
                expected_size = int(content_range.rsplit("/", 1)[1])
            elif response.headers.get("content-length", "").isdigit():
                response_size = int(response.headers["content-length"])
                expected_size = offset + response_size if append else response_size

            downloaded_size = offset
            with open(temp_filepath, "ab" if append else "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        now = time.monotonic()
                        if (
                            downloaded_size >= next_progress_at
                            or now >= next_progress_time
                        ):
                            elapsed = max(time.monotonic() - started_at, 0.001)
                            progress = f"{downloaded_size / (1024 * 1024):.0f} MB"
                            if expected_size:
                                percentage = downloaded_size * 100 / expected_size
                                progress += f" / {expected_size / (1024 * 1024):.0f} MB ({percentage:.1f}%)"
                            print(
                                f"   … {filename}: {progress}, "
                                f"{downloaded_size / elapsed / (1024 * 1024):.1f} MB/s",
                                flush=True,
                            )
                            next_progress_at = downloaded_size + progress_interval
                            next_progress_time = now + 5
    except requests.RequestException as exc:
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
        detail = f"HTTP {status_code}" if status_code else type(exc).__name__
        print(f"❌ Lỗi tải '{filename}' ({detail}).", flush=True)
        raise RuntimeError(
            f"Download failed for '{filename}' ({detail})."
        ) from None

    downloaded_size = os.path.getsize(temp_filepath)
    if expected_size is not None and downloaded_size != expected_size:
        print(
            f"❌ Tải chưa đủ '{filename}': {downloaded_size}/{expected_size} bytes.",
            flush=True,
        )
        raise IOError(
            f"Download incomplete for '{filename}': "
            f"expected {expected_size} bytes, got {downloaded_size}."
        )

    os.replace(temp_filepath, filepath)
    elapsed = max(time.monotonic() - started_at, 0.001)
    print(
        f"✅ Đã tải xong '{filename}' "
        f"({downloaded_size / (1024 * 1024):.1f} MB, {elapsed:.1f} giây)",
        flush=True,
    )

def extract_zip_to_path(url, extract_to_path, folder_name):
    # Runs inside Modal container
    try:
        print(f"⬇️ Tải và giải nén node '{folder_name}'...", flush=True)
        with requests.get(url, stream=True, timeout=(15, 120)) as response:
            response.raise_for_status()
            content_length = response.headers.get("content-length", "")
            expected_size = int(content_length) if content_length.isdigit() else None
            downloaded_size = 0
            started_at = time.monotonic()
            next_progress_at = 16 * 1024 * 1024
            next_progress_time = started_at + 5
            archive_data = io.BytesIO()
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    archive_data.write(chunk)
                    downloaded_size += len(chunk)
                    now = time.monotonic()
                    if (
                        downloaded_size >= next_progress_at
                        or now >= next_progress_time
                    ):
                        progress = f"{downloaded_size / (1024 * 1024):.0f} MB"
                        if expected_size:
                            percentage = downloaded_size * 100 / expected_size
                            progress += (
                                f" / {expected_size / (1024 * 1024):.0f} MB "
                                f"({percentage:.1f}%)"
                            )
                        print(
                            f"   … {folder_name}: đang tải {progress}",
                            flush=True,
                        )
                        next_progress_at = downloaded_size + 16 * 1024 * 1024
                        next_progress_time = now + 5
        
        # Check if folder exists
        target_dir = os.path.join(extract_to_path, folder_name)
        if os.path.exists(target_dir):
             print(f"⏩ Node '{folder_name}' đã tồn tại. Bỏ qua.", flush=True)
             return

        print(f"📦 Đang giải nén node '{folder_name}'...", flush=True)
        with zipfile.ZipFile(archive_data) as zip_ref:
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
                
            print(f"✅ Đã cài đặt node '{folder_name}'", flush=True)
            
    except Exception as e:
        print(f"❌ Lỗi xử lý node '{folder_name}': {e}", flush=True)
        raise


def run_asset_tasks(tasks, civitai_token=None):
    results = []
    category_counts = Counter(category for category, _, _, _ in tasks)
    category_progress = Counter()
    overall_total = len(tasks)

    for task_number, (category, name, volume_name, action) in enumerate(
        tasks, start=1
    ):
        category_progress[category] += 1
        index = category_progress[category]
        category_total = category_counts[category]
        print(
            f"📍 Tiến trình {task_number}/{overall_total} "
            f"| {category} {index}/{category_total}: {name}",
            flush=True,
        )
        try:
            action()
            results.append({
                "category": category,
                "name": name,
                "volume": volume_name,
                "status": "success",
                "details": "Downloaded or already present.",
            })
            print(
                f"✅ Hoàn tất asset {task_number}/{overall_total}: {name}",
                flush=True,
            )
        except Exception as exc:
            status_code = getattr(
                getattr(exc, "response", None), "status_code", None
            )
            if status_code is not None:
                details = f"HTTP {status_code}"
            elif isinstance(exc, (IOError, zipfile.BadZipFile)):
                details = f"{type(exc).__name__}: {exc}"
            elif isinstance(exc, RuntimeError) and str(exc).startswith("Download failed"):
                details = str(exc)
            else:
                details = type(exc).__name__
            if civitai_token:
                details = details.replace(civitai_token, "[REDACTED]")
            print(f"❌ {name}: {details}", flush=True)
            results.append({
                "category": category,
                "name": name,
                "volume": volume_name,
                "status": "failed",
                "details": details,
            })
            print(
                f"❌ Asset {task_number}/{overall_total} thất bại: {name}",
                flush=True,
            )

    return results


def commit_asset_volumes(results, volumes, civitai_token=None):
    total_volumes = len(volumes)
    for index, (volume_name, volume) in enumerate(volumes, start=1):
        print(
            f"💾 Đang commit volume {index}/{total_volumes}: {volume_name}...",
            flush=True,
        )
        try:
            volume.commit()
            print(f"✅ Đã commit volume '{volume_name}'.", flush=True)
        except Exception as exc:
            details = f"{type(exc).__name__}: {exc}"
            if civitai_token:
                details = details.replace(civitai_token, "[REDACTED]")
            print(f"❌ Commit volume '{volume_name}' thất bại: {details}", flush=True)
            successful_assets = [
                result for result in results
                if result["volume"] == volume_name and result["status"] == "success"
            ]
            if successful_assets:
                for result in successful_assets:
                    result["status"] = "failed"
                    result["details"] = f"Volume commit failed: {details}"
            else:
                results.append({
                    "category": "Volume commit",
                    "name": volume_name,
                    "volume": volume_name,
                    "status": "failed",
                    "details": details,
                })


# The main function that runs on Modal
@app.function(
    image=downloader_image,
    volumes={
        f"{MOUNT_PATH}/checkpoints": vol_checkpoints,
        f"{MOUNT_PATH}/loras": vol_loras,
        f"{MOUNT_PATH}/controlnet": vol_controlnet,
        f"{MOUNT_PATH}/custom_nodes": vol_custom_nodes,
        f"{MOUNT_PATH}/vae": vol_vae,
    },
    timeout=3600 # 1 hour timeout for large downloads
)
def download_assets(checkpoint_urls=None, checkpoint_names=None,
                    lora_urls=None, lora_names=None,
                    controlnet_urls=None, controlnet_names=None,
                    vae_urls=None, vae_names=None,
                    node_urls=None, node_dirs=None, civitai_token=None):
    checkpoint_urls = checkpoint_urls or []
    checkpoint_names = checkpoint_names or []
    lora_urls = lora_urls or []
    lora_names = lora_names or []
    controlnet_urls = controlnet_urls or []
    controlnet_names = controlnet_names or []
    vae_urls = vae_urls or []
    vae_names = vae_names or []
    node_urls = node_urls or []
    node_dirs = node_dirs or []

    for label, urls, names in (
        ("checkpoints", checkpoint_urls, checkpoint_names),
        ("LoRAs", lora_urls, lora_names),
        ("ControlNet", controlnet_urls, controlnet_names),
        ("VAE", vae_urls, vae_names),
        ("custom nodes", node_urls, node_dirs),
    ):
        if len(urls) != len(names):
            raise ValueError(
                f"{label}: received {len(urls)} URLs but {len(names)} target names."
            )
    
    tasks = []
    for category, urls, names, volume_name, directory, use_token in (
        ("Checkpoint", checkpoint_urls, checkpoint_names, "checkpoints", "checkpoints", True),
        ("LoRA", lora_urls, lora_names, "loras", "loras", True),
        ("ControlNet", controlnet_urls, controlnet_names, "controlnet", "controlnet", True),
        ("VAE", vae_urls, vae_names, "vae", "vae", False),
    ):
        print(f"📦 {category}: {len(urls)}", flush=True)
        for url, name in zip(urls, names):
            if use_token:
                url = add_civitai_token(url, civitai_token)
            filepath = os.path.join(MOUNT_PATH, directory, name)
            tasks.append((
                category,
                name,
                volume_name,
                lambda url=url, filepath=filepath: download_file_to_path(url, filepath),
            ))

    print(f"📦 Custom nodes: {len(node_urls)}", flush=True)
    for url, folder in zip(node_urls, node_dirs):
        extract_path = os.path.join(MOUNT_PATH, "custom_nodes")
        tasks.append((
            "Custom node",
            folder,
            "custom_nodes",
            lambda url=url, extract_path=extract_path, folder=folder: extract_zip_to_path(
                url, extract_path, folder
            ),
        ))

    total_assets = len(tasks)
    print(
        f"🚀 Worker Modal đã khởi động; xử lý {total_assets} asset.",
        flush=True,
    )
    results = run_asset_tasks(tasks, civitai_token=civitai_token)

    print("💾 Đang commit các Modal Volume...", flush=True)
    volumes = (
        ("checkpoints", vol_checkpoints),
        ("loras", vol_loras),
        ("controlnet", vol_controlnet),
        ("custom_nodes", vol_custom_nodes),
        ("vae", vol_vae),
    )
    commit_asset_volumes(results, volumes, civitai_token=civitai_token)

    successes = sum(result["status"] == "success" for result in results)
    failures = len(results) - successes
    print(
        f"✨ Worker hoàn tất: {successes} thành công, {failures} thất bại.",
        flush=True,
    )
    return {"results": results, "successes": successes, "failures": failures}

# Helper to be called from local script
def run_download(checkpoint_urls=None, checkpoint_names=None,
                 lora_urls=None, lora_names=None,
                 controlnet_urls=None, controlnet_names=None,
                 vae_urls=None, vae_names=None,
                 node_urls=None, node_dirs=None, civitai_token=None):
    
    print("⏳ Đang khởi tạo kết nối với Modal...", flush=True)
    with app.run():
        print("☁️ Đã kết nối Modal; bắt đầu worker tải assets...", flush=True)
        report = download_assets.remote(
            checkpoint_urls=checkpoint_urls, checkpoint_names=checkpoint_names,
            lora_urls=lora_urls, lora_names=lora_names,
            controlnet_urls=controlnet_urls, controlnet_names=controlnet_names,
            vae_urls=vae_urls, vae_names=vae_names,
            node_urls=node_urls, node_dirs=node_dirs,
            civitai_token=civitai_token
        )
    print("\n========== BÁO CÁO TẢI ASSET ==========", flush=True)
    for result in report["results"]:
        status = "THÀNH CÔNG" if result["status"] == "success" else "THẤT BẠI"
        print(
            f"[{status}] {result['category']}: {result['name']} — "
            f"{result['details']}",
            flush=True,
        )
    failed_results = [
        result for result in report["results"]
        if result["status"] == "failed"
    ]
    if failed_results:
        print("\n========== CÁC MỤC CẦN KIỂM TRA LẠI ==========", flush=True)
        for result in failed_results:
            print(
                f"- {result['category']}: {result['name']} — "
                f"{result['details']}",
                flush=True,
            )
    print(
        f"Tổng kết: {report['successes']} thành công, "
        f"{report['failures']} thất bại.",
        flush=True,
    )
    print("======================================", flush=True)
    return report
