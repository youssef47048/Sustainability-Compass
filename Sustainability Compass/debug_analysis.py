#!/usr/bin/env python3
"""
Debug Script for Sustainability Analysis
Helps identify where issues are occurring in the analysis pipeline
"""

import json
import traceback
from pdf_processor import PDFProcessor
from gemini_analyzer import GeminiAnalyzer
from export_manager import ReportExporter

def debug_analysis_pipeline(pdf_path: str):
    """
    Debug the complete analysis pipeline step by step
    
    Args:
        pdf_path (str): Path to the PDF file to analyze
    """
    
    print("🔍 Starting Sustainability Analysis Debug...")
    print(f"📄 PDF File: {pdf_path}")
    print("=" * 60)
    
    # Step 1: Test PDF Processing
    print("\n📋 STEP 1: PDF Processing")
    print("-" * 30)
    try:
        pdf_processor = PDFProcessor()
        pdf_content = pdf_processor.extract_content(pdf_path)
        
        print(f"✅ PDF processed successfully")
        print(f"📊 Pages: {pdf_content['page_count']}")
        print(f"🔤 Text length: {len(pdf_content['text'])} characters")
        print(f"📋 Tables found: {len(pdf_content['tables'])}")
        print(f"🌐 Language detected: {pdf_content['language_detected']}")
        
        # Show sample text
        sample_text = pdf_content['text'][:500] if pdf_content['text'] else "No text extracted"
        print(f"📝 Sample text: {sample_text}...")
        
        if not pdf_content['text'] or len(pdf_content['text']) < 100:
            print("⚠️  WARNING: Very little or no text extracted from PDF!")
            print("   This could cause analysis issues.")
            
    except Exception as e:
        print(f"❌ PDF processing failed: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")
        return None
    
    # Step 2: Test Gemini API Connection
    print("\n🤖 STEP 2: Gemini AI Configuration")
    print("-" * 30)
    try:
        gemini_analyzer = GeminiAnalyzer()
        model_name = getattr(gemini_analyzer.model, '_model_name', 'Unknown')
        print(f"✅ Gemini AI configured successfully")
        print(f"🎯 Model: {model_name}")
        
    except Exception as e:
        print(f"❌ Gemini AI configuration failed: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")
        return None
    
    # Step 3: Test Simple API Call
    print("\n🧪 STEP 3: Simple API Test")
    print("-" * 30)
    try:
        test_prompt = "Respond with 'API working' if you can read this."
        response_text = gemini_analyzer._make_api_call(test_prompt)
        print(f"✅ API call successful")
        print(f"📤 Test prompt: {test_prompt}")
        print(f"📥 Response: {response_text}")
        
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")
        return None
    
    # Step 4: Test ESG Analysis
    print("\n📊 STEP 4: ESG Analysis")
    print("-" * 30)
    try:
        esg_results = gemini_analyzer.analyze_esg_performance(pdf_content, 'en')
        print(f"✅ ESG analysis completed")
        print(f"📋 Result type: {type(esg_results)}")
        print(f"🔑 Keys: {list(esg_results.keys()) if isinstance(esg_results, dict) else 'Not a dict'}")
        
        # Show ESG results
        if isinstance(esg_results, dict):
            for category, data in esg_results.items():
                if isinstance(data, dict) and 'score' in data:
                    score = data.get('score', 'N/A')
                    print(f"   {category}: {score}/10")
                    
            # Check for errors
            if esg_results.get('error'):
                print(f"⚠️  ESG Analysis Error: {esg_results.get('error_message')}")
        else:
            print(f"⚠️  Unexpected ESG result format: {esg_results}")
            
    except Exception as e:
        print(f"❌ ESG analysis failed: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")
        esg_results = {}
    
    # Step 5: Test SDG Mapping
    print("\n🎯 STEP 5: SDG Mapping")
    print("-" * 30)
    try:
        sdg_results = gemini_analyzer.map_to_sdgs(pdf_content, esg_results, 'en')
        print(f"✅ SDG mapping completed")
        print(f"📋 Result type: {type(sdg_results)}")
        print(f"🔑 Keys: {list(sdg_results.keys()) if isinstance(sdg_results, dict) else 'Not a dict'}")
        
        # Show top SDGs
        if isinstance(sdg_results, dict):
            sdg_scores = []
            for key, data in sdg_results.items():
                if key.startswith('sdg_') and isinstance(data, dict):
                    score = data.get('score', 0)
                    if score > 0:
                        sdg_num = key.split('_')[1]
                        sdg_scores.append((f"SDG {sdg_num}", score))
            
            if sdg_scores:
                sdg_scores.sort(key=lambda x: x[1], reverse=True)
                print(f"   Top SDGs:")
                for sdg, score in sdg_scores[:5]:
                    print(f"   {sdg}: {score}/10")
            else:
                print("   ⚠️  No SDG scores found")
                
            # Check for errors
            if sdg_results.get('error'):
                print(f"⚠️  SDG Mapping Error: {sdg_results.get('error_message')}")
        else:
            print(f"⚠️  Unexpected SDG result format: {sdg_results}")
            
    except Exception as e:
        print(f"❌ SDG mapping failed: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")
        sdg_results = {}
    
    # Step 6: Test Complete Analysis
    print("\n🔄 STEP 6: Complete Analysis")
    print("-" * 30)
    try:
        complete_results = gemini_analyzer.generate_comprehensive_report(pdf_content, 'en')
        print(f"✅ Complete analysis finished")
        print(f"📋 Result type: {type(complete_results)}")
        
        if isinstance(complete_results, dict):
            print(f"🔑 Main keys: {list(complete_results.keys())}")
            
            # Check each section
            sections = ['executive_summary', 'esg_analysis', 'sdg_mapping', 'recommendations']
            for section in sections:
                if section in complete_results:
                    data = complete_results[section]
                    if isinstance(data, str):
                        length = len(data)
                        preview = data[:100] + "..." if len(data) > 100 else data
                        print(f"   {section}: {length} chars - '{preview}'")
                    elif isinstance(data, list):
                        print(f"   {section}: {len(data)} items")
                    elif isinstance(data, dict):
                        print(f"   {section}: {len(data)} keys")
                    else:
                        print(f"   {section}: {type(data)}")
                else:
                    print(f"   ❌ Missing: {section}")
                    
            # Check for errors
            if complete_results.get('error'):
                print(f"⚠️  Complete Analysis Error: {complete_results.get('error_message')}")
                
        else:
            print(f"⚠️  Unexpected complete result format: {complete_results}")
            
        return complete_results
        
    except Exception as e:
        print(f"❌ Complete analysis failed: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")
        return None
    
def debug_export(analysis_results, export_format='pdf'):
    """
    Debug the export functionality
    
    Args:
        analysis_results: Results from analysis
        export_format: Format to test ('pdf', 'word', 'excel')
    """
    
    print(f"\n📤 STEP 7: Export Debug ({export_format.upper()})")
    print("-" * 30)
    
    if not analysis_results:
        print("❌ No analysis results to export")
        return
    
    try:
        exporter = ReportExporter()
        test_file = f"debug_test_report.{export_format if export_format != 'word' else 'docx'}"
        
        if export_format == 'pdf':
            success = exporter.export_pdf_report(analysis_results, test_file, 'en')
        elif export_format == 'word':
            success = exporter.export_word_report(analysis_results, test_file, 'en')
        elif export_format == 'excel':
            success = exporter.export_excel_report(analysis_results, test_file, 'en')
        else:
            print(f"❌ Unknown export format: {export_format}")
            return
            
        if success:
            print(f"✅ {export_format.title()} export successful: {test_file}")
            import os
            if os.path.exists(test_file):
                size = os.path.getsize(test_file)
                print(f"📊 File size: {size} bytes")
                if size < 1000:
                    print("⚠️  WARNING: File size is very small - might be empty!")
            else:
                print("❌ Export reported success but file not found!")
        else:
            print(f"❌ {export_format.title()} export failed")
            
    except Exception as e:
        print(f"❌ Export error: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")

def main():
    """Main debug function"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python debug_analysis.py <pdf_file_path>")
        print("Example: python debug_analysis.py sample.pdf")
        return
    
    pdf_path = sys.argv[1]
    
    # Run complete debug
    analysis_results = debug_analysis_pipeline(pdf_path)
    
    if analysis_results:
        # Test exports
        debug_export(analysis_results, 'pdf')
        debug_export(analysis_results, 'word')
        
        print("\n" + "=" * 60)
        print("🎯 DEBUG SUMMARY")
        print("=" * 60)
        
        if isinstance(analysis_results, dict) and not analysis_results.get('error'):
            print("✅ Analysis pipeline completed successfully")
            print("💡 If exports are empty, the issue might be in the report templates")
        else:
            print("❌ Analysis pipeline has issues")
            print("💡 Check the errors above and fix the API/analysis problems first")
    else:
        print("\n❌ Analysis failed completely - check API key and PDF file")
        
    print("\n🔧 Next steps:")
    print("1. Fix any errors shown above")
    print("2. Run 'python test_api.py' to verify API")
    print("3. Try with a different PDF file")
    print("4. Check the generated debug files")

if __name__ == "__main__":
    main() 