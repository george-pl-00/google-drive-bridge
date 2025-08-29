# 🧪 Testing Google Drive Bridge API

This guide explains how to test your Google Drive Bridge API that's deployed on Heroku.

## 🚀 Quick Test

### 1. Update the Heroku URL
In both test files, update the `HEROKU_URL` variable with your actual Heroku app URL:
```python
HEROKU_URL = "https://your-actual-app-name.herokuapp.com"
```

### 2. Test Basic Endpoints
```bash
python test_heroku_endpoints.py
```

### 3. Test ChatGPT Simulation
```bash
python test_api.py
```

## 📋 What Gets Tested

### Health Check (`GET /`)
- ✅ API is running
- ✅ Returns available endpoints
- ✅ No authentication required

### Authentication (`GET /auth`)
- 🔐 Redirects to Google OAuth
- 🔐 Sets up session cookies
- 🔐 Required before creating documents

### Create Document (`POST /create_doc`)
- 📝 Creates Google Document
- 📝 Requires authentication
- 📝 Returns document link and ID

### Create Sheet (`POST /create_sheet`)
- 📊 Creates Google Spreadsheet
- 📊 Requires authentication
- 📊 Returns sheet link and ID

## 🔧 Setup Requirements

### 1. Google Cloud Console
- Enable Google Drive API
- Enable Google Docs API
- Enable Google Sheets API
- Create OAuth 2.0 credentials

### 2. Heroku Environment Variables
Set these in your Heroku app:
```bash
GOOGLE_OAUTH_CLIENT_ID=your_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
HEROKU_APP_NAME=your_app_name
JWT_SECRET=your_jwt_secret
```

### 3. OAuth Credentials File
For local development, you need `oauth_credentials.json` from Google Cloud Console.

## 🧪 Testing Flow

### Without Authentication
1. Health check works ✅
2. Auth endpoint redirects to Google ✅
3. Create endpoints return 401 (unauthorized) ✅

### With Authentication
1. Visit `/auth` to authenticate with Google
2. Grant permissions to your app
3. Create documents/sheets via API calls
4. Get back links to created files

## 🐛 Troubleshooting

### API Not Responding
- Check if Heroku app is running
- Verify the URL is correct
- Check Heroku logs: `heroku logs --tail`

### Authentication Errors
- Verify OAuth credentials are correct
- Check environment variables on Heroku
- Ensure redirect URIs match

### Document Creation Fails
- Verify Google Drive API is enabled
- Check if user has granted permissions
- Look for errors in Heroku logs

## 📱 ChatGPT Integration

When ChatGPT receives a request like:
> "Create a document called 'Meeting Notes'"

It should:
1. Call `POST /create_doc` with `{"name": "Meeting Notes"}`
2. Get back the document link
3. Return the link to the user in chat

## 🔗 Example API Calls

### Create Document
```bash
curl -X POST https://your-app.herokuapp.com/create_doc \
  -H "Content-Type: application/json" \
  -H "Cookie: session_token=your_session_token" \
  -d '{"name": "Test Document"}'
```

### Create Sheet
```bash
curl -X POST https://your-app.herokuapp.com/create_sheet \
  -H "Content-Type: application/json" \
  -H "Cookie: session_token=your_session_token" \
  -d '{"name": "Test Sheet"}'
```

## 📊 Expected Responses

### Success Response
```json
{
  "success": true,
  "docId": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "link": "https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit",
  "name": "Test Document",
  "message": "Google Document 'Test Document' created successfully!"
}
```

### Error Response
```json
{
  "detail": "Google authentication required. Please visit /auth to authenticate."
}
```
