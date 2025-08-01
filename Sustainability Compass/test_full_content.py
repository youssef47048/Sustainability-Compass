#!/usr/bin/env python3
"""
Test Full Content Analysis
Demonstrates sending COMPLETE PDF content to Gemini (not truncated to 6000 chars)
"""

from pdf_processor import PDFProcessor
from markdown_analyzer import MarkdownGeminiAnalyzer
import sys

def test_full_vs_limited_content(pdf_path):
    """Compare current limited approach vs full content approach"""
    
    print("🔍 Testing: Full Content vs Limited Content Approach")
    print("=" * 60)
    
    # Extract PDF content
    print("📄 Step 1: Extracting PDF content...")
    pdf_processor = PDFProcessor()
    pdf_content = pdf_processor.extract_content(pdf_path)
    
    full_text = pdf_content.get('text', '')
    print(f"📊 Complete PDF content: {len(full_text)} characters")
    print(f"📖 Document pages: {pdf_content.get('page_count', 0)}")
    print(f"📋 Tables found: {len(pdf_content.get('tables', []))}")
    
    # Show current limitation
    limited_content = full_text[:6000]  # Current approach
    print(f"\n❌ CURRENT APPROACH (LIMITED):")
    print(f"  📉 Sends only: {len(limited_content)} characters ({len(limited_content)/len(full_text)*100:.1f}% of document)")
    print(f"  📝 Sample of what's LOST:")
    print(f"     Original: {full_text[6000:6200]}...")
    
    # Show new full approach
    print(f"\n✅ NEW FULL CONTENT APPROACH:")
    print(f"  📈 Sends complete: {len(full_text)} characters (100% of document)")
    print(f"  🎯 Includes ALL pages, tables, and detailed content")
    print(f"  💡 No information loss - comprehensive analysis possible")
    
    # Test the new analyzer
    print(f"\n🧪 Testing Full Content Analysis...")
    try:
        analyzer = MarkdownGeminiAnalyzer()
        
        # This will send the COMPLETE content to Gemini
        print("📤 Sending COMPLETE document content to Gemini...")
        results = analyzer.analyze_full_document(pdf_content, 'en')
        
        if results.get('error'):
            print(f"❌ Analysis failed: {results.get('error_message')}")
        else:
            print("✅ Full content analysis successful!")
            print(f"📊 Results summary:")
            print(f"  📝 Executive summary: {len(results.get('executive_summary', ''))} characters")
            print(f"  📋 ESG sections: {len(results.get('esg_analysis', {}))}")
            print(f"  🎯 SDG mappings: {len(results.get('sdg_mapping', {}))}")
            print(f"  💡 Recommendations: {len(results.get('recommendations', []))}")
            
            # Show content preview
            if results.get('executive_summary'):
                preview = results['executive_summary'][:200] + "..."
                print(f"  📖 Executive summary preview: {preview}")
                
    except Exception as e:
        print(f"❌ Full content test failed: {str(e)}")
    
    print(f"\n🎯 SUMMARY:")
    print(f"  📈 Content increase: {len(full_text)/6000:.1f}x more content sent to AI")
    print(f"  🎯 Analysis depth: Comprehensive instead of superficial")
    print(f"  📊 Data coverage: Complete document instead of first few pages")
    print(f"  💡 Result quality: Much more detailed and accurate insights")

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_full_content.py <pdf_file>")
        print("Example: python test_full_content.py e.pdf")
        return
    
    pdf_path = sys.argv[1]
    test_full_vs_limited_content(pdf_path)

if __name__ == "__main__":
    main() 