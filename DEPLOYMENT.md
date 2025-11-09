# Streamlit Cloud Deployment Guide

Follow these steps to deploy your Political News Sentiment Analysis app on Streamlit Cloud:

## Prerequisites

1. **GitHub Account**: You'll need a GitHub account
2. **News API Key**: Get your free key from https://newsapi.org

## Step-by-Step Deployment

### 1. Create a GitHub Repository

1. Go to https://github.com and login
2. Click the **"+"** button (top right) → **"New repository"**
3. Name your repository (e.g., `political-news-sentiment`)
4. Choose **Public** or **Private**
5. Don't initialize with README (we already have one)
6. Click **"Create repository"**

### 2. Push Your Code to GitHub

Open PowerShell in your project folder and run:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Political News Sentiment Analysis App"

# Add your GitHub repository as remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your GitHub username and `YOUR_REPO` with your repository name.

### 3. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click **"New app"** or **"Deploy an app"**
3. Connect your GitHub account (if not already connected)
4. Select your repository
5. Set the following:
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (optional)

### 4. Configure Secrets

1. In the Streamlit Cloud dashboard, click on your app
2. Click **"Settings"** → **"Secrets"**
3. Add your News API key in TOML format:

```toml
NEWS_API_KEY = "your_actual_api_key_here"
```

4. Click **"Save"**

### 5. Deploy!

1. Click **"Deploy"** button
2. Wait for deployment (usually 2-3 minutes)
3. Your app will be live at: `https://your-app-name.streamlit.app`

## Troubleshooting

### If deployment fails:

1. **Check the logs** in Streamlit Cloud dashboard
2. **Verify requirements.txt** has all dependencies
3. **Check Python version compatibility** (Streamlit Cloud uses Python 3.9+)
4. **Ensure all imports are correct**

### Common Issues:

**Issue**: ModuleNotFoundError
- **Solution**: Add missing package to `requirements.txt`

**Issue**: API Key not working
- **Solution**: Check the secret name matches exactly: `NEWS_API_KEY`

**Issue**: App crashes on startup
- **Solution**: Check logs for specific error messages

## Updating Your App

After making changes locally:

```powershell
git add .
git commit -m "Description of your changes"
git push
```

Streamlit Cloud will automatically redeploy your app!

## Managing Users

- Default admin credentials work on cloud
- User data is stored in `users_data.json`
- **Note**: This file won't persist across deployments
- For production, consider using a proper database (PostgreSQL, MongoDB, etc.)

## Security Recommendations

1. **Never commit API keys** to GitHub
2. **Use Streamlit secrets** for sensitive data
3. **Change default admin password** after deployment
4. **Enable 2FA** on your GitHub account

## App URL

After deployment, your app will be accessible at:
`https://[your-app-name].streamlit.app`

Share this URL with anyone you want to access your app!

## Need Help?

- Streamlit Documentation: https://docs.streamlit.io/
- Streamlit Community Forum: https://discuss.streamlit.io/
- GitHub Issues: Create an issue in your repository

---

**Happy Deploying! 🚀**
