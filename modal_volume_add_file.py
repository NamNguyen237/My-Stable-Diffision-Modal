
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
    run_download(
        checkpoint_urls=checkpoint_urls, checkpoint_names=checkpoint_names,
        lora_urls=lora_urls, lora_names=lora_names,
        controlnet_urls=controlnet_urls, controlnet_names=controlnet_names,
        node_urls=custom_node_urls, node_dirs=custom_node_dirs
    )


# Tải từ local
#Examples
#upload_local_to_volume("/home/nam/local_checkpoints", comfy_checkpoints)
#upload_local_to_volume("/home/nam/local_loras", comfy_loras)
#upload_local_to_volume("/home/nam/local_nodes", comfy_custom_nodes, "MyLocalNode")
upload_local_to_volume("./LORAS", comfy_loras)
#upload_local_to_volume("./CONTROLNET", comfy_controlnet)