# 🛸 Drone Geo-Localization - Deployment Package

Complete package for deploying on local web server.

## 🚀 Quick Start

### Windows
```cmd
start.bat
```

### Linux/Mac
```bash
./start.sh
```

Then open: http://localhost:7860

## 📦 What's Included

```
drone-localization-deployment/
├── app.py                      # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── setup.py                    # Interactive setup
├── start.bat                   # Windows startup script
├── start.sh                    # Linux/Mac startup script
├── install.sh                  # Installation script
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose
├── DOCKER.md                   # Docker guide
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── configs/
│   ├── nginx.conf              # Nginx reverse proxy
│   └── drone-localization.service  # systemd service
├── scripts/
│   ├── check_system.py         # System checker
│   ├── backup.sh               # Backup utility
│   └── monitor.py              # Monitoring tool
└── docs/
    ├── FREE_HOSTING_GUIDE.md   # Free hosting options
    ├── OPTIMIZATION_REPORT.md  # Performance details
    ├── HOSTING_COMPARISON.md   # Platform comparison
    ├── RAILWAY_GUIDE.md        # Railway deployment
    └── README_OPTIMIZED.md     # Optimization info
```

## 📋 Installation Methods

### Method 1: Simple (Recommended)
```bash
# Linux/Mac
./install.sh
./start.sh

# Windows
# Double-click start.bat
```

### Method 2: Manual
```bash
pip install -r requirements.txt
python app.py
```

### Method 3: Docker
```bash
docker-compose up -d
```

### Method 4: System Service (Linux)
```bash
# Edit configs/drone-localization.service
sudo cp configs/drone-localization.service /etc/systemd/system/
sudo systemctl enable drone-localization
sudo systemctl start drone-localization
```

## 🌐 Deployment Options

### Local Access Only
```bash
python app.py
# Access: http://localhost:7860
```

### Network Access (LAN)
```bash
python app.py --server-name 0.0.0.0
# Access from any device: http://YOUR_IP:7860
```

### Public Access (with Cloudflare)
```bash
# Terminal 1
python app.py

# Terminal 2
cloudflared tunnel --url http://localhost:7860
# You get: https://xyz.trycloudflare.com
```

### Behind Nginx
```bash
# Setup nginx
sudo cp configs/nginx.conf /etc/nginx/sites-available/drone-localization
sudo ln -s /etc/nginx/sites-available/drone-localization /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Access: http://your-domain.com
```

## 🔧 System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 2-core CPU

**Recommended:**
- Python 3.10+
- 8GB RAM
- 4-core CPU
- NVIDIA GPU with 4GB VRAM

**Optimal:**
- Python 3.11+
- 16GB RAM
- 8-core CPU
- NVIDIA GPU with 8GB VRAM

## ⚡ Performance

| Hardware | 5×5 Grid | 10×10 Grid |
|----------|----------|------------|
| CPU only | 30-40s | 120-150s |
| GTX 1660 | 12-15s | 40-50s |
| RTX 3060 | 8-10s | 25-30s |
| RTX 4090 | 5-7s | 15-20s |

## 🔒 Security

### Add Authentication
Edit `app.py`:
```python
demo.launch(
    auth=("username", "password")
)
```

### Or use .env
```bash
cp .env.example .env
# Edit .env with your credentials
```

## 📊 Monitoring

### Check Status
```bash
# If running as service
sudo systemctl status drone-localization

# If running in terminal
# Look for "Running on http://..."
```

### View Logs
```bash
# Service logs
sudo journalctl -u drone-localization -f

# Docker logs
docker logs -f drone-localization

# Application logs
tail -f logs/app.log
```

### Monitor Resources
```bash
python scripts/monitor.py
```

## 🔄 Updates

### Update Application
```bash
git pull  # If using git
# Or replace app.py with new version
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Restart Service
```bash
# systemd
sudo systemctl restart drone-localization

# Docker
docker-compose restart

# Manual
# Press Ctrl+C and run start script again
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 7860
sudo lsof -i :7860

# Use different port
python app.py --server-port 8080
```

### GPU Not Detected
```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Install drivers
# NVIDIA: https://developer.nvidia.com/cuda-downloads
```

### Out of Memory
- Reduce grid size (5×5 instead of 10×10)
- Use "Basic" algorithm
- Close other applications
- Check system resources: `python scripts/check_system.py`

### Slow Performance
- Enable GPU (check above)
- Use faster algorithm (Basic/Fast)
- Reduce grid size
- Check network speed for satellite downloads

## 📚 Documentation

- `docs/FREE_HOSTING_GUIDE.md` - Free deployment options
- `docs/OPTIMIZATION_REPORT.md` - Performance optimizations
- `docs/HOSTING_COMPARISON.md` - Platform comparison
- `docs/RAILWAY_GUIDE.md` - Railway deployment
- `DOCKER.md` - Docker deployment guide

## 💡 Tips

1. **For personal use**: Just run `./start.sh`
2. **For team use**: Run with `--server-name 0.0.0.0`
3. **For public use**: Use Cloudflare Tunnel
4. **For production**: Use Docker or systemd service
5. **Behind firewall**: Use nginx reverse proxy

## 🆘 Support

Check the documentation in `docs/` folder or run:
```bash
python setup.py  # Interactive setup and diagnostics
```

## 📝 License

Same as original project.

---

**Ready to deploy!** 🚀

For detailed guides, check the `docs/` folder.
