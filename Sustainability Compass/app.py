#!/usr/bin/env python3
"""
Sustainability Compass Application Entry Point

A comprehensive desktop application for sustainability analysis that:
- Processes PDF documents (English & Arabic)
- Analyzes ESG performance using Gemini AI
- Maps results to UN Sustainable Development Goals
- Generates professional reports and visualizations

Usage:
    python app.py

Requirements:
    - Python 3.8+
    - All dependencies in requirements.txt
    - Valid Gemini API key
"""

import sys
import os
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('sustainability_compass.log'),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if core dependencies are installed"""
    # Essential dependencies
    essential_deps = [
        ('customtkinter', 'GUI framework'),
        ('google.generativeai', 'AI analysis'),
        ('pandas', 'data processing'),
        ('matplotlib', 'visualization'),
        ('plotly', 'interactive charts'),
        ('docx', 'Word export'),
        ('PyPDF2', 'PDF processing'),
        ('pdfplumber', 'PDF text extraction')
    ]
    
    # Optional dependencies
    optional_deps = [
        ('reportlab', 'PDF report generation'),
        ('arabic_reshaper', 'Arabic text support'),
        ('python_bidi', 'Arabic text support'),
        ('seaborn', 'enhanced visualization'),
        ('openpyxl', 'Excel support'),
        ('pytesseract', 'OCR support')
    ]
    
    missing_essential = []
    missing_optional = []
    
    # Check essential dependencies
    for dep, description in essential_deps:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            missing_essential.append(f"{dep} ({description})")
    
    # Check optional dependencies
    for dep, description in optional_deps:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            missing_optional.append(f"{dep} ({description})")
    
    if missing_essential:
        print("❌ Missing essential dependencies:")
        for dep in missing_essential:
            print(f"   - {dep}")
        print("\n🔧 Install with: pip install -r requirements_minimal.txt")
        return False
    
    if missing_optional:
        print("⚠️  Missing optional dependencies (app will still work):")
        for dep in missing_optional:
            print(f"   - {dep}")
        print("   Install full version with: pip install -r requirements.txt")
    
    return True

def main():
    """Main entry point"""
    print("🌱 Starting Sustainability Compass...")
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Import and run the main application
        from main_gui import SustainabilityCompassApp
        
        logger.info("Initializing Sustainability Compass Application")
        app = SustainabilityCompassApp()
        
        print("✅ Application started successfully!")
        print("📄 Upload a PDF document to begin sustainability analysis")
        
        app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        print(f"❌ Error: {str(e)}")
        print("Check the log file 'sustainability_compass.log' for details")
        sys.exit(1)

if __name__ == "__main__":
    main() 