# Visualization Module for Sustainability Analysis
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List
import base64
from io import BytesIO
from config import SDG_GOALS, ESG_CATEGORIES, COLORS

# Optional seaborn import
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

class SustainabilityVisualizer:
    """
    Create visualizations for ESG analysis and SDG mapping results
    """
    
    def __init__(self):
        # Set style for matplotlib
        if SEABORN_AVAILABLE:
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
        else:
            plt.style.use('default')
        
    def create_esg_dashboard(self, esg_analysis: Dict) -> Dict:
        """
        Create comprehensive ESG dashboard with multiple charts
        
        Args:
            esg_analysis (Dict): ESG analysis results
            
        Returns:
            Dict: Chart data and configurations
        """
        charts = {}
        
        # ESG Scores Bar Chart
        charts['esg_scores'] = self._create_esg_scores_chart(esg_analysis)
        
        # ESG Performance Radar Chart
        charts['esg_radar'] = self._create_esg_radar_chart(esg_analysis)
        
        # Strengths vs Weaknesses Analysis
        charts['strengths_weaknesses'] = self._create_strengths_weaknesses_chart(esg_analysis)
        
        return charts
    
    def create_sdg_dashboard(self, sdg_mapping: Dict) -> Dict:
        """
        Create SDG performance dashboard
        
        Args:
            sdg_mapping (Dict): SDG mapping results
            
        Returns:
            Dict: SDG visualization charts
        """
        charts = {}
        
        # SDG Impact Heatmap
        charts['sdg_heatmap'] = self._create_sdg_heatmap(sdg_mapping)
        
        # Top SDG Contributors
        charts['top_sdgs'] = self._create_top_sdgs_chart(sdg_mapping)
        
        # SDG Impact Distribution
        charts['sdg_distribution'] = self._create_sdg_distribution_chart(sdg_mapping)
        
        return charts
    
    def create_comprehensive_dashboard(self, analysis_results: Dict) -> str:
        """
        Create comprehensive HTML dashboard
        
        Args:
            analysis_results (Dict): Complete analysis results
            
        Returns:
            str: HTML dashboard content
        """
        esg_analysis = analysis_results.get('esg_analysis', {})
        sdg_mapping = analysis_results.get('sdg_mapping', {})
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                'ESG Performance Scores', 'SDG Impact Heatmap',
                'ESG Radar Chart', 'Top Contributing SDGs',
                'Strengths vs Weaknesses', 'SDG Impact Distribution'
            ],
            specs=[
                [{"type": "bar"}, {"type": "heatmap"}],
                [{"type": "scatterpolar"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "pie"}]
            ]
        )
        
        # Add ESG scores
        self._add_esg_scores_to_subplot(fig, esg_analysis, row=1, col=1)
        
        # Add SDG heatmap
        self._add_sdg_heatmap_to_subplot(fig, sdg_mapping, row=1, col=2)
        
        # Add ESG radar
        self._add_esg_radar_to_subplot(fig, esg_analysis, row=2, col=1)
        
        # Add top SDGs
        self._add_top_sdgs_to_subplot(fig, sdg_mapping, row=2, col=2)
        
        # Add strengths/weaknesses
        self._add_strengths_weaknesses_to_subplot(fig, esg_analysis, row=3, col=1)
        
        # Add SDG distribution
        self._add_sdg_distribution_to_subplot(fig, sdg_mapping, row=3, col=2)
        
        # Update layout
        fig.update_layout(
            height=1200,
            showlegend=True,
            title_text="Sustainability Analysis Dashboard",
            title_x=0.5,
            title_font_size=20
        )
        
        return fig.to_html(full_html=True, include_plotlyjs=True)
    
    def _create_esg_scores_chart(self, esg_analysis: Dict) -> go.Figure:
        """Create ESG scores bar chart"""
        categories = []
        scores = []
        colors = []
        
        for category, data in esg_analysis.items():
            if isinstance(data, dict) and 'score' in data:
                categories.append(category.title())
                scores.append(data['score'])
                
                # Color coding based on score
                if data['score'] >= 8:
                    colors.append(COLORS['success'])
                elif data['score'] >= 6:
                    colors.append(COLORS['warning'])
                else:
                    colors.append(COLORS['error'])
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=scores,
                marker_color=colors,
                text=scores,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='ESG Performance Scores',
            xaxis_title='ESG Categories',
            yaxis_title='Score (out of 10)',
            yaxis=dict(range=[0, 10])
        )
        
        return fig
    
    def _create_esg_radar_chart(self, esg_analysis: Dict) -> go.Figure:
        """Create ESG radar chart"""
        categories = []
        scores = []
        
        for category, data in esg_analysis.items():
            if isinstance(data, dict) and 'score' in data:
                categories.append(category.title())
                scores.append(data['score'])
        
        # Close the radar chart
        categories.append(categories[0])
        scores.append(scores[0])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='ESG Performance',
            line_color=COLORS['secondary']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="ESG Performance Radar"
        )
        
        return fig
    
    def _create_strengths_weaknesses_chart(self, esg_analysis: Dict) -> go.Figure:
        """Create strengths vs weaknesses chart"""
        strengths_count = []
        weaknesses_count = []
        categories = []
        
        for category, data in esg_analysis.items():
            if isinstance(data, dict):
                categories.append(category.title())
                strengths_count.append(len(data.get('strengths', [])))
                weaknesses_count.append(len(data.get('weaknesses', [])))
        
        fig = go.Figure(data=[
            go.Bar(name='Strengths', x=categories, y=strengths_count, marker_color=COLORS['success']),
            go.Bar(name='Weaknesses', x=categories, y=weaknesses_count, marker_color=COLORS['error'])
        ])
        
        fig.update_layout(
            barmode='group',
            title='Strengths vs Weaknesses by ESG Category',
            xaxis_title='ESG Categories',
            yaxis_title='Count'
        )
        
        return fig
    
    def _create_sdg_heatmap(self, sdg_mapping: Dict) -> go.Figure:
        """Create SDG impact heatmap"""
        sdg_numbers = []
        sdg_names = []
        scores = []
        
        for sdg_key, data in sdg_mapping.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                sdg_num = int(sdg_key.split('_')[1])
                sdg_numbers.append(sdg_num)
                sdg_names.append(SDG_GOALS.get(sdg_num, f'SDG {sdg_num}'))
                scores.append(data.get('score', 0))
        
        # Create matrix for heatmap (4x5 grid for 17 SDGs + 3 empty)
        matrix = [[0 for _ in range(5)] for _ in range(4)]
        labels = [["" for _ in range(5)] for _ in range(4)]
        
        for i, (num, score) in enumerate(zip(sdg_numbers, scores)):
            row = i // 5
            col = i % 5
            if row < 4:
                matrix[row][col] = score
                labels[row][col] = f"SDG {num}"
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            text=labels,
            texttemplate="%{text}<br>%{z:.1f}",
            textfont={"size": 10},
            colorscale='RdYlGn',
            zmin=0,
            zmax=10
        ))
        
        fig.update_layout(
            title='SDG Impact Heatmap',
            xaxis_title='',
            yaxis_title='',
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False)
        )
        
        return fig
    
    def _create_top_sdgs_chart(self, sdg_mapping: Dict) -> go.Figure:
        """Create top contributing SDGs chart"""
        sdg_scores = []
        
        for sdg_key, data in sdg_mapping.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                sdg_num = int(sdg_key.split('_')[1])
                score = data.get('score', 0)
                sdg_scores.append({
                    'sdg': f"SDG {sdg_num}: {SDG_GOALS.get(sdg_num, '')}",
                    'score': score
                })
        
        # Sort by score and get top 10
        sdg_scores.sort(key=lambda x: x['score'], reverse=True)
        top_sdgs = sdg_scores[:10]
        
        fig = go.Figure(data=[
            go.Bar(
                y=[sdg['sdg'] for sdg in top_sdgs],
                x=[sdg['score'] for sdg in top_sdgs],
                orientation='h',
                marker_color=COLORS['accent']
            )
        ])
        
        fig.update_layout(
            title='Top 10 Contributing SDGs',
            xaxis_title='Impact Score',
            yaxis_title='SDGs'
        )
        
        return fig
    
    def _create_sdg_distribution_chart(self, sdg_mapping: Dict) -> go.Figure:
        """Create SDG impact level distribution"""
        impact_levels = {'High': 0, 'Medium': 0, 'Low': 0, 'None': 0}
        
        for sdg_key, data in sdg_mapping.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                impact_level = data.get('impact_level', 'None')
                if impact_level in impact_levels:
                    impact_levels[impact_level] += 1
        
        fig = go.Figure(data=[go.Pie(
            labels=list(impact_levels.keys()),
            values=list(impact_levels.values()),
            hole=.3
        )])
        
        fig.update_layout(
            title='SDG Impact Level Distribution',
            annotations=[dict(text='SDG Impact', x=0.5, y=0.5, font_size=12, showarrow=False)]
        )
        
        return fig
    
    # Helper methods for adding to subplots
    def _add_esg_scores_to_subplot(self, fig, esg_analysis, row, col):
        """Add ESG scores to subplot"""
        categories = []
        scores = []
        
        for category, data in esg_analysis.items():
            if isinstance(data, dict) and 'score' in data:
                categories.append(category.title())
                scores.append(data['score'])
        
        fig.add_trace(
            go.Bar(x=categories, y=scores, name='ESG Scores'),
            row=row, col=col
        )
    
    def _add_sdg_heatmap_to_subplot(self, fig, sdg_mapping, row, col):
        """Add SDG heatmap to subplot"""
        # Simplified version for subplot
        sdg_numbers = list(range(1, 18))
        scores = []
        
        for sdg_num in sdg_numbers:
            sdg_key = f'sdg_{sdg_num}'
            score = sdg_mapping.get(sdg_key, {}).get('score', 0)
            scores.append(score)
        
        # Create a simple bar chart instead of heatmap for subplot
        fig.add_trace(
            go.Bar(x=[f'SDG{i}' for i in sdg_numbers[:10]], y=scores[:10], name='SDG Scores'),
            row=row, col=col
        )
    
    def _add_esg_radar_to_subplot(self, fig, esg_analysis, row, col):
        """Add ESG radar to subplot"""
        categories = []
        scores = []
        
        for category, data in esg_analysis.items():
            if isinstance(data, dict) and 'score' in data:
                categories.append(category.title())
                scores.append(data['score'])
        
        fig.add_trace(
            go.Scatterpolar(r=scores, theta=categories, fill='toself', name='ESG Radar'),
            row=row, col=col
        )
    
    def _add_top_sdgs_to_subplot(self, fig, sdg_mapping, row, col):
        """Add top SDGs to subplot"""
        sdg_scores = []
        
        for sdg_key, data in sdg_mapping.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                sdg_num = int(sdg_key.split('_')[1])
                score = data.get('score', 0)
                sdg_scores.append({'sdg': f'SDG{sdg_num}', 'score': score})
        
        sdg_scores.sort(key=lambda x: x['score'], reverse=True)
        top_5 = sdg_scores[:5]
        
        fig.add_trace(
            go.Bar(x=[s['sdg'] for s in top_5], y=[s['score'] for s in top_5], name='Top SDGs'),
            row=row, col=col
        )
    
    def _add_strengths_weaknesses_to_subplot(self, fig, esg_analysis, row, col):
        """Add strengths/weaknesses to subplot"""
        categories = []
        strengths = []
        weaknesses = []
        
        for category, data in esg_analysis.items():
            if isinstance(data, dict):
                categories.append(category.title())
                strengths.append(len(data.get('strengths', [])))
                weaknesses.append(len(data.get('weaknesses', [])))
        
        fig.add_trace(
            go.Bar(x=categories, y=strengths, name='Strengths'),
            row=row, col=col
        )
        fig.add_trace(
            go.Bar(x=categories, y=weaknesses, name='Weaknesses'),
            row=row, col=col
        )
    
    def _add_sdg_distribution_to_subplot(self, fig, sdg_mapping, row, col):
        """Add SDG distribution to subplot"""
        impact_levels = {'High': 0, 'Medium': 0, 'Low': 0, 'None': 0}
        
        for sdg_key, data in sdg_mapping.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                impact_level = data.get('impact_level', 'None')
                if impact_level in impact_levels:
                    impact_levels[impact_level] += 1
        
        fig.add_trace(
            go.Pie(labels=list(impact_levels.keys()), values=list(impact_levels.values()), name='SDG Distribution'),
            row=row, col=col
        ) 