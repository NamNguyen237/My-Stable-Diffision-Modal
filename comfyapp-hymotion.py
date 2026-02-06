import subprocess

import modal


image = (  # build up a Modal Image to run ComfyUI, step by step
    modal.Image.debian_slim(  # start from basic Linux with Python
        python_version="3.11"
    )
    .apt_install("git")  # install git to clone ComfyUI
    .apt_install("libgl1-mesa-glx")  # needed to run ComfyUI
    .apt_install("libglib2.0-0")  # needed to run ComfyUI
    .apt_install("wget")
    .run_commands("apt update & apt upgrade -y & apt autoremove -y")
    .pip_install_from_requirements(
        "requirements-hymotion.txt"
    )
    .run_commands(
        "comfy --skip-prompt install --nvidia"
    )
    .run_commands(
        "mkdir /root/comfy/ComfyUI/models/HY-Motion"
    )
    .run_commands(
        "mkdir /root/comfy/ComfyUI/models/HY-Motion/ckpts"
    )
    .run_commands(
        "huggingface-cli download tencent/HY-Motion-1.0 --local-dir /root/comfy/ComfyUI/models/HY-Motion/ckpts"
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
        "comfy node install https://github.com/jtydhr88/ComfyUI-HY-Motion1"
    )
)




app = modal.App(name="nam-dev-comfyui", image=image)

@app.function(
    max_containers=1,
    scaledown_window=3600,
    timeout=18000,
    gpu="A10G",
)
@modal.concurrent(max_inputs=10)
@modal.web_server(8000, startup_timeout=60)
def webui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)

