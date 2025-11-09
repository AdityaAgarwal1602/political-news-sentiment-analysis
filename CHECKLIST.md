# Deployment Checklist ✅

Before deploying to Streamlit Cloud, make sure you have:

## Files Ready
- [ ] `app.py` - Main application file
- [ ] `requirements.txt` - All dependencies listed
- [ ] `config.py` - Updated to use Streamlit secrets
- [ ] `users_db.py` - User authentication module
- [ ] `pdf_generator.py` - PDF generation module
- [ ] `README.md` - Project documentation
- [ ] `.gitignore` - Prevents sensitive files from being committed
- [ ] `assets/svgviewer-png-output.png` - Logo file

## GitHub Setup
- [ ] Created GitHub repository
- [ ] Initialized git in project folder (`git init`)
- [ ] Added all files (`git add .`)
- [ ] Made initial commit (`git commit -m "Initial commit"`)
- [ ] Added remote repository (`git remote add origin ...`)
- [ ] Pushed to GitHub (`git push -u origin main`)

## Streamlit Cloud Setup
- [ ] Created account on https://share.streamlit.io/
- [ ] Connected GitHub account
- [ ] Selected repository and branch
- [ ] Set main file path to `app.py`
- [ ] Added NEWS_API_KEY to Secrets section

## Testing
- [ ] Tested app locally (`streamlit run app.py`)
- [ ] Verified login functionality works
- [ ] Verified news fetching works
- [ ] Verified sentiment analysis page loads
- [ ] Verified PDF export works

## Post-Deployment
- [ ] App successfully deployed
- [ ] Tested live app URL
- [ ] Verified API key works in production
- [ ] Shared app URL with intended users

## Quick Commands Reference

### Initialize and Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Update Deployed App
```bash
git add .
git commit -m "Your update message"
git push
```

### Run Locally
```bash
streamlit run app.py
```

---
**Your App URL**: `https://[your-app-name].streamlit.app`
