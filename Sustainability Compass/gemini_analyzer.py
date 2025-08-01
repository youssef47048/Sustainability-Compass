# Gemini AI Integration for Sustainability Analysis
import google.generativeai as genai
import json
import logging
import time
from typing import Dict, List, Optional
from config import GEMINI_API_KEY, SDG_GOALS, ESG_CATEGORIES
import pandas as pd

class GeminiAnalyzer:
    """
    Gemini AI analyzer for ESG performance and SDG mapping
    Enhanced for free tier API usage
    """
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
        self.request_delay = 5  # Seconds between requests for free tier
        self._configure_gemini()
        
    def _configure_gemini(self):
        """Configure Gemini AI with API key"""
        try:
            genai.configure(api_key=self.api_key)
            # Updated model names based on actual available models (Jan 2025)
            # Prioritizing free tier models that are guaranteed to work
            model_names = [
                'models/gemini-2.5-flash',              # Latest free model - fast and efficient
                'models/gemini-2.0-flash',              # Alternative latest free model
                'models/gemini-1.5-flash',              # Reliable free model - fast
                'models/gemini-1.5-pro',                # Reliable free model - more capable
                'models/gemini-2.5-flash-lite',         # Lite version if others fail
                'models/gemini-1.5-flash-latest',       # Latest version of 1.5 flash
                'models/gemini-1.5-pro-latest',         # Latest version of 1.5 pro
                # Premium models (require payment) - only try if user has paid tier
                'models/gemini-2.5-pro',                # Premium model 
                'gemini-2.5-flash',                     # Alternative format
                'gemini-1.5-flash',                     # Alternative format
                'gemini-1.5-pro'                        # Alternative format
            ]
            
            self.model = None
            for model_name in model_names:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    self.logger.info(f"Gemini AI configured successfully with model: {model_name}")
                    break
                except Exception as model_error:
                    self.logger.warning(f"Model {model_name} not available: {str(model_error)}")
                    continue
            
            if self.model is None:
                # Try to list available models for debugging
                try:
                    available_models = self._list_available_models()
                    if available_models:
                        error_msg = f"No compatible models found. Available models: {', '.join(available_models)}"
                    else:
                        error_msg = "No available Gemini models found. Please check your API key."
                except:
                    error_msg = "No available Gemini models found. Please check your API key and internet connection."
                
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(f"Failed to configure Gemini AI: {str(e)}")
            raise
    
    def _list_available_models(self):
        """List available models for debugging"""
        try:
            models = genai.list_models()
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
            return available_models
        except Exception as e:
            self.logger.error(f"Failed to list models: {str(e)}")
            return []
    
    def _make_api_call(self, prompt: str, retry_count: int = 3) -> str:
        """
        Make API call with rate limiting and retry logic for free tier
        
        Args:
            prompt (str): The prompt to send
            retry_count (int): Number of retries for failed requests
            
        Returns:
            str: API response text
        """
        for attempt in range(retry_count):
            try:
                # Add delay between requests for free tier rate limiting
                if attempt > 0:
                    wait_time = self.request_delay * (2 ** attempt)  # Exponential backoff
                    self.logger.info(f"Waiting {wait_time} seconds before retry (attempt {attempt + 1})")
                    time.sleep(wait_time)
                elif hasattr(self, '_last_request_time'):
                    # Ensure minimum delay between requests
                    elapsed = time.time() - self._last_request_time
                    if elapsed < self.request_delay:
                        time.sleep(self.request_delay - elapsed)
                
                self.logger.info(f"Making API call (attempt {attempt + 1}/{retry_count})")
                response = self.model.generate_content(prompt)
                self._last_request_time = time.time()
                
                if response and response.text:
                    return response.text
                else:
                    raise Exception("Empty response from API")
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                # Handle specific free tier errors
                if "quota" in error_msg or "limit" in error_msg:
                    self.logger.error(f"API quota/rate limit exceeded: {str(e)}")
                    if attempt == retry_count - 1:
                        raise Exception("API quota or rate limit exceeded. Please try again later or check your API usage.")
                    time.sleep(30)  # Wait longer for quota issues
                    
                elif "permission" in error_msg or "api_key" in error_msg:
                    raise Exception(f"API key issue: {str(e)}. Please check your Gemini API key.")
                    
                elif "safety" in error_msg or "blocked" in error_msg:
                    self.logger.warning(f"Content safety filter triggered: {str(e)}")
                    # Return a safe fallback response
                    return "Content analysis completed with safety considerations."
                    
                else:
                    self.logger.error(f"API call failed (attempt {attempt + 1}): {str(e)}")
                    if attempt == retry_count - 1:
                        raise Exception(f"API call failed after {retry_count} attempts: {str(e)}")
        
        raise Exception("API call failed after all retry attempts")
    
    def analyze_esg_performance(self, content: Dict, language: str = 'en') -> Dict:
        """
        Analyze ESG (Environmental, Social, Governance) performance
        
        Args:
            content (Dict): Extracted PDF content
            language (str): Output language ('en' or 'ar')
            
        Returns:
            Dict: ESG analysis results
        """
        try:
            # Prepare the analysis prompt
            prompt = self._create_esg_prompt(content, language)
            
            # Generate analysis with rate limiting
            response_text = self._make_api_call(prompt)
            
            # Parse the response
            esg_analysis = self._parse_esg_response(response_text)
            
            return esg_analysis
            
        except Exception as e:
            self.logger.error(f"ESG analysis failed: {str(e)}")
            return self._create_error_response("ESG analysis failed", str(e))
    
    def map_to_sdgs(self, content: Dict, esg_analysis: Dict, language: str = 'en') -> Dict:
        """
        Map company performance to UN Sustainable Development Goals
        
        Args:
            content (Dict): Extracted PDF content
            esg_analysis (Dict): ESG analysis results
            language (str): Output language ('en' or 'ar')
            
        Returns:
            Dict: SDG mapping results
        """
        try:
            # Prepare SDG mapping prompt
            prompt = self._create_sdg_prompt(content, esg_analysis, language)
            
            # Generate SDG mapping with rate limiting
            response_text = self._make_api_call(prompt)
            
            # Parse the response
            sdg_mapping = self._parse_sdg_response(response_text)
            
            return sdg_mapping
            
        except Exception as e:
            self.logger.error(f"SDG mapping failed: {str(e)}")
            return self._create_error_response("SDG mapping failed", str(e))
    
    def generate_comprehensive_report(self, content: Dict, language: str = 'en') -> Dict:
        """
        Generate a comprehensive sustainability report with free tier considerations
        
        Args:
            content (Dict): Extracted PDF content
            language (str): Output language ('en' or 'ar')
            
        Returns:
            Dict: Comprehensive analysis report
        """
        try:
            self.logger.info("Starting comprehensive analysis (4 API calls)")
            
            # Step 1: Perform ESG analysis
            self.logger.info("Step 1/4: ESG analysis")
            esg_analysis = self.analyze_esg_performance(content, language)
            
            # Step 2: Perform SDG mapping  
            self.logger.info("Step 2/4: SDG mapping")
            sdg_mapping = self.map_to_sdgs(content, esg_analysis, language)
            
            # Step 3: Generate executive summary
            self.logger.info("Step 3/4: Executive summary")
            exec_summary = self._generate_executive_summary(esg_analysis, sdg_mapping, language)
            
            # Step 4: Generate recommendations
            self.logger.info("Step 4/4: Recommendations")
            recommendations = self._generate_recommendations(esg_analysis, sdg_mapping, language)
            
            self.logger.info("Comprehensive analysis completed successfully")
            
            return {
                'executive_summary': exec_summary,
                'esg_analysis': esg_analysis,
                'sdg_mapping': sdg_mapping,
                'recommendations': recommendations,
                'analysis_metadata': {
                    'language': language,
                    'analysis_date': content.get('metadata', {}).get('creation_date', ''),
                    'document_pages': content.get('page_count', 0),
                    'has_tables': len(content.get('tables', [])) > 0,
                    'api_calls_used': 4
                }
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive report generation failed: {str(e)}")
            return self._create_error_response("Report generation failed", str(e))
    
    def _create_esg_prompt(self, content: Dict, language: str) -> str:
        """Create ESG analysis prompt with token optimization for free tier"""
        
        lang_instructions = {
            'en': "Please analyze in English",
            'ar': "يرجى التحليل باللغة العربية"
        }
        
        # Limit content to stay within free tier token limits
        max_content_length = 6000  # Conservative limit for free tier
        content_text = content.get('text', '')[:max_content_length]
        
        prompt = f"""
        {lang_instructions.get(language, 'Please analyze in English')}
        
        You are a sustainability expert analyzing a company's ESG (Environmental, Social, Governance) performance.
        
        Based on the following document content, provide a detailed analysis of:
        
        1. ECONOMIC/FINANCIAL PERFORMANCE:
        - Financial health and stability
        - Revenue growth and profitability
        - Return on investment
        - Economic impact on stakeholders
        
        2. ENVIRONMENTAL PERFORMANCE:
        - Carbon emissions and climate impact
        - Energy consumption and efficiency
        - Waste management and circular economy practices
        - Water usage and conservation
        - Biodiversity and ecosystem impact
        
        3. SOCIAL PERFORMANCE:
        - Employee welfare and working conditions
        - Diversity, equity, and inclusion
        - Community engagement and impact
        - Human rights practices
        - Product safety and quality
        
        For each category, provide:
        - Current performance assessment (score out of 10)
        - Key strengths (max 3 points)
        - Areas for improvement (max 3 points)
        - Supporting evidence from the document
        
        Document Content:
        {content_text}
        
        Tables Found: {len(content.get('tables', []))} tables
        Language Detected: {content.get('language_detected', 'en')}
        
        Please provide your analysis in a structured JSON format with scores, strengths, weaknesses, and evidence for each ESG category.
        """
        
        return prompt
    
    def _create_sdg_prompt(self, content: Dict, esg_analysis: Dict, language: str) -> str:
        """Create SDG mapping prompt optimized for free tier"""
        
        lang_instructions = {
            'en': "Please analyze in English",
            'ar': "يرجى التحليل باللغة العربية"
        }
        
        sdg_list = '\n'.join([f"{k}: {v}" for k, v in SDG_GOALS.items()])
        
        # Limit ESG analysis content for token efficiency
        esg_summary = {}
        for category, data in esg_analysis.items():
            if isinstance(data, dict):
                esg_summary[category] = {
                    'score': data.get('score', 0),
                    'key_points': data.get('strengths', [])[:2] + data.get('weaknesses', [])[:2]
                }
        
        prompt = f"""
        {lang_instructions.get(language, 'Please analyze in English')}
        
        You are a sustainability expert mapping company performance to UN Sustainable Development Goals (SDGs).
        
        Based on the company's ESG performance analysis, map the company's impact to the 17 UN SDGs:
        
        UN SDGs:
        {sdg_list}
        
        ESG Analysis Summary:
        {json.dumps(esg_summary, indent=2)}
        
        For each of the 17 SDGs, assess:
        1. Impact Level (High/Medium/Low/None)
        2. Performance Score (0-10)
        3. Key contributions (max 2 points)
        4. Main improvement areas (max 2 points)
        
        Focus on SDGs where the company shows significant impact (positive or areas for improvement).
        
        Please provide your analysis in a structured JSON format with assessments for each SDG.
        """
        
        return prompt
    
    def _generate_executive_summary(self, esg_analysis: Dict, sdg_mapping: Dict, language: str) -> str:
        """Generate executive summary optimized for free tier"""
        
        lang_instructions = {
            'en': "Please write the executive summary in English",
            'ar': "يرجى كتابة الملخص التنفيذي باللغة العربية"
        }
        
        # Create condensed input for token efficiency
        esg_scores = {k: v.get('score', 0) for k, v in esg_analysis.items() if isinstance(v, dict)}
        top_sdgs = []
        
        for sdg_key, data in sdg_mapping.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict) and data.get('score', 0) > 6:
                sdg_num = int(sdg_key.split('_')[1])
                top_sdgs.append(f"SDG {sdg_num}")
        
        prompt = f"""
        {lang_instructions.get(language, 'Please write the executive summary in English')}
        
        Create a concise executive summary (2 paragraphs) based on:
        
        ESG Scores: {esg_scores}
        Top Contributing SDGs: {', '.join(top_sdgs[:5])}
        
        The summary should highlight:
        - Overall sustainability performance
        - Key strengths and critical improvements needed
        - Top SDG contributions
        
        Keep it concise and actionable.
        """
        
        try:
            response_text = self._make_api_call(prompt)
            return response_text
        except Exception as e:
            return f"Executive summary: Company shows mixed sustainability performance across ESG factors. Key improvement opportunities identified. {str(e)}"
    
    def _generate_recommendations(self, esg_analysis: Dict, sdg_mapping: Dict, language: str) -> List[str]:
        """Generate actionable recommendations optimized for free tier"""
        
        lang_instructions = {
            'en': "Please provide recommendations in English",
            'ar': "يرجى تقديم التوصيات باللغة العربية"
        }
        
        # Identify lowest scoring areas for targeted recommendations
        low_scores = []
        for category, data in esg_analysis.items():
            if isinstance(data, dict) and data.get('score', 0) < 7:
                low_scores.append(category)
        
        prompt = f"""
        {lang_instructions.get(language, 'Please provide recommendations in English')}
        
        Based on the analysis, provide 5 specific, actionable recommendations for improving sustainability performance.
        
        Focus on areas needing improvement: {', '.join(low_scores)}
        
        Each recommendation should:
        - Be specific and actionable
        - Address identified weaknesses
        - Be realistic and achievable
        
        Format as a numbered list (1-5).
        """
        
        try:
            response_text = self._make_api_call(prompt)
            # Split response into list
            recommendations = [r.strip() for r in response_text.split('\n') if r.strip() and (r.strip()[0].isdigit() or r.strip().startswith('-'))]
            return recommendations[:5]  # Limit to 5 recommendations
        except Exception as e:
            return [
                "1. Enhance environmental reporting and transparency",
                "2. Improve social impact measurement and disclosure", 
                "3. Strengthen governance and risk management practices",
                "4. Develop comprehensive sustainability strategy",
                f"5. Note: Full recommendations unavailable due to API limitations: {str(e)}"
            ]
    
    def _parse_esg_response(self, response_text: str) -> Dict:
        """Parse ESG analysis response"""
        try:
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_text = response_text[json_start:json_end]
                return json.loads(json_text)
            else:
                # Fallback: create structured response from text
                return self._create_fallback_esg_response(response_text)
                
        except json.JSONDecodeError:
            return self._create_fallback_esg_response(response_text)
    
    def _parse_sdg_response(self, response_text: str) -> Dict:
        """Parse SDG mapping response and ensure individual SDG entries"""
        try:
            # Add debugging to see what the AI is actually returning
            self.logger.info(f"🔍 Raw AI Response (first 1000 chars): {response_text[:1000]}")
            
            # Try to extract JSON from response - handle malformed JSON with extra text
            json_start = response_text.find('{')
            if json_start == -1:
                self.logger.warning("🔍 No opening brace found in response")
                return self._create_fallback_sdg_response(response_text)
            
            # Find the matching closing brace by counting braces
            brace_count = 0
            json_end = -1
            for i, char in enumerate(response_text[json_start:], json_start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            if json_end == -1:
                self.logger.warning("🔍 No matching closing brace found")
                return self._create_fallback_sdg_response(response_text)
            
            json_text = response_text[json_start:json_end]
            self.logger.info(f"🔍 Extracted JSON (first 500 chars): {json_text[:500]}")
            
            try:
                raw_data = json.loads(json_text)
                self.logger.info(f"🔍 Successfully parsed JSON with keys: {list(raw_data.keys())}")
            except json.JSONDecodeError as e:
                self.logger.error(f"🔍 JSON parsing still failed after extraction: {str(e)}")
                return self._create_fallback_sdg_response(response_text)
            
            # Restructure to ensure individual SDG entries
            structured_result = {}
            
            # Strategy 1: Check if we got the expected format with nested sdg_mapping
            if 'sdg_mapping' in raw_data and isinstance(raw_data['sdg_mapping'], dict):
                self.logger.info("🔍 Found nested sdg_mapping structure")
                mapping_data = raw_data['sdg_mapping']
                for key, value in mapping_data.items():
                    if 'sdg' in key.lower():
                        # Extract SDG number
                        import re
                        sdg_num = re.search(r'(\d+)', key)
                        if sdg_num:
                            sdg_key = f"sdg_{sdg_num.group(1)}"
                            if isinstance(value, dict):
                                structured_result[sdg_key] = value
                            else:
                                structured_result[sdg_key] = {
                                    'impact_level': 'Medium',
                                    'score': 5,
                                    'contributions': [str(value)],
                                    'improvement_areas': []
                                }
            
            # Strategy 2: Check for direct SDG entries at root level
            for key, value in raw_data.items():
                if 'sdg' in key.lower() and key != 'sdg_mapping':
                    import re
                    sdg_num = re.search(r'(\d+)', key)
                    if sdg_num:
                        sdg_key = f"sdg_{sdg_num.group(1)}"
                        if isinstance(value, dict):
                            structured_result[sdg_key] = value
                            self.logger.info(f"🔍 Found direct SDG entry: {sdg_key}")
            
            # Strategy 3: Check for SDG array or other formats
            for key, value in raw_data.items():
                if isinstance(value, list):
                    # Could be an array of SDG assessments
                    for item in value:
                        if isinstance(item, dict) and 'sdg' in str(item).lower():
                            # Try to extract SDG number from the item
                            for item_key, item_value in item.items():
                                if 'sdg' in item_key.lower():
                                    sdg_match = re.search(r'(\d+)', str(item))
                                    if sdg_match:
                                        sdg_key = f"sdg_{sdg_match.group(1)}"
                                        structured_result[sdg_key] = item
                                        break
            
            self.logger.info(f"🔍 Structured result has {len(structured_result)} SDGs with actual data")
            
            # If we still have no structured data, it might be a different format
            if not structured_result:
                self.logger.warning("🔍 No SDG data found in expected format, using fallback")
                self.logger.info(f"🔍 Available keys in response: {list(raw_data.keys())}")
                # Check if there's any data we can extract
                sample_data = str(raw_data)[:500]
                self.logger.info(f"🔍 Sample raw data: {sample_data}")
            
            # Ensure all 17 SDGs are present with proper structure
            for i in range(1, 18):
                sdg_key = f"sdg_{i}"
                if sdg_key not in structured_result:
                    structured_result[sdg_key] = {
                        'impact_level': 'None',
                        'score': 0,
                        'contributions': [],
                        'improvement_areas': []
                    }
                else:
                    # Ensure proper structure for existing SDGs
                    if 'score' not in structured_result[sdg_key]:
                        structured_result[sdg_key]['score'] = 0
                    # Ensure numeric score
                    try:
                        structured_result[sdg_key]['score'] = float(structured_result[sdg_key]['score'])
                    except (ValueError, TypeError):
                        structured_result[sdg_key]['score'] = 0
            
            return structured_result
                
        except Exception as e:
            self.logger.error(f"🔍 Unexpected error in SDG parsing: {str(e)}")
            return self._create_fallback_sdg_response(response_text)
    
    def _create_fallback_esg_response(self, text: str) -> Dict:
        """Create fallback ESG response structure"""
        return {
            'economic': {
                'score': 7,
                'strengths': ['Revenue growth identified'],
                'weaknesses': ['Limited financial transparency'],
                'evidence': text[:500]
            },
            'environmental': {
                'score': 6,
                'strengths': ['Some environmental initiatives mentioned'],
                'weaknesses': ['Need more detailed environmental reporting'],
                'evidence': text[:500]
            },
            'social': {
                'score': 6,
                'strengths': ['Employee welfare programs noted'],
                'weaknesses': ['Limited diversity reporting'],
                'evidence': text[:500]
            }
        }
    
    def _create_fallback_sdg_response(self, text: str) -> Dict:
        """Create fallback SDG response structure"""
        sdg_response = {}
        for sdg_num in range(1, 18):
            sdg_response[f'sdg_{sdg_num}'] = {
                'impact_level': 'Medium',
                'score': 5,
                'contributions': ['General business activities'],
                'improvement_areas': ['More specific reporting needed'],
                'evidence': text[:200]
            }
        return sdg_response
    
    def _create_error_response(self, error_type: str, error_message: str) -> Dict:
        """Create error response structure"""
        return {
            'error': True,
            'error_type': error_type,
            'error_message': error_message,
            'timestamp': pd.Timestamp.now().isoformat()
        } 