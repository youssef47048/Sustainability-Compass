# PDF Processing Module for Sustainability Compass
import PyPDF2
import pdfplumber
import pandas as pd
import re
from typing import Dict, List, Optional
import logging

class PDFProcessor:
    """
    Comprehensive PDF processor that handles text extraction, 
    table detection, and multi-language content (English/Arabic)
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def extract_content(self, pdf_path: str) -> Dict:
        """
        Extract all content from PDF including text, tables, and metadata
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict: Extracted content with text, tables, and metadata
        """
        try:
            content = {
                'text': '',
                'tables': [],
                'metadata': {},
                'page_count': 0,
                'language_detected': 'en'  # Default to English
            }
            
            # Extract text using pdfplumber (better for tables)
            with pdfplumber.open(pdf_path) as pdf:
                content['page_count'] = len(pdf.pages)
                all_text = []
                
                for page_num, page in enumerate(pdf.pages):
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        all_text.append(page_text)
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table in tables:
                        if table:  # Check if table is not None
                            df = pd.DataFrame(table[1:], columns=table[0])  # First row as header
                            content['tables'].append({
                                'page': page_num + 1,
                                'data': df,
                                'raw': table
                            })
                
                content['text'] = '\n'.join(all_text)
            
            # Extract metadata using PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                if pdf_reader.metadata:
                    content['metadata'] = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'creation_date': pdf_reader.metadata.get('/CreationDate', ''),
                    }
            
            # Detect language
            content['language_detected'] = self._detect_language(content['text'])
            
            # Clean and structure the text
            content['structured_text'] = self._structure_text(content['text'])
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error processing PDF: {str(e)}")
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    def _detect_language(self, text: str) -> str:
        """
        Detect if the text is primarily Arabic or English
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Language code ('ar' for Arabic, 'en' for English)
        """
        if not text:
            return 'en'
        
        # Count Arabic characters
        arabic_chars = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))
        total_chars = len(re.findall(r'[^\s\d\W]', text))
        
        if total_chars > 0:
            arabic_ratio = arabic_chars / total_chars
            return 'ar' if arabic_ratio > 0.3 else 'en'
        
        return 'en'
    
    def _structure_text(self, text: str) -> Dict:
        """
        Structure the extracted text into sections for better analysis
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            Dict: Structured text sections
        """
        structured = {
            'full_text': text,
            'sections': {},
            'financial_data': [],
            'environmental_data': [],
            'social_data': []
        }
        
        # Common section headers (English and Arabic)
        section_patterns = {
            'financial': [
                r'financial\s+performance',
                r'financial\s+results',
                r'revenue',
                r'profit',
                r'income\s+statement',
                r'balance\s+sheet',
                r'الأداء\s+المالي',
                r'النتائج\s+المالية',
                r'الإيرادات',
                r'الأرباح'
            ],
            'environmental': [
                r'environmental\s+impact',
                r'sustainability',
                r'carbon\s+emissions',
                r'energy\s+consumption',
                r'waste\s+management',
                r'التأثير\s+البيئي',
                r'الاستدامة',
                r'انبعاثات\s+الكربون',
                r'استهلاك\s+الطاقة'
            ],
            'social': [
                r'social\s+responsibility',
                r'employee\s+welfare',
                r'community\s+engagement',
                r'diversity',
                r'human\s+rights',
                r'المسؤولية\s+الاجتماعية',
                r'رفاهية\s+الموظفين',
                r'المشاركة\s+المجتمعية',
                r'التنوع'
            ]
        }
        
        # Extract sections based on patterns
        for category, patterns in section_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 500)  # Context before
                    end = min(len(text), match.end() + 1500)  # Context after
                    section_text = text[start:end]
                    
                    if category not in structured['sections']:
                        structured['sections'][category] = []
                    structured['sections'][category].append(section_text)
        
        return structured
    
    def extract_financial_metrics(self, text: str, tables: List) -> Dict:
        """
        Extract financial metrics from text and tables
        
        Args:
            text (str): Extracted text
            tables (List): Extracted tables
            
        Returns:
            Dict: Financial metrics found
        """
        financial_metrics = {
            'revenue': None,
            'profit': None,
            'assets': None,
            'liabilities': None,
            'growth_rate': None,
            'roi': None
        }
        
        # Common financial patterns
        patterns = {
            'revenue': [
                r'revenue[:\s]+[\$]?([0-9,\.]+)',
                r'sales[:\s]+[\$]?([0-9,\.]+)',
                r'الإيرادات[:\s]+([0-9,\.]+)'
            ],
            'profit': [
                r'profit[:\s]+[\$]?([0-9,\.]+)',
                r'net\s+income[:\s]+[\$]?([0-9,\.]+)',
                r'الأرباح[:\s]+([0-9,\.]+)'
            ]
        }
        
        # Extract from text
        for metric, metric_patterns in patterns.items():
            for pattern in metric_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        value = float(match.group(1).replace(',', ''))
                        financial_metrics[metric] = value
                        break
                    except:
                        continue
        
        # Extract from tables
        for table_info in tables:
            df = table_info['data']
            # Look for financial indicators in table data
            for col in df.columns:
                if any(keyword in str(col).lower() for keyword in ['revenue', 'profit', 'income', 'sales']):
                    # Extract numeric values from this column
                    for val in df[col]:
                        if isinstance(val, str):
                            numbers = re.findall(r'[\d,\.]+', val)
                            if numbers:
                                try:
                                    financial_metrics[col.lower()] = float(numbers[0].replace(',', ''))
                                except:
                                    continue
        
        return financial_metrics
    
    def get_summary_stats(self, content: Dict) -> Dict:
        """
        Get summary statistics of the processed PDF
        
        Args:
            content (Dict): Processed PDF content
            
        Returns:
            Dict: Summary statistics
        """
        return {
            'page_count': content['page_count'],
            'word_count': len(content['text'].split()) if content['text'] else 0,
            'table_count': len(content['tables']),
            'language': content['language_detected'],
            'has_financial_data': 'financial' in content.get('structured_text', {}).get('sections', {}),
            'has_environmental_data': 'environmental' in content.get('structured_text', {}).get('sections', {}),
            'has_social_data': 'social' in content.get('structured_text', {}).get('sections', {})
        } 