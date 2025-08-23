# Excel Add-in Setup Guide

## Issues Fixed in manifest.xml

The main validation errors have been resolved:

1. **HTTPS URLs**: Changed all localhost URLs from HTTP to HTTPS in the manifest
2. **Resource References**: Added proper resource ID references for labels and strings
3. **Manifest Structure**: Ensured all required elements are properly nested

## Running the Add-in

Since your Flask backend runs on port 5000 and your manifest expects the frontend on port 3000, you need to run two servers:

### Option 1: Simple HTTP Server (for development only)
```bash
python3 serve.py
```

### Option 2: HTTPS Server (recommended for admin center deployment)
```bash
python3 serve_https.py
```

This will create a self-signed certificate and serve your taskpane.html over HTTPS.

### Backend Server
In another terminal, run your Flask backend:
```bash
python3 app.py
```

## Common Validation Errors and Solutions

1. **HTTPS Required**: The Microsoft 365 admin center requires HTTPS URLs for production deployment. Use the `serve_https.py` script.

2. **Certificate Issues**: For production deployment, you'll need a valid SSL certificate from a certificate authority, not a self-signed one.

3. **Accessible URLs**: Make sure your server is accessible from the internet for production deployment.

## For Production Deployment

1. Host your files on a server with a valid SSL certificate
2. Update the manifest URLs to point to your production server
3. Replace placeholder icons with real icons hosted on your server
4. Ensure CORS is properly configured on your Flask backend

## Testing the Manifest

Before uploading to the admin center:
1. Validate your manifest using the Office Add-in Validator
2. Test the add-in locally using Excel Desktop with developer mode
3. Ensure all URLs in the manifest are accessible via HTTPS

## Current Manifest Configuration

- Frontend (taskpane.html): https://localhost:3000/taskpane.html
- Backend API: http://localhost:5000/api/generate-report (internal call from taskpane)
- Icons: Using placeholder images from placehold.co (should be replaced for production)
