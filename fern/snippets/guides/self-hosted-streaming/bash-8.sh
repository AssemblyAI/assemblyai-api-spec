# Verify NVIDIA drivers
nvidia-smi

# Verify Docker
docker --version

# Verify Docker Compose (v2 syntax)
docker compose version

# If the above fails, you may need to install Docker Compose v2
# Remove old version if present
sudo apt-get remove docker-compose

# Install Docker Compose v2 (plugin)
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Verify installation
docker compose version

# Verify GPU access in Docker
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
