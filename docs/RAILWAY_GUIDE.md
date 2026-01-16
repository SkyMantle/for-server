# 🚂 Railway Deployment Guide

## Why Railway for Your Drone Geo-Localization App?

✅ **GPU Support** - T4 GPU available (3x faster than CPU)  
✅ **Easy Setup** - Deploy in 5 minutes  
✅ **Affordable** - ~$45/month for GPU usage  
✅ **Auto-deploy** - Push to GitHub = automatic deployment  
✅ **No Docker needed** - Railway handles everything  

---

## Quick Start (5 Minutes)

### Step 1: Prepare Your Repository

Create these files in your project root:

#### `railway.toml`
```toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements_optimized.txt"

[deploy]
startCommand = "python app_optimized.py --server-port $PORT --server-name 0.0.0.0 --share"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

#### `nixpacks.toml`
```toml
[phases.setup]
nixPkgs = ["python310", "gcc", "cudatoolkit"]

[phases.install]
cmds = ["pip install -r requirements_optimized.txt"]

[phases.build]
cmds = []

[start]
cmd = "python app_optimized.py --server-port $PORT --server-name 0.0.0.0"
```

#### `runtime.txt` (optional)
```
python-3.10
```

### Step 2: Update app_optimized.py

Add this at the end of your file:

```python
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False  # Railway provides public URL
    )
```

### Step 3: Deploy to Railway

#### Option A: Using Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g railway

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up

# Enable GPU
railway settings --gpu T4

# Check status
railway status
```

#### Option B: Using Railway Dashboard (Easier)

1. **Visit** https://railway.app
2. **Sign up** with GitHub
3. **Create New Project** → Deploy from GitHub repo
4. **Select your repository**
5. **Configure Environment**:
   - Click on your service
   - Go to Settings → Environment
   - Add GPU → Select T4
   - Set Memory: 8GB
6. **Deploy** - Railway auto-deploys!

### Step 4: Configure GPU

In Railway dashboard:
1. Select your service
2. Settings → Resources
3. Enable GPU → T4 ($0.50/hour when active)
4. Set Memory: 8GB RAM
5. Save

### Step 5: Set Environment Variables

```bash
# Optional optimizations
PORT=7860
PYTHONUNBUFFERED=1
GRADIO_SERVER_NAME=0.0.0.0
```

---

## Configuration Files Explained

### railway.toml
Tells Railway how to build and run your app.

### nixpacks.toml
Specifies system dependencies (CUDA toolkit for GPU).

### requirements_optimized.txt
Python packages (already have this).

---

## Cost Breakdown

### Railway Pricing

**Starter Plan** (Hobby):
- $5/month for 500 hours compute
- $0.50/hour GPU usage
- 8GB RAM included

**Pro Plan**:
- $20/month
- Additional resources as needed
- Priority support

### Example Monthly Cost

**Scenario 1: Light usage** (10 hours GPU/month)
```
Base: $5/month
GPU: 10 hours × $0.50 = $5
Total: $10/month
```

**Scenario 2: Medium usage** (50 hours GPU/month)
```
Base: $20/month (upgrade to Pro)
GPU: 50 hours × $0.50 = $25
Total: $45/month
```

**Scenario 3: Heavy usage** (100 hours GPU/month)
```
Base: $20/month
GPU: 100 hours × $0.50 = $50
Total: $70/month
```

---

## Performance Expectations

### With T4 GPU on Railway:

| Grid Size | Processing Time | Estimated Cost/Search |
|-----------|----------------|----------------------|
| 5×5 | ~10-12s | $0.0017 |
| 7×7 | ~18-22s | $0.0031 |
| 10×10 | ~30-35s | $0.0049 |
| 15×15 | ~90-100s | $0.0139 |

### Concurrent Users:
- T4 GPU: 5-10 concurrent searches
- Auto-scales based on load

---

## Monitoring & Logs

### View Logs
```bash
# Using CLI
railway logs

# Or in dashboard: Service → Deployments → View Logs
```

### Monitor GPU Usage
1. Dashboard → Service → Metrics
2. Check GPU utilization
3. Monitor memory usage

### Set Up Alerts
1. Settings → Notifications
2. Configure email/Discord alerts
3. Set thresholds (e.g., >90% memory)

---

## Optimization Tips for Railway

### 1. Efficient Startup
```python
# Add health check endpoint
@app.route('/health')
def health():
    return {'status': 'healthy', 'gpu': torch.cuda.is_available()}
```

### 2. Caching Strategy
```python
# Railway has ephemeral storage
# Consider using Redis for caching satellite tiles
import redis

cache = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=6379
)
```

### 3. Auto-Sleep Configuration
```toml
# In railway.toml
[deploy]
sleepAfterMinutes = 60  # Sleep after 1 hour idle
```

### 4. Environment-Specific Settings
```python
import os

ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    # Production optimizations
    ENABLE_ANALYTICS = True
    DEBUG = False
else:
    DEBUG = True
```

---

## Troubleshooting

### Issue: GPU Not Detected

**Solution:**
```bash
# Check GPU status
railway run python -c "import torch; print(torch.cuda.is_available())"

# Ensure GPU is enabled in dashboard
# Settings → Resources → GPU → T4
```

### Issue: Out of Memory

**Solution:**
1. Increase memory allocation (8GB → 16GB)
2. Reduce batch size in code
3. Use Basic or Fast algorithm

### Issue: Cold Start Delays

**Solution:**
```toml
# Keep instance warm
[deploy]
sleepAfterMinutes = 1440  # 24 hours
```

### Issue: Slow Builds

**Solution:**
```toml
# Cache dependencies
[build]
cache = true
```

---

## Comparison: Railway vs Alternatives

| Feature | Railway | Hugging Face | GCP | AWS |
|---------|---------|--------------|-----|-----|
| **Setup Time** | 5 min | 2 min | 30 min | 45 min |
| **GPU Access** | ✅ T4 | ❌ Free tier | ✅ T4/V100/A100 | ✅ T4/A10G |
| **Cost (50h GPU)** | $45 | $50+ | $35-100 | $40-120 |
| **Auto-scaling** | ✅ | ❌ | ✅ | ✅ |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Monitoring** | ✅ Good | ❌ Basic | ✅ Excellent | ✅ Excellent |

---

## Advanced: Add Redis for Caching

### Step 1: Add Redis Plugin
```bash
railway plugin add redis
```

### Step 2: Update Code
```python
import redis
import os
import pickle

redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=6379,
    db=0
)

def get_cached_tile(lat, lon):
    key = f"tile:{lat}:{lon}"
    cached = redis_client.get(key)
    if cached:
        return pickle.loads(cached)
    return None

def cache_tile(lat, lon, image):
    key = f"tile:{lat}:{lon}"
    redis_client.setex(key, 3600, pickle.dumps(image))  # 1 hour TTL
```

### Step 3: Update requirements
```txt
# Add to requirements_optimized.txt
redis==5.0.0
```

**Benefit**: Share cache across instances, persist between deployments

---

## Migration Checklist

- [ ] Create railway.toml
- [ ] Create nixpacks.toml  
- [ ] Update app_optimized.py with port handling
- [ ] Push to GitHub
- [ ] Sign up for Railway
- [ ] Connect GitHub repository
- [ ] Enable T4 GPU
- [ ] Set memory to 8GB
- [ ] Deploy and test
- [ ] Monitor GPU usage
- [ ] Set up alerts (optional)
- [ ] Add Redis caching (optional)

---

## Cost Optimization Tips

### 1. Sleep When Idle
```toml
[deploy]
sleepAfterMinutes = 30  # Sleep after 30 min idle
```
Saves money when no one is using the app.

### 2. Use CPU for Light Loads
```python
# Auto-switch based on queue
if queue_length < 3:
    device = 'cpu'  # Use CPU for single requests
else:
    device = 'cuda'  # Use GPU for batches
```

### 3. Batch Requests
```python
# Process multiple requests together
@app.route('/batch', methods=['POST'])
def batch_process():
    requests = get_pending_requests()
    if len(requests) >= 5:
        # Process batch on GPU
        return process_batch_gpu(requests)
```

### 4. Monitor and Optimize
- Check Railway dashboard weekly
- Look for usage patterns
- Adjust sleep times accordingly

---

## Support & Resources

### Railway Documentation
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- GitHub: https://github.com/railwayapp

### Getting Help
1. Check Railway Discord #help channel
2. Railway GitHub Discussions
3. Railway documentation
4. Community forum

---

## Production Checklist

Before going live:

- [ ] Enable GPU (T4)
- [ ] Set memory to 8GB+
- [ ] Configure environment variables
- [ ] Set up monitoring/alerts
- [ ] Test with concurrent users
- [ ] Configure custom domain (optional)
- [ ] Set up CI/CD (auto-deploy on push)
- [ ] Add health check endpoint
- [ ] Implement error tracking (Sentry)
- [ ] Add analytics (optional)
- [ ] Document API endpoints
- [ ] Set up backup/recovery

---

## Next Steps After Deployment

1. **Test the deployment**
   ```bash
   curl https://your-app.railway.app/health
   ```

2. **Monitor GPU usage** for first week

3. **Optimize based on metrics**

4. **Consider adding**:
   - Redis caching
   - Rate limiting
   - User authentication
   - API keys

5. **Scale as needed**:
   - Add more memory
   - Upgrade GPU (if needed)
   - Multiple instances (Pro plan)

---

## FAQ

**Q: Can I use free tier?**
A: Railway has a trial with $5 credit. Need paid plan for GPU.

**Q: How do I update my app?**
A: Just push to GitHub. Railway auto-deploys!

**Q: Can I use V100 or A100?**
A: Currently Railway offers T4. For other GPUs, use GCP/AWS.

**Q: What if I exceed budget?**
A: Set spending limits in Railway dashboard.

**Q: Can I preview before deploying?**
A: Yes, Railway creates preview environments for PRs.

**Q: How do I rollback?**
A: Dashboard → Deployments → Select previous deployment → Rollback

---

## Conclusion

Railway is the **sweet spot** for your drone geo-localization app:

✅ **Easy setup** - 5 minutes from zero to production  
✅ **GPU support** - T4 available, 3x faster than CPU  
✅ **Affordable** - ~$45/month for moderate usage  
✅ **Auto-scaling** - Handles traffic spikes  
✅ **Great DX** - Git push to deploy  

**Ready to deploy? Follow the Quick Start guide above!** 🚀

