import subprocess

import modal


image = (  # build up a Modal Image to run ComfyUI, step by step
    modal.Image.debian_slim(  # start from basic Linux with Python
        python_version="3.11"
    )
    .apt_install("git")  # install git to clone ComfyUI
    .apt_install("nano")  # install to have a minimal text editor if we wanted to change something minimal
    .apt_install("libgl1-mesa-glx")  # needed to run ComfyUI
    .apt_install("libglib2.0-0")  # needed to run ComfyUI
    .apt_install("wget")
    .pip_install_from_requirements(
        "requirements.txt"
    )
    .run_commands(
        "comfy --skip-prompt install --nvidia"
    )
)

#image = (
#    image.run_commands(
#        "comfy --skip-prompt model download --url https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors --relative-path models/clip"
#    )

    
    # .run_commands(
    #     "comfy --skip-prompt model download --url https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors --relative-path models/unet"
    # )
    # Add .run_commands(...) calls for any other models you want to download
#)
#checkpoints
image = (
    image.run_commands(
        "wget -c \"https://civitai.com/api/download/models/1190596?type=Model&format=SafeTensor&size=full&fp=bf16&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"root/comfy/ComfyUI/models/checkpoints/NoobAI-XL V-Pred-1.0-Version.safetensors\""
    )
    .run_commands(
        "wget -c \"https://civitai.com/api/download/models/889818?type=Model&format=SafeTensor&size=pruned&fp=fp16&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"root/comfy/ComfyUI/models/checkpoints/Illustrious-XL v0.1.safetensors\""
    )
    .run_commands(
        "wget -c \"https://civitai.com/api/download/models/1130140?type=Model&format=SafeTensor&size=pruned&fp=fp16&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"root/comfy/ComfyUI/models/checkpoints/RouWei 0.6.1 vpred.safetensors\""
    )
)
#loras
image = (
    image.run_commands(
        "wget -c \"https://civitai.com/api/download/models/1312224?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"root/comfy/ComfyUI/models/loras/AI styles dump AIO-noob-vpred1.0_v5.safetensors\""
    )
    .run_commands(
        "wget -c \"https://civitai.com/api/download/models/1290145?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"root/comfy/ComfyUI/models/loras/Hara ID 21.safetensors\""
    )
    .run_commands(
        "wget -c \"https://civitai.com/api/download/models/1265180?type=Model&format=SafeTensor&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"root/comfy/ComfyUI/models/loras/Pixel Art LoRA noob vpred 1.0 v2.safetensors\""
    )
)

image = (
    image.run_commands(  # download a custom node
        "comfy node install image-resize-comfyui"
    )
    .run_commands(
        "comfy node install https://github.com/regiellis/ComfyUI-EasyNoobai.git"
    )
    .run_commands(
        "comfy node install efficiency-nodes-comfyui"
    )
    .run_commands(
        "comfy node install https://github.com/JuniorDevNam/Lora-Training-in-Comfy.git"
    )
    .run_commands(
        "comfy node install https://github.com/JuniorDevNam/Image-Captioning-in-ComfyUI.git"
    )
    # Add .run_commands(...) calls for any other custom nodes you want to download
)
image = (
    image.run_commands("mkdir /dataset")
    .run_commands(
        "git clone https://github.com/JuniorDevNam/luna_bloom.git /dataset"
    )
)

#(re)load workflows:
image = (
    image.add_local_dir("./WORKFLOWS/", remote_path="/root/comfy/ComfyUI/user/default/workflows")
)
app = modal.App(name="nam-dev-comfyui", image=image)

@app.function(
    allow_concurrent_inputs=10,
    concurrency_limit=1,
    container_idle_timeout=30,
    timeout=1800,
    gpu="A10G",
)
@modal.web_server(8000, startup_timeout=60)
def ui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)
