import modal
import subprocess
image = (  # build up a Modal Image to run ComfyUI, step by step
    modal.Image.debian_slim(  # start from basic Linux with Python
        python_version="3.11"
    )
    .apt_install("git")  # install git to clone ComfyUI
    .apt_install("nano")  # install to have a minimal text editor if we wanted to change something minimal
    .apt_install("libgl1-mesa-glx")  # needed to run ComfyUI
    .apt_install("libglib2.0-0")  # needed to run ComfyUI
    .run_commands("apt update & apt upgrade -y & apt autoremove -y")
    .pip_install_from_requirements(
        "requirements.txt"
    )
)
#load local loras
image = (
    image.add_local_dir("./LORAS/", 
        remote_path="/root/comfy/ComfyUI/models/loras"               
    )   
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
def webui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)