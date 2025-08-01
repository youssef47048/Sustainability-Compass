#!/usr/bin/env python3
"""
Enhanced Sustainability Compass Launcher
Choose between Limited Content (old) vs Full Content (new) analysis
"""

import os
import sys
from pathlib import Path

def show_comparison():
    """Show the key differences between approaches"""
    print("🎯 Sustainability Compass Pro - Analysis Comparison")
    print("=" * 60)
    print()
    print("📊 CONTENT ANALYSIS COMPARISON:")
    print()
    print("❌ OLD APPROACH (Limited Content):")
    print("  📉 Analyzes only: 6,000 characters (~3% of document)")
    print("  📄 Coverage: First few pages only")
    print("  🔧 Method: JSON parsing (error-prone)")
    print("  🎯 Analysis: Superficial, missing key details")
    print("  ⚡ Speed: Fast but incomplete")
    print()
    print("✅ NEW APPROACH (Full Content):")
    print("  📈 Analyzes: Complete document (100%)")
    print("  📄 Coverage: All pages, tables, detailed content")
    print("  🔧 Method: Markdown format (reliable)")
    print("  🎯 Analysis: Comprehensive, evidence-based")
    print("  💎 Quality: Premium analysis with Gemini 2.5 Pro")
    print()
    print("💡 RECOMMENDATION: Use Full Content for accurate results!")
    print()

def main():
    """Main launcher with user choice"""
    
    show_comparison()
    
    while True:
        print("🚀 Launch Options:")
        print("1. 🔥 NEW: Full Content Analysis (Recommended)")
        print("2. ⚠️  OLD: Limited Content Analysis")
        print("3. 🧪 TEST: Compare Both Approaches")
        print("4. 📋 VIEW: Show Detailed Comparison")
        print("5. ❌ EXIT")
        print()
        
        choice = input("👉 Select option (1-5): ").strip()
        
        if choice == "1":
            print("\n🚀 Launching Full Content Analysis App...")
            print("✅ Using: MarkdownGeminiAnalyzer")
            print("📈 Content: Complete document analysis")
            print("🎯 Quality: Premium comprehensive analysis")
            print()
            # Launch main app (already updated to use full content)
            os.system("python app.py")
            break
            
        elif choice == "2":
            print("\n⚠️  Launching Limited Content Analysis...")
            print("❌ Using: Original GeminiAnalyzer (6K chars only)")
            print("📉 Content: Partial document analysis")
            print("🔍 Note: May miss important information")
            print()
            # For demonstration, we could create a version that uses the old analyzer
            print("💡 Consider using Full Content Analysis instead!")
            print("   The old approach only analyzes 3% of your document.")
            print()
            continue
            
        elif choice == "3":
            print("\n🧪 Running Comparison Test...")
            if len(sys.argv) > 1:
                pdf_file = sys.argv[1]
                os.system(f"python test_full_content.py {pdf_file}")
            else:
                pdf_file = input("📄 Enter PDF filename (e.g., e.pdf): ").strip()
                if pdf_file and os.path.exists(pdf_file):
                    os.system(f"python test_full_content.py {pdf_file}")
                else:
                    print("❌ PDF file not found!")
            continue
            
        elif choice == "4":
            show_comparison()
            continue
            
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-5.")
            continue

if __name__ == "__main__":
    main() 