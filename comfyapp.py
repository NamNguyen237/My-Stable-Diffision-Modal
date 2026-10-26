import subprocess
import modal

# ==============================================================================
# 1. KHỞI TẠO DOCKER IMAGE CHO MODAL (CẤU HÌNH MÔI TRƯỜNG BASE)
# ==============================================================================
image = (  # Xây dựng Modal Image để chạy ComfyUI theo từng bước
    modal.Image.debian_slim(  # Bắt đầu từ hệ điều hành Linux cơ bản với Python 3.11
        python_version="3.11"
    )
    .apt_install("git")  # Cài đặt Git để clone ComfyUI và các Custom Nodes
    .apt_install("nano")  # Cài trình chỉnh sửa văn bản nano nhẹ
    .apt_install("libgl1-mesa-glx")  # Thư viện OpenGL cần thiết để chạy ComfyUI & xử lý ảnh
    .apt_install("libglib2.0-0")  # Thư viện hệ thống hỗ trợ OpenCV / ComfyUI
    .run_commands("apt update & apt upgrade -y & apt autoremove -y")
    .pip_install_from_requirements(
        "requirements.txt"  # Cài các thư viện Python từ file requirements.txt cục bộ
    )
    .run_commands(
        "comfy --skip-prompt install --nvidia"  # Tự động cài đặt ComfyUI hỗ trợ GPU NVIDIA
    )
)

# ==============================================================================
# 2. KHU VỰC CÀI ĐẶT CUSTOM NODES (GỒM CÁC NODE CŨ CỦA BẠN + NODE NSFW MỚI)
# ==============================================================================

image = (
    # --- CÁC NODE CŨ TRONG SCRIPT BÀI GỐC CỦA BẠN ---
    image.run_commands(
        "comfy node install image-resize-comfyui"  # Node thay đổi kích thước ảnh
    )
    .run_commands(
        "comfy node install efficiency-nodes-comfyui"  # Bộ node gom nhóm giúp workflow gọn gàng
    )
    .run_commands(
        "comfy node install https://github.com/JuniorDevNam/Lora-Training-in-Comfy.git"  # Train LoRA
    )
    .run_commands(
        "comfy node install https://github.com/JuniorDevNam/Image-Captioning-in-ComfyUI.git"  # Gán nhãn ảnh
    )
    .run_commands(
        "comfy node install https://github.com/pythongosssss/ComfyUI-WD14-Tagger.git"  # Auto tagger WD14
    )
    .run_commands(
        "comfy node install https://github.com/alexopus/ComfyUI-Image-Saver.git"  # Lưu ảnh nâng cao
    )
    .run_commands(
        "comfy node install https://github.com/jtydhr88/ComfyUI-HY-Motion1"  # Motion video
    )

    # ==========================================================================
    # --- BỔ SUNG CÁC NODE CHUYÊN DỤNG CHO AI NSFW & CHỈNH SỬA CHI TIẾT ---
    # ==========================================================================
    .run_commands(
        # BẮT BUỘC: Chứa node FaceDetailer & PersonMaskGenerator.
        # Giúp tự động nhận diện khuôn mặt/cơ thể bị méo khi vẽ ảnh toàn thân và vẽ lại nét căng.
        "comfy node install ComfyUI-Impact-Pack"
    )
    .run_commands(
        # Tối ưu hóa việc nhập và mã hóa Prompt cho các model NSFW (như Pony V6 / SDXL).
        "comfy node install ComfyUI-Advanced-CLIP-Text-Encode"
    )
    .run_commands(
        # Bổ sung các công cụ chỉnh sửa UI, quản lý lịch sử và tiện ích bổ trợ cho ComfyUI.
        "comfy node install ComfyUI-Custom-Scripts"
    )
    .run_commands(
        # Bộ công cụ ControlNet auxiliary (OpenPose, Depth, Canny) dùng để giữ tư thế nhân vật NSFW.
        "comfy node install ComfyUI_ControlNet_Aux"
    )
)

# --- CÁC ĐOẠN ĐÃ DISABLED ĐỂ DÙNG VOLUME (GIỮ NGUYÊN COMMENT CỦA BẠN) ---
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

# Thêm file extra_model_paths.yaml để ComfyUI nhận diện đường dẫn các Volume bên dưới
image = image.add_local_file(
    "extra_model_paths.yaml",
    remote_path="/root/comfy/ComfyUI/extra_model_paths.yaml"
)

# ==============================================================================
# 3. KHỞI TẠO APP VÀ KHAI BÁO VOLUMES (LƯU TRỮ VĨNH VIỄN MODEL)
# ==============================================================================
app = modal.App(name="nam-dev-comfyui", image=image)

# Khai báo các Volume lưu trữ (Tự động tạo mới nếu chưa có)
vol_checkpoints = modal.Volume.from_name("comfy_checkpoints", create_if_missing=True)
vol_loras = modal.Volume.from_name("comfy_loras", create_if_missing=True)
vol_controlnet = modal.Volume.from_name("comfy_controlnet", create_if_missing=True)
vol_custom_nodes = modal.Volume.from_name("comfy_custom_nodes", create_if_missing=True)
vol_vae = modal.Volume.from_name("comfy_vae", create_if_missing=True)  # Thêm Volume chứa file VAE chống nhạt màu


# ==============================================================================
# 4. SERVER CONTAINER CHÍNH: KHỞI CHẠY COMFYUI WEBUI VỚI GPU A10G
# ==============================================================================
@app.function(
    max_containers=1,
    scaledown_window=3600,  # Giữ container sống 1 tiếng sau khi hết request để tránh Cold Start
    timeout=18000,          # Timeout tối đa 5 tiếng cho mỗi session
    gpu="A10G",             # Sử dụng GPU A10G (24GB VRAM) gánh mượt SDXL/Pony/Video AI
    volumes={
        "/root/vol_models/checkpoints": vol_checkpoints,
        "/root/vol_models/loras": vol_loras,
        "/root/vol_models/controlnet": vol_controlnet,
        "/root/vol_models/custom_nodes": vol_custom_nodes,  # Optional nếu bạn dùng volume cho custom nodes
        "/root/vol_models/vae": vol_vae,                   # Mount thêm thư mục VAE
    }
)
@modal.concurrent(max_inputs=10)  # Cho phép xử lý đồng thời tối đa 10 request
@modal.web_server(8000, startup_timeout=60)
def webui():
    # Khởi chạy ComfyUI ngầm ở cổng 8000 và lắng nghe trên tất cả địa chỉ IP (0.0.0.0)
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)