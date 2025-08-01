#!/usr/bin/env python3
"""
SDG Contribution Chart Generator
Creates the specific SDG contribution chart as requested by user
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List, Tuple
import os
from config import SDG_GOALS, COLORS

class SDGContributionChart:
    """Generate SDG contribution charts for sustainability reports"""
    
    def __init__(self):
        self.colors = {
            'high': '#4a4a4a',      # Dark gray for High contribution
            'medium': '#9a9a9a',    # Light gray for Medium contribution  
            'low': '#d4d4d4',       # Very light gray for Low contribution
            'none': '#f0f0f0'       # Almost white for No contribution
        }
        
        # SDG Names for display
        self.sdg_names = {
            'sdg_1': 'No Poverty',
            'sdg_2': 'Zero Hunger', 
            'sdg_3': 'Good Health',
            'sdg_4': 'Quality Education',
            'sdg_5': 'Gender Equality',
            'sdg_6': 'Clean Water',
            'sdg_7': 'Affordable Energy',
            'sdg_8': 'Decent Work',
            'sdg_9': 'Innovation',
            'sdg_10': 'Reduced Inequalities',
            'sdg_11': 'Sustainable Cities',
            'sdg_12': 'Responsible Consumption',
            'sdg_13': 'Climate Action',
            'sdg_14': 'Life Below Water',
            'sdg_15': 'Life on Land', 
            'sdg_16': 'Peace & Justice',
            'sdg_17': 'Partnerships'
        }
    
    def create_sdg_contribution_chart(self, sdg_data: Dict, language: str = 'en', 
                                    save_path: str = 'sdg_contribution_chart.png') -> str:
        """
        Create SDG contribution chart like the user's example
        
        Args:
            sdg_data: Dictionary with SDG analysis results
            language: 'en' or 'ar'
            save_path: Path to save the chart
            
        Returns:
            str: Path to saved chart
        """
        
        # Extract contribution levels from SDG data
        contributions = self._extract_contribution_levels(sdg_data)
        
        # Filter to show only relevant SDGs (Medium and High contributions)
        relevant_sdgs = {k: v for k, v in contributions.items() 
                        if v in ['Medium', 'High']}
        
        if not relevant_sdgs:
            # If no significant contributions, show top scored SDGs
            relevant_sdgs = self._get_top_sdgs(sdg_data, limit=9)
        
        # Create the chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data
        sdg_numbers = []
        contribution_levels = []
        colors = []
        
        # Sort SDGs by number for consistent display
        sorted_sdgs = sorted(relevant_sdgs.items(), 
                           key=lambda x: int(x[0].split('_')[1]))
        
        for sdg_key, contribution in sorted_sdgs:
            sdg_num = int(sdg_key.split('_')[1])
            sdg_numbers.append(f'SDG {sdg_num}')
            contribution_levels.append(contribution)
            
            # Map contribution to height and color
            if contribution == 'High':
                colors.append(self.colors['high'])
            elif contribution == 'Medium':
                colors.append(self.colors['medium'])
            elif contribution == 'Low':
                colors.append(self.colors['low'])
            else:
                colors.append(self.colors['none'])
        
        # Create bars
        x_pos = np.arange(len(sdg_numbers))
        heights = [3.0 if level == 'High' else 2.0 if level == 'Medium' else 1.0 
                  for level in contribution_levels]
        
        bars = ax.bar(x_pos, heights, color=colors, edgecolor='white', linewidth=1)
        
        # Add contribution level labels on top of bars
        for i, (bar, level) in enumerate(zip(bars, contribution_levels)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                   level, ha='center', va='bottom', fontsize=10, 
                   fontweight='bold', color='#333333')
        
        # Customize chart
        if language == 'ar':
            title = 'مساهمة تحليل الاستدامة الذكي في أهداف التنمية المستدامة'
            ylabel = 'مستوى المساهمة'
        else:
            title = 'Contribution of AI Sustainability Analysis to SDGs'
            ylabel = 'Contribution Level'
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Sustainable Development Goals', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        
        # Set x-axis
        ax.set_xticks(x_pos)
        ax.set_xticklabels(sdg_numbers, rotation=45, ha='right')
        
        # Set y-axis
        ax.set_ylim(0, 3.5)
        ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
        
        # Add horizontal grid for better readability
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Style the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cccccc')
        ax.spines['bottom'].set_color('#cccccc')
        
        # Tight layout
        plt.tight_layout()
        
        # Save the chart
        plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        return save_path
    
    def _extract_contribution_levels(self, sdg_data: Dict) -> Dict[str, str]:
        """Extract contribution levels from SDG analysis data"""
        contributions = {}
        
        for sdg_key, data in sdg_data.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                score = data.get('score', 0)
                impact_level = data.get('impact_level', 'None')
                
                # Determine contribution level based on score and impact
                if score >= 7 or impact_level == 'High':
                    contributions[sdg_key] = 'High'
                elif score >= 4 or impact_level in ['Medium', 'Moderate']:
                    contributions[sdg_key] = 'Medium'
                elif score >= 1 or impact_level == 'Low':
                    contributions[sdg_key] = 'Low'
                else:
                    contributions[sdg_key] = 'None'
        
        return contributions
    
    def _get_top_sdgs(self, sdg_data: Dict, limit: int = 9) -> Dict[str, str]:
        """Get top SDGs by score if no explicit contribution levels"""
        sdg_scores = []
        
        for sdg_key, data in sdg_data.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                score = data.get('score', 0)
                if score > 0:
                    sdg_scores.append((sdg_key, score))
        
        # Sort by score and take top ones
        sdg_scores.sort(key=lambda x: x[1], reverse=True)
        top_sdgs = sdg_scores[:limit]
        
        # Assign contribution levels based on score
        result = {}
        for sdg_key, score in top_sdgs:
            if score >= 7:
                result[sdg_key] = 'High'
            elif score >= 4:
                result[sdg_key] = 'Medium'
            else:
                result[sdg_key] = 'Low'
        
        return result
    
    def create_comprehensive_sdg_chart(self, sdg_data: Dict, language: str = 'en',
                                     save_path: str = 'comprehensive_sdg_chart.png') -> str:
        """Create a comprehensive chart showing all 17 SDGs"""
        
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Prepare data for all 17 SDGs
        sdg_numbers = [f'SDG {i}' for i in range(1, 18)]
        scores = []
        colors = []
        
        for i in range(1, 18):
            sdg_key = f'sdg_{i}'
            data = sdg_data.get(sdg_key, {})
            score = data.get('score', 0)
            scores.append(score)
            
            # Color based on score
            if score >= 7:
                colors.append(self.colors['high'])
            elif score >= 4:
                colors.append(self.colors['medium'])
            elif score >= 1:
                colors.append(self.colors['low'])
            else:
                colors.append(self.colors['none'])
        
        # Create bars
        x_pos = np.arange(len(sdg_numbers))
        bars = ax.bar(x_pos, scores, color=colors, edgecolor='white', linewidth=1)
        
        # Add score labels
        for bar, score in zip(bars, scores):
            if score > 0:
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                       f'{score:.1f}', ha='center', va='bottom', fontsize=9)
        
        # Customize
        if language == 'ar':
            title = 'تقييم شامل لأهداف التنمية المستدامة'
        else:
            title = 'Comprehensive SDG Assessment'
            
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Sustainable Development Goals', fontsize=12)
        ax.set_ylabel('Performance Score', fontsize=12)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(sdg_numbers, rotation=45, ha='right')
        ax.set_ylim(0, 10)
        
        # Add legend
        legend_elements = [
            patches.Patch(color=self.colors['high'], label='High (7-10)'),
            patches.Patch(color=self.colors['medium'], label='Medium (4-6)'),
            patches.Patch(color=self.colors['low'], label='Low (1-3)'),
            patches.Patch(color=self.colors['none'], label='None (0)')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Grid and styling
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        return save_path

def test_chart_generation():
    """Test the SDG chart generation"""
    
    # Sample SDG data
    sample_data = {
        'sdg_4': {'score': 8.5, 'impact_level': 'High'},
        'sdg_5': {'score': 8.0, 'impact_level': 'High'},
        'sdg_7': {'score': 8.2, 'impact_level': 'High'},
        'sdg_8': {'score': 7.8, 'impact_level': 'High'},
        'sdg_9': {'score': 5.5, 'impact_level': 'Medium'},
        'sdg_10': {'score': 8.0, 'impact_level': 'High'},
        'sdg_12': {'score': 5.0, 'impact_level': 'Medium'},
        'sdg_13': {'score': 7.5, 'impact_level': 'High'},
        'sdg_17': {'score': 5.8, 'impact_level': 'Medium'}
    }
    
    chart_gen = SDGContributionChart()
    
    # Generate contribution chart
    chart_path = chart_gen.create_sdg_contribution_chart(
        sample_data, 'en', 'test_sdg_contribution.png'
    )
    print(f"✅ SDG Contribution Chart created: {chart_path}")
    
    # Generate comprehensive chart
    comprehensive_path = chart_gen.create_comprehensive_sdg_chart(
        sample_data, 'en', 'test_comprehensive_sdg.png'
    )
    print(f"✅ Comprehensive SDG Chart created: {comprehensive_path}")

if __name__ == "__main__":
    test_chart_generation() 