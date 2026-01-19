# Docker Deployment

## Quick Start

### Build and Run
```bash
docker-compose up -d
```

Access at: http://localhost:7860

### View Logs
```bash
docker-compose logs -f
```

### Stop
```bash
docker-compose down
```

## GPU Support

Requires nvidia-docker:
```bash
# Install nvidia-docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### Test GPU
```bash
docker run --rm --gpus all pytorch/pytorch:2.0.1-cuda11.8-cudnn8-runtime nvidia-smi
```

## Production Deployment

1. Build optimized image:
```bash
docker build -t drone-localization:latest .
```

2. Run with resource limits:
```bash
docker run -d \
  --name drone-localization \
  --gpus all \
  -p 7860:7860 \
  --memory=8g \
  --cpus=4 \
  --restart=unless-stopped \
  drone-localization:latest
```

## Troubleshooting

### Container won't start
```bash
docker logs drone-localization
```

### No GPU detected
```bash
docker exec drone-localization python -c "import torch; print(torch.cuda.is_available())"
```
