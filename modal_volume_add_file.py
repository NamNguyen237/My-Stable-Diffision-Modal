
checkpoint_urls = [
    "https://civitai.com/api/download/models/1190596?type=Model&format=SafeTensor&size=full&fp=bf16&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/889818?type=Model&format=SafeTensor&size=pruned&fp=fp16&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/1130140?type=Model&format=SafeTensor&size=pruned&fp=fp16&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/1140829?type=Model&format=SafeTensor&size=full&fp=bf16&token=403d7e6612cfb89e27559bedd1bb2dbb"
]
checkpoint_names = [
    "NoobAI-XL-V-Pred-1.0-Version.safetensors",
    "Illustrious-XL-v0.1.safetensors",
    "RouWei-0.6.1-vpred.safetensors",
    "NoobAI-XL-V-Pred-0.75S-Version.safetensors"
]

lora_urls = [
    "https://civitai.com/api/download/models/1312224?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/1290145?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/1265180?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/1187614?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/1167067?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb",
    "https://civitai.com/api/download/models/1173678?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb"
]
lora_names = [
    "AI styles dump AIO-noob-vpred1.0_v5.safetensors",
    "Hara ID 21.safetensors",
    "Pixel Art LoRA noob vpred 1.0 v2.safetensors",
    "Miside(米塔)|NoobAI-XL eps v1.1.safetensors",
    "Miside(米塔)|NoobAI-XL v-pred 0.75s.safetensors",
    "Miside(米塔)|NoobAI-XL v-pred 0.75s new.safetensors"
]

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

from modal_asset_loader import (
    download_files_to_volume,
    download_and_extract_nodes,
    upload_local_to_volume,
    comfy_checkpoints,
    comfy_loras,
    comfy_custom_nodes
)

# Tải từ URL
download_files_to_volume(checkpoint_urls, checkpoint_names, comfy_checkpoints)
download_files_to_volume(lora_urls, lora_names, comfy_loras)
download_and_extract_nodes(custom_node_urls, custom_node_dirs, comfy_custom_nodes)

# Tải từ local
#Examples
#upload_local_to_volume("/home/nam/local_checkpoints", comfy_checkpoints)
#upload_local_to_volume("/home/nam/local_loras", comfy_loras)
#upload_local_to_volume("/home/nam/local_nodes", comfy_custom_nodes, "MyLocalNode")
upload_local_to_volume("./LORAS", comfy_loras)