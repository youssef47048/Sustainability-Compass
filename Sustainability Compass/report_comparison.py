#!/usr/bin/env python3
"""
Multi-Report Comparison Module
Handles comparison of sustainability reports across multiple years
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import pandas as pd
import google.generativeai as genai
from config import GEMINI_API_KEY, SDG_GOALS, ESG_CATEGORIES

class ReportComparison:
    """
    Manages storage, comparison, and analysis of multiple sustainability reports
    """
    
    def __init__(self, storage_dir: str = "stored_reports"):
        self.storage_dir = storage_dir
        self.logger = logging.getLogger(__name__)
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize Gemini for comparative analysis
        self._setup_gemini()
        
    def _setup_gemini(self):
        """Setup Gemini AI for comparative analysis"""
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            # Use the same model priority as the main analyzer
            model_names = [
                'models/gemini-2.5-flash',
                'models/gemini-2.0-flash', 
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro'
            ]
            
            self.model = None
            for model_name in model_names:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    self.logger.info(f"✅ Comparison engine configured with: {model_name}")
                    break
                except Exception as model_error:
                    continue
                    
            if self.model is None:
                raise Exception("No compatible Gemini models found for comparison!")
                
        except Exception as e:
            self.logger.error(f"Failed to setup Gemini for comparison: {str(e)}")
            self.model = None
    
    def store_report(self, company_name: str, year: int, analysis_results: Dict, 
                     metadata: Optional[Dict] = None) -> bool:
        """
        Store a report for future comparison
        
        Args:
            company_name (str): Company identifier
            year (int): Report year
            analysis_results (Dict): Complete analysis results from analyzer
            metadata (Dict): Additional metadata (file info, analysis date, etc.)
            
        Returns:
            bool: Success status
        """
        try:
            # Create company directory
            company_dir = os.path.join(self.storage_dir, self._sanitize_name(company_name))
            os.makedirs(company_dir, exist_ok=True)
            
            # Prepare report data
            report_data = {
                'company_name': company_name,
                'year': year,
                'analysis_date': datetime.now().isoformat(),
                'analysis_results': analysis_results,
                'metadata': metadata or {}
            }
            
            # Save report
            filename = f"report_{year}.json"
            filepath = os.path.join(company_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Stored report for {company_name} ({year})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to store report: {str(e)}")
            return False
    
    def get_company_reports(self, company_name: str) -> Dict[int, Dict]:
        """
        Get all stored reports for a company
        
        Args:
            company_name (str): Company identifier
            
        Returns:
            Dict[int, Dict]: Reports indexed by year
        """
        try:
            company_dir = os.path.join(self.storage_dir, self._sanitize_name(company_name))
            
            if not os.path.exists(company_dir):
                return {}
            
            reports = {}
            for filename in os.listdir(company_dir):
                if filename.startswith('report_') and filename.endswith('.json'):
                    try:
                        year = int(filename.replace('report_', '').replace('.json', ''))
                        filepath = os.path.join(company_dir, filename)
                        
                        with open(filepath, 'r', encoding='utf-8') as f:
                            report_data = json.load(f)
                        
                        reports[year] = report_data
                        
                    except (ValueError, json.JSONDecodeError) as e:
                        self.logger.warning(f"⚠️ Skipping invalid report file: {filename}")
                        continue
            
            return reports
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get reports for {company_name}: {str(e)}")
            return {}
    
    def get_all_companies(self) -> List[str]:
        """Get list of all companies with stored reports"""
        try:
            if not os.path.exists(self.storage_dir):
                return []
            
            companies = []
            for item in os.listdir(self.storage_dir):
                item_path = os.path.join(self.storage_dir, item)
                if os.path.isdir(item_path):
                    # Check if directory has any report files
                    if any(f.startswith('report_') and f.endswith('.json') 
                          for f in os.listdir(item_path)):
                        companies.append(item)
            
            return sorted(companies)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get companies list: {str(e)}")
            return []
    
    def compare_reports(self, company_name: str, years: List[int]) -> Dict:
        """
        Compare multiple reports for the same company
        
        Args:
            company_name (str): Company identifier
            years (List[int]): Years to compare
            
        Returns:
            Dict: Comprehensive comparison analysis
        """
        try:
            self.logger.info(f"🔍 Comparing reports for {company_name}: {years}")
            
            # Get reports for specified years
            all_reports = self.get_company_reports(company_name)
            selected_reports = {year: all_reports[year] for year in years if year in all_reports}
            
            if len(selected_reports) < 2:
                raise ValueError("At least 2 reports needed for comparison")
            
            # Prepare comparison data
            comparison_data = self._prepare_comparison_data(selected_reports)
            
            # Generate AI-powered comparative analysis
            ai_analysis = self._generate_comparative_analysis(company_name, comparison_data)
            
            # Calculate trends and metrics
            trends = self._calculate_trends(comparison_data)
            
            # Compile comprehensive comparison
            comparison_result = {
                'company_name': company_name,
                'years_compared': sorted(years),
                'comparison_date': datetime.now().isoformat(),
                'reports_data': selected_reports,
                'comparison_data': comparison_data,
                'ai_analysis': ai_analysis,
                'trends': trends,
                'summary': self._generate_comparison_summary(comparison_data, trends)
            }
            
            self.logger.info(f"✅ Comparison completed for {company_name}")
            return comparison_result
            
        except Exception as e:
            self.logger.error(f"❌ Comparison failed: {str(e)}")
            raise Exception(f"Comparison failed: {str(e)}")
    
    def _prepare_comparison_data(self, reports: Dict[int, Dict]) -> Dict:
        """Prepare structured data for comparison"""
        comparison_data = {
            'esg_scores': {},
            'sdg_scores': {},
            'kpis': {},
            'recommendations': {},
            'executive_summaries': {}
        }
        
        for year, report in reports.items():
            analysis = report['analysis_results']
            
            # Extract ESG scores
            esg_analysis = analysis.get('esg_analysis', {})
            comparison_data['esg_scores'][year] = {}
            
            for category, data in esg_analysis.items():
                if isinstance(data, dict) and 'score' in data:
                    comparison_data['esg_scores'][year][category] = data['score']
            
            # Extract SDG scores
            sdg_mapping = analysis.get('sdg_mapping', {})
            comparison_data['sdg_scores'][year] = {}
            
            for sdg, data in sdg_mapping.items():
                if isinstance(data, dict) and data.get('score', 0) > 0:
                    comparison_data['sdg_scores'][year][sdg] = data['score']
            
            # Extract other data
            comparison_data['recommendations'][year] = analysis.get('recommendations', [])
            comparison_data['executive_summaries'][year] = analysis.get('executive_summary', '')
        
        return comparison_data
    
    def _calculate_trends(self, comparison_data: Dict) -> Dict:
        """Calculate trends across years"""
        trends = {
            'esg_trends': {},
            'sdg_trends': {},
            'overall_progress': {}
        }
        
        # ESG trends
        esg_data = comparison_data['esg_scores']
        years = sorted(esg_data.keys())
        
        for category in ESG_CATEGORIES:
            category_scores = []
            for year in years:
                score = esg_data.get(year, {}).get(category, 0)
                category_scores.append(score)
            
            if len(category_scores) >= 2:
                trends['esg_trends'][category] = {
                    'scores': dict(zip(years, category_scores)),
                    'change': category_scores[-1] - category_scores[0],
                    'trend': 'improving' if category_scores[-1] > category_scores[0] else 'declining'
                }
        
        # SDG trends
        sdg_data = comparison_data['sdg_scores']
        all_sdgs = set()
        for year_data in sdg_data.values():
            all_sdgs.update(year_data.keys())
        
        for sdg in all_sdgs:
            sdg_scores = []
            for year in years:
                score = sdg_data.get(year, {}).get(sdg, 0)
                sdg_scores.append(score)
            
            if any(score > 0 for score in sdg_scores):
                trends['sdg_trends'][sdg] = {
                    'scores': dict(zip(years, sdg_scores)),
                    'change': sdg_scores[-1] - sdg_scores[0],
                    'trend': 'improving' if sdg_scores[-1] > sdg_scores[0] else 'declining'
                }
        
        return trends
    
    def _generate_comparative_analysis(self, company_name: str, comparison_data: Dict) -> str:
        """Generate AI-powered comparative analysis"""
        if not self.model:
            return "AI comparative analysis not available (Gemini not configured)"
        
        try:
            # Prepare comprehensive prompt
            prompt = self._create_comparison_prompt(company_name, comparison_data)
            
            # Generate analysis
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            self.logger.error(f"❌ AI comparative analysis failed: {str(e)}")
            return f"AI analysis failed: {str(e)}"
    
    def _create_comparison_prompt(self, company_name: str, comparison_data: Dict) -> str:
        """Create comprehensive comparison prompt for Gemini"""
        
        # Extract years
        years = sorted(comparison_data['esg_scores'].keys())
        
        prompt = f"""# Sustainability Report Comparison Analysis

Analyze the sustainability performance trends for **{company_name}** across multiple years: {', '.join(map(str, years))}.

## ESG Performance Data:
{json.dumps(comparison_data['esg_scores'], indent=2)}

## SDG Performance Data:
{json.dumps(comparison_data['sdg_scores'], indent=2)}

## Executive Summaries by Year:
"""
        
        for year in years:
            summary = comparison_data['executive_summaries'].get(year, 'Not available')
            prompt += f"\n**{year}:** {summary[:200]}...\n"
        
        prompt += """

## Analysis Requirements:

Please provide a comprehensive comparative analysis including:

### 1. Performance Trends
- Identify the most significant improvements and deteriorations
- Analyze year-over-year changes in ESG categories
- Highlight standout SDG performance changes

### 2. Strategic Insights
- What strategic shifts can be inferred from the data?
- Which sustainability areas show consistent progress?
- Where are the persistent challenges?

### 3. Future Recommendations
- Based on the trends, what should be the priority focus areas?
- What strategies could accelerate positive trends?
- How can declining areas be addressed?

### 4. Benchmark Analysis
- How does the overall sustainability trajectory look?
- What does this progression suggest about the company's commitment?
- Are there any concerning patterns that need immediate attention?

Please structure your response with clear headings and provide specific, actionable insights based on the data trends.
"""
        
        return prompt
    
    def _generate_comparison_summary(self, comparison_data: Dict, trends: Dict) -> Dict:
        """Generate quantitative comparison summary"""
        years = sorted(comparison_data['esg_scores'].keys())
        
        summary = {
            'total_years_compared': len(years),
            'year_range': f"{min(years)}-{max(years)}",
            'esg_summary': {},
            'sdg_summary': {},
            'key_insights': []
        }
        
        # ESG summary
        improving_esg = 0
        declining_esg = 0
        
        for category, trend_data in trends['esg_trends'].items():
            if trend_data['trend'] == 'improving':
                improving_esg += 1
            else:
                declining_esg += 1
        
        summary['esg_summary'] = {
            'improving_categories': improving_esg,
            'declining_categories': declining_esg,
            'total_categories': improving_esg + declining_esg
        }
        
        # SDG summary
        improving_sdg = 0
        declining_sdg = 0
        
        for sdg, trend_data in trends['sdg_trends'].items():
            if trend_data['trend'] == 'improving':
                improving_sdg += 1
            else:
                declining_sdg += 1
        
        summary['sdg_summary'] = {
            'improving_sdgs': improving_sdg,
            'declining_sdgs': declining_sdg,
            'total_active_sdgs': improving_sdg + declining_sdg
        }
        
        return summary
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize company name for filesystem"""
        import re
        return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

# Example usage and testing
if __name__ == "__main__":
    # Test the comparison system
    comparison = ReportComparison()
    
    # Sample data for testing
    sample_report_2022 = {
        'executive_summary': 'Company shows strong ESG performance in 2022',
        'esg_analysis': {
            'economic_financial_performance': {'score': 7.5},
            'environmental_performance': {'score': 6.8},
            'social_performance': {'score': 8.1}
        },
        'sdg_mapping': {
            'SDG7': {'score': 7.2},
            'SDG8': {'score': 8.0},
            'SDG13': {'score': 6.5}
        }
    }
    
    sample_report_2023 = {
        'executive_summary': 'Company improves environmental performance in 2023',
        'esg_analysis': {
            'economic_financial_performance': {'score': 7.8},
            'environmental_performance': {'score': 7.5},
            'social_performance': {'score': 8.3}
        },
        'sdg_mapping': {
            'SDG7': {'score': 7.8},
            'SDG8': {'score': 8.2},
            'SDG13': {'score': 7.1}
        }
    }
    
    # Store sample reports
    comparison.store_report("TestCompany", 2022, sample_report_2022)
    comparison.store_report("TestCompany", 2023, sample_report_2023)
    
    # Test comparison
    result = comparison.compare_reports("TestCompany", [2022, 2023])
    print("✅ Comparison test completed!")