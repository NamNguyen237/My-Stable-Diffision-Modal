import socket
import threading
import os
import secrets
import subprocess
import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
         "jupyter", 
         "jupyterlab", 
         "jupyter_http_over_ws", 
         "toml", 
         "requests==2.32.3", 
         "PySocks==1.7.1"
         )
    .apt_install(
         "curl", 
         "unzip", 
         "fuse3", 
         "git-all", 
         "aria2"
         )
    .run_commands("curl -fsSL https://tailscale.com/install.sh | sh")
    .add_local_file("./entrypoint.sh", "/root/entrypoint.sh", copy=True)
    .dockerfile_commands(
        "RUN chmod a+x /root/entrypoint.sh",
        'ENTRYPOINT ["/root/entrypoint.sh"]',
    )
    .run_commands("echo 'net.ipv4.ip_forward = 1' | tee -a /etc/sysctl.conf")
    .run_commands("echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.conf")
    .run_commands("sysctl -p /etc/sysctl.conf")
    
)
app = modal.App(image=image)
with image.imports():
    import socks
    socks.set_default_proxy(socks.SOCKS5, "0.0.0.0", 1080)
    socket.socket = socks.socksocket
JUPYTER_TOKEN = "23072007" 
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
    secrets=[
        modal.Secret.from_name(
            "tailscale-auth", required_keys=["TAILSCALE_AUTHKEY"]#["tskey-auth-kwGLkdfq1221CNTRL-ZE9QXA7BG5FNxw2PA3NG6Fajdbaconfs"]
        ),
        modal.Secret.from_dict(
            {
                "ALL_PROXY": "socks5://localhost:1080/",
                "HTTP_PROXY": "http://localhost:1080/",
                "http_proxy": "http://localhost:1080/",
            }
        ),
    ],
)

#tailscale serve --tcp 9000 tcp://localhost:9000

def tcp_tunnel():
    # This exposes port to public Internet traffic over TCP.
    with modal.forward(9000, unencrypted=True) as tunnel:
        # You can connect to this TCP socket from outside the container, for example, using `nc`:
        #  nc <HOST> <PORT>
        print("TCP tunnel listening at:", tunnel.tcp_socket)
        url = tunnel.url + "/?token=" + JUPYTER_TOKEN
        print(f"Starting Jupyter at {url}")
        run_jupyter(9000)

