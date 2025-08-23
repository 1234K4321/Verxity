# Deployment Guide for Excel Add-in

## The Problem
Microsoft 365 admin center cannot validate manifests with localhost URLs. You need publicly accessible HTTPS URLs.

## Quick Solution with GitHub Pages

### 1. Create a GitHub Repository
1. Go to GitHub and create a new repository
2. Upload these files:
   - `taskpane.html`
   - `manifest.xml` (after updating URLs)
   - Any icon files

### 2. Enable GitHub Pages
1. Go to repository Settings → Pages
2. Select "Deploy from a branch" → "main"
3. Your site will be available at: `https://username.github.io/repository-name`

### 3. Update Your Manifest
Replace `https://localhost:3000` with your GitHub Pages URL in:
- `manifest.xml` (lines with SourceLocation and Taskpane.Url)
- Update AppDomains as well

### 4. Backend Considerations
Your Flask backend needs to be deployed separately:
- **Heroku** (free tier discontinued, but still available)
- **Railway** (free tier available)
- **Render** (free tier available)
- **PythonAnywhere** (free tier available)

Update the fetch URL in `taskpane.html` to point to your deployed backend.

## Alternative: Using ngrok (for testing only)

### 1. Install ngrok
```bash
# macOS
brew install ngrok

# Or download from https://ngrok.com/
```

### 2. Start your servers
```bash
# Terminal 1: Frontend server
python3 serve_https.py

# Terminal 2: Backend server  
python3 app.py

# Terminal 3: Create public tunnels
ngrok http 3000 --host-header="localhost:3000"
# This will give you a public HTTPS URL like: https://abc123.ngrok.io
```

### 3. Update manifest with ngrok URL
Replace localhost URLs with the ngrok URL in your manifest.

## Production Deployment Checklist

- [ ] Deploy frontend to a public HTTPS hosting service
- [ ] Deploy backend to a cloud service with HTTPS
- [ ] Update all URLs in manifest.xml
- [ ] Replace placeholder icons with real icons
- [ ] Test the add-in with the public URLs
- [ ] Upload updated manifest to Microsoft 365 admin center

## Current Status
Your current manifest uses localhost URLs, which is why it fails validation in the admin center. The manifest structure is correct - you just need publicly accessible URLs.
