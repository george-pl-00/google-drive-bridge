# 🚀 Setup Guide for ChatGPT Middleware

After cloning this repository, follow these steps to get the ChatGPT middleware working:

## 🔑 Step 1: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Create a new API key or copy an existing one
4. Copy the key (it starts with `sk-`)

## ⚙️ Step 2: Configure the Middleware

1. **Copy the template:**
   ```bash
   cp config_template.py config.py
   ```

2. **Edit config.py:**
   ```python
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```

3. **Replace** `"sk-your-actual-api-key-here"` with your actual API key

## 🧪 Step 3: Test the Setup

1. **Test the bridge connection:**
   ```bash
   python test_middleware.py
   ```

2. **Start the interactive middleware:**
   ```bash
   python middleware.py
   ```

3. **Try creating a document:**
   ```
   You: Create a Google Doc called Meeting Notes
   ```

## 🔐 Step 4: Google Authentication

1. **First request** will return authentication required
2. **Click the auth link** to authenticate with Google
3. **Return to the middleware** and try again
4. **Document will be created** and link returned

## 📁 File Structure

- **`config_template.py`** → Copy to `config.py` and add your keys
- **`config.py`** → Your actual configuration (not in git)
- **`middleware.py`** → ChatGPT integration script
- **`main.py`** → Google Drive Bridge API

## 🚨 Security Notes

- ✅ **`config_template.py`** is safe to share
- ❌ **`config.py`** contains your actual API keys
- ❌ **Never commit** `config.py` to git
- ✅ **`.gitignore`** protects sensitive files

## 🎯 Ready to Use!

Once configured, you can:
- Create Google Docs through natural language
- Create Google Sheets through natural language
- Let ChatGPT handle the document creation
- Get real-time links to created documents

---

**Your ChatGPT + Google Drive integration is ready! 🎉**
