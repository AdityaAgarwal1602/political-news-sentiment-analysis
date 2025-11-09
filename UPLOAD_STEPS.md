# 📤 Step-by-Step Upload Guide to GitHub & Streamlit Cloud

## ✅ Your API Key is Now Secure!
Your API key has been removed from all public files and is only in:
- `.streamlit/secrets.toml` (won't be uploaded - it's in .gitignore)

---

## 🚀 Step 1: Upload to GitHub

### A. Create GitHub Repository
1. Go to **https://github.com**
2. Click the **"+"** button (top right corner)
3. Select **"New repository"**
4. Fill in:
   - **Repository name**: `political-news-sentiment` (or any name you like)
   - **Description**: "Political News Sentiment Analysis App"
   - **Visibility**: Choose **Public** (required for free Streamlit Cloud hosting)
   - **DO NOT** check "Initialize with README" (we already have one)
5. Click **"Create repository"**

### B. Upload Your Code

**Option 1: Using Git Commands (Recommended)**

Open PowerShell in your project folder (`C:\Users\aspire\OneDrive\Desktop\test1`) and run:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Commit your files
git commit -m "Initial commit: Political News Sentiment Analysis App"

# Add your GitHub repository as remote
# REPLACE YOUR_USERNAME and YOUR_REPO with your actual GitHub username and repo name
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Option 2: Using GitHub Desktop (If you have it installed)**
1. Open GitHub Desktop
2. File → Add Local Repository
3. Choose your project folder
4. Publish repository to GitHub

**Option 3: Manual Upload**
1. Go to your new GitHub repository page
2. Click "uploading an existing file"
3. Drag and drop all files EXCEPT `.streamlit/secrets.toml`
4. Click "Commit changes"

---

## 🌐 Step 2: Deploy on Streamlit Cloud

### A. Sign Up/Login
1. Go to **https://share.streamlit.io/**
2. Click **"Sign in"** or **"Sign up"**
3. **"Continue with GitHub"**
4. Authorize Streamlit Cloud to access your GitHub

### B. Create New App
1. Click **"New app"** button
2. You'll see a form with these fields:
   - **Repository**: Select your repository (e.g., `YOUR_USERNAME/political-news-sentiment`)
   - **Branch**: Select `main`
   - **Main file path**: Type `app.py`
   - **App URL** (optional): Choose a custom name or use auto-generated

### C. Add Your API Key (IMPORTANT!)
1. Click **"Advanced settings"** at the bottom
2. Click on **"Secrets"** section
3. In the text box, add:
```toml
NEWS_API_KEY = "40645c397b7b435fb7eae1cedc1f7d5b"
```
4. Click **"Save"**

### D. Deploy!
1. Click the **"Deploy!"** button
2. Wait 2-3 minutes while it deploys
3. Watch the logs as it installs packages
4. Once you see "Your app is live!", you're done! 🎉

---

## 🎊 Your App is Live!

Your app will be available at:
```
https://YOUR-APP-NAME.streamlit.app
```

Share this URL with anyone!

---

## 🔄 Updating Your App

Whenever you make changes:

```powershell
# Make your changes to the code
# Then commit and push:

git add .
git commit -m "Description of your changes"
git push
```

Streamlit Cloud will **automatically redeploy** your app! No need to do anything else.

---

## 🐛 Troubleshooting

### Problem: Git command not found
**Solution**: Install Git from https://git-scm.com/download/win

### Problem: Authentication failed when pushing
**Solution**: 
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Use the token as password when pushing

### Problem: App shows "Error: No articles found"
**Solution**: Check if your API key is correctly set in Streamlit Cloud secrets

### Problem: Deployment failed
**Solution**: 
1. Check the logs in Streamlit Cloud dashboard
2. Make sure all dependencies are in `requirements.txt`
3. Verify `app.py` is the correct main file

---

## 📝 Quick Reference Commands

```powershell
# Check if git is installed
git --version

# See current status
git status

# See your changes
git diff

# Update app after changes
git add .
git commit -m "Your message"
git push
```

---

## ✅ Final Checklist

Before deploying, verify:
- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] `.streamlit/secrets.toml` is NOT in GitHub (check .gitignore)
- [ ] Logged into Streamlit Cloud
- [ ] Selected correct repository and branch
- [ ] Set main file to `app.py`
- [ ] Added API key to Streamlit Cloud secrets
- [ ] Clicked Deploy

---

**Need Help?** 
- Check logs in Streamlit Cloud dashboard
- Visit: https://docs.streamlit.io/
- Ask on: https://discuss.streamlit.io/

**🎉 Congratulations on deploying your app!**
