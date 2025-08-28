# 🚀 Google Drive Chat - AI-Powered File Creation

A web-based chat interface that allows you to create Google Drive files (Documents and Spreadsheets) directly through natural language conversations with ChatGPT.

## ✨ Features

- **Natural Language Processing**: Simply tell the AI what you want to create
- **Google Drive Integration**: Automatically creates files in your Google Drive
- **Multiple File Types**: Supports Google Docs and Google Sheets
- **Smart Content Generation**: AI analyzes your request and creates appropriate content
- **Modern Web Interface**: Beautiful, responsive chat interface
- **Secure Authentication**: Uses Google OAuth 2.0 for secure access

## 🛠️ Prerequisites

Before you begin, ensure you have:

1. **Python 3.7+** installed on your system
2. **Google Cloud Project** with Google Drive API enabled
3. **OpenAI API Key** for ChatGPT integration
4. **Google OAuth 2.0 Credentials** for Drive access

## 📋 Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Navigate to your project directory
cd multi-agent-system

# Install required packages
pip install -r requirements.txt
```

### 2. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Download the credentials file and rename it to `oauth_credentials.json`
   - Place it in your project root directory

### 3. OpenAI API Setup

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key for the next step

### 4. Environment Configuration

1. Copy the example environment file:
   ```bash
   copy env_example.txt .env
   ```

2. Edit the `.env` file with your actual values:
   ```env
   # Flask Configuration
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DEBUG=True
   HOST=0.0.0.0
   PORT=5000

   # OpenAI Configuration
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here

   # Google OAuth Configuration
   GOOGLE_OAUTH_CREDENTIALS_FILE=oauth_credentials.json
   ```

### 5. First Run Setup

1. Run the application:
   ```bash
   python webdrive.py
   ```

2. On first run, you'll be redirected to Google's OAuth consent screen
3. Grant permissions to access your Google Drive
4. The application will create a `token.pickle` file for future use

## 🚀 Usage

### Starting the Application

```bash
python webdrive.py
```

The application will start and display:
- Configuration validation status
- Local server URL (usually http://localhost:5000)
- Any setup requirements

### Using the Chat Interface

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Type your request** in natural language, for example:
   - "Create a document about artificial intelligence trends in 2024"
   - "Make a spreadsheet for tracking monthly expenses"
   - "Write a document about sustainable living practices"
3. **Click Send** or press Enter
4. **Wait for the AI** to analyze your request and create the file
5. **Click the link** to open your newly created file in Google Drive

### Example Requests

| Request Type | Example | What Gets Created |
|--------------|---------|-------------------|
| **Document** | "Write a document about climate change solutions" | Google Doc with AI-generated content about climate change |
| **Spreadsheet** | "Create a budget tracker spreadsheet" | Google Sheet with budget categories and sample data |
| **Mixed** | "Make a project management document with a task tracker" | Both a document and a spreadsheet |

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Random string |
| `DEBUG` | Enable debug mode | True |
| `HOST` | Server host address | 0.0.0.0 |
| `PORT` | Server port | 5000 |
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `GOOGLE_OAUTH_CREDENTIALS_FILE` | Path to OAuth credentials | oauth_credentials.json |

### Customizing File Creation

The application automatically determines what type of file to create based on your request:

- **Keywords like "doc", "document", "write"** → Creates Google Doc
- **Keywords like "sheet", "spreadsheet", "table"** → Creates Google Sheet
- **Default behavior** → Creates Google Doc

## 🚨 Troubleshooting

### Common Issues

1. **"oauth_credentials.json not found"**
   - Ensure you've downloaded the OAuth credentials from Google Cloud Console
   - Check the file path in your `.env` file

2. **"OPENAI_API_KEY is required"**
   - Verify your `.env` file exists and contains the correct API key
   - Check that the key is valid and has sufficient credits

3. **Google OAuth errors**
   - Delete `token.pickle` and re-authenticate
   - Ensure your OAuth credentials are for a desktop application
   - Check that the required APIs are enabled in Google Cloud Console

4. **Port already in use**
   - Change the `PORT` in your `.env` file
   - Or stop other applications using port 5000

### Getting Help

- Check the console output for detailed error messages
- Verify all configuration files are in place
- Ensure you have the latest version of all dependencies

## 🔒 Security Considerations

- **Never commit** your `.env` file or `oauth_credentials.json` to version control
- **Use strong secret keys** in production
- **Limit OAuth scopes** to only what's necessary
- **Regularly rotate** your API keys
- **Monitor usage** of both OpenAI and Google APIs

## 📁 Project Structure

```
multi-agent-system/
├── webdrive.py              # Main application file
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── env_example.txt         # Environment variables template
├── .env                    # Your environment variables (create this)
├── oauth_credentials.json  # Google OAuth credentials
├── token.pickle           # Google OAuth token (auto-generated)
└── templates/
    └── chat.html          # Web interface template
```

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy file creating! 🎉**
