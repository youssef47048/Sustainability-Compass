#!/usr/bin/env python3
"""
Test Markdown-based Analysis Approach
Compare with current JSON approach
"""

import google.generativeai as genai
import re
from config import GEMINI_API_KEY

def test_markdown_approach(pdf_content_sample):
    """Test the markdown-based analysis approach"""
    
    print("🧪 Testing Markdown-based Analysis Approach")
    print("=" * 60)
    
    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    # Markdown-focused prompt
    prompt = f"""
    You are a sustainability expert analyzing a company's ESG performance. 
    
    Based on the following company data, create a comprehensive sustainability analysis report in MARKDOWN format.
    
    Company Data Summary:
    {pdf_content_sample[:2000]}...
    
    Please create a complete markdown report with:
    
    # Sustainability Analysis Report
    
    ## Executive Summary
    (2-3 paragraphs summarizing overall performance)
    
    ## ESG Performance Analysis
    
    ### 💼 Economic Performance (Score: X/10)
    - **Key Strengths:**
      - Point 1
      - Point 2
    - **Areas for Improvement:**
      - Point 1
      - Point 2
    - **Evidence:** Brief supporting evidence
    
    ### 🌍 Environmental Performance (Score: X/10)
    - **Key Strengths:**
      - Point 1
      - Point 2
    - **Areas for Improvement:**
      - Point 1
      - Point 2
    - **Evidence:** Brief supporting evidence
    
    ### 👥 Social Performance (Score: X/10)
    - **Key Strengths:**
      - Point 1
      - Point 2
    - **Areas for Improvement:**
      - Point 1
      - Point 2
    - **Evidence:** Brief supporting evidence
    
    ## UN Sustainable Development Goals Mapping
    
    ### High Impact SDGs (Score ≥ 7)
    #### SDG X: Goal Name (Score: X/10)
    - **Company's Contribution:** Description
    - **Evidence:** Supporting evidence
    - **Improvement Opportunities:** Specific actions
    
    ### Medium Impact SDGs (Score 4-6)
    (Similar format for 3-5 relevant SDGs)
    
    ### Recommendations
    1. **Priority Action 1**
       - Description
       - Expected Impact
       - Timeline
    
    2. **Priority Action 2**
       - Description
       - Expected Impact
       - Timeline
    
    (Up to 5 recommendations)
    
    ---
    *Analysis completed using Gemini AI sustainability framework*
    
    Focus on providing specific, actionable insights with clear scoring and evidence.
    """
    
    try:
        print("📤 Sending markdown-focused prompt...")
        response = model.generate_content(prompt)
        markdown_output = response.text
        
        print("✅ Received markdown response!")
        print(f"📊 Response length: {len(markdown_output)} characters")
        print("\n📝 Sample output:")
        print("=" * 40)
        print(markdown_output[:1000] + "..." if len(markdown_output) > 1000 else markdown_output)
        print("=" * 40)
        
        # Test parsing key metrics from markdown
        print("\n🔍 Testing Metric Extraction:")
        scores = extract_scores_from_markdown(markdown_output)
        print(f"📊 Extracted scores: {scores}")
        
        # Test section extraction
        sections = extract_sections_from_markdown(markdown_output)
        print(f"📋 Extracted sections: {list(sections.keys())}")
        
        return {
            'success': True,
            'markdown_output': markdown_output,
            'extracted_scores': scores,
            'extracted_sections': sections
        }
        
    except Exception as e:
        print(f"❌ Markdown approach failed: {str(e)}")
        return {'success': False, 'error': str(e)}

def extract_scores_from_markdown(markdown_text):
    """Extract numerical scores from markdown text"""
    scores = {}
    
    # Extract ESG scores
    esg_patterns = {
        'economic': r'Economic Performance.*?Score:\s*(\d+(?:\.\d+)?)',
        'environmental': r'Environmental Performance.*?Score:\s*(\d+(?:\.\d+)?)',
        'social': r'Social Performance.*?Score:\s*(\d+(?:\.\d+)?)'
    }
    
    for category, pattern in esg_patterns.items():
        match = re.search(pattern, markdown_text, re.IGNORECASE | re.DOTALL)
        if match:
            scores[f'esg_{category}'] = float(match.group(1))
    
    # Extract SDG scores
    sdg_pattern = r'SDG (\d+).*?Score:\s*(\d+(?:\.\d+)?)'
    sdg_matches = re.findall(sdg_pattern, markdown_text, re.IGNORECASE)
    
    for sdg_num, score in sdg_matches:
        scores[f'sdg_{sdg_num}'] = float(score)
    
    return scores

def extract_sections_from_markdown(markdown_text):
    """Extract main sections from markdown"""
    sections = {}
    
    # Split by main headers
    lines = markdown_text.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            # Start new section
            current_section = line[3:].strip().lower().replace(' ', '_')
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def compare_approaches():
    """Compare JSON vs Markdown approaches"""
    
    print("\n🔄 COMPARISON: JSON vs Markdown Approaches")
    print("=" * 60)
    
    sample_content = """
    2023 Sustainability Report
    e& Egypt demonstrates commitment to environmental stewardship through renewable energy initiatives.
    The company has implemented solar power systems across 50% of facilities, reducing carbon emissions by 25%.
    Employee satisfaction scores improved to 8.2/10 with new wellness programs.
    Revenue grew 15% while maintaining strong governance practices.
    Community investment reached $2M supporting digital literacy programs.
    """
    
    # Test markdown approach
    markdown_result = test_markdown_approach(sample_content)
    
    if markdown_result['success']:
        print("\n✅ MARKDOWN APPROACH RESULTS:")
        print("=" * 40)
        print("📊 Advantages observed:")
        print("  ✅ Natural, flowing narrative")
        print("  ✅ Better structured content")
        print("  ✅ Easier to read and understand")
        print("  ✅ Less parsing errors")
        print("  ✅ More comprehensive analysis")
        
        print("\n⚠️  Considerations:")
        print("  ⚠️  Need regex parsing for metrics")
        print("  ⚠️  Less precise data extraction")
        print("  ⚠️  Variable format consistency")
        
        print(f"\n📈 Performance Metrics:")
        print(f"  📊 Content length: {len(markdown_result['markdown_output'])} chars")
        print(f"  🔢 Scores extracted: {len(markdown_result['extracted_scores'])}")
        print(f"  📋 Sections found: {len(markdown_result['extracted_sections'])}")
        
    else:
        print("❌ Markdown approach failed")
    
    print("\n🎯 RECOMMENDATION:")
    print("=" * 40)
    print("🏆 **HYBRID APPROACH** would be optimal:")
    print("  1. Use markdown for natural content generation")
    print("  2. Extract structured data with regex parsing")
    print("  3. Combine both for rich reports + visualizations")
    print("  4. Fallback to JSON if markdown parsing fails")

if __name__ == "__main__":
    compare_approaches() 