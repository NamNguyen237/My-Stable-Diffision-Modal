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
    .run_commands("rm -rf /root/comfy/ComfyUI/")
    .pip_install_from_requirements(
        "requirements.txt"
    )
    .run_commands(
        "comfy --skip-prompt install --nvidia"
    )
)



#image = (
#    image.run_commands(
#        "wget -c \"https://civitai.com/api/download/models/1360303?type=Model&format=SafeTensor&size=pruned&fp=fp16&token=403d7e6612cfb89e27559bedd1bb2dbb\" -O \"
#    )
#)



#load local loras
image = (
    image.add_local_dir("./LORAS/", 
        remote_path="/root/comfy/ComfyUI/models/loras"               
    )   
)

app = modal.App(name="nams-dev-comfyui", image=image)
comfy_checkpoints = modal.Volume.from_name("comfy_checkpoints")
comfy_loras = modal.Volume.from_name("comfy_loras")
comfy_custom_nodes = modal.Volume.from_name("comfy_custom_nodes")
@app.function(
    max_containers=1,
    scaledown_window=3600,
    timeout=18000,
    gpu="A10G",
    volumes={
        "/root/comfy/ComfyUI/models/checkpoints/": comfy_checkpoints,
        "/root/comfy/ComfyUI/models/loras/": comfy_loras,
        "/root/comfy/ComfyUI/custom_nodes/": comfy_custom_nodes
    }
)
@modal.concurrent(max_inputs=10)
@modal.web_server(8000, startup_timeout=60)
def webui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)

