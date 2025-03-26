# ---
# args: ["--timeout", 10]
# ---

# ## Overview
#
# Quick snippet showing how to connect to a Jupyter notebook server running inside a Modal container,
# especially useful for exploring the contents of Modal Volumes.
# This uses [Modal Tunnels](https://modal.com/docs/guide/tunnels#tunnels-beta)
# to create a tunnel between the running Jupyter instance and the internet.
#
# If you want to your Jupyter notebook to run _locally_ and execute remote Modal Functions in certain cells, see the `basic.ipynb` example :)
#https://github.com/modal-labs/modal-examples/blob/main/11_notebooks/jupyter_inside_modal.py
import socket
import threading
import os
import secrets
import subprocess
import modal

app = modal.App(
    image=(
        modal.Image.debian_slim(python_version="3.13")
        .pip_install(
             "jupyter", 
             "jupyterlab", 
             "jupyter_http_over_ws", 
             "toml", 
             "safetensors", 
             "torch", 
             "accelerate",
             "transformers",
             "einops",
             "diffusers",
             "torchvision",
             "opencv-python-headless",
             "imagesize",
             "voluptuous",
             "bitsandbytes"
             )
        .apt_install("curl", "unzip", "fuse3", "git-all", "aria2")
        .run_commands("curl https://rclone.org/install.sh | bash")
        .run_commands("mkdir /root/.config/")
        .run_commands("mkdir /root/.config/rclone/")
        .run_commands("mkdir /root/content/")
        .run_commands("mkdir /root/content/drive/")   
        .run_commands("mkdir /root/content/drive/MyDrive/")
        .run_commands("mkdir /root/content/drive/MyDrive/Loras/")
        .run_commands("mkdir /root/notebooks/")
        .run_commands("git clone https://github.com/derrian-distro/LoRA_Easy_Training_scripts_Backend /root/content/trainer/")
        .run_commands("rm -r /root/content/trainer/sd_scripts")
        .run_commands("git clone https://github.com/kohya-ss/sd-scripts /root/content/trainer/sd_scripts")
        .run_commands("chmod 755 /root/content/trainer/install_312.sh")
        .add_local_dir("./rclone/", 
        remote_path="/root/.config/rclone/",copy=True)
        
        
        #.run_commands("rclone copy --multi-thread-streams=16 --update "$vi_tri_cu_the_file_can_copy" "$dich_den_cua_file_can_copy" --ignore-existing --checksum --transfers 16 -v --stats 10s")

        .run_commands("rclone copy --multi-thread-streams=16 --update \"GDrive16T:/Loras/yuki_asayuki101\" \"/root/content/drive/MyDrive/Loras/yuki_asayuki101\" --ignore-existing --checksum --transfers 16 -v --stats 10s")

        #rclone copy --multi-thread-streams=16 --update "/root/content/drive/MyDrive/Loras/yuki_asayuki101/output" "GDrive16T:/Loras/yuki_asayuki101/output" --ignore-existing --checksum --transfers 16 -v --stats 10s
        .add_local_dir("./notebooks/", 
        remote_path="/root/notebooks/")
    )
)

JUPYTER_TOKEN = "23072007"  # Change me to something non-guessable!




def run_jupyter(port):
        subprocess.run(
            [
                "jupyter",
                "notebook",
                "--no-browser",
                "--allow-root",
                "--ip=0.0.0.0",
                f"--port={port}",
                "--LabApp.allow_origin='*'",
                "--LabApp.allow_remote_access=1",
                "--NotebookApp.allow_origin='https://colab.research.google.com'",
                "--NotebookApp.port_retries=0",
            ],
            env={**os.environ, "JUPYTER_TOKEN": JUPYTER_TOKEN, "SHELL": "/bin/bash"},
            stderr=subprocess.DEVNULL,
        )


@app.function(
    allow_concurrent_inputs=10,
    concurrency_limit=1,
    container_idle_timeout=30,
    timeout=36000,
    gpu="A10G",
)

def tcp_tunnel():
    # This exposes port to public Internet traffic over TCP.
    with modal.forward(9000, unencrypted=True) as tunnel:
        # You can connect to this TCP socket from outside the container, for example, using `nc`:
        #  nc <HOST> <PORT>
        print("TCP tunnel listening at:", tunnel.tcp_socket)
        url = tunnel.url + "/?token=" + JUPYTER_TOKEN
        print(f"Starting Jupyter at {url}")
        run_jupyter(9000)


