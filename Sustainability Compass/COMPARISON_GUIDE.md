# Multi-Year Report Comparison Guide

## Overview

The Sustainability Compass now supports **multi-year report comparison**, allowing you to track sustainability performance trends across multiple years for the same company. This powerful feature includes AI-powered comparative analysis and comprehensive visualizations.

## New Features Added

### 🔥 Core Capabilities
- **Report Storage**: Save analysis results for future comparisons
- **Multi-Year Analysis**: Compare 2-10 reports across different years
- **AI-Powered Insights**: Gemini AI generates comparative analysis
- **Trend Visualization**: Interactive charts showing year-over-year progress
- **Comprehensive Exports**: Export comparison dashboards and charts

### 📊 Comparison Analytics
- **ESG Trend Analysis**: Track Economic, Environmental, and Social performance
- **SDG Progress Tracking**: Monitor UN SDG alignment over time
- **Performance Metrics**: Quantitative analysis of improvements/declines
- **Strategic Insights**: AI identifies patterns and recommends focus areas

## How to Use

### Step 1: Generate and Save Reports

1. **Analyze Your First Report**
   - Upload a PDF sustainability report as usual
   - Click "⚡ Process Analysis" to generate the analysis
   - Review the results in the Results tab

2. **Save the Report for Comparison**
   - Click "💾 Save Current Report" in the sidebar
   - Enter the company name (e.g., "ABC Corporation")
   - Enter the report year (e.g., 2022)
   - Click "Save"

3. **Repeat for Additional Years**
   - Upload and analyze reports for other years (2023, 2024, etc.)
   - Save each one with the same company name but different years

### Step 2: Compare Reports

1. **Open Comparison Manager**
   - Click "📊 Manage Reports" in the sidebar
   - The Comparison Manager window will open

2. **Select Company and Years**
   - Choose your company from the list on the left
   - Select 2 or more years using the checkboxes
   - Click "📊 Compare Reports"

3. **Review Comparison Results**
   - **Summary Metrics**: Key statistics about trends
   - **AI Analysis**: Comprehensive insights from Gemini
   - **Trend Visualization**: Charts showing performance changes

### Step 3: Export and Share

1. **Export Comparison Dashboard**
   - Click "📈 Export Comparison" in the manager
   - Multiple chart files will be generated
   - Comprehensive dashboard opens in your browser

2. **Share Results**
   - Use exported HTML files for presentations
   - Charts are interactive and professional-quality
   - Perfect for board reports and stakeholder meetings

## What You Get in Comparisons

### 📈 Performance Trends
- **ESG Score Changes**: Track improvements in Economic, Environmental, Social categories
- **SDG Alignment Progress**: See how UN SDG performance evolves
- **Year-over-Year Analysis**: Quantified changes with trend directions

### 🤖 AI-Generated Insights
- **Strategic Analysis**: What strategic shifts can be inferred?
- **Improvement Areas**: Which sustainability areas show consistent progress?
- **Challenge Identification**: Where are the persistent issues?
- **Future Recommendations**: AI suggests priority focus areas

### 📊 Visual Analytics
- **ESG Trend Lines**: Line charts showing score evolution
- **SDG Heatmaps**: Color-coded performance across goals
- **Improvement Analysis**: Bar charts highlighting changes
- **Radar Charts**: Multi-dimensional performance comparison

### 📋 Export Formats
- **Interactive Dashboard**: Comprehensive HTML with all charts
- **Individual Charts**: Separate files for each visualization type
- **Professional Layout**: Ready for reports and presentations

## Example Workflow

### Scenario: 4 Years of Company Analysis

Let's say you have reports for XYZ Corp from 2021-2024:

1. **Year 1 (2021)**
   - Upload: `XYZ_Sustainability_2021.pdf`
   - Analyze and save as "XYZ Corp", year 2021

2. **Year 2 (2022)**
   - Upload: `XYZ_Sustainability_2022.pdf`
   - Analyze and save as "XYZ Corp", year 2022

3. **Year 3 (2023)**
   - Upload: `XYZ_Sustainability_2023.pdf`
   - Analyze and save as "XYZ Corp", year 2023

4. **Year 4 (2024)**
   - Upload: `XYZ_Sustainability_2024.pdf`
   - Analyze and save as "XYZ Corp", year 2024

5. **Comparison Analysis**
   - Open Comparison Manager
   - Select "XYZ Corp"
   - Check all 4 years (2021-2024)
   - Generate comprehensive 4-year analysis

### Sample AI Analysis Output

```
# Sustainability Performance Analysis: XYZ Corp (2021-2024)

## Performance Trends
Over the 4-year period, XYZ Corp demonstrates significant improvement in environmental performance (+2.3 points) while maintaining strong social performance. Economic performance shows steady growth with a +1.1 point improvement.

## Strategic Insights
The data suggests a strategic shift toward environmental initiatives starting in 2022, likely driven by new carbon neutrality commitments. SDG 13 (Climate Action) shows the most dramatic improvement (+3.2 points), indicating successful climate initiatives.

## Future Recommendations
1. **Accelerate Social Innovation**: While environmental gains are strong, social performance has plateaued
2. **Diversify SDG Portfolio**: Focus on underperforming SDGs 5 (Gender Equality) and 10 (Reduced Inequalities)
3. **Maintain Momentum**: Environmental initiatives should continue current trajectory

## Benchmark Analysis
XYZ Corp's sustainability trajectory shows above-average improvement rates, particularly in environmental categories. The consistent year-over-year growth indicates strong organizational commitment to sustainability goals.
```

## Technical Details

### Data Storage
- Reports stored locally in `stored_reports/` directory
- JSON format with complete analysis results
- Organized by company name folders
- Includes metadata (file names, analysis dates, etc.)

### AI Analysis Engine
- Uses same Gemini models as main analysis
- Comprehensive prompts for comparative insights
- Structured analysis with actionable recommendations
- Handles 2-10 year comparisons efficiently

### Visualization Engine
- Built on Plotly for interactive charts
- Professional styling and color schemes
- Responsive design for all screen sizes
- Export to HTML with embedded JavaScript

## Tips for Best Results

### 🎯 Report Consistency
- Use the same company name exactly across years
- Ensure reports are from the same organization/division
- Maintain consistent document quality and completeness

### 📅 Year Selection
- Compare at least 2 years for meaningful trends
- 3-4 years optimal for trend analysis
- 5+ years excellent for long-term strategic insights

### 🏢 Company Management
- Use clear, consistent company names
- Consider using official names (e.g., "Apple Inc." not "Apple")
- Organize by subsidiary if analyzing multiple divisions

### 📊 Analysis Interpretation
- Pay attention to trend directions, not just absolute scores
- Look for consistency in improvements/declines
- Consider external factors (regulations, market changes, etc.)

## Troubleshooting

### Common Issues

**"No saved reports" in company list**
- Ensure you've saved at least one report using "💾 Save Current Report"
- Check that the company name was entered correctly

**"Comparison failed" error**
- Verify at least 2 years are selected
- Ensure saved reports contain valid analysis data
- Check internet connection for AI analysis

**Charts not displaying properly**
- Ensure you have a modern web browser
- Check that JavaScript is enabled
- Try refreshing the dashboard page

**Export not working**
- Verify you have write permissions in the project directory
- Check available disk space
- Ensure no antivirus blocking file creation

### Support
If you encounter issues:
1. Check the `sustainability_compass.log` file for errors
2. Verify all dependencies are installed
3. Try with a simpler comparison (2 years only)
4. Restart the application if needed

## Advanced Features

### Custom Analysis Prompts
The AI analysis can be customized by modifying the prompts in `report_comparison.py`. Look for the `_create_comparison_prompt` method to adjust the analysis focus.

### Batch Comparisons
For analyzing multiple companies, you can script the comparison process using the `ReportComparison` class directly:

```python
from report_comparison import ReportComparison

comparison = ReportComparison()
companies = comparison.get_all_companies()

for company in companies:
    reports = comparison.get_company_reports(company)
    if len(reports) >= 2:
        years = list(reports.keys())
        result = comparison.compare_reports(company, years)
        print(f"Analysis complete for {company}")
```

### Export Customization
Modify the `comparison_visualizer.py` file to customize chart styles, colors, and layouts according to your branding needs.

---

## 🎉 Congratulations!

You now have a powerful multi-year sustainability analysis system that can:
- Track performance trends across multiple years
- Generate AI-powered comparative insights
- Create professional visualizations
- Export comprehensive dashboards

This feature transforms your sustainability reporting from single-point analysis to comprehensive trend tracking and strategic planning tool.

Happy analyzing! 🌱📊