# Sustainability Compass - Installation Guide

## Option 1: Using the Executable (Recommended for End Users)

### Quick Start
1. Download the `SustainabilityCompass.exe` file
2. Double-click to run the application
3. Configure your Gemini API key (see API Setup below)
4. Start analyzing PDF documents!

### System Requirements
- Windows 10 or later (64-bit)
- At least 4GB RAM
- 500MB free disk space
- Internet connection for AI analysis

---

## Option 2: Running from Source Code (For Developers)

### Prerequisites
- Python 3.8 or later
- pip (Python package manager)

### Installation Steps

1. **Extract the source code** to your desired directory

2. **Install dependencies** (choose one):
   ```bash
   # Full installation (all features)
   pip install -r requirements.txt
   
   # OR minimal installation (essential features only)
   pip install -r requirements_minimal.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

---

## API Setup (Required for Both Options)

### Getting Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### Configuring the API Key
1. Launch the application
2. Go to Settings/Configuration
3. Enter your Gemini API key
4. Save the configuration

**Important**: Keep your API key secure and never share it publicly.

---

## Troubleshooting

### Common Issues

**Application won't start:**
- Ensure you have administrator privileges
- Check Windows Defender hasn't quarantined the file
- Try running as administrator

**PDF processing fails:**
- Ensure PDF is not password-protected
- Try with a different PDF file
- Check internet connection

**AI analysis fails:**
- Verify your Gemini API key is correct
- Check your internet connection
- Ensure you haven't exceeded API quotas

**Export features not working:**
- Check you have write permissions in the output directory
- Ensure sufficient disk space

### Getting Help
- Check the log file: `sustainability_compass.log`
- Contact support with error details and log file

---

## Features Overview

- **PDF Processing**: Extract text from English and Arabic documents
- **AI Analysis**: Comprehensive ESG assessment using Google Gemini
- **SDG Mapping**: Automatic mapping to UN Sustainable Development Goals
- **Visualizations**: Interactive charts and graphs
- **Report Export**: Export to Word, Excel, and PDF formats
- **Report Comparison**: Compare multiple sustainability reports
- **Data Storage**: Save and manage analysis results

---

## Data Privacy

- PDF content is processed by Google Gemini AI
- No data is stored permanently by the application beyond your local machine
- Analysis results are saved locally in the `stored_reports` folder
- API usage follows Google's data handling policies
