# 🤖 ChatGPT Middleware for Google Drive Bridge

This middleware connects ChatGPT's function calling directly to your Google Drive Bridge API, allowing ChatGPT to create Google Docs and Sheets through natural language.

## 🚀 Quick Setup

### 1. Get Your OpenAI API Key
- Go to [OpenAI Platform](https://platform.openai.com/api-keys)
- Create a new API key
- Copy the key

### 2. Configure the Middleware
Edit `config.py`:
```python
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

### 3. Run the Middleware
```bash
python middleware.py
```

## 🎯 How It Works

### **User Input:**
```
You: Create a Google Doc called Meeting Notes
```

### **What Happens:**
1. **ChatGPT receives** your request
2. **ChatGPT calls** the `create_google_doc` function
3. **Middleware calls** your bridge at `/create_doc_chat`
4. **Bridge responds** with either:
   - ✅ Document link (if authenticated)
   - 🔐 Auth required message with link

### **Example Response:**
```json
{
  "status": "error",
  "message": "Authentication required. Please visit:",
  "auth_url": "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com/auth"
}
```

## 🔧 Available Functions

### **Create Google Document**
- **Function:** `create_google_doc`
- **Parameter:** `name` (string)
- **Example:** "Create a Google Doc called Project Plan"

### **Create Google Sheet**
- **Function:** `create_google_sheet`
- **Parameter:** `name` (string)
- **Example:** "I need a spreadsheet named Budget 2024"

## 📋 Test Commands

Try these in the middleware:

```
You: Create a Google Doc called Meeting Notes
You: Make me a spreadsheet for Inventory Tracking
You: I need a document titled "Project Plan"
You: Create a sheet named "Budget 2024"
```

## 🔐 Authentication Flow

1. **First request** → Returns auth required message
2. **User clicks auth link** → Goes through Google OAuth
3. **User returns** → Can now create documents
4. **Subsequent requests** → Return document links directly

## 🎉 Benefits

- ✅ **No token management** in ChatGPT
- ✅ **Clean user experience** with friendly auth messages
- ✅ **Secure OAuth flow** handled by your bridge
- ✅ **Natural language** document creation
- ✅ **Real-time integration** with Google Drive

## 🚨 Troubleshooting

### **"Module not found" errors:**
```bash
pip install openai requests
```

### **API key issues:**
- Check your OpenAI API key in `config.py`
- Ensure you have credits in your OpenAI account

### **Bridge connection issues:**
- Verify your Heroku app is running
- Check the `BRIDGE_URL` in `config.py`

## 🔗 Files

- **`middleware.py`** - Main middleware script
- **`config.py`** - Configuration settings
- **`README_MIDDLEWARE.md`** - This file

## 🎯 Next Steps

1. **Set your OpenAI API key** in `config.py`
2. **Run the middleware** with `python middleware.py`
3. **Test with natural language** requests
4. **Authenticate** when prompted
5. **Create documents** seamlessly!

---

**Your Google Drive Bridge is now fully integrated with ChatGPT! 🎉**
