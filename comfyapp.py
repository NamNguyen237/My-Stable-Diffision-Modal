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
    .run_commands("apt update & apt upgrade -y & apt autoremove -y")
    .pip_install_from_requirements(
        "requirements.txt"
    )
    .run_commands(
        "comfy --skip-prompt install --nvidia"
    )
)

#checkpoints



#image = (
#    image.run_commands(
#        "wget -c \"https://civitai.com/api/download/models/1360303?type=Model&format=SafeTensor&size=pruned&fp=fp16&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"root/comfy/ComfyUI/models/loras/name.safetensors\""
#    )
#)



image = (
    image.run_commands(  # download a custom node
        "comfy node install image-resize-comfyui"
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
    .run_commands(
        "comfy node install https://github.com/pythongosssss/ComfyUI-WD14-Tagger.git"
    )
    .run_commands(
        "comfy node install https://github.com/alexopus/ComfyUI-Image-Saver.git"
    )
    .run_commands(
        "comfy node install https://github.com/jtydhr88/ComfyUI-HY-Motion1"
    )
)


# load local loras -> DISABLED to use Volume instead
# image = (
#     image.add_local_dir("./LORAS/", 
#         remote_path="/root/comfy/ComfyUI/models/loras"               
#     )   
# )
# load local controlnet -> DISABLED to use Volume instead
# image = (
#     image.add_local_dir("./CONTROLNET/", 
#         remote_path="/root/comfy/ComfyUI/models/controlnet"               
#     )   
# )

# Add extra_model_paths.yaml to let ComfyUI know about the volume mount paths
image = image.add_local_file("extra_model_paths.yaml", remote_path="/root/comfy/ComfyUI/extra_model_paths.yaml")

app = modal.App(name="nam-dev-comfyui", image=image)

# Define Volumes (create if missing to avoid errors, but user should populate them)
vol_checkpoints = modal.Volume.from_name("comfy_checkpoints", create_if_missing=True)
vol_loras = modal.Volume.from_name("comfy_loras", create_if_missing=True)
vol_controlnet = modal.Volume.from_name("comfy_controlnet", create_if_missing=True)
vol_custom_nodes = modal.Volume.from_name("comfy_custom_nodes", create_if_missing=True)

@app.function(
    max_containers=1,
    scaledown_window=3600,
    timeout=18000,
    gpu="A10G",
    volumes={
        "/root/vol_models/checkpoints": vol_checkpoints,
        "/root/vol_models/loras": vol_loras,
        "/root/vol_models/controlnet": vol_controlnet,
        "/root/vol_models/custom_nodes": vol_custom_nodes, # Optional if you use volume for custom nodes
    }
)
@modal.concurrent(max_inputs=10)
@modal.web_server(8000, startup_timeout=60)
def webui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)

