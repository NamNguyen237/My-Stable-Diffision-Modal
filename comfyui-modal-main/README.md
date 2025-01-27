## ComfyUI + Flux dev + PULid setup for [modal.com](https://modal.com/) environment

This setup allows to run free image generation environment in [modal.com](https://modal.com/). Best environment for people who has no GPU available.

Modal gives you 30$ for free and you can use it as your ComfyUI experimental environment for any diffusion model.

Default setup includes:
- ComfyUI(installed with [comfy-cli](https://github.com/Comfy-Org/comfy-cli))
- [Flux1.Dev GGUF model](https://huggingface.co/city96/FLUX.1-dev-gguf/blob/main/flux1-dev-Q8_0.gguf) 
- [PuLID-Flux for ComfyUI](https://github.com/balazik/ComfyUI-PuLID-Flux?tab=readme-ov-file)

You can customize it for your needs in file [comfyapp.py](./comfyapp.py
)
### How to run

0) Install python(i hope you have it)

1) Create Account in https://modal.com/


2) Install Modal CLI

```bash
pip install modal
python3 -m modal setup
```
Now you have Modal CLI tool and ready to deploy your setup.

3) Deploy setup into the cloud

To run this setup in live mode run:

```bash
modal serve comfyapp.py
```  

As alternative, you can run app in detached mode:
```bash
modal deploy comfyapp.py
```

After that you can go to [Modal Dashboard](https://modal.com/apps) and get link to your app. 
Now, when you have your environment up and ready, you can try PuLID + Flux Workflow, just drag and drop this image to your ComfyUI environment https://github.com/balazik/ComfyUI-PuLID-Flux/blob/master/examples/pulid_flux_einstein.png

### 