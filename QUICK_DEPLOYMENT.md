# Streamlit Cloud Deployment Guide

## 🚀 Deploy to Streamlit Cloud (5 minutes)

Streamlit Cloud is the easiest way to deploy your app with zero configuration.

### Step 1: Prepare Your Repository

1. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Click "Deploy"

3. **Your app is live!**
   - Available at: `https://your-app-name.streamlit.app`
   - Automatic deployments on every git push

## 📋 Required Files (All Present ✅)

Your project contains all necessary files for Streamlit Cloud:

- ✅ `app.py` - Main Streamlit application
- ✅ `ai_agent.py` - AI agent functionality
- ✅ `loader.py` - Data loading utilities
- ✅ `plots.py` - Plotting functions
- ✅ `simulation.py` - Monte Carlo simulation logic
- ✅ `sidebar.py` - UI sidebar components
- ✅ `requirements.txt` - Python dependencies
- ✅ `Project 2 - CLD Workflow Step 1 Results.xlsx` - Data file

## 🧪 Test Locally First

Before deploying, test your app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🔧 Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check that `app.py` is in the root directory

2. **Data file not found:**
   - Make sure the Excel file is included in your repository
   - Check file paths in `loader.py`

3. **Deployment fails:**
   - Check Streamlit Cloud logs for error messages
   - Ensure your repository is public or you have Streamlit Cloud Pro

### Streamlit Cloud Features:

- **Free tier available** - No cost for basic usage
- **Automatic deployments** - Updates on every git push
- **Built-in analytics** - Track app usage and performance
- **Custom domains** - Available with Pro plan
- **Team collaboration** - Share apps with your team

## 📊 Monitoring Your App

After deployment, you can:

1. **View analytics** in your Streamlit Cloud dashboard
2. **Check logs** for any errors
3. **Monitor performance** and usage statistics
4. **Manage deployments** and rollbacks

## 💡 Pro Tips

1. **Test locally first** - Always test before pushing to GitHub
2. **Use descriptive commit messages** - Helps track changes
3. **Monitor your app** - Check analytics and logs regularly
4. **Keep dependencies updated** - Update `requirements.txt` as needed
5. **Backup your data** - Keep copies of your Excel file

## 🎯 One-Command Local Testing

```bash
# Install and run locally
pip install -r requirements.txt && streamlit run app.py
```

---

**Ready to deploy?** Just push to GitHub and connect to Streamlit Cloud! 