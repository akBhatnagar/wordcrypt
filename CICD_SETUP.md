# CI/CD Setup Guide

This guide will help you set up automatic deployment from GitHub to your DigitalOcean droplet.

## Prerequisites

1. GitHub repository set up (wordcrypt)
2. DigitalOcean droplet with SSH access
3. Application deployed and working on the droplet

## Setup Steps

### 1. Prepare Your DigitalOcean Droplet

First, SSH into your droplet and set up Git on the server:

```bash
ssh root@wordcrypt.in

# Find your app directory (likely one of these)
cd /var/www/wordcrypt  # or /root/wordcrypt or ~/wordcrypt

# Initialize git repository if not already done
git init
git remote add origin https://github.com/akBhatnagar/wordcrypt.git
git fetch origin
git checkout -b main
git branch --set-upstream-to=origin/main main
git pull

# Ensure the correct permissions
chown -R www-data:www-data /var/www/wordcrypt  # adjust path as needed
```

### 2. Generate SSH Key for GitHub Actions

On your **local machine**, generate a new SSH key pair:

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/wordcrypt_deploy
```

This creates two files:
- `~/.ssh/wordcrypt_deploy` (private key)
- `~/.ssh/wordcrypt_deploy.pub` (public key)

### 3. Add Public Key to DigitalOcean Droplet

Copy the public key to your droplet:

```bash
ssh-copy-id -i ~/.ssh/wordcrypt_deploy.pub root@wordcrypt.in
```

Or manually:

```bash
# Copy the public key content
cat ~/.ssh/wordcrypt_deploy.pub

# SSH into droplet and add it
ssh root@wordcrypt.in
echo "PASTE_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 4. Add Secrets to GitHub

Go to your GitHub repository: https://github.com/akBhatnagar/wordcrypt

1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these three secrets:

#### Secret 1: DO_HOST
- Name: `DO_HOST`
- Value: `wordcrypt.in` (or your droplet IP: `206.189.129.16`)

#### Secret 2: DO_USERNAME
- Name: `DO_USERNAME`
- Value: `root` (or your droplet username)

#### Secret 3: DO_SSH_KEY
- Name: `DO_SSH_KEY`
- Value: Copy the **entire private key** content:

```bash
cat ~/.ssh/wordcrypt_deploy
```

Copy everything including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`

### 5. Update Deployment Script (if needed)

The workflow file (`.github/workflows/deploy.yml`) may need adjustment based on your server setup:

**Find your app directory:**
```bash
ssh root@wordcrypt.in "find / -name 'app.py' 2>/dev/null | grep wordcrypt"
```

**Check your process manager:**
```bash
# Check if using systemd
sudo systemctl status wordcrypt

# Or supervisor
sudo supervisorctl status

# Or gunicorn directly
ps aux | grep gunicorn
```

Update the workflow script accordingly.

### 6. Test the Setup

1. Commit and push the workflow file:

```bash
cd /Users/akshay/Desktop/Projects/wordcrypt
git add .github/workflows/deploy.yml CICD_SETUP.md
git commit -m "Add CI/CD workflow for automatic deployment"
git push origin main
```

2. Go to GitHub → **Actions** tab
3. You should see the workflow running
4. Click on it to see the deployment logs

### 7. Troubleshooting

**If deployment fails:**

1. **Check GitHub Actions logs** for error messages
2. **Verify SSH access** from GitHub:
   ```bash
   ssh -i ~/.ssh/wordcrypt_deploy root@wordcrypt.in
   ```
3. **Check app directory** exists and has git initialized
4. **Verify service name** matches your actual service:
   ```bash
   sudo systemctl list-units --type=service | grep word
   ```

**Common fixes:**

```bash
# If git pull fails, you might need to configure git on the server
ssh root@wordcrypt.in
git config --global user.email "akshaybhatnagar1998@gmail.com"
git config --global user.name "Akshay Bhatnagar"

# If permission issues
cd /var/www/wordcrypt  # or your app directory
sudo chown -R $USER:$USER .
```

## How It Works

Once set up, every time you push to the `main` branch:

1. GitHub Actions triggers automatically
2. Connects to your DigitalOcean droplet via SSH
3. Pulls the latest code from GitHub
4. Installs any new dependencies
5. Restarts the application
6. Your site is live with the latest changes!

## Security Notes

- Never commit the private SSH key to your repository
- Keep your GitHub secrets secure
- Consider using a dedicated deploy user instead of root
- Regularly rotate your SSH keys

## Next Steps

After successful setup, your workflow is:

```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Automatic deployment happens!
# Check https://wordcrypt.in in ~30 seconds
```

Enjoy your automated deployments! 🚀
