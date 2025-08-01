#!/usr/bin/env python3
"""
Markdown-based Gemini Analyzer - Full Content Analysis
Sends complete PDF content to Gemini for comprehensive sustainability analysis
"""

import google.generativeai as genai
import json
import logging
import time
import re
from typing import Dict, List, Optional
from config import GEMINI_API_KEY, SDG_GOALS, ESG_CATEGORIES
import pandas as pd

class MarkdownGeminiAnalyzer:
    """
    Enhanced Gemini AI analyzer using markdown approach
    Sends FULL PDF content for comprehensive analysis
    """
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
        self.request_delay = 3  # Shorter delay for premium model
        self._configure_gemini()
        
    def _configure_gemini(self):
        """Configure Gemini AI with API key"""
        try:
            genai.configure(api_key=self.api_key)
            
            # Try premium models first (since user is using gemini-2.5-pro)
            model_names = [
                'gemini-2.5-pro',                   # Premium - highest capability
                'models/gemini-2.5-pro',            # Alternative format
                'models/gemini-2.5-flash',          # Fast alternative
                'models/gemini-1.5-pro',            # Fallback
                'models/gemini-1.5-flash'           # Final fallback
            ]
            
            self.model = None
            for model_name in model_names:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    self.logger.info(f"✅ Configured with model: {model_name}")
                    break
                except Exception as model_error:
                    self.logger.warning(f"❌ {model_name} failed: {model_error}")
                    continue
            
            if self.model is None:
                raise Exception("No compatible Gemini models found!")
                
        except Exception as e:
            self.logger.error(f"Failed to configure Gemini AI: {str(e)}")
            raise Exception(f"Gemini AI configuration failed: {str(e)}")
    
    def analyze_full_document(self, content: Dict, language: str = 'en') -> Dict:
        """
        Analyze the COMPLETE document using markdown approach
        
        Args:
            content (Dict): Complete extracted PDF content
            language (str): Output language ('en' or 'ar')
            
        Returns:
            Dict: Complete analysis results
        """
        try:
            self.logger.info("🚀 Starting FULL document analysis with markdown approach")
            
            # Get COMPLETE text content (no truncation!)
            full_text = content.get('text', '')
            document_pages = content.get('page_count', 0)
            tables_found = len(content.get('tables', []))
            language_detected = content.get('language_detected', 'en')
            
            self.logger.info(f"📄 Processing complete document:")
            self.logger.info(f"  📊 Pages: {document_pages}")
            self.logger.info(f"  🔤 Text length: {len(full_text)} characters")
            self.logger.info(f"  📋 Tables: {tables_found}")
            self.logger.info(f"  🌐 Language: {language_detected}")
            
            # Create comprehensive markdown prompt
            prompt = self._create_comprehensive_markdown_prompt(
                full_text, tables_found, document_pages, language_detected, language
            )
            
            # Make API call with full content
            self.logger.info("📤 Sending COMPLETE document to Gemini for analysis...")
            markdown_response = self._make_api_call(prompt)
            
            # Parse the markdown response
            self.logger.info("📥 Received comprehensive markdown analysis")
            parsed_results = self._parse_markdown_response(markdown_response, language)
            
            # Add metadata
            parsed_results['analysis_metadata'] = {
                'analysis_date': pd.Timestamp.now().isoformat(),
                'document_pages': document_pages,
                'content_length': len(full_text),
                'tables_processed': tables_found,
                'language': language_detected,
                'model_used': getattr(self.model, '_model_name', 'Unknown'),
                'approach': 'full_content_markdown'
            }
            
            self.logger.info("✅ Full document analysis completed successfully!")
            return parsed_results
            
        except Exception as e:
            self.logger.error(f"❌ Full document analysis failed: {str(e)}")
            return self._create_error_response("Full analysis failed", str(e))
    
    def _create_comprehensive_markdown_prompt(self, full_text: str, tables_count: int, 
                                            pages_count: int, detected_lang: str, output_lang: str) -> str:
        """Create comprehensive markdown analysis prompt with FULL content"""
        
        lang_instructions = {
            'en': "Please provide your complete analysis in English",
            'ar': "يرجى تقديم التحليل الكامل باللغة العربية"
        }
        
        # Include tables information if available
        tables_info = f"\n\nDocument also contains {tables_count} tables with structured data." if tables_count > 0 else ""
        
        prompt = f"""
{lang_instructions.get(output_lang, 'Please provide your complete analysis in English')}

You are a senior sustainability expert conducting a comprehensive ESG (Environmental, Social, Governance) analysis and UN SDG mapping for a company.

You have been provided with the COMPLETE sustainability/annual report ({pages_count} pages, {len(full_text)} characters) to conduct a thorough analysis.{tables_info}

Please create a comprehensive sustainability analysis report in MARKDOWN format covering:

# Complete Sustainability Analysis Report

## Executive Summary
Provide a comprehensive 3-4 paragraph executive summary covering:
- Overall sustainability performance assessment
- Key achievements and critical gaps identified
- Strategic recommendations for improvement
- Alignment with global sustainability frameworks

## ESG Performance Analysis

### 💼 Economic & Financial Performance (Score: X/10)
**Overall Assessment:** [Detailed assessment paragraph]

**Key Strengths:**
- [Specific strength 1 with supporting evidence from document]
- [Specific strength 2 with supporting evidence from document]
- [Specific strength 3 with supporting evidence from document]

**Areas for Improvement:**
- [Specific improvement area 1 with evidence]
- [Specific improvement area 2 with evidence]
- [Specific improvement area 3 with evidence]

**Supporting Evidence:** [Detailed evidence from the document]

**Financial Metrics Identified:** [List any specific financial ESG metrics found]

### 🌍 Environmental Performance (Score: X/10)
**Overall Assessment:** [Detailed assessment paragraph]

**Key Strengths:**
- [Environmental strength 1 with specific data/evidence]
- [Environmental strength 2 with specific data/evidence]
- [Environmental strength 3 with specific data/evidence]

**Areas for Improvement:**
- [Environmental improvement area 1 with evidence]
- [Environmental improvement area 2 with evidence]
- [Environmental improvement area 3 with evidence]

**Supporting Evidence:** [Detailed environmental evidence from document]

**Environmental Metrics Identified:** [List specific environmental KPIs found]

### 👥 Social Performance (Score: X/10)
**Overall Assessment:** [Detailed assessment paragraph]

**Key Strengths:**
- [Social strength 1 with supporting evidence]
- [Social strength 2 with supporting evidence]
- [Social strength 3 with supporting evidence]

**Areas for Improvement:**
- [Social improvement area 1 with evidence]
- [Social improvement area 2 with evidence]
- [Social improvement area 3 with evidence]

**Supporting Evidence:** [Detailed social evidence from document]

**Social Metrics Identified:** [List specific social/employee KPIs found]

## UN Sustainable Development Goals (SDG) Mapping

Based on the comprehensive document analysis, assess the company's contribution to each relevant SDG:

### SDG Contribution Analysis Chart
**CHART DATA FOR VISUALIZATION:**
For each relevant SDG, specify the contribution level for chart generation:
- SDG [Number]: [High/Medium/Low] - Score: [X/10]
- SDG [Number]: [High/Medium/Low] - Score: [X/10]
[Continue for all relevant SDGs that show meaningful contribution]

### High Impact SDGs (Score 7-10)
#### SDG X: [Goal Name] (Score: X/10)
- **Company's Specific Contribution:** [Detailed contribution with evidence]
- **Evidence from Document:** [Specific quotes/data from document]
- **Performance Assessment:** [Detailed assessment]
- **Improvement Opportunities:** [Specific recommendations]

[Repeat for each high-impact SDG - typically 3-5 SDGs]

### Medium Impact SDGs (Score 4-6)
#### SDG X: [Goal Name] (Score: X/10)
- **Company's Contribution:** [Contribution description]
- **Evidence:** [Supporting evidence]
- **Potential for Enhancement:** [Improvement suggestions]

[Include 3-5 medium impact SDGs]

### Lower Impact SDGs (Score 1-3)
[Brief assessment of remaining SDGs with potential for future development]

## Strategic Recommendations

### Priority 1: [Specific Action Area]
**Recommendation:** [Detailed recommendation]
**Expected Impact:** [Specific impact on ESG/SDG performance]
**Implementation Timeline:** [Suggested timeframe]
**Resource Requirements:** [Estimated resources needed]
**Success Metrics:** [How to measure success]

### Priority 2: [Specific Action Area]
**Recommendation:** [Detailed recommendation]
**Expected Impact:** [Specific impact on ESG/SDG performance]
**Implementation Timeline:** [Suggested timeframe]
**Resource Requirements:** [Estimated resources needed]
**Success Metrics:** [How to measure success]

### Priority 3: [Specific Action Area]
**Recommendation:** [Detailed recommendation]
**Expected Impact:** [Specific impact on ESG/SDG performance]
**Implementation Timeline:** [Suggested timeframe]
**Resource Requirements:** [Estimated resources needed]
**Success Metrics:** [How to measure success]

### Priority 4: [Specific Action Area]
**Recommendation:** [Detailed recommendation]
**Expected Impact:** [Specific impact on ESG/SDG performance]
**Implementation Timeline:** [Suggested timeframe]
**Resource Requirements:** [Estimated resources needed]
**Success Metrics:** [How to measure success]

### Priority 5: [Specific Action Area]
**Recommendation:** [Detailed recommendation]
**Expected Impact:** [Specific impact on ESG/SDG performance]
**Implementation Timeline:** [Suggested timeframe]
**Resource Requirements:** [Estimated resources needed]
**Success Metrics:** [How to measure success]

## Key Performance Indicators (KPIs) Assessment

### Environmental KPIs
- [List specific environmental metrics found in document with values]

### Social KPIs  
- [List specific social metrics found in document with values]

### Economic KPIs
- [List specific economic metrics found in document with values]

### Governance KPIs
- [List specific governance metrics found in document with values]

## Compliance and Standards Assessment
- **Global Reporting Initiative (GRI):** [Assessment of GRI compliance]
- **UN Global Compact:** [Assessment of UNGC alignment]
- **Task Force on Climate-related Financial Disclosures (TCFD):** [TCFD assessment]
- **Sustainability Accounting Standards Board (SASB):** [SASB assessment]

---
*Comprehensive analysis completed using advanced AI sustainability framework*
*Document processed: {pages_count} pages, {len(full_text)} characters*

IMPORTANT: Base your analysis ENTIRELY on the actual content provided. Use specific data, quotes, and evidence from the document. Provide realistic scores based on actual performance indicators found in the text.

COMPLETE DOCUMENT CONTENT TO ANALYZE:

{full_text}

Please analyze this complete document thoroughly and provide comprehensive, evidence-based insights with specific scores and detailed recommendations.
"""
        
        return prompt
    
    def _make_api_call(self, prompt: str, retry_count: int = 3) -> str:
        """Make API call with retry logic"""
        for attempt in range(retry_count):
            try:
                if attempt > 0:
                    wait_time = self.request_delay * (2 ** attempt)
                    self.logger.info(f"⏳ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                
                self.logger.info(f"📡 Making API call (attempt {attempt + 1}/{retry_count})")
                response = self.model.generate_content(prompt)
                
                if response and response.text:
                    self.logger.info(f"✅ Received response: {len(response.text)} characters")
                    return response.text
                else:
                    raise Exception("Empty response from API")
                    
            except Exception as e:
                error_msg = str(e).lower()
                if "quota" in error_msg or "limit" in error_msg:
                    self.logger.error(f"💰 API quota exceeded: {str(e)}")
                    if attempt == retry_count - 1:
                        raise Exception(f"API quota exceeded after {retry_count} attempts")
                else:
                    self.logger.error(f"❌ API call failed: {str(e)}")
                    if attempt == retry_count - 1:
                        raise Exception(f"API call failed after {retry_count} attempts: {str(e)}")
        
        raise Exception("All API attempts failed")
    
    def _parse_markdown_response(self, markdown_text: str, language: str) -> Dict:
        """Parse comprehensive markdown response into structured format"""
        try:
            self.logger.info("🔍 Parsing comprehensive markdown response...")
            
            # Extract main sections
            sections = self._extract_sections(markdown_text)
            
            # Extract scores
            scores = self._extract_all_scores(markdown_text)
            
            # Extract structured data
            result = {
                'executive_summary': sections.get('executive_summary', 'Executive summary not found'),
                'esg_analysis': {
                    'economic_financial_performance': self._extract_esg_section(markdown_text, 'economic'),
                    'environmental_performance': self._extract_esg_section(markdown_text, 'environmental'),  
                    'social_performance': self._extract_esg_section(markdown_text, 'social')
                },
                'sdg_mapping': self._extract_sdg_mapping(markdown_text),
                'recommendations': self._extract_recommendations(markdown_text),
                'kpis_assessment': self._extract_kpis(markdown_text),
                'compliance_assessment': self._extract_compliance(markdown_text),
                'raw_markdown': markdown_text  # Keep full markdown for reference
            }
            
            self.logger.info("✅ Markdown parsing completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Markdown parsing failed: {str(e)}")
            return {
                'executive_summary': 'Parsing failed - using raw response',
                'raw_markdown': markdown_text,
                'parsing_error': str(e)
            }
    
    def _extract_sections(self, markdown_text: str) -> Dict:
        """Extract main sections from markdown"""
        sections = {}
        
        # Extract executive summary
        exec_match = re.search(r'## Executive Summary\s*\n(.*?)(?=##|\Z)', markdown_text, re.DOTALL | re.IGNORECASE)
        if exec_match:
            sections['executive_summary'] = exec_match.group(1).strip()
        
        return sections
    
    def _extract_all_scores(self, markdown_text: str) -> Dict:
        """Extract all numerical scores from markdown"""
        scores = {}
        
        # Extract ESG scores
        esg_patterns = {
            'economic': r'Economic.*?Performance.*?Score:\s*(\d+(?:\.\d+)?)',
            'environmental': r'Environmental.*?Performance.*?Score:\s*(\d+(?:\.\d+)?)',
            'social': r'Social.*?Performance.*?Score:\s*(\d+(?:\.\d+)?)'
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
    
    def _extract_esg_section(self, markdown_text: str, category: str) -> Dict:
        """Extract detailed ESG section analysis"""
        category_patterns = {
            'economic': r'### 💼 Economic.*?(?=###|\Z)',
            'environmental': r'### 🌍 Environmental.*?(?=###|\Z)',
            'social': r'### 👥 Social.*?(?=###|\Z)'
        }
        
        pattern = category_patterns.get(category, '')
        if not pattern:
            return {}
        
        match = re.search(pattern, markdown_text, re.DOTALL | re.IGNORECASE)
        if not match:
            return {}
        
        section_text = match.group()
        
        # Extract score
        score_match = re.search(r'Score:\s*(\d+(?:\.\d+)?)', section_text)
        score = float(score_match.group(1)) if score_match else 0
        
        # Extract strengths
        strengths_match = re.search(r'Key Strengths:\*\*(.*?)(?=\*\*Areas|\*\*Supporting|\Z)', section_text, re.DOTALL)
        strengths = self._parse_bullet_points(strengths_match.group(1)) if strengths_match else []
        
        # Extract weaknesses/improvements
        improvements_match = re.search(r'Areas for Improvement:\*\*(.*?)(?=\*\*Supporting|\*\*Environmental|\Z)', section_text, re.DOTALL)
        improvements = self._parse_bullet_points(improvements_match.group(1)) if improvements_match else []
        
        # Extract evidence
        evidence_match = re.search(r'Supporting Evidence:\*\*(.*?)(?=\*\*|\Z)', section_text, re.DOTALL)
        evidence = evidence_match.group(1).strip() if evidence_match else ""
        
        return {
            'score': score,
            'strengths': strengths,
            'weaknesses': improvements,
            'evidence': evidence
        }
    
    def _extract_sdg_mapping(self, markdown_text: str) -> Dict:
        """Extract individual SDG mappings"""
        sdg_mapping = {}
        
        # Find all SDG sections
        sdg_pattern = r'#### SDG (\d+): ([^(]+)\(Score: (\d+(?:\.\d+)?)\)(.*?)(?=####|\Z)'
        sdg_matches = re.findall(sdg_pattern, markdown_text, re.DOTALL | re.IGNORECASE)
        
        for sdg_num, sdg_name, score, content in sdg_matches:
            sdg_key = f"sdg_{sdg_num}"
            
            # Extract contribution
            contrib_match = re.search(r'Company\'s.*?Contribution:\*\*(.*?)(?=\*\*|\n\n)', content, re.DOTALL)
            contribution = contrib_match.group(1).strip() if contrib_match else ""
            
            # Extract evidence
            evidence_match = re.search(r'Evidence.*?:\*\*(.*?)(?=\*\*|\n\n)', content, re.DOTALL)
            evidence = evidence_match.group(1).strip() if evidence_match else ""
            
            # Extract improvement opportunities
            improve_match = re.search(r'Improvement.*?:\*\*(.*?)(?=\*\*|\Z)', content, re.DOTALL)
            improvements = improve_match.group(1).strip() if improve_match else ""
            
            sdg_mapping[sdg_key] = {
                'score': float(score),
                'name': sdg_name.strip(),
                'impact_level': 'High' if float(score) >= 7 else 'Medium' if float(score) >= 4 else 'Low',
                'contributions': [contribution] if contribution else [],
                'evidence': evidence,
                'improvement_areas': [improvements] if improvements else []
            }
        
        # Ensure all 17 SDGs are present
        for i in range(1, 18):
            sdg_key = f"sdg_{i}"
            if sdg_key not in sdg_mapping:
                sdg_mapping[sdg_key] = {
                    'score': 0,
                    'name': SDG_GOALS.get(sdg_key, f"SDG {i}"),
                    'impact_level': 'None',
                    'contributions': [],
                    'evidence': '',
                    'improvement_areas': []
                }
        
        return sdg_mapping
    
    def _extract_recommendations(self, markdown_text: str) -> List[str]:
        """Extract strategic recommendations"""
        recommendations = []
        
        # Find priority recommendations
        priority_pattern = r'### Priority \d+: ([^#]+?)(?=###|\Z)'
        priority_matches = re.findall(priority_pattern, markdown_text, re.DOTALL | re.IGNORECASE)
        
        for match in priority_matches:
            # Clean up the recommendation text
            clean_rec = re.sub(r'\*\*[^*]+\*\*', '', match)  # Remove bold formatting
            clean_rec = re.sub(r'\n+', ' ', clean_rec)  # Replace newlines with spaces
            clean_rec = clean_rec.strip()
            if clean_rec:
                recommendations.append(clean_rec)
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _extract_kpis(self, markdown_text: str) -> Dict:
        """Extract KPIs assessment"""
        kpis = {}
        
        kpi_section_match = re.search(r'## Key Performance Indicators.*?(?=##|\Z)', markdown_text, re.DOTALL | re.IGNORECASE)
        if kpi_section_match:
            kpis['raw_content'] = kpi_section_match.group().strip()
        
        return kpis
    
    def _extract_compliance(self, markdown_text: str) -> Dict:
        """Extract compliance assessment"""
        compliance = {}
        
        compliance_section_match = re.search(r'## Compliance and Standards.*?(?=##|\Z)', markdown_text, re.DOTALL | re.IGNORECASE)
        if compliance_section_match:
            compliance['raw_content'] = compliance_section_match.group().strip()
        
        return compliance
    
    def _parse_bullet_points(self, text: str) -> List[str]:
        """Parse bullet points from text"""
        points = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('*'):
                clean_line = line[1:].strip()
                if clean_line:
                    points.append(clean_line)
        
        return points
    
    def _create_error_response(self, error_type: str, error_message: str) -> Dict:
        """Create error response structure"""
        return {
            'error': True,
            'error_type': error_type,
            'error_message': error_message,
            'timestamp': pd.Timestamp.now().isoformat()
        } 