# Configuration file for Sustainability Compass Application
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')  # Set your API key in .env file

# Application Settings
APP_TITLE = "Sustainability Compass Pro"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "1400x900"
COMPANY_TAGLINE = "Enterprise ESG Analytics Platform"

# Supported Languages
LANGUAGES = {
    'en': 'English',
    'ar': 'العربية'
}

# UN Sustainable Development Goals
SDG_GOALS = {
    1: "No Poverty",
    2: "Zero Hunger", 
    3: "Good Health and Well-being",
    4: "Quality Education",
    5: "Gender Equality",
    6: "Clean Water and Sanitation",
    7: "Affordable and Clean Energy",
    8: "Decent Work and Economic Growth",
    9: "Industry, Innovation and Infrastructure",
    10: "Reduced Inequalities",
    11: "Sustainable Cities and Communities",
    12: "Responsible Consumption and Production",
    13: "Climate Action",
    14: "Life Below Water",
    15: "Life on Land",
    16: "Peace, Justice and Strong Institutions",
    17: "Partnerships for the Goals"
}

# ESG Categories
ESG_CATEGORIES = {
    'economic': 'Economic/Financial Performance',
    'environmental': 'Environmental Impact',
    'social': 'Social Responsibility'
}

# File Types
SUPPORTED_PDF_TYPES = ['.pdf']
EXPORT_FORMATS = ['PDF Report', 'Word Document', 'Excel Spreadsheet']

# UI Colors (Professional Enterprise Theme)
COLORS = {
    'primary': '#1e3a8a',       # Deep corporate blue
    'secondary': '#059669',     # Professional green
    'accent': '#dc2626',        # Corporate red
    'background': '#f8fafc',    # Light professional gray
    'sidebar': '#f1f5f9',       # Sidebar background
    'text': '#1f2937',          # Dark professional text
    'success': '#047857',       # Success green
    'warning': '#d97706',       # Warning amber
    'error': '#dc2626',         # Error red
    'chart_primary': '#3b82f6', # Chart blue
    'chart_secondary': '#10b981', # Chart green
    'border': '#e5e7eb'         # Subtle borders
}

# Professional UI Labels
UI_LABELS = {
    'en': {
        'app_title': 'Sustainability Compass Pro',
        'tagline': 'Enterprise ESG Analytics Platform',
        'upload_section': 'Document Processing',
        'analysis_section': 'ESG Analysis Engine',
        'export_section': 'Report Generation',
        'dashboard_section': 'Analytics Dashboard',
        'select_file': '📄 Import Document',
        'start_analysis': '⚡ Process Analysis',
        'export_pdf': '📋 Generate PDF Report',
        'export_word': '📄 Generate Word Report', 
        'export_excel': '📊 Generate Excel Report',
        'view_dashboard': '📈 Open Analytics Dashboard',
        'processing_status': 'Processing Status',
        'analysis_complete': 'Analysis Complete - Ready for Export'
    },
    'ar': {
        'app_title': 'منصة التحليل المؤسسي للاستدامة',
        'tagline': 'نظام تحليل الأداء البيئي والاجتماعي والحوكمة',
        'upload_section': 'معالجة المستندات',
        'analysis_section': 'محرك تحليل الاستدامة',
        'export_section': 'إنتاج التقارير',
        'dashboard_section': 'لوحة التحليلات',
        'select_file': '📄 استيراد المستند',
        'start_analysis': '⚡ تشغيل التحليل',
        'export_pdf': '📋 إنتاج تقرير PDF',
        'export_word': '📄 إنتاج تقرير Word',
        'export_excel': '📊 إنتاج تقرير Excel',
        'view_dashboard': '📈 فتح لوحة التحليلات',
        'processing_status': 'حالة المعالجة',
        'analysis_complete': 'اكتمل التحليل - جاهز للتصدير'
    }
}

# Analysis Categories for Professional Display
ANALYSIS_CATEGORIES = {
    'esg_metrics': {
        'economic': {
            'icon': '💼',
            'title': 'Economic Performance',
            'subtitle': 'Financial Health & Growth Metrics'
        },
        'environmental': {
            'icon': '🌍',
            'title': 'Environmental Impact',
            'subtitle': 'Sustainability & Climate Metrics'
        },
        'social': {
            'icon': '👥',
            'title': 'Social Responsibility', 
            'subtitle': 'Stakeholder & Community Impact'
        }
    },
    'sdg_framework': {
        'icon': '🎯',
        'title': 'UN SDG Alignment',
        'subtitle': 'Sustainable Development Goals Mapping'
    }
} 