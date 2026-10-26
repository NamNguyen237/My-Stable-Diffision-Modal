
import os
from pathlib import Path


def load_env_file(env_path=None):
    if env_path is None:
        env_path = Path(__file__).resolve().with_name(".env")
    if not env_path.exists():
        env_path.write_text("CIVITAI_TOKEN=\n", encoding="utf-8")
        print(
            f"Đã tạo {env_path}. Điền token vào CIVITAI_TOKEN rồi chạy lại.",
            flush=True,
        )

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            os.environ.setdefault(key, value)
    print(f"✅ Đã đọc cấu hình từ {env_path}.", flush=True)


checkpoint_urls = [
    "https://civitai.com/api/download/models/290640?fileId=228616&type=Model&format=SafeTensor&size=full&fp=bf16",
    "https://civitai.com/api/download/models/1190596?type=Model&format=SafeTensor&size=full&fp=bf16",
    "https://civitai.com/api/download/models/889818?type=Model&format=SafeTensor&size=pruned&fp=fp16",
    "https://civitai.com/api/download/models/1130140?type=Model&format=SafeTensor&size=pruned&fp=fp16",
    "https://civitai.com/api/download/models/1140829?type=Model&format=SafeTensor&size=full&fp=bf16"
]
checkpoint_names = [
    "ponyDiffusionV6XL_v6StartWithThisOne.safetensors",
    "NoobAI-XL-V-Pred-1.0-Version.safetensors",
    "Illustrious-XL-v0.1.safetensors",
    "RouWei-0.6.1-vpred.safetensors",
    "NoobAI-XL-V-Pred-0.75S-Version.safetensors"
]

lora_urls = [
    "https://civitai.com/api/download/models/1312224?type=Model&format=SafeTensor",
    "https://civitai.com/api/download/models/1290145?type=Model&format=SafeTensor",
    "https://civitai.com/api/download/models/1265180?type=Model&format=SafeTensor",
    "https://civitai.com/api/download/models/1187614?type=Model&format=SafeTensor",
    "https://civitai.com/api/download/models/1167067?type=Model&format=SafeTensor",
    "https://civitai.com/api/download/models/1173678?type=Model&format=SafeTensor"
]
lora_names = [
    "AI styles dump AIO-noob-vpred1.0_v5.safetensors",
    "Hara ID 21.safetensors",
    "Pixel Art LoRA noob vpred 1.0 v2.safetensors",
    "Miside(米塔)-NoobAI-XL eps v1.1.safetensors",
    "Miside(米塔) -NoobAI-XL v-pred 0.75s.safetensors",
    "Miside(米塔)-NoobAI-XL v-pred 0.75s new.safetensors"
]

controlnet_urls = [
    # Add ControlNet URLs here
    "https://civitai.com/api/download/models/1077649?type=Model&format=SafeTensor"
]
controlnet_names = [
    # Add corresponding filenames here
    "noobaiXLControlnet_openposeModel.safetensors"
]

vae_urls = [
    "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors"
]
vae_names = ["sdxl_vae.safetensors"]

custom_node_urls = [
    "https://github.com/regiellis/ComfyUI-EasyNoobai/archive/refs/heads/main.zip",
    "https://github.com/jags111/efficiency-nodes-comfyui/archive/refs/heads/main.zip",
    "https://github.com/alexopus/ComfyUI-Image-Saver/archive/refs/heads/master.zip",
    "https://github.com/palant/image-resize-comfyui/archive/refs/heads/main.zip"
]
custom_node_dirs = [
    "ComfyUI-EasyNoobai",
    "efficiency-nodes-comfyui",
    "ComfyUI-Image-Saver",
    "image-resize-comfyui"
]


from modal_asset_loader import run_download

if __name__ == "__main__":
    load_env_file()
    token_configured = bool(os.getenv("CIVITAI_TOKEN"))
    if token_configured:
        print("🔑 CIVITAI_TOKEN đã được nạp (không hiển thị token).", flush=True)
    else:
        print(
            "⚠️ CIVITAI_TOKEN chưa được đặt; tải từ Civitai có thể bị từ chối.",
            flush=True,
        )
    print(
        "📋 Danh sách: "
        f"{len(checkpoint_urls)} checkpoint, {len(lora_urls)} LoRA, "
        f"{len(controlnet_urls)} ControlNet, {len(vae_urls)} VAE, "
        f"{len(custom_node_urls)} custom node.",
        flush=True,
    )
    print("▶️ Bắt đầu gửi tác vụ tải lên Modal...", flush=True)
    report = run_download(
        checkpoint_urls=checkpoint_urls, checkpoint_names=checkpoint_names,
        lora_urls=lora_urls, lora_names=lora_names,
        controlnet_urls=controlnet_urls, controlnet_names=controlnet_names,
        vae_urls=vae_urls, vae_names=vae_names,
        node_urls=custom_node_urls, node_dirs=custom_node_dirs,
        civitai_token=os.getenv("CIVITAI_TOKEN")
    )
    print(
        "🏁 Script kết thúc. "
        f"{report['failures']} mục cần kiểm tra lại.",
        flush=True,
    )


import modal

app = modal.App("volume-uploader")

def upload_local_to_volume(local_path, volume_name, remote_path=""):
    print(f"Uploading {local_path} to volume {volume_name} at remote path /{remote_path}")
    vol = modal.Volume.from_name(volume_name, create_if_missing=True)
    with vol.batch_upload(force=True) as batch:
        batch.put_directory(local_path, f"/{remote_path}")
    print("Upload complete!")

# Define volume names
comfy_checkpoints = "comfy_checkpoints"
comfy_loras = "comfy_loras"
comfy_controlnet = "comfy_controlnet"
comfy_custom_nodes = "comfy_custom_nodes"

@app.local_entrypoint()
def main():
    # Tải từ local
    #Examples
    #upload_local_to_volume("/home/nam/local_checkpoints", comfy_checkpoints)
    #upload_local_to_volume("/home/nam/local_loras", comfy_loras)
    #upload_local_to_volume("/home/nam/local_nodes", comfy_custom_nodes, "MyLocalNode")
    upload_local_to_volume("./LORAS", comfy_loras)
    #upload_local_to_volume("./CONTROLNET", comfy_controlnet)