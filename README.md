# 🌱 Sustainability Compass

A comprehensive desktop application for analyzing company sustainability performance using AI-powered ESG analysis and UN SDG mapping.

## 🎯 Features

### Core Capabilities
- **📄 Multi-language PDF Processing**: Support for English and Arabic documents
- **🤖 AI-Powered Analysis**: Gemini AI integration for comprehensive ESG evaluation
- **🎯 Complete SDG Mapping**: Analysis across all 17 UN Sustainable Development Goals
- **📊 Interactive Dashboards**: Beautiful visualizations and charts
- **📋 Professional Reports**: Export in PDF, Word, and Excel formats

### ESG Analysis Categories
- **🏢 Economic/Financial Performance**: Financial health, growth, and economic impact
- **🌍 Environmental Impact**: Carbon emissions, energy efficiency, waste management
- **👥 Social Responsibility**: Employee welfare, diversity, community engagement

### SDG Integration
Maps company performance to all 17 UN Sustainable Development Goals:
1. No Poverty
2. Zero Hunger
3. Good Health and Well-being
4. Quality Education
5. Gender Equality
6. Clean Water and Sanitation
7. Affordable and Clean Energy
8. Decent Work and Economic Growth
9. Industry, Innovation and Infrastructure
10. Reduced Inequalities
11. Sustainable Cities and Communities
12. Responsible Consumption and Production
13. Climate Action
14. Life Below Water
15. Life on Land
16. Peace, Justice and Strong Institutions
17. Partnerships for the Goals

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (Free tier works!)
- Windows, macOS, or Linux

### Installation

1. **Clone or download the application files**
   ```bash
   # If using git
   git clone <repository-url>
   cd sustainability-compass
   
   # Or extract if downloaded as ZIP
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key** 🔐
   
   **IMPORTANT: For security, never hardcode your API key in source code!**
   
   Create a `.env` file in the project directory:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   You can copy from the template:
   ```bash
   cp .env.example .env
   # Then edit .env with your actual API key
   ```

4. **Test your API key (recommended)**
   ```bash
   python test_api.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 🔧 Configuration

### API Key Setup 🔐
1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **SECURE SETUP** - Choose one method:
   - **Recommended**: Create `.env` file: `GEMINI_API_KEY=your_key_here`
   - Set environment variable: `export GEMINI_API_KEY=your_key_here`
   
   **⚠️ NEVER hardcode API keys in source code files!**

### 🆓 Free Tier vs 💰 Paid Models

**Current Model Priority (User Configured):**
1. 💰 `gemini-2.5-pro` - Premium model (requires payment)
2. ✅ `models/gemini-2.5-flash` - Latest flash model (free)
3. ✅ `models/gemini-2.5-flash-lite` - Lite version (free)

**Additional Available Models:**
- ✅ `gemini-1.5-flash` - Fast, efficient (free)
- ✅ `gemini-1.5-pro` - More capable, limited free usage
- 💰 `gemini-2.0-pro` - Advanced model (requires payment)

**The app tries premium models first, then automatically falls back to free models!**

### Supported File Types
- PDF documents (up to 100 pages recommended)
- Both English and Arabic content supported

## 📖 Usage Guide

### 0. Test API (First Time)
- Run `python test_api.py` to verify your setup
- This will show available models and test connectivity
- Helps diagnose any API issues before running the main app
- **Shows which models are free vs paid**

### 1. Upload Document
- Click "📄 Import Document" in the sidebar
- Choose your sustainability report or company document
- Supported: Annual reports, sustainability reports, ESG disclosures

### 2. Select Language
- Choose output language (English/العربية)
- The app auto-detects PDF content language
- Analysis and reports will be in your selected language

### 3. Run Analysis
- Click "⚡ Process Analysis"
- Wait for AI processing (typically 2-5 minutes)
- Progress bar shows current status

### 4. View Results
- Review the analysis summary in the Results tab
- See ESG scores and top contributing SDGs
- Executive summary provides key insights

### 5. Export Reports
- **📋 PDF Report**: Professional formatted report
- **📄 Word Document**: Editable document with tables
- **📊 Excel Spreadsheet**: Detailed data and metrics
- **📈 Dashboard**: Interactive web-based visualizations

## 🏗️ Application Architecture

```
sustainability-compass/
├── app.py                 # Main entry point
├── main_gui.py           # GUI application
├── config.py             # Configuration settings
├── pdf_processor.py      # PDF text extraction
├── gemini_analyzer.py    # AI analysis engine
├── visualization.py      # Chart generation
├── export_manager.py     # Report exports
├── test_api.py           # API testing utility
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 🔍 Technical Details

### PDF Processing
- **Text Extraction**: Using pdfplumber and PyPDF2
- **Table Detection**: Automatic table extraction and parsing
- **Language Detection**: Arabic/English detection algorithms
- **Metadata Extraction**: Document properties and creation info

### AI Analysis
- **Model**: Automatically selects best model from priority list
- **Primary**: gemini-2.5-pro (premium, with automatic fallback)
- **Secondary**: gemini-2.5-flash, gemini-2.5-flash-lite (free)
- **Fallback**: gemini-1.5-flash, gemini-1.5-pro (free)
- **Analysis Types**: ESG performance scoring, SDG mapping
- **Language Support**: Bilingual prompts and responses
- **Fallback Handling**: Robust error handling and automatic model fallback

### Visualization
- **Charts**: Bar charts, radar charts, heatmaps, pie charts
- **Interactive**: Plotly-based interactive dashboards
- **Export**: Static charts in reports, interactive HTML dashboards

### Export Formats
- **PDF**: ReportLab-based professional reports
- **Word**: python-docx with proper formatting
- **Excel**: Multi-sheet workbooks with data and summaries
- **HTML**: Interactive dashboard with all visualizations

## 🛠️ Troubleshooting

### Common Issues

**"Missing dependency" error**
```bash
pip install -r requirements.txt
```

**"Gemini AI configuration failed" or "404 models/gemini-pro is not found"**
- Run `python test_api.py` to diagnose the issue
- Check your API key is correct: `AIzaSy...` format
- Ensure you have internet connection
- Verify API key has proper permissions
- The app now automatically tries multiple model versions

**"429 Quota exceeded" or "Free tier limit" errors**
- ✅ **You're trying to use a paid model with free API key**
- 🔧 **Solution**: The app now automatically uses free models
- 💡 **Tip**: Run `python test_api.py` to see free vs paid models
- 🆓 **Recommended**: Use `gemini-1.5-flash` (shows as 🟢 Free Tier)

**"PDF processing failed"**
- Ensure PDF is not password-protected
- Try with a smaller PDF file
- Check if PDF contains readable text

**Arabic text not displaying correctly**
- Ensure arabic-reshaper and python-bidi are installed
- Try updating the packages: `pip install --upgrade arabic-reshaper python-bidi`

### Performance Tips
- Use PDFs under 100 pages for best performance
- Ensure stable internet connection for AI analysis
- Close other applications if analysis is slow
- **Use free-tier models** for consistent performance

## 📊 Sample Output

The application generates:
- **ESG Scores**: 0-10 ratings for Economic, Environmental, Social performance
- **SDG Mapping**: Impact level and scores for all 17 SDGs
- **Executive Summary**: AI-generated overview of sustainability performance
- **Recommendations**: Actionable suggestions for improvement
- **Visual Dashboard**: Interactive charts and graphs

## 🔒 Privacy & Security

- **Local Processing**: PDF processing happens locally
- **API Usage**: Only text content sent to Gemini AI
- **No Storage**: No data stored on external servers
- **Logs**: Local log files for debugging only

## 💰 Cost Information

### Current Configuration (Hybrid)
- **Primary Model**: gemini-2.5-pro (💰 paid - premium analysis)
- **Fallback Models**: gemini-2.5-flash, gemini-2.5-flash-lite (🆓 free)
- **Strategy**: Try premium first, fallback to free automatically

### Free Tier Fallback
- **Models**: gemini-2.5-flash, gemini-2.5-flash-lite, gemini-1.5-flash
- **Cost**: $0 (within quotas)
- **Quota**: 15 requests/minute, 1,500/day
- **Perfect for**: Individual users, small businesses

### Paid Tier (Primary)
- **Model**: gemini-2.5-pro
- **Cost**: Pay per token
- **Benefits**: Best analysis quality, higher quotas
- **Best for**: Enterprise use, premium analysis

**The app tries premium models but works perfectly with free tier fallbacks!**

## 🆘 Support

If you encounter issues:
1. **First**: Run `python test_api.py` for diagnosis
2. Check the log file: `sustainability_compass.log`
3. Verify all dependencies are installed
4. Ensure your API key is valid
5. Try with a different PDF file

## 📝 License

This application is provided as-is for sustainability analysis purposes.

## 🙏 Acknowledgments

- Google Gemini AI for analysis capabilities
- Open source libraries for PDF processing and visualization
- UN Sustainable Development Goals framework

---

**Note**: This application is optimized for **free-tier Gemini API usage**. Premium models require a paid Google Cloud account. 