#!/usr/bin/env python3
"""
Local Deployment Quick Start Script
Helps you run the drone localization app on your laptop
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Need 3.8+")
        return False

def check_gpu():
    """Check if GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU Detected: {gpu_name}")
            print(f"   CUDA Version: {torch.version.cuda}")
            return True
        else:
            print("⚠️  No GPU detected - will use CPU (slower)")
            print("   To install CUDA: https://developer.nvidia.com/cuda-downloads")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'gradio',
        'torch',
        'torchvision',
        'PIL',
        'numpy',
        'requests',
        'plotly',
        'scipy'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    return len(missing) == 0, missing

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements_optimized.txt"
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def get_local_ip():
    """Get local IP address"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to detect"

def print_access_info(port=7860):
    """Print access information"""
    local_ip = get_local_ip()
    
    print_header("🎉 App Started Successfully!")
    
    print("📍 Access URLs:")
    print(f"   Local:           http://localhost:{port}")
    print(f"   Local Network:   http://{local_ip}:{port}")
    print()
    print("💡 Tips:")
    print("   - Press Ctrl+C to stop")
    print("   - Share with devices on same WiFi using Local Network URL")
    print("   - For public access, see FREE_HOSTING_GUIDE.md")
    print()

def print_cloudflare_setup():
    """Print Cloudflare Tunnel setup instructions"""
    print_header("🌐 Make Your App Publicly Accessible (FREE)")
    
    print("Option 1: Cloudflare Tunnel (Recommended)")
    print("-" * 60)
    print("1. Download cloudflared:")
    
    os_type = platform.system()
    if os_type == "Windows":
        print("   winget install --id Cloudflare.cloudflared")
    elif os_type == "Darwin":
        print("   brew install cloudflared")
    else:
        print("   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb")
        print("   sudo dpkg -i cloudflared-linux-amd64.deb")
    
    print("\n2. Create tunnel:")
    print("   cloudflared tunnel --url http://localhost:7860")
    print("\n   You'll get a public URL like: https://xyz.trycloudflare.com")
    print()
    
    print("Option 2: ngrok (Alternative)")
    print("-" * 60)
    print("1. Download ngrok: https://ngrok.com/download")
    print("2. Run: ngrok http 7860")
    print("3. Get public URL from terminal output")
    print()

def setup_autostart():
    """Provide instructions for auto-start on boot"""
    print_header("🔄 Auto-Start on Boot (Optional)")
    
    os_type = platform.system()
    
    if os_type == "Windows":
        print("Windows Task Scheduler:")
        print("1. Open Task Scheduler")
        print("2. Create Basic Task")
        print("3. Trigger: At startup")
        print("4. Action: Start a program")
        print(f"5. Program: {sys.executable}")
        print(f"6. Arguments: {os.path.abspath('app_optimized.py')}")
        
    elif os_type == "Darwin":
        print("Mac LaunchAgent:")
        print("1. Create file: ~/Library/LaunchAgents/com.dronelocalization.plist")
        print("2. Add configuration (see FREE_HOSTING_GUIDE.md)")
        print("3. Run: launchctl load ~/Library/LaunchAgents/com.dronelocalization.plist")
        
    else:
        print("Linux systemd:")
        print("1. Create file: /etc/systemd/system/drone-localization.service")
        print("2. Add configuration (see FREE_HOSTING_GUIDE.md)")
        print("3. Run: sudo systemctl enable drone-localization")
        print("4. Run: sudo systemctl start drone-localization")
    
    print()

def main():
    """Main setup function"""
    print_header("🛸 Drone Geo-Localization - Local Setup")
    
    # Check Python version
    print("Checking system requirements...\n")
    if not check_python():
        print("\n❌ Please upgrade Python to 3.8 or higher")
        return
    
    # Check dependencies
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print(f"\n📦 Missing packages: {', '.join(missing)}")
        response = input("\nInstall missing dependencies? (y/n): ").lower()
        if response == 'y':
            if not install_dependencies():
                print("\n❌ Setup failed. Please install manually:")
                print("   pip install -r requirements_optimized.txt")
                return
        else:
            print("\n❌ Cannot proceed without dependencies")
            return
    
    # Check GPU
    print()
    has_gpu = check_gpu()
    
    # Print success message
    print_header("✅ System Ready!")
    
    if has_gpu:
        print("🚀 Your system has GPU support!")
        print("   Expected performance: ~10-12s for 5×5 grid")
    else:
        print("💻 Running on CPU")
        print("   Expected performance: ~30-40s for 5×5 grid")
        print("   Tip: Install CUDA for 3-5x speedup")
    
    print()
    
    # Ask if user wants to start now
    response = input("Start the app now? (y/n): ").lower()
    
    if response == 'y':
        print_access_info()
        
        # Show how to make it public
        public = input("\nWant to make it publicly accessible? (y/n): ").lower()
        if public == 'y':
            print_cloudflare_setup()
        
        # Show auto-start
        autostart = input("\nWant to set up auto-start on boot? (y/n): ").lower()
        if autostart == 'y':
            setup_autostart()
        
        print("\n🚀 Starting application...")
        print("   (Press Ctrl+C to stop)\n")
        
        try:
            # Start the app
            subprocess.run([sys.executable, "app_optimized.py"])
        except KeyboardInterrupt:
            print("\n\n👋 App stopped. Thanks for using Drone Geo-Localization!")
    else:
        print("\n📚 To start manually:")
        print("   python app_optimized.py")
        print()
        print("📖 For more options, see FREE_HOSTING_GUIDE.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFor help, see FREE_HOSTING_GUIDE.md")
