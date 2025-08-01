#!/usr/bin/env python3
"""
Debug Script for Sustainability Analysis
Helps identify where issues are occurring in the analysis pipeline
"""

import json
import traceback
from pdf_processor import PDFProcessor
from markdown_analyzer import MarkdownGeminiAnalyzer  # Changed to MarkdownGeminiAnalyzer
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
    
    # Step 2: Test Gemini AI Configuration
    print("\n🤖 STEP 2: Gemini AI Configuration")
    print("-" * 30)
    try:
        gemini_analyzer = MarkdownGeminiAnalyzer()  # Changed to MarkdownGeminiAnalyzer
        print(f"✅ Gemini AI configured successfully")
        
        # Get model info
        model_name = getattr(gemini_analyzer.model, '_model_name', 'Unknown')
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
        # Use markdown analyzer's full document analysis
        full_results = gemini_analyzer.analyze_full_document(pdf_content, 'en')
        
        print(f"✅ Full analysis completed")
        print(f"📋 Result type: {type(full_results)}")
        print(f"🔑 Keys: {list(full_results.keys()) if isinstance(full_results, dict) else 'Not a dict'}")
        
        # Extract ESG analysis from results
        esg_results = full_results.get('esg_analysis', {}) if isinstance(full_results, dict) else {}
        
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
        full_results = {}
    
    # Step 5: Test SDG Mapping (extracted from full results)
    print("\n🎯 STEP 5: SDG Mapping")
    print("-" * 30)
    try:
        # Extract SDG mapping from full results
        sdg_results = full_results.get('sdg_mapping', {}) if isinstance(full_results, dict) else {}
        
        print(f"✅ SDG mapping completed")
        print(f"📋 Result type: {type(sdg_results)}")
        print(f"🔑 Keys: {list(sdg_results.keys()) if isinstance(sdg_results, dict) else 'Not a dict'}")
        
        # Show top SDGs
        if isinstance(sdg_results, dict):
            sdg_scores = []
            print("   🔍 Detailed SDG Data:")
            for key, data in sdg_results.items():
                if key.startswith('sdg_') and isinstance(data, dict):
                    score = data.get('score', 0)
                    impact = data.get('impact_level', 'Unknown')
                    contributions = data.get('contributions', [])
                    print(f"     {key}: score={score}, impact={impact}, contributions={len(contributions)}")
                    if score > 0:
                        sdg_num = key.split('_')[1]
                        sdg_scores.append((f"SDG {sdg_num}", score))
            
            if sdg_scores:
                sdg_scores.sort(key=lambda x: x[1], reverse=True)
                print(f"   Top SDGs:")
                for sdg, score in sdg_scores[:5]:
                    print(f"   {sdg}: {score}/10")
            else:
                print("   ⚠️  No SDG scores found (all scores are 0)")
                # Show a few example SDG entries for debugging
                sample_keys = [k for k in sdg_results.keys() if k.startswith('sdg_')][:3]
                for key in sample_keys:
                    print(f"   📋 Sample {key}: {sdg_results[key]}")
                
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
        # Results are already available from the full analysis above
        complete_results = full_results
        
        print(f"✅ Complete analysis finished")
        print(f"📋 Result type: {type(complete_results)}")
        print(f"🔑 Main keys: {list(complete_results.keys()) if isinstance(complete_results, dict) else 'Not a dict'}")
        
        # Show summary of each section
        if isinstance(complete_results, dict):
            for key, value in complete_results.items():
                if key == 'executive_summary':
                    print(f"   {key}: {len(str(value))} chars - '{str(value)[:100]}...'")
                elif isinstance(value, dict):
                    print(f"   {key}: {len(value)} keys")
                elif isinstance(value, list):
                    print(f"   {key}: {len(value)} items")
                else:
                    print(f"   {key}: {type(value)}")
                    
    except Exception as e:
        print(f"❌ Complete analysis failed: {str(e)}")
        print(f"🔧 Error details: {traceback.format_exc()}")
        complete_results = full_results  # Use whatever we have
    
    # Step 7: Test Export
    print("\n📤 STEP 7: Export Debug (PDF)")
    print("-" * 30)
    try:
        exporter = ReportExporter()
        test_file = f"debug_test_report.pdf"
        
        success = exporter.export_pdf_report(complete_results, test_file, 'en')
        
        if success:
            print(f"✅ PDF export successful: {test_file}")
            import os
            if os.path.exists(test_file):
                size = os.path.getsize(test_file)
                print(f"📊 File size: {size} bytes")
                if size < 1000:
                    print("⚠️  WARNING: File size is very small - might be empty!")
            else:
                print("❌ Export reported success but file not found!")
        else:
            print(f"❌ PDF export failed")
            
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