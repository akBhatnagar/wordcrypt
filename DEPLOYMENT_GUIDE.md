# WordCrypt Deployment Guide

## 🌐 Deploying to wordcrypt.co on GoDaddy

### Important Note About GoDaddy
**GoDaddy shared hosting does NOT support Python/Flask applications directly.** You have several options:

---

## Option 1: Use GoDaddy VPS (Recommended)

GoDaddy offers VPS (Virtual Private Server) hosting which gives you full control.

### Requirements
- **GoDaddy VPS** (not shared hosting)
- **Ubuntu/Linux** server
- **Root/SSH access**

### Step-by-Step Deployment

#### 1. Access Your VPS
```bash
ssh root@your-server-ip
```

#### 2. Install Required Software
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx (web server)
sudo apt install nginx -y

# Install Supervisor (process manager)
sudo apt install supervisor -y
```

#### 3. Upload Your Application
```bash
# Create application directory
sudo mkdir -p /var/www/wordcrypt
cd /var/www/wordcrypt

# Upload files (from your local machine)
# Option A: Using scp
scp -r /Users/akshay/Desktop/Projects/wordcrypt/* root@your-server-ip:/var/www/wordcrypt/

# Option B: Using Git
git clone your-repo-url /var/www/wordcrypt
```

#### 4. Set Up Python Environment
```bash
cd /var/www/wordcrypt

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn
```

#### 5. Create Gunicorn Configuration
```bash
sudo nano /etc/supervisor/conf.d/wordcrypt.conf
```

Add this content:
```ini
[program:wordcrypt]
directory=/var/www/wordcrypt
command=/var/www/wordcrypt/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/wordcrypt.err.log
stdout_logfile=/var/log/wordcrypt.out.log
environment=SECRET_KEY="your-secret-key-here",PORT="8000"
```

#### 6. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/wordcrypt
```

Add this content:
```nginx
server {
    listen 80;
    server_name wordcrypt.co www.wordcrypt.co;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/wordcrypt/static;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/wordcrypt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. Start the Application
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start wordcrypt
```

#### 8. Configure SSL (HTTPS) - FREE with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d wordcrypt.co -d www.wordcrypt.co

# Auto-renewal is set up automatically
```

#### 9. Update DNS on GoDaddy
1. Go to GoDaddy DNS Management
2. Add/Update A Records:
   - Type: `A`
   - Name: `@`
   - Value: `your-vps-ip-address`
   - TTL: `600`
3. Add www subdomain:
   - Type: `A`
   - Name: `www`
   - Value: `your-vps-ip-address`
   - TTL: `600`

Wait 10-30 minutes for DNS propagation.

---

## Option 2: Deploy to DigitalOcean (Easier & Recommended)

DigitalOcean is easier and more developer-friendly than GoDaddy VPS.

### Why DigitalOcean?
- ✅ $4-6/month for basic droplet
- ✅ Easy one-click apps
- ✅ Better documentation
- ✅ Simpler interface
- ✅ Free $200 credit for new users

### Quick Deployment
1. Create DigitalOcean account
2. Create a Droplet (Ubuntu 22.04)
3. Choose $4/month plan (enough for this app)
4. Follow steps 2-9 from Option 1 above
5. Point your GoDaddy domain to DigitalOcean IP

### Point Domain to DigitalOcean
1. Get your Droplet IP from DigitalOcean
2. In GoDaddy DNS:
   - Update A record @ → DigitalOcean IP
   - Update A record www → DigitalOcean IP

---

## Option 3: Deploy to Railway/Render (Easiest)

### Railway.app (Recommended for Beginners)
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy from project directory
cd /Users/akshay/Desktop/Projects/wordcrypt
railway init
railway up

# 4. Set environment variables
railway variables set SECRET_KEY=your-secret-key

# 5. Add custom domain (wordcrypt.co)
# Go to Railway dashboard → Settings → Domains → Add Custom Domain
# Then update GoDaddy DNS with Railway's CNAME
```

### Pricing
- **Free tier**: $5 credit/month (enough for this app)
- **Paid**: $5/month for more resources

---

## Option 4: PythonAnywhere (Flask-Specific)

Good for Python/Flask apps specifically.

### Steps
1. Create account at pythonanywhere.com
2. Upload code via Files tab
3. Set up virtual environment
4. Configure WSGI file
5. Point domain in Web tab

### Pricing
- **Free tier**: Limited
- **Hacker plan**: $5/month
- Can use custom domain (wordcrypt.co)

---

## 🔧 Required Files for Deployment

### 1. requirements.txt
Already created:
```
Flask==3.0.0
gunicorn==21.2.0
```

### 2. Procfile (for Railway/Render)
Create this file:
```
web: gunicorn app:app
```

### 3. .env file
Create for environment variables:
```
SECRET_KEY=your-secret-key-here
PORT=8000
FLASK_DEBUG=False
```

### 4. Production Configuration
Update `app.py` line 258:
```python
if __name__ == '__main__':
    load_words()
    
    if DEBUG_MODE:
        print(f"🎮 DEBUG MODE: Today's word is: {get_daily_word()}")
    
    print(f"🚀 Starting server on port {PORT}")
    # Use 0.0.0.0 to accept external connections
    app.run(debug=DEBUG_MODE, port=PORT, host='0.0.0.0')
```

---

## 🎯 Recommended Approach

For **wordcrypt.co**, I recommend:

### Best Option: DigitalOcean Droplet
**Why:**
- Full control
- $6/month (affordable)
- Can host multiple apps
- Easy to scale
- Better than GoDaddy VPS
- Professional setup

### Steps:
1. Keep domain at GoDaddy (you already paid for it)
2. Create DigitalOcean droplet ($6/month)
3. Follow deployment steps above
4. Point GoDaddy DNS to DigitalOcean IP
5. Set up SSL with Let's Encrypt (free)

### Alternative: Railway (Quickest)
**Why:**
- Deploy in 5 minutes
- No server management
- Free to start
- Easy custom domain setup

---

## 📊 Cost Comparison

| Service | Monthly Cost | Difficulty | Best For |
|---------|-------------|------------|----------|
| GoDaddy VPS | $15-30 | Medium | Not recommended |
| DigitalOcean | $4-6 | Medium | Best value |
| Railway | $0-5 | Easy | Quick start |
| PythonAnywhere | $0-5 | Easy | Python apps only |
| Render | $0-7 | Easy | Modern apps |

---

## 🚀 Quick Start (Railway - Recommended)

```bash
# 1. Install Railway
npm install -g @railway/cli

# 2. Login
railway login

# 3. From your project
cd /Users/akshay/Desktop/Projects/wordcrypt

# 4. Create Procfile
echo "web: gunicorn app:app" > Procfile

# 5. Update requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# 6. Deploy
railway init
railway up

# 7. Add domain in Railway dashboard
# Then update GoDaddy DNS:
# CNAME: @ → railway-provided-url
# CNAME: www → railway-provided-url
```

Done! Your site will be live at wordcrypt.co in minutes.

---

## 🔒 Security Checklist

- [ ] Change SECRET_KEY to random string
- [ ] Set FLASK_DEBUG=False in production
- [ ] Enable HTTPS/SSL
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Set up firewall rules
- [ ] Regular backups

---

## 📞 Need Help?

Common issues and solutions:

**DNS not working?**
- Wait 24-48 hours for full propagation
- Clear DNS cache: `sudo systemd-resolve --flush-caches`

**App not starting?**
- Check logs: `sudo supervisorctl tail wordcrypt`
- Test locally first: `python3 app.py`

**502 Bad Gateway?**
- Check if gunicorn is running: `sudo supervisorctl status`
- Restart: `sudo supervisorctl restart wordcrypt`

---

**Choose your deployment method and follow the specific guide above!**
