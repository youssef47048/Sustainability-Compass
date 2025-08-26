# Sustainability Compass - User Guide

## Getting Started

### 1. First Launch
- Start the application using `SustainabilityCompass.exe` or `python app.py`
- The main window will open with a clean, modern interface
- You'll see tabs for Analysis, Comparison, and Reports

### 2. Configure API Key (First Time Only)
- Go to the Settings/Configuration section
- Enter your Google Gemini API key
- Click Save to store the configuration

## Main Features

### PDF Analysis

#### Uploading Documents
1. Click **"Upload PDF"** or **"Select File"**
2. Choose your sustainability report (PDF format)
3. The application supports both English and Arabic text
4. File processing will begin automatically

#### Analysis Process
1. **Text Extraction**: PDF content is extracted and cleaned
2. **AI Analysis**: Gemini AI analyzes the content for:
   - ESG (Environmental, Social, Governance) metrics
   - Sustainability indicators
   - Performance assessment
3. **SDG Mapping**: Results are mapped to UN Sustainable Development Goals
4. **Visualization**: Charts and graphs are generated

#### Viewing Results
- **Summary Tab**: Overview of key findings
- **Detailed Analysis**: In-depth ESG breakdown
- **SDG Alignment**: Visual representation of goal alignment
- **Charts**: Interactive visualizations

### Report Comparison

#### Comparing Reports
1. Go to the **Comparison** tab
2. Select multiple saved reports or upload new ones
3. Choose comparison criteria:
   - Year-over-year performance
   - Different companies
   - Specific ESG categories
4. Generate comparison visualizations

#### Comparison Features
- Side-by-side metric comparison
- Trend analysis over time
- Performance benchmarking
- Gap analysis

### Export and Reporting

#### Export Options
- **Word Document**: Comprehensive report with charts
- **Excel Spreadsheet**: Data tables and metrics
- **PDF Report**: Professional formatted document
- **Charts**: Individual visualizations as images

#### Customizing Exports
1. Select the data/charts to include
2. Choose format and layout options
3. Add custom headers, footers, or notes
4. Generate and save the export

### Data Management

#### Saving Analysis Results
- Results are automatically saved in `stored_reports/`
- Organized by company/organization
- Include metadata (date, version, source file)

#### Managing Saved Reports
- View all saved analyses
- Delete outdated reports
- Export historical data
- Backup and restore functionality

## Tips for Best Results

### PDF Preparation
- Use high-quality, text-based PDFs (not scanned images)
- Ensure documents are not password-protected
- Remove any confidential information before analysis
- For Arabic documents, ensure proper text encoding

### Analysis Optimization
- Use comprehensive sustainability reports for best results
- Include financial and operational data where possible
- Ensure documents contain quantitative metrics
- Multi-year reports provide better trend analysis

### Interpreting Results
- Review the confidence scores for each analysis section
- Cross-reference AI findings with your domain knowledge
- Use visualizations to identify patterns and trends
- Consider context and industry-specific factors

## Understanding the Analysis

### ESG Categories

**Environmental:**
- Carbon emissions and climate impact
- Resource usage and waste management
- Environmental compliance and policies
- Renewable energy adoption

**Social:**
- Employee relations and diversity
- Community engagement
- Customer satisfaction
- Human rights and labor practices

**Governance:**
- Board composition and independence
- Executive compensation
- Risk management
- Transparency and reporting

### SDG Alignment
The application maps findings to the 17 UN Sustainable Development Goals:
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

## Troubleshooting

### Common Issues
- **Slow processing**: Large PDFs may take several minutes
- **API errors**: Check internet connection and API key validity
- **Export failures**: Ensure sufficient disk space and write permissions
- **Display issues**: Try adjusting window size or restarting application

### Performance Tips
- Close unnecessary applications while processing large files
- Ensure stable internet connection for AI analysis
- Use minimal requirements installation for basic functionality
- Regularly clean up old reports to save disk space

## Support and Resources

### Log Files
- Check `sustainability_compass.log` for detailed error information
- Include log files when reporting issues

### Best Practices
- Regular backups of saved reports
- Keep API keys secure
- Update the application regularly
- Test with sample documents first

For technical support or questions, refer to the documentation or contact the development team.
